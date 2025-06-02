import os
import requests
import asyncio
import yaml
from telegram import Bot
from telegram.constants import ParseMode
import urllib.parse

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# 这里改成从环境变量读取多个订阅链接（以逗号分割），也可以写死在列表里
CLASH_SUBSCRIBE_URLS = os.getenv("CLASH_SUBSCRIBE_URLS", "").split(",")
# 如果环境变量没配置，默认给几个演示链接（实际部署建议用环境变量配置）
if not any(CLASH_SUBSCRIBE_URLS):
    CLASH_SUBSCRIBE_URLS = [
        "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/clash.yml",
        # 你可以继续添加默认有效的订阅URL
    ]

def validate_subscription(url):
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200 and "proxies" in res.text:
            return True
    except:
        pass
    return False

def search_github_clash_urls():
    print("🔍 GitHub 搜索订阅文件中...")
    try:
        headers = {
            "Accept": "application/vnd.github.v3.text-match+json"
        }
        query = "clash filename:clash.yaml in:path extension:yaml"
        url = f"https://api.github.com/search/code?q={query}&per_page=100"
        res = requests.get(url, headers=headers, timeout=15)
        items = res.json().get("items", [])
        links = []
        for item in items:
            raw_url = item["html_url"].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            links.append(raw_url)
        print(f"✨ GitHub 搜索到 {len(links)} 个可能的订阅链接")
        return links
    except Exception as e:
        print("GitHub 搜索失败:", e)
        return []

def get_subscription_country_info(url):
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return None

        data = yaml.safe_load(res.text)
        proxies = data.get("proxies", [])
        countries = set()

        for proxy in proxies:
            country = proxy.get("country")
            if country and isinstance(country, str) and len(country) <= 5:
                countries.add(country.strip())
                continue

            region = proxy.get("region")
            if region and isinstance(region, str) and len(region) <= 5:
                countries.add(region.strip())
                continue

            # 备用：用name字段前2个字母作为简写
            name = proxy.get("name") or proxy.get("remark") or proxy.get("remarks")
            if name and isinstance(name, str) and len(name) >= 2:
                countries.add(name[:2].strip())

        if countries:
            return ", ".join(sorted(countries))
        else:
            return None
    except Exception as e:
        print(f"解析节点地区失败：{url}，错误：{e}")
        return None

async def send_to_telegram(bot_token, channel_id, urls):
    if not urls:
        print("❌ 没有可用节点，跳过推送")
        return

    text = "🆕 <b>最新 Clash 订阅节点 免费 VPN 节点合集</b>\n\n"
    for i, url in enumerate(urls[:20], start=1):
        country_info = get_subscription_country_info(url)
        if country_info:
            country_info = f"（节点地区: {country_info}）"
        else:
            country_info = ""

        safe_url = urllib.parse.quote(url, safe=":/?=&")
        text += f"👉 <a href=\"{safe_url}\">{url}</a> {country_info}\n（可长按复制，或粘贴到 Clash / Shadowrocket 导入）\n\n"

    if len(text.encode('utf-8')) > 4000:
        text = text.encode("utf-8")[:4000].decode("utf-8", errors="ignore") + "\n..."

    bot = Bot(token=bot_token)
    try:
        await bot.send_message(chat_id=channel_id, text=text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        print("✅ 推送成功")
    except Exception as e:
        print("❌ 推送失败:", e)

async def get_all_valid_subscriptions():
    print("🔍 验证预定义订阅链接...")
    valid_static = [url for url in CLASH_SUBSCRIBE_URLS if url and validate_subscription(url)]

    github_links = search_github_clash_urls()
    print("🔍 验证 GitHub 搜索到的订阅链接...")
    valid_dynamic = [url for url in github_links if validate_subscription(url)]

    all_valid = valid_static + valid_dynamic
    print(f"✔️ 共验证通过的有效订阅链接数量: {len(all_valid)}")

    with open("valid_links.txt", "w", encoding="utf-8") as f:
        for link in all_valid:
            f.write(link + "\n")
    print("📄 已保存到 valid_links.txt")

    return all_valid

async def main():
    if not BOT_TOKEN or not CHANNEL_ID:
        print("环境变量 BOT_TOKEN 或 CHANNEL_ID 未设置")
        return

    all_valid_urls = await get_all_valid_subscriptions()
    await send_to_telegram(BOT_TOKEN, CHANNEL_ID, all_valid_urls)

if __name__ == "__main__":
    asyncio.run(main())
