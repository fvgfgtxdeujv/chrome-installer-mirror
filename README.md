# 🚀 Chrome Standalone Installer Mirror

[![GitHub release](https://img.shields.io/github/v/release/fvgfgtxdeujv/chrome-installer-mirror?color=blue&label=最新版本)](https://github.com/fvgfgtxdeujv/chrome-installer-mirror/releases/latest)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/fvgfgtxdeujv/chrome-installer-mirror/download-chrome.yml?label=自动更新)](https://github.com/fvgfgtxdeujv/chrome-installer-mirror/actions)
[![GitHub](https://img.shields.io/github/license/fvgfgtxdeujv/chrome-installer-mirror)](https://github.com/fvgfgtxdeujv/chrome-installer-mirror/blob/main/LICENSE)

> 📦 每天自动同步 Google Chrome 最新稳定版独立安装包，无需访问 Google 官网即可下载。

---

## ✨ 特性

- 🔄 **每日自动检测**：通过 GitHub Actions 定时检查 Chrome 新版本
- 📥 **官方直链下载**：从 Google 官方 CDN 获取安装包，安全可靠
- ✅ **完整性校验**：自动生成 SHA256 哈希值，确保文件未被篡改
- 🗑️ **自动清理**：每次更新只保留最新版本，节省存储空间
- 🔗 **永久下载链接**：通过 GitHub Releases 提供稳定下载地址

---

## 📥 下载最新版

### 方式一：直接下载（推荐）

访问 [Releases 页面](https://github.com/fvgfgtxdeujv/chrome-installer-mirror/releases/latest)，下载 `chrome_installer.exe`

### 方式二：使用命令行

```bash
# 获取最新 Release 下载链接
curl -s https://api.github.com/repos/fvgfgtxdeujv/chrome-installer-mirror/releases/latest \
  | grep "browser_download_url" \
  | grep ".exe" \
  | cut -d '"' -f 4 \
  | wget -i -
