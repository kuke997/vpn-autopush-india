import os
import requests
import base64

def get_v2ray_links():
    urls_str = os.getenv("V2RAY_SOURCE_URLS", "")
    urls = [url.strip() for url in urls_str.split(",") if url.strip()]
    all_links = []

    for url in urls:
        print(f"🌐 正在抓取 V2Ray 订阅：{url}")
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                try:
                    decoded = base64.b64decode(res.text.strip()).decode()
                    links = decoded.strip().splitlines()
                    all_links.extend([l.strip() for l in links if l.strip()])
                except Exception as decode_err:
                    print(f"❌ 解码 V2Ray 数据失败：{decode_err}")
            else:
                print(f"⚠️ {url} 返回状态码：{res.status_code}")
        except Exception as e:
            print(f"❌ 抓取 {url} 时出错：{e}")

    print(f"📦 总共收集 V2Ray 链接数：{len(all_links)}")
    return all_links
