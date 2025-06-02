import os
import requests
import yaml

def get_clash_nodes():
    urls_str = os.getenv("CLASH_SOURCE_URLS", "")
    urls = [url.strip() for url in urls_str.split(",") if url.strip()]
    proxies = []

    for url in urls:
        print(f"🌐 正在抓取 Clash 订阅：{url}")
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                try:
                    content = yaml.safe_load(res.text)
                    if isinstance(content, dict) and content.get("proxies"):
                        proxies.extend(content["proxies"])
                    else:
                        print(f"⚠️ {url} 不包含 'proxies' 字段")
                except Exception as e:
                    print(f"❌ 解析 YAML 时出错：{e}")
            else:
                print(f"⚠️ {url} 返回状态码：{res.status_code}")
        except Exception as e:
            print(f"❌ 抓取 {url} 时出错：{e}")

    print(f"📦 总共收集 Clash 节点数：{len(proxies)}")
    return {"port": 7890, "proxies": proxies}
