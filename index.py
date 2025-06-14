from scraper import *
import asyncio
import os

print("SnowMTL Downloader by Egwau")

base_url = input("Enter URL : ").replace("comics", "reader").rstrip("/")
chapters = input("Enter Chapters (e.g. 1-5 or 7) : ")

# Extract manga name from URL
manga_name = base_url.split("/")[-1]
download_dir = os.path.join("downloads", manga_name)

# Create main downloads directory if needed
os.makedirs(download_dir, exist_ok=True)
print(f"Download directory: {download_dir}")

if "-" in chapters:
    start, end = map(int, chapters.split("-"))
    url_array = [f"{base_url}/{i}" for i in range(start, end + 1)]
else:
    url_array = [f"{base_url}/{chapters}"]

print(f"Downloading {len(url_array)} chapters...")

async def main():
    for url in url_array:
        await scrape_snowmtl(url, download_dir)

asyncio.run(main())
print("Download completed.")