# Telegram 数据爬虫 - 使用指南

## 📋 功能特点

✅ **自动化**: 每天定时执行，无需人工干预  
✅ **容错性强**: 单个失败不影响其他资源  
✅ **智能重试**: 失败的资源下次自动重试（最多3次）  
✅ **进度保存**: 断点续传，不会重复更新  
✅ **详细日志**: 完整的执行日志，便于调试  
✅ **多类型支持**: 
- **频道**: 自动获取订阅者数 (subscribers)
- **群组**: 自动获取成员数 (memberCount) + 在线人数 (onlineCount)
- **机器人**: 自动获取月活跃用户数 (monthlyUsers)  

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 Playwright（浏览器自动化工具）
pip install playwright

# 安装浏览器驱动
playwright install chromium
```

### 2. 本地测试

```bash
# 进入项目目录
cd /Users/yaya/Documents/Workspace/TGDHSite/hwtg

# 运行爬虫
python scripts/crawler_telegram_stats.py
```

### 3. 查看结果

```bash
# 查看更新的数据
git diff resources.json

# 查看日志
cat crawler.log

# 查看进度文件
cat scripts/.crawler_progress.json
```

---

## ⏰ 自动化执行

### 方案 A: GitHub Actions（推荐）

已配置好，每天凌晨 2:00 自动执行：

1. **查看执行状态**
   - 访问: `https://github.com/CJSS-Tech/hwtg/actions`
   - 查看 "Telegram Stats Crawler" 工作流

2. **手动触发**
   - Actions → Telegram Stats Crawler → Run workflow

3. **查看日志**
   - 每次运行的日志会自动上传为 Artifact
   - 保留 7 天

### 方案 B: 本地定时任务（cron）

```bash
# 编辑 crontab
crontab -e

# 添加任务（每天凌晨 2:00 执行）
0 2 * * * cd /Users/yaya/Documents/Workspace/TGDHSite/hwtg && /usr/local/bin/python3 scripts/crawler_telegram_stats.py && git add resources.json scripts/.crawler_progress.json && git commit -m "Update stats" && git push
```

---

## 📊 工作流程

```
每天凌晨 2:00
↓
启动浏览器（Chromium）
↓
按顺序访问每个 Telegram 链接
  ├─ 成功: 更新数据 ✅
  └─ 失败: 记录到进度文件，下次重试 ⚠️
↓
保存 resources.json
↓
提交到 GitHub
↓
自动部署到网站 🌐
```

---

## 🔧 配置说明

### 关键参数（`crawler_telegram_stats.py`）

```python
DELAY_BETWEEN_REQUESTS = 3  # 请求间隔（秒）
MAX_RETRY_PER_LINK = 3      # 最大重试次数
BROWSER_TIMEOUT = 30000     # 浏览器超时（毫秒）
```

### 进度文件（`.crawler_progress.json`）

```json
{
  "last_run": "2025-11-18T02:00:00",
  "failed_links": {
    "https://t.me/+xxx": 2  // 失败次数
  },
  "last_index": 65
}
```

---

## 📈 预期效果

### 首次运行

```
📊 共找到 65 个资源需要更新
✅ 成功更新: 52 个
❌ 失败: 13 个
```

### 第二次运行（第二天）

```
📊 共找到 65 个资源需要更新
⏭️  跳过已更新的 52 个
✅ 新成功: 10 个（之前失败的）
❌ 仍失败: 3 个
```

### 第三次运行

```
📊 共找到 65 个资源需要更新
✅ 新成功: 2 个
❌ 永久失败: 1 个（超过3次重试）
⏭️  跳过 64 个
```

---

## ⚠️ 已知限制

### 1. **无法获取在线人数**
- ❌ Telegram Web 不显示在线人数
- ✅ 解决: `onlineCount` 保持原值或手动更新

### 2. **部分私有链接可能失败**
- ❌ 需要登录才能查看的群组
- ✅ 解决: 失败会自动重试，最多3次

### 3. **速率限制**
- ❌ 访问过快可能被临时限制
- ✅ 解决: 每次请求间隔 3 秒

### 4. **数据准确性**
- ⚠️  爬取的数据可能稍有延迟
- ✅ 解决: 每天更新，数据足够新鲜

---

## 🐛 故障排查

### 问题 1: 浏览器启动失败

```bash
# 安装系统依赖
playwright install-deps
```

### 问题 2: 无法访问某些链接

查看日志文件 `crawler.log`，检查错误信息：

```bash
tail -f crawler.log
```

### 问题 3: GitHub Actions 失败

1. 检查 Actions 日志
2. 下载 Artifact 查看详细日志
3. 手动运行工作流测试

### 问题 4: 数据未更新

检查进度文件：

```bash
cat scripts/.crawler_progress.json
```

如果失败次数 ≥ 3，手动重置：

```bash
rm scripts/.crawler_progress.json
```

---

## 📝 日志示例

```
2025-11-18 02:00:00 - INFO - 🚀 Telegram 数据爬虫启动
2025-11-18 02:00:00 - INFO - ⏰ 执行时间: 2025-11-18 02:00:00

2025-11-18 02:00:01 - INFO - 📚 开始更新资源数据...
2025-11-18 02:00:01 - INFO - 📊 共找到 65 个资源需要更新
2025-11-18 02:00:02 - INFO - 🌐 启动浏览器...
2025-11-18 02:00:05 - INFO - ✅ 浏览器启动成功

2025-11-18 02:00:05 - INFO - ============================================================
2025-11-18 02:00:05 - INFO - 进度: [1/65]
2025-11-18 02:00:05 - INFO - 📡 访问: 海外吃瓜 @hwcg
2025-11-18 02:00:08 - INFO - ✅ 海外吃瓜 @hwcg: 10234 成员
2025-11-18 02:00:08 - INFO -    📢 订阅者: 10000 → 10234
2025-11-18 02:00:11 - DEBUG - ⏳ 等待 3 秒...

2025-11-18 02:00:14 - INFO - ============================================================
2025-11-18 02:00:14 - INFO - 进度: [2/65]
...

2025-11-18 02:03:30 - INFO - ============================================================
2025-11-18 02:03:30 - INFO - 📈 统计报告:
2025-11-18 02:03:30 - INFO -   ✅ 成功更新: 52 个
2025-11-18 02:03:30 - INFO -   ❌ 失败: 13 个
2025-11-18 02:03:30 - INFO - ✅ 任务完成
```

---

## 🎯 优势总结

| 特性 | 爬虫方案 | API方案 |
|------|---------|---------|
| 无需登录 | ✅ | ❌ 需要账号 |
| 支持私有链接 | ⚠️ 部分支持 | ❌ 需要加入 |
| 自动化程度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 维护成本 | ⭐⭐⭐⭐ | ⭐⭐ |
| 数据准确性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 容错能力 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 📚 相关文档

- [Playwright 文档](https://playwright.dev/python/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Cron 语法](https://crontab.guru/)

---

**创建日期**: 2025-11-18  
**最后更新**: 2025-11-18  
**维护者**: CJSS-Tech
