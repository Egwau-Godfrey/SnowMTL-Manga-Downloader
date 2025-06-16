from scraper import scrape_snowmtl
import asyncio
import os
import time

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
    # Create a list of tasks to run concurrently
    tasks = [scrape_snowmtl(url, download_dir) for url in url_array]
    
    # Use asyncio.gather to run tasks concurrently
    start_time = time.time()
    await asyncio.gather(*tasks)  # The * unpacks the list into separate arguments
    end_time = time.time()
    print(f"Downloaded {len(url_array)} chapters in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":  # Add this to allow running asyncio.run()
    asyncio.run(main())
    print("Download completed.")