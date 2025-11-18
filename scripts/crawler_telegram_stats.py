#!/usr/bin/env python3
"""
Telegram 群组/频道数据爬虫
通过模拟浏览器访问 Telegram Web 获取成员数据

特点：
1. 每天定时执行
2. 失败自动跳过，下次重试
3. 按顺序逐个获取，避免被限制
4. 自动保存进度
"""

import json
import time
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置
RESOURCES_FILE = 'resources.json'
PROGRESS_FILE = 'scripts/.crawler_progress.json'
DELAY_BETWEEN_REQUESTS = 3  # 每次请求间隔3秒，避免被限制
MAX_RETRY_PER_LINK = 3  # 每个链接最多重试3次
BROWSER_TIMEOUT = 30000  # 浏览器超时30秒


class TelegramCrawler:
    """Telegram 数据爬虫"""
    
    def __init__(self):
        self.progress = self.load_progress()
        self.updated_count = 0
        self.failed_links = []
        self.browser = None
        self.context = None
        self.page = None
    
    def load_progress(self):
        """加载进度文件"""
        try:
            if Path(PROGRESS_FILE).exists():
                with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"无法加载进度文件: {e}")
        
        return {
            'last_run': None,
            'failed_links': {},  # {link: retry_count}
            'last_index': 0
        }
    
    def save_progress(self):
        """保存进度"""
        try:
            Path(PROGRESS_FILE).parent.mkdir(exist_ok=True)
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.progress, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存进度失败: {e}")
    
    async def init_browser(self):
        """初始化浏览器"""
        logger.info("🌐 启动浏览器...")
        playwright = await async_playwright().start()
        
        # 使用 Chromium，模拟真实浏览器
        self.browser = await playwright.chromium.launch(
            headless=True,  # 无头模式，设为 False 可以看到浏览器
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox'
            ]
        )
        
        # 创建浏览器上下文（模拟真实用户）
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        
        # 创建页面
        self.page = await self.context.new_page()
        
        # 设置超时
        self.page.set_default_timeout(BROWSER_TIMEOUT)
        
        logger.info("✅ 浏览器启动成功")
    
    async def close_browser(self):
        """关闭浏览器"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        logger.info("🔒 浏览器已关闭")
    
    async def get_telegram_stats(self, link, title):
        """
        从 Telegram 链接获取统计数据
        
        返回: (member_count, online_count, success)
        """
        try:
            # 将私有邀请链接转换为可访问的 URL
            if '/+' in link:
                # 私有链接需要登录，先尝试公开预览
                invite_code = link.split('/+')[1]
                preview_url = f'https://t.me/+{invite_code}'
            else:
                preview_url = link
            
            logger.info(f"📡 访问: {title}")
            logger.debug(f"   URL: {preview_url}")
            
            # 访问链接
            await self.page.goto(preview_url, wait_until='networkidle')
            
            # 等待页面加载
            await asyncio.sleep(2)
            
            # 方法1: 尝试从页面元素中提取成员数
            member_count = None
            online_count = None
            
            # 尝试多种选择器（Telegram Web 的不同版本）
            selectors = [
                # 频道/群组的成员数显示
                'text=/\\d+[KM]?\\s+(members?|subscribers?)/i',
                '.tgme_page_extra',
                '[class*="member"]',
                '[class*="subscriber"]',
                # Telegram Web App 选择器
                '.chat-info-members',
                '.group-info .info-row:has-text("members")',
            ]
            
            page_content = await self.page.content()
            
            # 从页面内容中提取数字
            import re
            
            # 优先查找机器人的 "XXX monthly users" 格式
            # 例如: "10 392 monthly users"
            bot_pattern = r'(\d+(?:\s\d+)*)\s*monthly\s+users'
            bot_match = re.search(bot_pattern, page_content, re.IGNORECASE)
            
            if bot_match:
                # 这是一个机器人，返回月活跃用户数
                monthly_users = self.parse_count(bot_match.group(1))
                logger.info(f"✅ {title}: {monthly_users} 月活跃用户")
                return monthly_users, None, True
            
            # 查找群组的 "XXX members, XXX online" 格式
            # 例如: "2 462 members, 723 online"
            group_pattern = r'(\d+(?:\s\d+)*)\s*members?,\s*(\d+(?:\s\d+)*)\s*online'
            group_match = re.search(group_pattern, page_content, re.IGNORECASE)
            
            if group_match:
                # 这是一个群组，同时有成员数和在线数
                member_count = self.parse_count(group_match.group(1))
                online_count = self.parse_count(group_match.group(2))
                logger.info(f"✅ {title}: {member_count} 成员, {online_count} 在线")
                return member_count, online_count, True
            
            # 如果没找到群组格式，查找频道的 "XXX subscribers" 模式
            # 注意：Telegram 使用空格而不是逗号作为千位分隔符
            patterns = [
                r'(\d+(?:\s\d+)*)\s*subscribers',  # "8 689 subscribers"
                r'(\d+(?:\s\d+)*)\s*members',      # "8 689 members"
                r'(\d+(?:,\d+)*)\s*subscribers',   # "8,689 subscribers"
                r'(\d+(?:,\d+)*)\s*members',       # "8,689 members"
                r'(\d+\.?\d*[KM]?)\s*subscribers',
                r'(\d+\.?\d*[KM]?)\s*members',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, page_content, re.IGNORECASE)
                if match:
                    count_str = match.group(1)
                    member_count = self.parse_count(count_str)
                    if member_count:
                        break
            
            if member_count:
                logger.info(f"✅ {title}: {member_count} 成员")
                return member_count, None, True
            else:
                logger.warning(f"⚠️  {title}: 未找到成员数数据")
                # 保存页面截图用于调试
                screenshot_path = f'debug_{int(time.time())}.png'
                await self.page.screenshot(path=screenshot_path)
                logger.debug(f"   已保存截图: {screenshot_path}")
                return None, None, False
        
        except Exception as e:
            logger.error(f"❌ {title}: 获取失败 - {e}")
            return None, None, False
    
    def parse_count(self, count_str):
        """
        解析成员数字符串
        
        例如:
        - "1,234" -> 1234
        - "1 234" -> 1234 (Telegram 使用空格分隔)
        - "10K" -> 10000
        - "1.5M" -> 1500000
        """
        try:
            # 移除逗号和空格
            count_str = count_str.replace(',', '').replace(' ', '').strip().upper()
            
            if 'M' in count_str:
                number = float(count_str.replace('M', ''))
                return int(number * 1000000)
            elif 'K' in count_str:
                number = float(count_str.replace('K', ''))
                return int(number * 1000)
            else:
                return int(float(count_str))
        except Exception as e:
            logger.debug(f"解析数字失败: {count_str} - {e}")
            return None
    
    async def update_resources(self):
        """更新 resources.json"""
        logger.info("📚 开始更新资源数据...")
        
        # 读取资源文件
        with open(RESOURCES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 收集所有需要更新的资源
        resources_to_update = []
        
        for category in data['categories']:
            if category.get('hasSubcategories'):
                for subcategory in category['subcategories']:
                    for resource in subcategory['resources']:
                        if 'link' in resource:
                            resources_to_update.append({
                                'resource': resource,
                                'category_id': category['id']
                            })
            else:
                if 'resources' in category:
                    for resource in category['resources']:
                        if 'link' in resource:
                            resources_to_update.append({
                                'resource': resource,
                                'category_id': category['id']
                            })
        
        total = len(resources_to_update)
        logger.info(f"📊 共找到 {total} 个资源需要更新")
        
        # 初始化浏览器
        await self.init_browser()
        
        try:
            # 按顺序处理每个资源
            for index, item in enumerate(resources_to_update, 1):
                resource = item['resource']
                link = resource['link']
                title = resource['title']
                
                # 检查是否需要跳过（失败次数过多）
                retry_count = self.progress['failed_links'].get(link, 0)
                if retry_count >= MAX_RETRY_PER_LINK:
                    logger.info(f"⏭️  [{index}/{total}] 跳过 {title} (已失败 {retry_count} 次)")
                    continue
                
                logger.info(f"\n{'='*60}")
                logger.info(f"进度: [{index}/{total}]")
                
                # 获取数据
                member_count, online_count, success = await self.get_telegram_stats(link, title)
                
                if success and member_count:
                    # 更新数据
                    if 'subscribers' in resource:
                        old_count = resource['subscribers']
                        resource['subscribers'] = member_count
                        logger.info(f"   📢 订阅者: {old_count} → {member_count}")
                    elif 'memberCount' in resource:
                        old_count = resource['memberCount']
                        resource['memberCount'] = member_count
                        logger.info(f"   👥 成员数: {old_count} → {member_count}")
                        
                        # 如果有在线人数，也更新
                        if online_count is not None:
                            old_online = resource.get('onlineCount', 0)
                            resource['onlineCount'] = online_count
                            logger.info(f"   💬 在线数: {old_online} → {online_count}")
                    elif 'monthlyUsers' in resource:
                        old_count = resource['monthlyUsers']
                        resource['monthlyUsers'] = member_count
                        logger.info(f"   📊 月活跃: {old_count} → {member_count}")
                    
                    self.updated_count += 1
                    
                    # 清除失败记录
                    if link in self.progress['failed_links']:
                        del self.progress['failed_links'][link]
                else:
                    # 记录失败
                    self.progress['failed_links'][link] = retry_count + 1
                    self.failed_links.append(title)
                    logger.warning(f"   ⚠️  失败次数: {retry_count + 1}/{MAX_RETRY_PER_LINK}")
                
                # 保存进度
                self.progress['last_index'] = index
                self.progress['last_run'] = datetime.now().isoformat()
                self.save_progress()
                
                # 延迟，避免请求过快
                if index < total:
                    logger.debug(f"⏳ 等待 {DELAY_BETWEEN_REQUESTS} 秒...")
                    await asyncio.sleep(DELAY_BETWEEN_REQUESTS)
        
        finally:
            await self.close_browser()
        
        # 更新时间戳
        data['updateTime'] = datetime.now().strftime('%Y-%m-%d')
        
        # 保存文件
        with open(RESOURCES_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n{'='*60}")
        logger.info("📈 统计报告:")
        logger.info(f"  ✅ 成功更新: {self.updated_count} 个")
        logger.info(f"  ❌ 失败: {len(self.failed_links)} 个")
        
        if self.failed_links:
            logger.info(f"\n⚠️  失败的资源:")
            for title in self.failed_links[:10]:
                logger.info(f"  - {title}")
            if len(self.failed_links) > 10:
                logger.info(f"  ... 还有 {len(self.failed_links) - 10} 个")
        
        logger.info(f"{'='*60}\n")


async def main():
    """主函数"""
    logger.info("🚀 Telegram 数据爬虫启动")
    logger.info(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    crawler = TelegramCrawler()
    
    try:
        await crawler.update_resources()
        logger.info("✅ 任务完成")
        return 0
    except Exception as e:
        logger.error(f"❌ 任务失败: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    exit(exit_code)
