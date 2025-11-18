# Telegram 数据自动获取实现指南

## 📊 目标数据

我们需要自动获取以下数据：
- **频道**: `subscribers` (订阅者数量)
- **群组**: `memberCount` (总成员数)
- **群组**: `onlineCount` (在线人数) ⚠️ **API 不支持**

---

## ⚠️ 协议号（私有邀请链接）的限制

**您的资源大多使用私有邀请链接 `t.me/+xxxxx`，这带来了自动化的挑战：**

1. ❌ **Bot 无法自动加入**
   - 私有链接需要用户点击或管理员邀请
   - Bot 不能通过 API 自动访问这些链接

2. ❌ **手动成本高**
   - 65+ 个群组/频道需要逐个邀请 Bot
   - 需要所有群主/管理员配合
   - Bot 可能随时被踢出

3. ❌ **数据访问受限**
   - 即使 Bot 加入，也可能无读取成员权限
   - 私有群组通常有更严格的隐私保护

---

## 🔧 实际可行的技术方案

### 方案 A: Telegram Desktop 自动化 + Selenium/Playwright (最实用)

**原理**: 模拟真实用户在 Telegram Web 上查看群组信息

#### ✅ 优点
- ✅ 可以访问私有邀请链接（用你的个人账号）
- ✅ 无需 Bot 加入群组
- ✅ 获取公开显示的成员数
- ✅ 自动化程度高

#### ❌ 缺点
- ❌ 需要登录你的个人 Telegram 账号
- ❌ 依赖 Telegram Web 界面（可能变化）
- ❌ 仍然**无法获取在线人数**（Web 界面不显示）
- ❌ 速度较慢（需要加载页面）

---

### 方案 B: GitHub Actions + Telegram Bot API (理论方案)

### 方案 B: GitHub Actions + Telegram Bot API (理论方案)

#### ⚠️ 前提条件（难以满足）
- Bot 必须被邀请加入所有 65+ 个群组/频道
- 需要所有群主/管理员配合
- Bot 需要读取成员权限
- **私有邀请链接无法通过 API 自动加入**

**结论**: 对于使用私有邀请链接的资源，此方案**不实用**

---

### 方案 C: 半自动化（推荐实际使用）

#### 📝 实现方式

**工具**: Python + Telethon (个人账号) + 手动点击链接

```python
#!/usr/bin/env python3
"""
半自动化获取 Telegram 数据
适用于私有邀请链接的场景
"""
import json
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest

# 使用个人账号的凭证
API_ID = 12345678  # 从 my.telegram.org 获取
API_HASH = 'your_api_hash'
PHONE = '+86 138 0000 0000'  # 你的手机号

async def get_stats_from_joined_chats():
    """从已加入的群组/频道获取数据"""
    
    # 创建客户端（使用个人账号）
    client = TelegramClient('my_account', API_ID, API_HASH)
    await client.start(phone=PHONE)
    
    # 读取现有数据
    with open('resources.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 获取所有已加入的对话
    dialogs = await client.get_dialogs()
    dialog_dict = {}
    
    # 建立链接到对话的映射
    for dialog in dialogs:
        entity = dialog.entity
        # 保存实体信息
        if hasattr(entity, 'username') and entity.username:
            dialog_dict[entity.username.lower()] = entity
        if hasattr(entity, 'id'):
            dialog_dict[str(entity.id)] = entity
    
    print(f"📊 已加入 {len(dialogs)} 个对话")
    print(f"🔍 开始匹配资源...\n")
    
    updated = 0
    not_found = []
    
    # 遍历所有资源
    for category in data['categories']:
        resources = []
        
        if category.get('hasSubcategories'):
            for subcategory in category['subcategories']:
                resources.extend(subcategory['resources'])
        else:
            resources = category.get('resources', [])
        
        for resource in resources:
            if 'link' not in resource:
                continue
            
            link = resource['link']
            title = resource['title']
            
            try:
                # 尝试从链接解析实体
                entity = None
                
                # 方法1: 通过用户名
                if 't.me/' in link and '/+' not in link:
                    username = link.split('/')[-1].lower()
                    entity = dialog_dict.get(username)
                
                # 方法2: 手动输入群组ID（需要提前记录）
                # 你可以先运行一次，打印所有已加入群组的ID和标题
                
                if entity:
                    # 获取成员数
                    try:
                        if hasattr(entity, 'megagroup') or hasattr(entity, 'broadcast'):
                            # 频道或超级群组
                            full = await client(GetFullChannelRequest(channel=entity))
                            count = full.full_chat.participants_count
                            
                            if 'subscribers' in resource:
                                resource['subscribers'] = count
                                print(f"✅ 📢 {title}: {count} 订阅者")
                            elif 'memberCount' in resource:
                                resource['memberCount'] = count
                                print(f"✅ 👥 {title}: {count} 成员")
                            updated += 1
                        else:
                            # 普通群组
                            full = await client(GetFullChatRequest(chat_id=entity.id))
                            count = full.full_chat.participants_count
                            resource['memberCount'] = count
                            print(f"✅ 👥 {title}: {count} 成员")
                            updated += 1
                    
                    except Exception as e:
                        print(f"❌ {title}: 获取数据失败 - {e}")
                        not_found.append(title)
                else:
                    print(f"⚠️  {title}: 未加入此群组/频道")
                    not_found.append(title)
                
                # 避免速率限制
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ {title}: 错误 - {e}")
                not_found.append(title)
    
    # 更新时间戳
    from datetime import date
    data['updateTime'] = date.today().strftime('%Y-%m-%d')
    
    # 保存数据
    with open('resources.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📈 统计:")
    print(f"  ✅ 成功更新: {updated} 个")
    print(f"  ❌ 未找到: {len(not_found)} 个")
    
    if not_found:
        print(f"\n⚠️  未更新的资源:")
        for title in not_found[:10]:  # 只显示前10个
            print(f"  - {title}")
    
    await client.disconnect()

async def list_all_joined_chats():
    """列出所有已加入的群组/频道（辅助工具）"""
    client = TelegramClient('my_account', API_ID, API_HASH)
    await client.start(phone=PHONE)
    
    dialogs = await client.get_dialogs()
    
    print("📋 所有已加入的群组/频道:\n")
    print(f"{'ID':<15} {'标题':<30} {'类型':<10} {'成员数':<10}")
    print("-" * 70)
    
    for dialog in dialogs:
        entity = dialog.entity
        title = getattr(entity, 'title', getattr(entity, 'first_name', 'Unknown'))
        entity_id = entity.id
        
        # 获取成员数
        try:
            if hasattr(entity, 'megagroup') or hasattr(entity, 'broadcast'):
                full = await client(GetFullChannelRequest(channel=entity))
                count = full.full_chat.participants_count
                entity_type = "频道" if getattr(entity, 'broadcast', False) else "超级群组"
            else:
                full = await client(GetFullChatRequest(chat_id=entity.id))
                count = full.full_chat.participants_count
                entity_type = "群组"
            
            print(f"{entity_id:<15} {title[:28]:<30} {entity_type:<10} {count:<10}")
        except:
            pass
    
    await client.disconnect()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        # python fetch_stats.py list - 列出所有已加入的群组
        asyncio.run(list_all_joined_chats())
    else:
        # python fetch_stats.py - 更新数据
        asyncio.run(get_stats_from_joined_chats())
```

#### 📝 使用步骤

1. **手动加入所有群组/频道**
   ```
   # 用你的个人账号点击所有 65+ 个邀请链接
   # 这是一次性工作，加入后就不用再管
   ```

2. **首次运行：列出所有群组**
   ```bash
   python scripts/fetch_stats.py list
   ```

3. **更新数据**
   ```bash
   python scripts/fetch_stats.py
   ```

4. **提交到 GitHub**
   ```bash
   git add resources.json
   git commit -m "更新 Telegram 统计数据"
   git push
   ```

#### ⏰ 定时任务（可选）

在本地设置 cron 或使用 GitHub Actions 手动触发：

```yaml
# .github/workflows/manual-update-stats.yml
name: Manual Update Telegram Stats

on:
  workflow_dispatch:  # 手动触发

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install telethon
      - name: Update stats
        env:
          API_ID: ${{ secrets.API_ID }}
          API_HASH: ${{ secrets.API_HASH }}
          PHONE: ${{ secrets.PHONE }}
          # 需要session文件，首次运行需要验证码
        run: python scripts/fetch_stats.py
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add resources.json
          git commit -m "Update stats" || exit 0
          git push
```

---

### 方案 D: 完全手动（最简单最可靠）

#### � 建议流程

每周或每月手动更新一次：

1. **打开 Telegram**
2. **依次访问每个群组/频道**
3. **查看成员数**
4. **手动更新 `resources.json`**

**优点:**
- ✅ 100% 准确
- ✅ 无需复杂配置
- ✅ 可以同时更新在线人数（目测估算）
- ✅ 没有 API 限制

**缺点:**
- ❌ 耗时（约 30-60 分钟）
- ❌ 容易遗漏
- ❌ 需要定期执行

---

## 🎯 针对您的情况的最佳方案

### 推荐: 方案 C (半自动化) + 方案 D (手动补充)

**具体实施:**

1. **一次性准备** (30分钟)
   - 用你的个人 Telegram 账号点击所有 65+ 个邀请链接加入
   - 获取 API 凭证（my.telegram.org）
   - 配置 Python 脚本

2. **每周/每月执行** (5分钟)
   - 运行脚本自动更新 `memberCount` 和 `subscribers`
   - 手动估算并更新 `onlineCount`（可选）
   - 提交到 GitHub

3. **优势对比**
   | 方案 | 自动化程度 | 准确性 | 实施难度 | 维护成本 |
   |------|-----------|--------|----------|----------|
   | Bot API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ 高（需要Bot加入所有群） | ⭐⭐⭐ |
   | 半自动(推荐) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ 中（一次性加入群组） | ⭐⭐⭐⭐ |
   | 完全手动 | ⭐ | ⭐⭐⭐⭐⭐ | ✅ 低 | ⭐⭐ |

---

## ⚠️ 重要限制（无法解决的问题）

### 1. **在线人数无法自动获取**
```
❌ Telegram API 不提供
❌ Telegram Web 不显示
❌ 任何方案都无法自动获取
```

**解决方案:**
- 手动访问群组查看（需要是成员）
- 按比例估算（如 memberCount * 0.1）
- 保持固定值，仅更新总人数

### 2. **私有邀请链接的限制**
```
❌ Bot 无法自动通过 t.me/+ 链接加入
❌ 需要管理员手动邀请 Bot
❌ 或使用个人账号（需要点击链接加入）
```

### 3. **API 速率限制**
```
⚠️  每秒最多 30 次请求
⚠️  每分钟最多 20 次 getChat 请求
⚠️  需要添加延迟避免封禁
```

---

## 📋 实施建议

### 对于您的项目，我建议:

✅ **短期方案** (立即可用)
1. 保持当前手动更新的数据结构
2. 每月手动更新一次主要数据
3. trending 字段手动标记

✅ **中期方案** (1-2周实施)
1. 用个人账号加入所有群组/频道（一次性）
2. 配置半自动化脚本
3. 每周运行一次自动更新

✅ **长期方案** (未来优化)
1. 考虑使用 GitHub Actions 定时触发
2. 建立数据历史记录
3. 添加数据可视化（增长趋势图）

---

## 🔧 需要我帮您创建什么？

我可以为您准备:

---

## 📚 相关文档

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telethon 文档](https://docs.telethon.dev/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Telegram API 限制](https://core.telegram.org/api/obtaining_api_id)

---

**创建日期**: 2025-11-18  
**维护者**: CJSS-Tech  
**仓库**: github.com/CJSS-Tech/hwtg
