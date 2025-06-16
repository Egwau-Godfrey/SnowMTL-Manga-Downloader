from playwright.async_api import async_playwright
import os
import zipfile
import shutil
import asyncio  # Import asyncio


async def scrape_snowmtl(url, base_download_dir):
    chapter_number = url.split("/")[-1]  # Get chapter number outside try-except
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            print(f"Downloading chapter {chapter_number} from {url}")  # Print URL being scraped

            await page.goto(url, timeout=90000)

            await page.locator("div.loading-spinner").wait_for(state='detached', timeout=120000)
            await page.wait_for_timeout(60000) 


            cbz_filename = f"chapter_{chapter_number}.cbz"
            image_dir = f"temp_images_{chapter_number}"

            # Create manga-specific directory
            os.makedirs(base_download_dir, exist_ok=True)
            
            # Create temporary image directory
            temp_dir = os.path.join(base_download_dir, image_dir)
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)

            try:
                comic_image_containers = await page.locator("div.comic-image-container").all()
                
                # Use asyncio.gather for concurrent screenshot capture.  Important: Limit concurrency
                # to avoid overwhelming the browser and the server.  We are using a semaphore.
                semaphore = asyncio.Semaphore(4)  # Limits to 4 concurrent screenshots 
                async def take_screenshot(i, container):
                    async with semaphore:  # Acquire the semaphore before taking the screenshot
                        image_path = os.path.join(temp_dir, f'page_{i+1:03d}.png')
                        await container.screenshot(path=image_path)


                screenshot_tasks = [take_screenshot(i, container) for i, container in enumerate(comic_image_containers)]
                await asyncio.gather(*screenshot_tasks)


                # Create CBZ in manga directory
                cbz_path = os.path.join(base_download_dir, cbz_filename)
                with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_DEFLATED) as cbz_file:
                    for filename in sorted(os.listdir(temp_dir)):
                        filepath = os.path.join(temp_dir, filename)
                        cbz_file.write(filepath, filename)
                
                print(f"Downloaded chapter {chapter_number} to {cbz_path}")
            except Exception as e: # catch specific playwright errors and other potential errors
                print(f"Error downloading chapter {chapter_number}: {e}") # Print the error
            finally:
                # Cleanup temporary files
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                await browser.close()
    except Exception as e:
        print(f"Error launching browser or playwright for chapter {chapter_number}: {e}")