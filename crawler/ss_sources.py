import requests
import base64

def get_ss_links():
    urls = [
        'https://raw.githubusercontent.com/freefq/free/master/ss',
        'https://raw.githubusercontent.com/ermaozi01/free_clash_vpn/main/shadowsocks.txt'
    ]
    links = []
    for url in urls:
        try:
            resp = requests.get(url, timeout=10)
            lines = resp.text.splitlines()
            for line in lines:
                if line.startswith("ss://"):
                    links.append(line.strip())
        except:
            continue
    return links
