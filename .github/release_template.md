<div align=center>

[![Downloads](https://img.shields.io/github/downloads/__REPO__/__VERSION__/total?style=flat-square&logo=github)](https://github.com/__REPO__/releases/tag/__VERSION__)
[![MCDR](https://img.shields.io/badge/MCDR-v2-fac00f?style=flat-square&labelColor=3876a9&logo=python&logoColor=white)](https://mcdreforged.com/zh-CN)

</div>

### ⬇️ Downloads

| 文件 | 说明 |
|------|------|
| [📦 `mcdr_listener_ws_server-__VERSION__.mcdr`](__BASE_URL__/mcdr_listener_ws_server-__VERSION__.mcdr) | MCDR 插件包，放入 `plugins/` 目录即可 |

### 📥 安装方法

1. 下载 `.mcdr` 文件放入 MCDR 的 `plugins/` 目录，也可以克隆仓库源代码：

   ```bash
   # GitHub
   git clone https://github.com/VincentZyuApps/mcdr_listener_ws_server.git
   # 或 Gitee（国内加速）
   git clone https://gitee.com/vincent-zyu/mcdr_listener_ws_server.git
   ```
2. 根据需要修改配置文件 `config/mcdr_listener_ws_server/config.yml`（首次加载后自动生成）
3. 确保已安装依赖：

   ```bash
   pip install mcdreforged websockets>=15.0.0 Pillow>=10.0.0 requests>=2.32.0
   ```

4. 在 MCDR 控制台执行：`!!MCDR plg reload mcdr_listener_ws_server`

---

### 📋 更新说明

__COMMIT_LOG__

---

### 📊 Build Info

- **Build date**: __BUILD_DATE__
- **Commit**: __COMMIT_HASH__
- **Full Changelog**: __CHANGELOG_URL__
