# Telegram 数据爬虫 - 快速测试

## 测试步骤

### 1. 安装依赖
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. 测试运行
```bash
# 测试单个链接（修改脚本临时添加测试代码）
python scripts/crawler_telegram_stats.py
```

### 3. 检查结果
```bash
# 查看修改
git diff resources.json

# 查看日志
cat crawler.log
```

## 预期输出

```
2025-11-18 14:30:00 - INFO - 🚀 Telegram 数据爬虫启动
2025-11-18 14:30:00 - INFO - ⏰ 执行时间: 2025-11-18 14:30:00

2025-11-18 14:30:01 - INFO - 📚 开始更新资源数据...
2025-11-18 14:30:01 - INFO - 📊 共找到 65 个资源需要更新
2025-11-18 14:30:02 - INFO - 🌐 启动浏览器...
2025-11-18 14:30:05 - INFO - ✅ 浏览器启动成功

进度: [1/65]
📡 访问: 海外吃瓜 @hwcg
✅ 海外吃瓜 @hwcg: 10234 成员
   📢 订阅者: 10000 → 10234

...

📈 统计报告:
  ✅ 成功更新: 52 个
  ❌ 失败: 13 个
```

## 故障排查

### 如果浏览器启动失败
```bash
# macOS
brew install --cask chromium

# 或重新安装 Playwright
playwright install --with-deps chromium
```

### 如果无法访问链接
- 检查网络连接
- 查看日志文件 `crawler.log`
- 某些私有链接可能需要登录

### 如果全部失败
- 可能是 Telegram Web 界面改版
- 需要更新选择器代码
- 查看保存的截图文件 `debug_*.png`

## GitHub Actions 测试

1. 提交代码到 GitHub
2. Actions → Telegram Stats Crawler → Run workflow
3. 查看执行日志
4. 下载 Artifact 查看详细日志

## 注意事项

⚠️ **首次运行可能较慢** (10-15分钟)  
⚠️ **部分失败是正常的** (私有链接、网络波动)  
✅ **失败的会在下次自动重试**  
✅ **每天定时执行，数据会越来越完整**
