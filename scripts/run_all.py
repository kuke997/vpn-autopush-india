import os
import requests
import yaml

def get_clash_nodes():
    # 从环境变量读取订阅地址，方便动态修改
    url = os.getenv("CLASH_SUBSCRIBE_URL")
    if not url:
        print("⚠️ CLASH_SUBSCRIBE_URL 未设置")
        return []

    print(f"🌐 正在抓取 Clash 订阅：{url}")
    try:
        resp = requests.get(url, timeout=10)
    except Exception as e:
        print(f"❌ 抓取 {url} 时出错：{e}")
        return []

    if resp.status_code != 200:
        print(f"⚠️ {url} 返回状态码：{resp.status_code}")
        return []

    try:
        data = yaml.safe_load(resp.text)
    except Exception as e:
        print(f"❌ 解析 YAML 失败：{e}")
        return []

    if not data or "proxies" not in data:
        print("⚠️ YAML 文件没有找到 proxies 字段")
        return []

    proxies = data["proxies"]

    # 你可以在这里做简单过滤，比如只返回支持的类型
    # 比如只要 type 在 ['vmess', 'ss', 'trojan'] 等
    # 现在先全返回
    print(f"📦 总共收集 Clash 节点数：{len(proxies)}")
    return proxies
