import requests
import json
import base64
import os

# GitHub Secrets üzerinden gelecek bilgiler
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")
REPO_NAME = "nookjoook56-web/m3" # Kendi kullanıcı adın/repo adın
FILE_PATH = "playlist.m3u"

def update_github(content):
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Mevcut dosyanın SHA değerini al
    res = requests.get(url, headers=headers)
    sha = res.json().get('sha') if res.status_code == 200 else None

    base64_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    
    data = {
        "message": "Otomatik Güncelleme - backdor22",
        "content": base64_content,
        "branch": "main"
    }
    if sha: data["sha"] = sha

    requests.put(url, headers=headers, json=data)
    print("[+] Liste GitHub'a başarıyla itildi.")

def run():
    vavoo_url = "https://vavoo.to/channels?output=json"
    try:
        r = requests.get(vavoo_url, headers={'User-Agent': 'VAVOO/2.6'}, timeout=20)
        data = r.json()
        
        m3u = "#EXTM3U\n"
        for ch in data:
            name = ch.get('name') or "Kanal"
            group = ch.get('country', 'Global').upper()
            chid = ch.get('id')
            m3u += f'#EXTINF:-1 group-title="{group}", {name}\nhttp://vavoo.to/play/{chid}/index.m3u8\n'
        
        update_github(m3u)
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    run()
  
