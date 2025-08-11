# PhD Exam Downloader for sahla-dz.com

This tool automatically downloads PhD entrance exam content (PDFs and images) from the sahla-dz.com website. It scrapes the main page to find links to individual exam pages, extracts PDF URLs or embedded images, and downloads them to a specified folder.

## Features

- Scrapes the main page to find links to exam pages
- **NEW**: Handles lazy-loaded content using Selenium WebDriver
- Extracts PDF URLs from Google Docs viewer iframes
- Detects and downloads embedded images from iframes and divs
- Organizes images from each exam into dedicated folders
- Downloads PDFs to a specified folder
- Handles various URL formats and edge cases
- Provides detailed logging of the download process
- Automatic fallback from Selenium to requests-only mode if needed

## Requirements

- Python 3.6 or higher
- Google Chrome browser (for Selenium WebDriver)
- Required packages: requests, beautifulsoup4, selenium, webdriver-manager

**Note**: The tool will automatically download and manage ChromeDriver using webdriver-manager. If Chrome is not installed or Selenium fails to initialize, the tool will automatically fall back to requests-only mode (which may not work with lazy-loaded content).

## Installation

1. Clone or download this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script with Python:

```bash
python download_exams.py
```

### Command-Line Interface

For more flexibility, you can use the CLI script:

```bash
python cli.py --url "https://lmd.sahla-dz.com/sujets-concours-doctorat-informatique/" --output "path/to/output/folder"
```

Command-line arguments:
- `--url`: Base URL containing links to exam pages (optional)
- `--output`: Destination folder to save PDFs (optional)
- `--no-selenium`: Disable Selenium WebDriver and use only requests (optional)

### Handling Lazy-Loaded Content

By default, the tool uses Selenium WebDriver to handle lazy-loaded content (content that loads dynamically with JavaScript). This is particularly useful for pages where iframes are loaded after the initial page load.

```bash
# Use Selenium (default behavior)
python cli.py --url "https://example.com" --output "./downloads"

# Disable Selenium (faster but may miss lazy-loaded content)
python cli.py --url "https://example.com" --output "./downloads" --no-selenium
```

The script will:
1. Use the specified output folder (default: `d:/Developpement/Projets/Side_Projects/download_phd_exam_sahla_mahla/exams/`)
2. Scrape the main page to find links to exam pages
3. Extract PDF URLs or image URLs from each exam page
4. Download PDFs directly to the destination folder
5. For pages with images, create a dedicated subfolder and download all images there

## Customization

You can modify the following variables in the `main()` function of `download_exams.py`:

- `base_url`: The main URL containing links to exam pages
- `destination_folder`: The folder where PDFs will be saved

## How it Works

1. The script first visits the main page and finds all links that might lead to exam pages
2. For each exam page, it attempts to extract content using two methods:
   - **Selenium Method (default)**: Uses Chrome WebDriver to load the page, execute JavaScript, and handle lazy-loaded content
   - **Requests Method (fallback)**: Uses traditional HTTP requests for static content
3. **Selenium Process**:
   - Loads the page in a headless Chrome browser
   - Scrolls down and up to trigger lazy loading
   - Waits for iframes to load dynamically
   - Extracts the fully-rendered HTML for parsing
4. For each exam page, it looks for an iframe containing a Google Docs viewer
5. It extracts the PDF URL from the iframe's src attribute
6. If PDF iframes are found, it downloads the PDFs to the destination folder
7. If no PDF is found, it looks for embedded images in iframes or divs
8. For pages with images, it creates a dedicated subfolder named after the page and downloads all images there
9. If neither PDFs nor images are found, it tries to find direct download buttons or PDF links
10. **Automatic Fallback**: If Selenium fails or is disabled, the tool automatically falls back to the requests-only method

## Troubleshooting

If you encounter any issues:

- Make sure you have a stable internet connection
- Check that the website structure hasn't changed
- Verify that you have write permissions for the destination folder
- Try running the script with administrator privileges if necessary

### Selenium-Related Issues

- **Chrome not found**: Install Google Chrome browser
- **ChromeDriver issues**: The tool automatically manages ChromeDriver, but if issues persist, try updating Chrome
- **Selenium timeout errors**: The page might be taking longer to load; the tool will automatically fall back to requests-only mode
- **Performance issues**: Use `--no-selenium` flag to disable Selenium if you don't need lazy-loading support
- **Headless browser issues**: If you encounter display-related errors, the tool runs Chrome in headless mode by default

## Disclaimer

This tool is for educational purposes only. Please respect the website's terms of service and do not overload their servers with requests.