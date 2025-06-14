from playwright.async_api import async_playwright
import os
import zipfile
import shutil

async def scrape_snowmtl(url, base_download_dir):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        await page.locator("div.loading-spinner").wait_for(state='detached', timeout=120000)
        await page.wait_for_timeout(60000)

        chapter_number = url.split("/")[-1]
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

            for i, container in enumerate(comic_image_containers):
                image_path = os.path.join(temp_dir, f'page_{i+1:03d}.png')
                await container.screenshot(path=image_path)

            # Create CBZ in manga directory
            cbz_path = os.path.join(base_download_dir, cbz_filename)
            with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_DEFLATED) as cbz_file:
                for filename in sorted(os.listdir(temp_dir)):
                    filepath = os.path.join(temp_dir, filename)
                    cbz_file.write(filepath, filename)
            
            print(f"Downloaded chapter {chapter_number} to {cbz_path}")
        finally:
            # Cleanup temporary files
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            await browser.close()