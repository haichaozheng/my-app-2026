"""
股吧评论情感双标注：jieba 词典法 + 西财大模型（并发、断点续跑）

给 cleaned_300251_comments.csv 增加两列：
  jieba_score : 正面/负面/中性 —— jieba(+userdict.txt) 分词后命中
                zhang_unformal_pos/neg.txt 词典计分，>0 正面，<0 负面，=0 中性
  llm_score   : 正面/负面/中性 —— 西财大模型批量标注（.env 里的 SwufeModel_API_KEY）

结果存 cleaned_300251_comments_scored.csv（原始 csv 不改动）。
LLM 标注每完成一批就写入 llm_labels_checkpoint.csv，中断后重跑会自动跳过已标注的行。

用法（在 case-nlp 目录下，先激活仓库根目录 .venv）：
  python llm_jieba_score.py --limit 100    # 先跑 100 条验证管道（推荐第一次）
  python llm_jieba_score.py                # 全量 124,126 条，约 25-40 分钟
  python llm_jieba_score.py --skip-llm     # 只算 jieba_score，不调大模型

依赖：pip install pandas jieba openai
"""

import argparse
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import jieba
import pandas as pd

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

base = Path(__file__).parent
repo_root = base.parents[3]          # case-nlp -> week01 -> weeks -> ai4s -> 仓库根

# ---------------- 可调参数 ----------------
MODEL = 'Qwen/Qwen3.8-Flash-Next'
BASE_URL = 'http://llm.swufe.edu.cn/v1'
# Qwen3.8 尊重该参数：关闭思考，单条 15 秒级 -> 秒级
EXTRA_BODY = {'chat_template_kwargs': {'enable_thinking': False}}
BATCH_SIZE = 20        # 每次请求让大模型标多少条
MAX_WORKERS = 10       # 并发线程数上限（学校共享网关，夜间 10，禁止调更高）
MAX_CHARS = 500        # 单条评论截断长度（0=不截断）
MAX_RETRIES = 3
VALID = {'正面', '负面', '中性'}
# -----------------------------------------


def read_api_key():
    """从仓库根目录 .env 读 SwufeModel_API_KEY（不引入 python-dotenv 依赖）"""
    env = repo_root / '.env'
    if not env.exists():
        sys.exit(f'未找到 {env}，请先在根目录 .env 配置 SwufeModel_API_KEY')
    for line in env.read_text(encoding='utf-8').splitlines():
        m = re.match(r'\s*SwufeModel_API_KEY\s*=\s*(.+)', line)
        if m:
            return m.group(1).strip().strip('"').strip("'")
    sys.exit('.env 里没有 SwufeModel_API_KEY')


# ---------- Step 1: jieba 词典法打分 ----------

def load_dict(path):
    return {w.strip() for w in path.read_text(encoding='utf-8').splitlines() if w.strip()}


def jieba_score_all(df):
    for f in ('userdict.txt', 'zhang_unformal_pos.txt', 'zhang_unformal_neg.txt'):
        p = base / f
        if p.exists():
            jieba.load_userdict(str(p))

    pos_words = load_dict(base / 'zhang_unformal_pos.txt')
    neg_words = load_dict(base / 'zhang_unformal_neg.txt')
    print(f"jieba 词典加载：正面 {len(pos_words)} 词，负面 {len(neg_words)} 词")

    def score(text):
        words = jieba.lcut(text)
        s = sum(1 for w in words if w in pos_words) - sum(1 for w in words if w in neg_words)
        return '正面' if s > 0 else ('负面' if s < 0 else '中性')

    t0 = time.time()
    df['jieba_score'] = df['comment'].map(score)
    print(f"jieba 打分完成 {len(df)} 条，耗时 {time.time() - t0:.0f} 秒")
    print(df['jieba_score'].value_counts().to_string(), '\n')
    return df


# ---------- Step 2: 大模型批量标注 ----------

ckpt_lock = threading.Lock()


def load_checkpoint(n_rows):
    """断点续跑：返回 {行号: 标签}，并校验行号与本数据集匹配"""
    ckpt = base / 'llm_labels_checkpoint.csv'
    if not ckpt.exists():
        return {}
    prev = pd.read_csv(ckpt, dtype={'row': int, 'llm_score': str})
    dup = prev['row'].duplicated().sum()
    if dup:
        sys.exit(f'断点文件有 {dup} 个重复行号，请先检查 {ckpt}')
    bad = prev[prev['row'] >= n_rows]
    if len(bad):
        sys.exit(f'断点文件有 {len(bad)} 个行号超出本数据集（共 {n_rows} 行），'
                 f'断点可能来自另一次数据，请删除或改名 {ckpt} 后重跑')
    labels = prev[prev['llm_score'].isin(VALID)]
    if len(labels) < len(prev):
        print(f'警告：断点文件有 {len(prev) - len(labels)} 个无效标签，忽略')
    print(f"断点文件已有 {len(labels)} 条，自动跳过")
    return dict(zip(labels['row'], labels['llm_score']))


def append_checkpoint(pairs):
    """把 [(行号, 标签), ...] 追加到断点文件"""
    ckpt = base / 'llm_labels_checkpoint.csv'
    with ckpt_lock:
        new_file = not ckpt.exists()
        with open(ckpt, 'a', encoding='utf-8-sig', newline='') as f:
            if new_file:
                f.write('row,llm_score\n')
            for r, label in pairs:
                f.write(f'{r},{label}\n')


SYSTEM_PROMPT = (
    '你是中文股吧评论情感标注助手。对每条评论判断散户情绪，'
    '只能输出三类标签之一：正面、负面、中性。'
    '反讽（如"又一个韭菜"）按评论的真实情绪判断。'
    '只输出 JSONL，每行一条：{"id": <编号>, "label": "<正面|负面|中性>"}，'
    '不要输出其他任何内容。'
)


def build_user_prompt(items):
    """items: [(行号, 文本), ...]"""
    lines = [f'{r}\t{t}' for r, t in items]
    return '请给下面每条评论打情感标签：\n' + '\n'.join(lines)


def parse_labels(content, want_ids=None):
    """从大模型返回的 JSONL/文本里解析 {行号: 标签}；
    want_ids=None 时返回解析出的全部条目"""
    got = {}
    for m in re.finditer(r'\{[^{}]*\}', content):
        try:
            obj = json.loads(m.group())
            label = str(obj.get('label', '')).strip()
            if label in VALID:
                got[int(obj['id'])] = label
        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            continue
    if want_ids is None:
        return got
    return {i: got[i] for i in want_ids if i in got}


def llm_label_batch(client, items, batch_no, n_batches, stats):
    """标注一批，返回 [(行号, 标签), ...]；全部失败返回 []"""
    prompt = build_user_prompt(items)
    want_ids = [r for r, _ in items]
    # 输出 token 预算：开思考模式时思考 token 也计入，需更宽松
    max_tokens = min(16384, len(items) * 300 + 500)
    # 超时随批量放大：开思考后单条 5~15 秒
    timeout = max(120.0, len(items) * 12.0)
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': prompt},
                ],
                temperature=0,
                max_tokens=max_tokens,
                timeout=timeout,
                extra_body=EXTRA_BODY,
            )
            # content 可能为 None（思考 token 耗尽时正文为空）
            got = parse_labels(resp.choices[0].message.content or '', want_ids)
            if got:
                return [(r, got[r]) for r in want_ids if r in got]
            print(f'  [批次 {batch_no}/{n_batches}] 返回可解析条目不足，重试(第{attempt + 1}次)')
        except Exception as e:
            print(f'  [批次 {batch_no}/{n_batches}] 请求失败(第{attempt + 1}次)：'
                  f'{type(e).__name__}: {e}')
            time.sleep(2 * (attempt + 1))
    return []


def llm_score_all(df, rows_todo, workers=MAX_WORKERS, batch_size=BATCH_SIZE):
    from openai import OpenAI
    # timeout 必须设：默认无限等待，网关偶发挂起会卡死整个程序
    client = OpenAI(api_key=read_api_key(), base_url=BASE_URL,
                    timeout=60.0, max_retries=0)

    items = [(int(r), df.at[r, 'comment'][:MAX_CHARS]) for r in rows_todo]
    batches = [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
    total = len(batches)
    print(f'LLM 标注：{len(items)} 条评论，{total} 个批次，'
          f'每批 {batch_size} 条，{workers} 线程并发\n')

    t0 = time.time()
    stats = {'done': 0, 'fail': 0}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(llm_label_batch, client, b, i + 1, total, stats)
                   for i, b in enumerate(batches)}
        for i, fut in enumerate(as_completed(futures), 1):
            pairs = fut.result()
            if pairs:
                append_checkpoint(pairs)
                stats['done'] += len(pairs)
            else:
                stats['fail'] += 1
            elapsed = time.time() - t0
            rate = stats['done'] / elapsed * 60 if elapsed > 0 else 0
            remain = (len(items) - stats['done']) / (rate / 60) if rate > 0 else 0
            eta = (f'{remain / 3600:.1f} 小时' if remain >= 3600
                   else f'{remain / 60:.0f} 分钟')
            print(f'[批次 {i}/{total}] {time.strftime("%H:%M:%S")} '
                  f'累计 {stats["done"]}/{len(items)} 条 '
                  f'({stats["done"] * 100 // len(items)}%) | '
                  f'速率 {rate:.0f} 条/分 | 剩余约 {eta} | 失败批次 {stats["fail"]}',
                  flush=True)
    print(f'\nLLM 批量标注完成，耗时 {time.time() - t0:.0f} 秒\n')
    return stats['fail']


def retry_missing_individually(df, done, missing, max_rounds=3):
    """对批量后仍缺的行分轮重新标注，直到全部成功。
    失败就是失败：任何情况下都不编造标签（绝不填中性）。
    多轮仍失败的行留空（NaN），下次运行本脚本会自动重新标注这些行。"""
    if not missing:
        return done
    from openai import OpenAI
    client = OpenAI(api_key=read_api_key(), base_url=BASE_URL,
                    timeout=60.0, max_retries=0)

    pending = list(missing)
    for rnd in range(1, max_rounds + 1):
        print(f'\n第 {rnd}/{max_rounds} 轮重新标注：{len(pending)} 条失败行……')
        still = []
        for r in pending:
            text = df.at[r, 'comment'][:MAX_CHARS]
            label = None
            for _ in range(2):
                try:
                    resp = client.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {'role': 'system', 'content': SYSTEM_PROMPT},
                            # 带行号的 prompt（与批量一致），模型会回显行号
                            {'role': 'user',
                             'content': build_user_prompt([(r, text)])},
                        ],
                        temperature=0,
                        extra_body=EXTRA_BODY,
                    )
                    content = resp.choices[0].message.content or ''
                    got = parse_labels(content, [r])
                    if not got:
                        # 兜底：单条请求下模型可能无视行号（恒回 id:1），
                        # 只要返回了唯一一个合法标签，就是这条评论的结果
                        all_got = parse_labels(content)
                        if len(all_got) == 1:
                            got = {r: next(iter(all_got.values()))}
                    if got:
                        label = got[r]
                        break
                except Exception:
                    time.sleep(1)
            if label:
                append_checkpoint([(r, label)])
                done[r] = label
            else:
                still.append(r)
        if not still:
            print(f'失败行全部重新标注成功（第 {rnd} 轮）')
            return done
        pending = still
        if rnd < max_rounds:
            print(f'{len(pending)} 条仍失败，30 秒后进入下一轮……')
            time.sleep(30)

    print(f'\n警告：{len(pending)} 条经 {max_rounds} 轮重新标注仍失败——'
          '不填充任何标签，输出中保留为空')
    print('重新运行本脚本会自动重新标注这些行')
    return done


# ---------- Step 3: 合并输出 ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0, help='只处理前 N 条（测试用），0=全量')
    ap.add_argument('--skip-llm', action='store_true', help='只算 jieba_score')
    ap.add_argument('--workers', type=int, default=MAX_WORKERS,
                    help='并发线程数（上限 10）')
    ap.add_argument('--batch-size', type=int, default=BATCH_SIZE, help='每批评论数')
    args = ap.parse_args()
    # 并发硬上限：学校共享网关保护，传入再大也只按 10 跑
    if args.workers > MAX_WORKERS:
        print(f'警告：并发 {args.workers} 超过上限，已强制改为 {MAX_WORKERS}'
              '（学校共享网关，禁止更高并发）')
        args.workers = MAX_WORKERS

    csv_path = base / 'cleaned_300251_comments.csv'
    out_path = base / 'cleaned_300251_comments_scored.csv'
    # 读全部列：输出 = 原文件所有列 + 新增两列，行顺序不变，防止后续合并错位
    df = pd.read_csv(csv_path)
    df['comment'] = df['comment'].fillna('').str.replace(r'\s+', '', regex=True)
    if args.limit:
        df = df.head(args.limit)
    print(f'共 {len(df)} 条评论（光线传媒 300251 股吧），'
          f'行号 0~{len(df) - 1} 对应原 csv 数据行（0-based）\n')

    df = jieba_score_all(df)

    if not args.skip_llm:
        done = load_checkpoint(len(df))
        missing = [r for r in range(len(df)) if r not in done]
        print(f'待 LLM 标注 {len(missing)} 条')
        if missing:
            n_fail_batches = llm_score_all(df, missing,
                                           workers=args.workers,
                                           batch_size=args.batch_size)
            done = load_checkpoint(len(df))
            missing2 = [r for r in range(len(df)) if r not in done]
            if missing2:
                retry_missing_individually(df, done, missing2)
        df['llm_score'] = pd.Series(done).reindex(df.index)
        print('\nLLM 标签分布：')
        print(df['llm_score'].value_counts().to_string())
        unlabeled = int(df['llm_score'].isna().sum())
        if unlabeled:
            print(f'\n注意：{unlabeled} 条未成功标注，输出中保留为空——'
                  '重新运行本脚本会自动重新标注这些行（绝不填充编造标签）')

        # 两法一致率 —— 课堂讨论点
        agree = (df['jieba_score'] == df['llm_score']).mean()
        print(f'\njieba 与 LLM 标签一致率：{agree:.1%}')

        # 抽样核对：行号、评论原文、两列标签并排，肉眼检查对齐
        print('\n抽样核对（行号 | 评论开头 | jieba_score | llm_score）：')
        for r in [0, len(df) // 2, len(df) - 1]:
            print(f'  {r} | {df.at[r, "comment"][:24]} | '
                  f'{df.at[r, "jieba_score"]} | {df.at[r, "llm_score"]}')

    df.to_csv(out_path, encoding='utf-8-sig', index=False)
    print(f'\n已保存 {out_path.name}（原列全部保留，'
          + ('新增 jieba_score、llm_score 两列）' if not args.skip_llm
            else '新增 jieba_score 一列）'))


if __name__ == '__main__':
    main()
