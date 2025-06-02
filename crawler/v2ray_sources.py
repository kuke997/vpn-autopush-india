import requests

def get_v2ray_links():
    urls = [
        'https://raw.githubusercontent.com/freefq/free/master/v2',
        'https://raw.githubusercontent.com/ermaozi01/free_clash_vpn/main/v2ray.txt'
    ]
    links = []
    for url in urls:
        try:
            resp = requests.get(url, timeout=10)
            links += [line.strip() for line in resp.text.splitlines() if line.startswith("vmess://")]
        except:
            continue
    return links
