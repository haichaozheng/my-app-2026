# MCP-zotero上机实验 — AI辅助个人项目调研与写作

> **实验时长**：约 105 分钟 + 选题交流环节（可分两次完成：步骤 1-4 一次，步骤 5-10 一次）  
> **实验目标**：升级 OpenCode v2 → 理解 MCP 概念 → 配置并体验 tushare MCP（金融数据）→ 配置并体验 zotero MCP（文献库）→ 用 Zotero 精读一篇论文并入门文本分词 → 掌握 APA「作者-日期」引用规范 → 为后续「文献检索 Skill」和开题打磨做准备  
> **参考文档**：OpenCode v2 [https://opencode.ai/v2/docs/](https://opencode.ai/v2/docs/)　MCP 官网 [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)

---

## 前置条件检查


| 检查项          | 验证命令                 | 预期结果         | 备注                                          |
| ------------ | -------------------- | ------------ | ------------------------------------------- |
| Node.js 已安装  | `node -v`            | `v24.x.x` 左右 | W2 已装，装不上见 `weeks/week02/opencode-setup.md` |
| opencode 已安装 | `opencode --version` | 显示版本号        | 见步骤 1                                       |
| Zotero 已安装   | 打开 Zotero 看到主界面      | Zotero 7+    | 步骤 5 前装好即可                                  |


---



## 步骤 1 · 升级到 OpenCode v2（5 分钟）

v2 是当前官方主线（一个后台服务统一支撑终端/桌面/Web），课程后续内容都按 v2 文档讲。W2 用 npm 装过的同学只需确认版本。

**升级 / 更新**（PowerShell 中执行，没装过和装过都跑同一条）：

> ⚠️ **先关掉所有正在运行的 opencode，再执行安装**：
>
> 1. 每个开着 opencode 界面的终端窗口，按 `Ctrl+C`（或直接 `q`）退出，然后关掉该窗口
> 2. opencode v2 还有一个常驻后台服务；想确认没有残留，可在 PowerShell 里执行 `tasklist /FI "IMAGENAME eq opencode.exe"`，有输出就说明还有进程没退干净（任务管理器里结束它，或重启电脑兜底）
> 3. **重新开一个 PowerShell** 再执行下面的安装命令
>
> 不先关闭就直接装，Windows 下常报 `EPERM`/`EACCES`（文件被占用）；即使装上了，旧的后台服务还跑着旧版本，`opencode --version` 会让你误以为升级失败。

```text
npm install -g @opencode/cli
```

若提示禁止运行脚本，用 `npm.cmd install -g @opencode/cli`。装完后**新开一个终端**（让 PATH 生效）再验收——下次运行 `opencode` 时它会自动拉起新版本的后台服务。

**验收**：

```text
opencode --version
```

输出 `opencode v2.x.x` 即通过。若显示 `v1.x.x`（老版本），在 opencode 界面里输入 `/update` 选择升级，或执行 `opencode upgrade --major`，完成后再验收一次。

> v1 的配置文件 v2 直接兼容，不必删除旧配置。终端主题等偏好若丢失，重新设置一次即可（v2 里它们保存在单独的 `cli.json`）。

---



## 步骤 2 · 理解 MCP 是什么（10 分钟）

读两篇官方入门（英文读不动就交给 AI 翻译总结，这本身就是合法用法）：

1. Introduction：[https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro)
2. Architecture：[https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)

读完能用自己的话回答三问（写在实验记录里，各 ≤2 行）：

1. **MCP 解决什么问题**：以前每个 AI 应用都要单独对接每个数据源，MCP 把「AI ↔ 外部工具」的接口标准化（官方比喻：AI 世界的 USB-C 口）。
2. **三方架构**：Host（跑 AI 的程序，如 opencode）、Client（Host 里管连接的部件）、Server（提供工具的一方，如 tushare）各是什么？
3. **两种服务器**：`local`（本地命令启动，stdio 通信，如 zotero-mcp）和 `remote`（远程 URL，HTTP 通信，如 tushare）——本实验两种都会配。

---



## 步骤 3 · 配置 tushare MCP（10 分钟）



### 3.1 获取你自己的 token

1. 注册/登录 [https://tushare.pro](https://tushare.pro)
2. 进入**个人中心 → MCP Server**，复制你的 MCP token
3. 注意：MCP token 的入口和普通「接口 TOKEN」**不是同一个**，别拿错



### 3.2 新建 opencode.jsonc

在你的项目工作文件夹根目录新建 `opencode.jsonc`，内容如下（把 `tushare_token` 换成你刚复制的 token）：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "tushare": {
        "type": "remote",
        "url": "https://api.tushare.pro/mcp/?token=5c426f5af978fd42fe0f81fe7e60c02ada33d6c79347b61ccb44f521",
        "oauth": false
      }
    }
  }
}
```

三个要点，配错多半错在这里：

- v2 的写法是 `"mcp": { "servers": { ... } }`，服务器放在 `mcp.servers` 下面。tushare 官网示例的 `mcpServers` 是 Claude/Cursor 的格式，**直接照抄会读不到**。
- `"type": "remote"`：tushare 是远程服务，不用在本地装任何东西。
- `"oauth": false`：tushare 用 URL 里的 token 鉴权，不是 OAuth 登录，这行要加。

**安全红线**（同 W9 的 LLM Key 规则）：token 只写在自己本地的 `opencode.jsonc` 里——不截图发群、不提交到 GitHub。若你的工作文件夹是 git 仓库，先把 `opencode.jsonc` 加进 `.gitignore`；已经推上去的，去 tushare 个人中心刷新 token 重新生成一个。

### 3.3 验证连接

保存后**重启 opencode**（退出再进，配置才会重新加载），然后：

```text
opencode mcp list
```

看到 `✓ tushare connected` 即成功。也可以在 opencode 界面里输入 `/mcps` 查看连接状态。若显示连接失败，九成是 token 复制错了或少了 `oauth: false`。

---



## 步骤 4 · 体验 tushare MCP（15 分钟）

在 opencode 里依次输入（可按自己的项目改股票和行业）：

**① 基础查询**：

```text
获取贵州茅台（600519.SH）最近 10 个交易日的日线行情
```

**② 换成你项目相关的标的**：

```text
查询我项目关注的股票 XXX 的最新行情和基本资料
```

**③ 让数据直接进分析流程**：

```text
用 tushare 获取 XXX 最近 60 个交易日收盘价，存成 CSV，并画出走势图
```

**观察三件事**（写进实验记录）：

1. AI 是不是**没有写 Python 调 tushare pro 接口的代码**，直接调用了 `tushare` 的 MCP 工具？这就是 MCP 的意义：零代码取数。
2. 工具是怎么被点名的：对话里说「用 tushare」，或在提示词里点 `tools.tushare` 均可。
3. 数据回来的形态：是结构化的行情记录，不是网页文本。

**限额提醒**：tushare 按积分限调用频率，新注册用户积分有限。体验阶段每个查询 1-2 次足够，别在课堂上循环刷。

---



## 步骤 5 · 为 Zotero 准备文献（10 分钟）

后面要学「文献检索 Skill」，在那之前先让你的 Zotero 库里有料，zotero MCP 才有东西可查。

1. 打开 Zotero，新建一个集合（collection），命名如「项目文献」
2. 围绕你的项目选题/开题方向，导入 **3-5 篇文献**，任选方式：
  - 装浏览器插件 Zotero Connector，在知网 / 谷歌学术 / 万方等页面一键抓取
  - 直接把下载好的 PDF 拖进该集合
3. 检查：点开每条文献，确认标题、作者、年份等元数据是完整的（抓取失败的条目 AI 后面也读不出来）

> 没有明确选题的同学：就按 W7 开题报告的备选方向抓文献。这一步攒下的库，步骤 7 会直接用来做选题评估。

---



## 步骤 6 · 配置 Zotero MCP（10 分钟）



### 6.1 打开 Zotero 的本地通讯开关

zotero MCP 走的是 Zotero 桌面端的本地接口，要先放行：

1. Zotero 菜单：**编辑 → 设置 → 高级**
2. 勾选 **「允许此计算机上的其他应用程序与 Zotero 通讯」**
3. **保持 Zotero 一直开着**（后面所有 zotero 查询都要求它在运行）



### 6.2 安装 zotero-mcp 服务器

本地型 MCP 需要装一个小程序。在 PowerShell 里：

```text
py -3.13 -m pip install zotero-mcp-server
```

装完新开一个终端，验收：

```text
zotero-mcp --help
```

能打印帮助信息即通过。若提示「无法识别命令」：执行 `where zotero-mcp` 找到它的完整路径，下一步的 `command` 里改用完整路径（JSON 里 Windows 路径要写双反斜杠 `\\`）。

> 注意：这个包装在 Python 全局环境，**不要**装进项目 `.venv`——opencode 启动 MCP 时不会经过你的虚拟环境。



### 6.3 加进 opencode.jsonc

在步骤 3 的文件里追加 zotero 条目（一个文件同时管两个 MCP）：

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "tushare": {
        "type": "remote",
        "url": "https://api.tushare.pro/mcp/?token=tushare_token",
        "oauth": false
      },
      "zotero": {
        "type": "local",
        "command": ["zotero-mcp"],
        "environment": {
          "ZOTERO_LOCAL": "true",
          "PYTHONUTF8": "1"
        }
      }
    }
  }
}
```

对照步骤 2 的概念：tushare 是 `remote`（URL 连接），zotero 是 `local`（本地命令启动）——两种类型齐了。`ZOTERO_LOCAL: "true"` 表示读本地 Zotero，**不需要**申请任何 API key；`PYTHONUTF8: "1"` 是 Windows 中文编码的经验配置。

### 6.4 验证

重启 opencode（Zotero 保持运行），再执行：

```text
opencode mcp list
```

这次应看到两条：`✓ tushare connected` 和 `✓ zotero connected`。zotero 显示失败时，先检查 Zotero 是否开着、6.1 的勾是否打上了。

---



## 步骤 7 · 体验 Zotero MCP：文献综述与选题评估（15 分钟）

依次输入（把「我的项目文献」换成你的集合名）：

**① 清点家底**：

```text
列出我的 Zotero「项目文献」集合里的所有文献：标题、作者、年份、期刊
```

**② 单篇速读**：

```text
读库里 XXX 这篇文献的元数据和摘要，给我一段 100 字左右的中文小结，说清它研究什么问题、用什么方法、什么结论
```

**③ 文献综述草稿**：

```text
基于我 Zotero「项目文献」集合里的全部文献，围绕我的研究题目「XXX」，写一段 300 字的文献综述草稿。要求：说明现有研究做了什么、还缺什么，并注明每句话依据的是哪篇文献
```

**④ 选题评估**（直接对接 W7 开题报告）：

```text
结合我库里的文献，评估我的选题「XXX」：新颖性如何（和已有研究的区别）、可行性（数据和方法拿不拿得到）、可能的贡献点，最后给 3 条具体的改进建议
```

**必做核对**（本实验最重要的一条经验）：AI 做文献综述时会**编造不存在的引用**。把它提到的每一篇都回到 Zotero 里对一遍：题目对得上吗？它说的观点文献里真有吗？对不上的记下来——这就是「核对结果是否可信」，和 W8 文本分析里核对情感标签是同一个动作。

---



## 步骤 8 · 精读一篇论文：AI 导向与中文分词（15 分钟）

最后用一篇真实的论文，把「Zotero 读文献」和「文本分析」串起来。课程提供论文 PDF：**《Strategic Directions for AI: The Role of CIOs and Boards of Directors》**（Li Jingyu、Li Mengxiang、Wang Xincheng、Thatcher Jason Bennett，发表于 *MIS Quarterly* 2021 年「Managing AI」专刊），文件在课程仓库 `weeks/week08/STRATEGIC DIRECTIONS FOR AI.pdf`（或从课程群下载）。这篇论文研究**中国上市公司的 AI 战略导向（AI orientation）由谁驱动**，和本课程「财经 + 数据分析」的背景高度契合。

### 8.1 导入论文

1. 拿到 PDF 后，直接**拖进** Zotero 的「项目文献」集合
2. 检查元数据：这类工作论文/专刊论文常抓不全 DOI，字段缺失就手动补——至少把**四位作者、标题、期刊名、年份**补齐（AI 后面读的就是这些元数据，补不齐它就「不认识」这篇文献）



### 8.2 用 Zotero 精读：盯住「测量」和「结论」

依次输入：

**① 速览**：

```text
读我 Zotero 里「Strategic Directions for AI」这篇文献的元数据和摘要，给我一段 150 字左右的中文小结：研究什么问题、用什么数据、什么结论
```

**② 深挖测量方法**（本步骤的重点）：

```text
用 zotero 读这篇论文的正文，详细说明 AI orientation（AI 导向）这个变量是怎么测量的：用了什么数据源、分了哪几类关键词、用了什么工具、最终编码成什么变量
```

**③ 挖核心结论**：

```text
这篇论文的核心结论是什么？CIO 在场对 AI orientation 有什么影响？董事会的哪些特征在起作用？post hoc 分析有什么发现？
```

**④ 批判性追问**：

```text
这种基于年报关键词的测量方法有什么局限？如果让我改进，可以从哪里入手？
```

**对照参考**（读完自查，别直接抄）：

- 测量：作者对 **1,454 家中国上市公司 2016-2018 年的年报**做文本挖掘，按 7 类关键词（机器学习、自然语言处理、专家系统、语音、视觉、规划、高智能机器人）提取，先用 Python 程序跑，再由受训的研究助理人工校验，最终把 AI orientation 编码成 **0/1 二值变量**（年报里有没有体现 AI 战略）
- 结论：**CIO 在场正向影响 AI orientation**；董事会的**教育多样性、R&D 经验、AI 经验**会放大 CIO 的作用；而这些董事会特征**只影响 AI orientation，不影响传统 IT orientation**——说明 AI 战略与传统 IT 战略的驱动机制不同



### 8.3 从这篇论文认识「分词」

看明白测量方法后你会发现：作者的核心操作其实是**在中文年报里数关键词**。但中文和英文不一样——英文单词之间有空格，计算机天然知道 `machine learning` 是两个词；中文「公司将加快人工智能与机器学习应用」是一整串汉字，计算机并不知道「人工智能」是一个词还是四个独立的字。**把连续的汉字串切分成词，就是分词（word segmentation）**——它是几乎所有中文文本分析（词频统计、情感分析、主题模型）的第一步。没有分词，论文里那套关键词计数就无从谈起。

### 8.4 jieba：最常用的中文分词工具

jieba（结巴分词）是 Python 生态最常用的中文分词库，基础用法只要三行。在项目 `.venv` 里装一下（参照 week01 的环境说明）：

```text
python -m pip install jieba
```

然后**新建一个 Python 文件**来试运行（模仿论文的测量思路）。在你的项目工作文件夹里新建 `jieba_demo.py`（名字随意，`.py` 后缀即可），把下面的代码写进去再运行——别在 opencode 对话里贴一段跑一段，代码留在文件里，后面才能反复改、反复跑。

> 💡 **推荐做法：让 opencode 帮你建文件写代码**。在 opencode 里输入类似下面的提示词，它会自动新建文件、写入代码，你只需要运行看结果：
>
> ```text
> 在我的项目文件夹里新建 jieba_demo.py，写一段演示 jieba 中文分词的代码：用精确模式和全模式分别切分一句模拟的年报文本，并对照一个 AI 关键词列表统计命中了哪些关键词。写完告诉我怎么运行。
> ```
>
> 也可以自己手敲——两种方式都行，重点是**代码要落在 `.py` 文件里**，并且**自己运行一遍、亲眼看输出**。运行方法：在 opencode 里让 AI 帮你跑，或在激活项目 `.venv` 的终端里执行 `python jieba_demo.py`（激活方法见 week01 环境说明）。

下面是完整的参考代码（可直接让 opencode 写入文件，或自己抄写）：

```python
import jieba

# 模拟一句年报文本
text = "公司将积极推进人工智能与机器学习技术在生产管理中的应用"

# 精确模式：每个字只属于一个词，不重不漏
print(jieba.lcut(text))
# ['公司', '将', '积极', '推进', '人工智能', '与', '机器', '学习', '技术', '在', '生产', '管理', '中', '的', '应用']

# 全模式：把句子里所有「能成词」的组合都扫出来
print(jieba.lcut(text, cut_all=True))
# ['公司', '将', '积极', '推进', '人工', '人工智能', '智能', '与', '机器', '学习', '技术', '在', '生产', '管理', '中', '的', '应用']
```

两种模式的区别（对照参考，跑一遍亲眼看）：


|      | 精确模式 `jieba.lcut(text)` | 全模式 `jieba.lcut(text, cut_all=True)` |
| ---- | ----------------------- | ------------------------------------ |
| 切分原则 | 每个字只属于一个词，不重不漏          | 把所有「能成词」的组合全扫出来                      |
| 重叠冗余 | 无                       | 有——「人工智能」同时产出「人工」「人工智能」「智能」三个词       |
| 典型用途 | 词频统计、关键词计数              | 搜索引擎索引（宁可多召回，不怕冗余）                   |


「数关键词」要用**精确模式**：全模式下「人工智能」会同时贡献「人工」「智能」两个噪声词，同一处文本被重复计数，统计口径就乱了——这正是论文做词频测量必须避开的问题。

**再留意一个坑**：上面精确模式把「机器学习」切成了「机器」+「学习」——jieba 的默认词典未必收录你研究领域的术语。解决办法是先注册自定义词：

```python
jieba.add_word("机器学习")   # 注册后「机器学习」会作为一个整词被切出

# 仿照论文：统计 AI 关键词命中情况
ai_keywords = ["人工智能", "机器学习", "深度学习", "自然语言处理", "图像识别", "机器人", "专家系统"]
words = jieba.lcut(text)
print([w for w in words if w in ai_keywords])
# 注册前: ['人工智能']        ← 「机器学习」被切碎，漏计了
# 注册后: ['人工智能', '机器学习']
```

这也解释了论文作者为什么要预先定义那 7 类关键词词表：词典分词工具「认识什么词」，直接决定你的测量能「数到什么」——**词典就是测量工具的一部分**。

### 8.5 大模型时代还需要学分词吗？

需要**理解**，不需要**精通**。jieba 这类工具诞生于大模型之前，规则和词典再精细也总有切错的句子。如今大模型已经把分词解决得很好——把句子直接交给大模型（在 opencode 里对话，或通过 API 接入你自己的程序），它不但能分词，还能顺手完成关键词提取、语义判断、情感倾向这些原本要专门写代码的活。所以本课程的态度是：**用 5 分钟跑一遍 jieba，理解「分词是什么、为什么中文绕不开它」；实际项目里，优先把这类文本处理交给大模型 API**。这也是后面周次「调用 LLM API 做文本分析」的伏笔。

---



## 步骤 9 · 文献引用规范：APA 格式（10 分钟）

写作绕不开引用。课程统一采用 **APA 格式**——美国心理学会（American Psychological Association）制定的引用规范，当前通行的是**第 7 版**（APA 7th）。

### 9.1 核心机制：「作者-日期」制

APA 的核心是**「作者-日期」（author-date）制**：引用时不给文献编号，而是随文标出「谁 + 哪一年」。它要求你的论文中必须包含**两个相互对应的部分**：

1. **文中引注（in-text citation）**：出现在正文里，紧跟被引用的观点
2. **文末参考文献列表（reference list）**：论文末尾，给出每条文献的完整信息

两者**共同构成一次完整的引用**：正文里出现过的每一个引注，列表里必须有对应条目；列表里的每一条，正文里也必须引过——一一对应，缺一边都是不完整的引用。

### 9.2 示例（直接用步骤 8 精读过的那篇）

**文中引注**（两种写法）：

> 已有研究表明，CIO 的存在能显著推动企业形成 AI 战略导向（Li et al., 2021）。　　　← 括号式，句末
>
> Li et al.（2021）基于 1,454 家中国上市公司的数据发现……　　　← 叙述式，作者做主语

**文末参考文献列表**：

> Li, J., Li, M., Wang, X., & Thatcher, J. B. (2021). Strategic directions for AI: The role of CIOs and boards of directors. *MIS Quarterly, 45*(3), 1603–1643. [https://doi.org/10.25300/MISQ/2021/16523](https://doi.org/10.25300/MISQ/2021/16523)

对照着看对应关系：正文里的 `Li et al., 2021` ↔ 列表开头的 `Li, J., ... (2021)`；列表条目还要补全期刊、卷期、页码和 DOI，让读者能按图索骥找到原文。

几条最常用规则（够你完成课程论文）：


| 场景       | 写法                              |
| -------- | ------------------------------- |
| 1 位作者    | （张三， 2022）                      |
| 2 位作者    | （Li & Wang, 2021），两人都要写         |
| 3 位及以上   | 第一作者 + et al.：（Li et al., 2021） |
| 直接引用原文   | 加页码：（Li et al., 2021, p. 1610）  |
| 同一作者同年多篇 | 年份加字母：（Li, 2021a； Li, 2021b）    |




### 9.3 用 opencode 辅助加引用

引用是**格式活**，正是 AI 擅长的。把步骤 7 的综述草稿拿出来，在 opencode 里试：

```text
这是我写的一段文献综述：XXX（贴你的段落）。请为其中每个观点补上 APA 7 的文中引注，
格式为（作者, 年份）；文献只能用我 Zotero「项目文献」集合里的，先列出库里的文献再对应，
不要编造引文。最后按 APA  格式生成文末参考文献列表。
```

> ⚠️ **老规矩**（同步骤 7 的必做核对）：AI 排 APA 格式很在行，但**仍会编造不存在的引用**。让它只从你的 Zotero 库里取文献；生成后逐条回 Zotero 核对——文中引注的作者、年份和列表条目是否对得上库里真实的文献。**AI 辅助写作，作者负责核对**，这是本课程一以贯之的原则。

---



## 步骤 10 · 个人项目选题：调研、写作与老师交流（课堂时间 + 课后）

同学们开始调研、写作，并和老师单独交流选题，以及本周课堂内容。

---



## 自检（达标线）

- [ ] 能不看笔记说出 `local` 和 `remote` 两种 MCP 的区别，以及本实验各对应谁
- [ ] 能说清为什么 tushare 官网示例不能直接抄进 opencode v2（`mcpServers` vs `mcp.servers`）
- [ ] tushare 和 zotero 两个 MCP 都是「我自己配出来的」，不是别人代配
- [ ] token 没出现在任何提交物里（截图记得打码）
- [ ] AI 文献综述里每一条引用都回 Zotero 核对过
- [ ] 能说出《Strategic Directions for AI》把 AI orientation 编码成了什么变量、用了什么数据
- [ ] 能用自己的话说清什么是分词、为什么中文文本分析绕不开它，以及大模型时代怎么看待 jieba 这类工具
- [ ] 能说清 APA「作者-日期」制的两个组成部分及其对应关系，并写出一组合格的文中引注 + 参考文献条目



## 卡住了找谁

卡住 → ①先把报错原文交给 AI 问（附 `opencode mcp list` 输出和 `opencode.jsonc` 内容，**token 打码**）→ ②互助组（当日）→ ③课程群（教师承诺 24h 内响应）。

高频卡点速查：


| 现象                                   | 多半是                                                   |
| ------------------------------------ | ----------------------------------------------------- |
| 安装时报 `EPERM`/`EACCES` 或升级后版本没变       | 没先关掉所有 opencode 进程（见步骤 1 的 ⚠️）就执行了 npm install        |
| tushare 连不上 / 报 token 无效             | token 复制错、拿了普通接口 TOKEN 而非 MCP token、少了 `oauth: false` |
| zotero 连不上                           | Zotero 没开、6.1 的勾没打、`zotero-mcp` 不在 PATH（用完整路径）        |
| 改了配置没反应                              | 没重启 opencode                                          |
| zotero 查询返回空                         | 集合名打错，或文献元数据没抓全                                       |
| `import jieba` 报 ModuleNotFoundError | 装包和运行用的不是同一个 Python（确认跑在项目 `.venv` 里）                 |
| zotero 读不到论文正文                       | PDF 没导入成条目（只是拖进了文件夹），或导入时元数据没补齐                       |


