# 云部署

> **引入时机**：W11 | **核心挑战**：产品只能在本地跑，如何让目标用户公网访问？ | **层级**：Essential

## 为什么要在项目阶段学习这个知识点？

当你的金融数据分析产品在本地上跑得很好时，你会面临一个现实问题：你的目标用户——无论是投资俱乐部成员、课程导师还是潜在客户——都无法访问你电脑上的应用。产品只有在被用户使用时才有价值，而本地运行的程序对你的用户来说等于不存在。云部署是产品从"我能用"到"大家能用"的关键一步。

很多同学在开发阶段忽略了部署问题，到了需要公开展示或交付时才匆忙处理，结果遇到端口配置、依赖冲突、域名解析等一系列问题。提前了解部署方案和工作流，不仅能让最终交付更顺畅，还能在开发过程中就考虑部署相关的技术约束（如文件大小、依赖管理、环境变量），减少后期的返工。

云部署还涉及安全性和可靠性问题——金融数据产品可能包含用户的持仓信息或交易策略，你需要确保数据传输和存储的安全。理解基本的部署架构，是构建用户信任的基础。

## 这个知识点的核心内容

### 部署方案对比

不同的产品形态适合不同的部署方案，选择时需要综合考虑技术栈、成本、流量和团队能力：

- **Streamlit Community Cloud**：最简单的Streamlit应用部署方案，免费、一键部署、自带HTTPS，适合原型展示和课程项目。限制：单应用资源有限、不支持自定义后端、每月有限运行时长
- **Vercel / Netlify**：前端应用和静态站点的首选，支持自动CI/CD、全球CDN、免费额度充足。如果你的产品是纯前端（如Dash应用编译后的静态版本），这是最佳选择
- **Docker + 云服务器**：最灵活的方案，适用于任何技术栈。你可以在阿里云、腾讯云、AWS等平台上租用云服务器，用Docker容器化部署。成本较高但可控性最强，适合需要后端服务的产品
- **平台即服务（PaaS）**：如Railway、Render、Fly.io，介于托管平台和自建服务器之间，支持Docker部署但无需管理服务器，适合中小规模产品

### 部署工作流

一个标准的部署工作流包含以下步骤：

1. **环境准备**：确保应用能在目标环境运行，包括Python版本、依赖列表（requirements.txt）、环境变量配置
2. **代码仓库**：将代码推送到GitHub/GitLab，大多数部署平台支持从仓库自动部署
3. **配置部署**：在部署平台上创建项目，关联代码仓库，配置环境变量和构建命令
4. **域名与HTTPS**：绑定自定义域名，配置SSL证书（多数平台自动提供）
5. **验证测试**：部署后进行功能测试，确保所有功能在生产环境正常工作
6. **持续更新**：后续代码更新通过git push触发自动重新部署

### 域名与SSL

域名是用户访问你产品的入口，SSL证书确保数据传输加密：

- **域名选择**：简短、易记、与产品相关。常见域名注册商：阿里云、腾讯云、GoDaddy
- **DNS解析**：将域名指向部署平台提供的服务器地址，通常在域名管理后台配置A记录或CNAME记录
- **SSL证书**：Let's Encrypt提供免费证书，大多数部署平台（Streamlit Cloud、Vercel等）自动配置HTTPS。金融产品必须使用HTTPS

### 监控基础

部署不是终点，产品上线后需要持续监控：

- **可用性监控**：确保服务持续在线，UptimeRobot等免费工具可以每5分钟检测一次
- **错误监控**：捕获和记录运行时错误，Sentry提供免费额度
- **访问统计**：了解用户行为，Google Analytics或Plausible（注重隐私）
- **性能监控**：页面加载时间、API响应时间，影响用户留存

## 关键细节与易错点

### 依赖版本不一致

本地运行正常但部署后报错，最常见的原因是依赖版本不一致。务必使用`pip freeze > requirements.txt`锁定版本，并在部署前在干净环境中测试。

### 环境变量泄露

API密钥、数据库密码等敏感信息绝不能硬编码在代码中。使用环境变量管理，在部署平台的设置面板中配置。`.env`文件必须加入`.gitignore`，防止推送到公开仓库。

### 资源超限

免费额度有限，Streamlit Community Cloud限制应用内存和运行时长，Vercel有Serverless函数执行时间限制。金融数据获取如果耗时较长，可能触发超时。解决方案：预计算数据、使用缓存、升级付费计划。

### 忽视冷启动

Serverless和托管平台存在冷启动问题——应用一段时间无访问后会休眠，首次访问需要重新启动，可能等待10-30秒。对于金融仪表板这种需要快速响应的产品，这会严重影响用户体验。可以设置定时唤醒或使用常驻实例。

### 数据持久化

Streamlit Community Cloud等平台不保证文件持久化，每次重新部署可能丢失本地文件。如果你的产品需要存储用户数据或分析结果，必须使用外部数据库或云存储，而非本地文件系统。

## 金融数据分析示例

**场景**：你开发了一个Streamlit金融仪表板，展示A股行业轮动分析、个股技术指标和投资组合表现。现在需要部署到公网，让投资俱乐部的成员可以访问。

**步骤1：准备部署文件**

```txt
# requirements.txt
streamlit==1.37.0
pandas==2.2.2
akshare==1.14.0
plotly==5.22.0
```

**步骤2：创建Streamlit配置**

```toml
# .streamlit/config.toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = true

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
```

**步骤3：推送代码到GitHub**

```bash
git init
git add .
git commit -m "Initial commit for deployment"
git remote add origin https://github.com/yourname/finance-dashboard.git
git push -u origin main
```

**步骤4：部署到Streamlit Community Cloud**

1. 访问 https://share.streamlit.io/
2. 点击"New app"，选择GitHub仓库
3. 指定主文件路径（如`app.py`）
4. 在Secrets中配置API密钥：
```toml
TUSHARE_TOKEN = "your_token_here"
```
5. 点击"Deploy"，等待构建完成

**步骤5：绑定自定义域名（可选）**

在Streamlit Cloud设置中添加自定义域名，如`finance.example.com`，然后在域名DNS管理中添加CNAME记录指向Streamlit提供的地址。

部署完成后，投资俱乐部成员通过公网链接即可访问仪表板，查看实时行业轮动分析和个股指标。

## 拓展学习

- **Docker入门**：容器化部署是进阶必备技能，理解Dockerfile编写和镜像管理能让你部署任何类型的应用
- **CI/CD流水线**：GitHub Actions可以自动化测试和部署流程，每次push代码自动部署到生产环境
- **云原生架构**：了解微服务、容器编排（Kubernetes）等概念，为大规模产品做好准备
- **CDN与缓存策略**：对于全球用户的金融数据产品，CDN能显著提升访问速度
- **成本优化**：云服务费用可以快速增长，学习如何选择合适的实例类型、使用Spot实例、设置费用告警

## 参考链接

- https://docs.streamlit.io/streamlit-community-cloud - Streamlit Community Cloud官方文档
- https://vercel.com/docs - Vercel部署文档
- https://docs.docker.com/get-started/ - Docker官方入门教程
- https://letsencrypt.org/ - Let's Encrypt免费SSL证书
- https://uptimerobot.com/ - UptimeRobot免费可用性监控
