import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from crawler.clash_sources import get_clash_nodes
from crawler.v2ray_sources import get_v2ray_links
from crawler.ss_sources import get_ss_links
import yaml
import telegram
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

WORKER_BASE_URL = "https://vpn4india.ttnf918.workers.dev"  # 你的 Workers 域名

def ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data")

def save_clash():
    clash = get_clash_nodes()
    with open("data/clash.yaml", "w", encoding="utf-8") as f:
        yaml.dump(clash, f, allow_unicode=True)
    return clash

def save_v2ray():
    v2ray = get_v2ray_links()
    with open("data/v2ray.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(v2ray))
    return v2ray

def save_shadowsocks():
    ss = get_ss_links()
    with open("data/shadowsocks.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(ss))
    return ss

def send_to_telegram(clash, v2ray, ss):
    bot = telegram.Bot(token=BOT_TOKEN)
    text = "🌐 免费 VPN 节点每日更新（印度专用版） 🇮🇳\n\n"
    text += f"✅ Clash 节点数：{len(clash)}\n"
    text += f"✅ V2Ray 链接数：{len(v2ray)}\n"
    text += f"✅ Shadowsocks 链接数：{len(ss)}\n\n"
    text += "📎 订阅文件：\n"
    text += f"👉 Clash: {WORKER_BASE_URL}/clash\n"
    text += f"👉 V2Ray: {WORKER_BASE_URL}/v2ray\n"
    text += f"👉 Shadowsocks: {WORKER_BASE_URL}/ss\n\n"
    text += "#VPN #FreeVPN #Clash #V2Ray #Shadowsocks #IndiaVPN"

    try:
        bot.send_message(chat_id=CHANNEL_ID, text=text)
        print("✅ 已发送 Telegram 推送")
    except Exception as e:
        print("❌ Telegram 推送失败:", e)

if __name__ == "__main__":
    ensure_data_dir()
    clash = save_clash()
    v2ray = save_v2ray()
    ss = save_shadowsocks()
    print("✅ 所有节点信息已保存完毕。")

    if BOT_TOKEN and CHANNEL_ID:
        send_to_telegram(clash, v2ray, ss)
    else:
        print("⚠️ BOT_TOKEN 或 CHANNEL_ID 未配置，跳过推送")
