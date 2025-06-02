import os
import requests

def get_ss_links():
    urls_str = os.getenv("SS_SOURCE_URLS", "")
    urls = [url.strip() for url in urls_str.split(",") if url.strip()]
    all_links = []

    for url in urls:
        print(f"🌐 正在抓取 Shadowsocks 订阅：{url}")
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                links = res.text.strip().splitlines()
                all_links.extend([l.strip() for l in links if l.strip()])
            else:
                print(f"⚠️ {url} 返回状态码：{res.status_code}")
        except Exception as e:
            print(f"❌ 抓取 {url} 时出错：{e}")

    print(f"📦 总共收集 Shadowsocks 链接数：{len(all_links)}")
    return all_links
