import requests
import yaml

def get_clash_nodes():
    urls = [
        'https://raw.githubusercontent.com/freefq/free/master/clash.yaml',
        'https://raw.githubusercontent.com/ermaozi01/free_clash_vpn/main/clash.yaml'
    ]
    nodes = []
    for url in urls:
        try:
            resp = requests.get(url, timeout=10)
            data = yaml.safe_load(resp.text)
            if 'proxies' in data:
                nodes += data['proxies']
        except:
            continue
    return {'proxies': nodes, 'port': 7890}
