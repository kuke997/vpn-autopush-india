import os
import yaml

from crawler.clash_sources import get_clash_nodes
from crawler.v2ray_sources import get_v2ray_links
from crawler.ss_sources import get_ss_links
from push.telegram_bot import push_to_channel

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def save_data():
    clash = get_clash_nodes()
    with open("data/clash.yaml", "w", encoding="utf-8") as f:
        yaml.dump(clash, f, allow_unicode=True)

    v2ray = get_v2ray_links()
    with open("data/v2ray.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(v2ray))

    ss = get_ss_links()
    with open("data/shadowsocks.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(ss))

    return (
        "https://yourdomain.com/clash.yaml",
        "https://yourdomain.com/v2ray.txt",
        "https://yourdomain.com/shadowsocks.txt"
    )

if __name__ == "__main__":
    urls = save_data()
    if BOT_TOKEN and CHANNEL_ID:
        push_to_channel(BOT_TOKEN, CHANNEL_ID, *urls)
