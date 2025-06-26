import asyncio
import aiohttp
import os

PLAYLIST_FILE = "playlists/tr.m3u"
TIMEOUT = 10

async def check_url(session, url):
    try:
        async with session.get(url, timeout=TIMEOUT) as resp:
            if resp.status == 200:
                print(f"[✔] Çalışıyor: {url}")
                return True
            else:
                print(f"[✘] Erişilemiyor (Status {resp.status}): {url}")
                return False
    except Exception as e:
        print(f"[✘] Hata: {url} -> {e}")
        return False

async def check_playlist():
    if not os.path.exists(PLAYLIST_FILE):
        print(f"Dosya bulunamadı: {PLAYLIST_FILE}")
        return

    with open(PLAYLIST_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    urls = []
    for line in lines:
        line = line.strip()
        if line.startswith("http"):
            urls.append(line)

    async with aiohttp.ClientSession() as session:
        tasks = [check_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    print("\nKontrol edilen linkler sayısı:", len(urls))
    print("Çalışan link sayısı:", sum(results))

if __name__ == "__main__":
    asyncio.run(check_playlist())
