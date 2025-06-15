# SnowMTL Downloader

A simple Python tool to download manga chapters from SnowMTL and save them as CBZ files.

## Description

This tool uses Playwright to automate the process of downloading manga chapters from SnowMTL. It captures each page as an image and compiles them into a CBZ file that can be read with most comic/manga readers.

## Installation

1. Clone this repository or download the files
2. Make sure you have Python 3.6+ installed
3. Create a virtual environment:

```bash
# For Windows
python -m venv venv

# For macOS/Linux
python3 -m venv venv
```

4. Activate the virtual environment:

```bash
# For Windows
venv\Scripts\activate

# For macOS/Linux
source venv/bin/activate
```

5. Install the required dependencies:

```bash
pip install playwright
```

6. Install the Playwright browsers:

```bash
python -m playwright install chromium
```

## Usage

1. Run the script:

```bash
python index.py
```

2. Enter the URL of the manga e.g ( https://snowmtl.net/comics/a-will-eternal )
3. Enter the chapter(s) you want to download:
   - Single chapter: Enter the chapter number (e.g., `7`)
   - Range of chapters: Enter a range (e.g., `1-5`)
4. Wait for the download to complete
5. Check your directory for the CBZ files (named `chapter_X.cbz`)

## License

This code is free to use, modify, and distribute for any purpose.

## Contributing

This project may have bugs or areas for improvement. Feel free to:

- Open an issue if you find a bug
- Submit a pull request if you have a fix or enhancement
- Fork the project for your own needs

## Disclaimer

This tool is for personal use only. Please respect copyright laws and terms of service for the websites you access with this tool.
