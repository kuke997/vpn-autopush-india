import requests
import yaml

def get_clash_nodes():
    all_nodes = []
    
    # 你可以添加或替换这些订阅链接
    urls = [
        "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/clash.yaml",
        "https://sub.v1.mk/clash.yaml",
        "https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet.yaml",
    ]

    for url in urls:
        try:
            print(f"🌐 正在抓取 Clash 订阅：{url}")
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = yaml.safe_load(resp.text)
                proxies = data.get("proxies", [])
                print(f"✅ {url} 返回节点数量：{len(proxies)}")
                all_nodes.extend(proxies)
            else:
                print(f"⚠️ {url} 返回状态码：{resp.status_code}")
        except Exception as e:
            print(f"❌ 抓取 {url} 时出错：{e}")

    print(f"📦 总共收集 Clash 节点数：{len(all_nodes)}")

    return {
        "port": 7890,
        "proxies": all_nodes
    }
