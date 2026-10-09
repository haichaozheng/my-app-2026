# 部署排障 FAQ — 数据分析与可视化

> **何时用**：W10 试部署（进阶任务，允许失败）与 W11 部署验收期间。
> **排障流程**：先按症状查本 FAQ → 试 3 个最常见解法仍不通 → 带"三件套"（报错截图、你执行的命令、部署平台）走课程群（教师 24h 内响应）。
> **兜底规则**：W11 周末仍不通 → 本地运行 + 录屏 Demo 暂过本周验收，完整部署顺延至 W12 周末前。

---

## 第 0 步：先分清走哪条路线

| 路线 | 适合 | 上手难度 | 注意 |
|---|---|---|---|
| **Streamlit Cloud** | 纯 Streamlit 应用、想最快公网可达 | 低：连 GitHub 仓库即自动部署 | 仓库须公开或授权；冷启动慢；有资源限额；**文件系统临时性——运行时写入的文件重启即丢** |
| **Hugging Face Spaces / Gradio** | Gradio 应用或想附带展示 | 低 | 同上，免费额度内 |
| **腾讯云轻量应用服务器** | 需要常驻进程、数据库、自定义端口 | 中：Linux 基本功 | 校园额度**审核有等待期，周初就申请**；防火墙=安全组+系统防火墙两层 |

选一个主路线 + 一个备选路线写进部署方案；两条都卡时，先用备选保验收。

---

## 第 0.5 步：部署前检查清单

> 对应 plan.md 第 2 节第 4 步。部署前花 2 分钟逐项自查，能消除 80% 的部署后报错。

- [ ] `requirements.txt` 存在且与本地 `pip list` 一致（`python -m pip freeze > requirements.txt`）
- [ ] `.env` 在 `.gitignore` 中（`git status` 看不到 `.env`）
- [ ] 代码里无硬编码路径 `C:\...`（用 `pathlib.Path` 或相对路径）
- [ ] 数据文件 >50MB 的不进 git（改为启动时拉取或手动上传）
- [ ] 代码里密钥用 `os.getenv()` / `st.secrets` 读取（未硬编码）

未通过的项目当场改；全部通过再进入部署。

---

## 一、环境与依赖类

**症状：本地能跑，服务器上跑不起来（ModuleNotFoundError / 版本冲突）**

1. 服务器上生成依赖清单：`pip freeze > requirements.txt`，或检查本地 `pip list` 与 requirements 是否一致。
2. 确认 Python 版本一致（本地 3.1x，服务器别用系统自带的 3.6）。
3. Streamlit 版本过旧会报奇怪的 API 错误：`pip install -U streamlit`。
4. Windows↔Linux 路径差异：代码里用 `pathlib.Path` 或相对路径，别写 `C:\...`。
5. 中文字体/编码报错：文件统一存 UTF-8；绘图中文乱码时显式指定字体。

## 二、进程与端口类

**症状：关掉终端/退出 SSH，网站就访问不了了**

1. 原因：`streamlit run app.py` 是前台进程，会话结束即被杀。
2. 轻量服务器解法（三选一）：
   - `nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > app.log 2>&1 &`（最简单，日志在 app.log）
   - `screen -S app` 或 `tmux` 会话内运行
   - 配置 systemd 服务（进阶，开机自启+崩溃自动拉起）
3. 服务没起来先自查：`ps aux | grep streamlit` 看进程在不在；`tail -n 50 app.log` 看报错。
4. 端口占用：`Address already in use` → 换端口或杀掉旧进程。

## 三、网络与公网访问类

**症状：进程活着，但浏览器打不开 `http://<公网IP>:8501`**

按顺序排查（大概率是前两条）：

1. **监听地址**：日志里是 `127.0.0.1:8501` 还是 `0.0.0.0:8501`？前者只接受本机访问，须加 `--server.address 0.0.0.0`。
2. **云安全组**：腾讯云控制台 → 轻量服务器 → 防火墙 → 放行 TCP 8501（或你用的端口）。这是最常漏的一步。
3. **系统防火墙**：服务器上 `sudo ufw status` / `firewall-cmd --list-ports`，未放行则加上。
4. **本机自查**：在服务器上 `curl 127.0.0.1:8501` 能通说明应用正常，问题在网络层。
5. 校园网访问受限：换手机热点试一次，区分"服务器没起来"和"你网络到不了"。

## 四、API Key 与敏感信息管理

> 课程用到的密钥：`TUSHARE_TOKEN`（Tushare 数据接口）、`DEEPSEEK_API_KEY`（或其它 LLM 平台 Key）。
> 详细申请与使用见 `weeks/week09/llm-key-guide.md`。

**症状：部署后 AI 功能失效 / 收到异常消费提醒 / GitHub 安全告警**

### 4.1 三条安全红线

1. **Key 绝不写进代码**——用环境变量或 `.env` 文件读取：
   ```bash
   # .env（加入 .gitignore，永不提交）
   TUSHARE_TOKEN=你的token
   DEEPSEEK_API_KEY=sk-xxxx
   ```
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   token = os.getenv("TUSHARE_TOKEN")
   ```

2. **`.env` 绝不入 git**——确认 `.gitignore` 包含 `.env`：
   ```bash
   # 检查 .gitignore 是否有 .env
   grep ".env" .gitignore
   # 检查 git 是否已跟踪 .env（应为空）
   git ls-files | grep ".env"
   ```

3. **课程演示 Key 只能本地用**——部署必须换自己的 Key（见 `weeks/week09/llm-key-guide.md`）

### 4.2 已经把 Key 推到 GitHub 了怎么办

**视同泄露，立即处理：**

1. **去平台吊销旧 Key**：Tushare → 个人主页 → token 管理 → 删除；LLM 平台 → 控制台 → API Keys → 删除
2. **重新生成新 Key**
3. **清理 git 历史**（否则旧 Key 永远在历史里）：
   ```bash
   # 查看哪个提交泄露了 Key
   git log -p | grep -n "TUSHARE_TOKEN\|DEEPSEEK_API_KEY\|sk-"
   # 最简单：把 .env 加入 .gitignore 后，从 git 移除（不删本地文件）
   git rm --cached .env
   git commit -m "remove .env from tracking"
   # 彻底清除历史（进阶，会改写所有提交）：
   # git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all
   ```
4. **GitHub 安全提醒**：如果 GitHub 已发邮件告警（Secret Scanning），说明 Key 已被公开扫描到，必须吊销。

### 4.3 部署时密钥怎么配

| 平台 | 方法 | 格式 |
|---|---|---|
| **Streamlit Cloud** | App Settings → Secrets | TOML 格式（见下方详细步骤） |
| **腾讯云服务器** | `~/.env` 文件 或 systemd `Environment=` | `KEY=value` 逐行 |
| **本地开发** | 项目根目录 `.env` 文件 | `KEY=value` 逐行 |

#### Streamlit Cloud Secrets 配置（详细步骤）

**第 1 步：打开 Secrets 页面**

1. 登录 https://share.streamlit.io
2. 在你的 App 卡片右下角点击 ⋮ 菜单 → **Settings**（或 App 页面右上角菜单 → Settings）
3. 在弹出面板中找到 **Secrets** 区域

**第 2 步：粘贴密钥（TOML 格式，注意不是 .env 格式）**

```toml
# Secrets 文本框内容（TOML 格式，每行一个变量）
# 注意：有等号、有引号、没有 export
TUSHARE_TOKEN = "你的tushare_token"
DEEPSEEK_API_KEY = "sk-你的deepseek_key"
```

> **TOML 格式与 .env 格式的区别**（最容易踩的坑）：
>
> | | `.env`（本地用） | Secrets TOML（Streamlit Cloud 用） |
> |---|---|---|
> | 格式 | `KEY=value` | `KEY = "value"` |
> | 引号 | 不需要 | **必须加双引号** |
> | 空格 | 不能有空格 | 等号两边可以有空格 |
> | export | 可加可不加 | 不能加 |
>
> 错误示例：`DEEPSEEK_API_KEY=sk-xxxx`（少了引号，TOML 会报错）
> 正确示例：`DEEPSEEK_API_KEY = "sk-xxxx"`

**第 3 步：点 Save，等待 App 自动重启**

保存后 App 会自动重新部署，日志区显示 `Secrets updated`。如果没自动重启，手动点 Reboot。

**第 4 步：代码中读取**

```python
import streamlit as st

# 方式一：只用 Streamlit Cloud（适合纯部署场景）
token = st.secrets["TUSHARE_TOKEN"]
```

```python
# 方式二：Streamlit Cloud + 本地兼容（推荐）
# 本地用 .env，云端用 st.secrets，同一份代码跑两套环境
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # 本地读 .env（云端无此文件，静默跳过）

def get_secret(key: str) -> str:
    """优先读 st.secrets（云端），回退到环境变量（本地 .env）"""
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return os.getenv(key)

# 使用
tushare_token = get_secret("TUSHARE_TOKEN")
deepseek_key = get_secret("DEEPSEEK_API_KEY")
```

> `st.secrets` 在本地运行时会尝试读取 `.streamlit/secrets.toml` 文件。
> 如果该文件不存在（正常情况），抛出 `FileNotFoundError`——上面的 `get_secret()` 会回退到 `os.getenv()`，本地照常工作。

**第 5 步：验证密钥生效**

部署完成后打开 App，触发用到密钥的功能（如调用 LLM 解读）。如果报错：
- 报 `KeyError` → Secrets 里键名和代码不一致，检查拼写
- 报 401/403 → Key 本身无效或已过期，去平台重新生成
- 功能正常但返回空 → 看日志（App 页面菜单 → Logs）确认 API 调用是否发出

### 4.4 推荐做法：`.env.example` 模板

在仓库里放一个 `.env.example`（不含真实值），让其他人知道需要哪些环境变量：
```bash
# .env.example（可以入 git）
TUSHARE_TOKEN=在此填入你的tushare_token
DEEPSEEK_API_KEY=在此填入你的api_key
```

### 4.5 部署后 AI 功能 500/超时

1. 先看应用日志是不是 key 无效或过期
2. 看服务器能否出网访问 API 域名：`curl -I https://api.deepseek.com`（腾讯云服务器需检查出网规则）
3. 检查密钥键名是否一致：代码里 `os.getenv("DEEPSEEK_API_KEY")` ≠ Secrets 里 `DEEPSEEK_KEY`

## 五、数据与持久化类

**症状：网页报"找不到数据文件" / git push 被拒 / 重启后数据丢失**

1. 数据文件太大（>50MB 或仓库超限）：不要提交进 git；改为**产品启动时由获取脚本现场拉取**（把 W4 脚本挂到服务器定时跑），或走对象存储/手动 scp 上传并在代码中按绝对路径读取。
2. SQLite 路径写死本地路径 → 服务器上换成实际路径；确认运行用户对库文件有写权限。
3. **Streamlit Cloud 文件系统是临时的**：容器重建后所有运行时写入的文件都会丢——不只是 SQLite，还包括用户上传的文件、缓存、日志。需要持久化的数据必须走外部存储（对象存储 / 外部数据库），或改为只读模式。
4. 云端只读文件系统/权限报错：数据目录放到用户 home 下，别写 `/` 或 `/opt`。
5. W12-W15 模型文件（pkl 等）同理：太大的不进 git，放服务器本地，代码按路径加载。

---

## 升级求助模板（走课程群时照抄）

```
平台：腾讯云轻量 / Streamlit Cloud / 其他
症状：（如：curl 127.0.0.1:8501 通，公网打不开）
已做：（对照 FAQ 第__类，试过：1... 2... 3...）
报错截图 + 执行命令：
部署方案链接：
```
