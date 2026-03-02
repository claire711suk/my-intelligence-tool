# 蒂蒂的智库自动化 (Didi's Intelligence Hub)

这是一个基于 Python 和 GitHub Actions 的自动化情报收集系统。它每天会自动抓取科技、投资和全球热点的 RSS 资讯，利用 Gemini 1.5 Flash 进行深度摘要，并生成一个精美的 HTML 仪表盘，同时发送到你的邮箱。

## 🚀 快速开始 (非代码人员指南)

### 1. 创建 GitHub 仓库
1. 登录你的 GitHub 账号。
2. 点击右上角的 `+` -> `New repository`。
3. 仓库名称填写 `didi-intelligence-hub`（或任何你喜欢的名字）。
4. 选择 `Public` 或 `Private`（建议 Private 以保护隐私）。
5. 点击 `Create repository`。

### 2. 上传代码
1. 将本项目中的 `main.py` 和 `.github/workflows/daily_update.yml` 文件上传到你的仓库。
2. 确保文件路径正确（`.yml` 文件必须在 `.github/workflows/` 目录下）。

### 3. 配置 Secrets (敏感信息)
为了安全，我们需要在 GitHub 设置中存储你的 API Key 和邮箱密码：
1. 在你的仓库页面，点击顶部的 `Settings`。
2. 在左侧菜单找到 `Secrets and variables` -> `Actions`。
3. 点击 `New repository secret`，依次添加以下三个变量：
   - `GEMINI_API_KEY`: 你的 Google AI Studio API Key。
   - `EMAIL_USER`: 你的 Gmail 地址。
   - `EMAIL_PASSWORD`: 你的 Gmail **应用专用密码** (App Password)。
     - *注意：不是你的登录密码。请在 Google 账号设置 -> 安全 -> 2步验证 -> 应用专用密码中生成。*

### 4. 开启 GitHub Pages
1. 在 `Settings` -> `Pages` 中。
2. 在 `Build and deployment` 下，`Source` 选择 `Deploy from a branch`。
3. `Branch` 选择 `gh-pages` (该分支会在第一次运行 Actions 后自动创建)。
4. 保存后，你就可以通过 GitHub 提供的 URL 访问你的智库仪表盘了。

### 5. 手动测试运行
1. 点击仓库顶部的 `Actions` 选项卡。
2. 在左侧选择 `Daily Intelligence Update`。
3. 点击右侧的 `Run workflow` -> `Run workflow`。
4. 等待几分钟，检查你的邮箱和生成的 `index.html`。

## 🛠️ 技术栈
- **Python**: 核心逻辑处理。
- **feedparser**: RSS 抓取。
- **Gemini 3 Flash**: AI 智能摘要。
- **GitHub Actions**: 自动化定时任务。
- **Tailwind CSS**: 仪表盘 UI 设计。

## 📬 订阅内容
- **科技/互联网**: 36氪、虎嗅、钛媒体。
- **投资逻辑**: 雪球深度。
- **全球热点**: Hacker News、Product Hunt。
