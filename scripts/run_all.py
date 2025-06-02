import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from crawler.clash_sources import get_clash_nodes
from crawler.v2ray_sources import get_v2ray_links
from crawler.ss_sources import get_ss_links
import yaml

def ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data")

def save_clash():
    clash = get_clash_nodes()
    with open("data/clash.yaml", "w", encoding="utf-8") as f:
        yaml.dump(clash, f, allow_unicode=True)

def save_v2ray():
    v2ray = get_v2ray_links()
    with open("data/v2ray.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(v2ray))

def save_shadowsocks():
    ss = get_ss_links()
    with open("data/shadowsocks.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(ss))

if __name__ == "__main__":
    ensure_data_dir()
    save_clash()
    save_v2ray()
    save_shadowsocks()
    print("✅ 所有节点信息已保存完毕。")
