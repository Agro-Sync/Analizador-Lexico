"""
    This script scrapes news content from the Canal Rural agriculture section using Playwright.
    Constants:
        LINK (str): Base URL for Canal Rural agriculture news pages.
        SELECTOR (dict): CSS selectors for scraping elements.
        path (str): Directory path for storing scraped data.
        ARQUIVO (str): File path for saving raw scraped content.
    Functions:
        main():
            Launches a headless Chromium browser using Playwright.
            Iterates through up to 14 paginated news pages.
            For each page:
                - Navigates to the URL.
                - Waits for the main content selector.
                - Extracts and formats the news content.
                - Writes the content to a timestamped text file.
            Handles timeouts and other exceptions gracefully.
            Closes the browser after scraping.
    Usage:
        Run the script directly to start scraping and saving news content.
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import os

LINK = "https://www.canalrural.com.br/agricultura/page/"
SELECTOR = {
    "noticia": "body > main",
}

PATH = 'src/scraping'
os.makedirs(PATH, exist_ok=True)
data_formated = datetime.now().strftime('%Y-%m-%d')
ARQUIVO = os.path.join(PATH, f'raw_scraping_{data_formated}.txt')


def main():
    """
    Scrape news articles from multiple pages using Playwright and save to a file.
    Launches a headless Chromium browser and iterates through pages (1-14) to extract
    news content. For each page, it waits for a specific selector to load, extracts
    text content, processes it by removing header lines and extra content, then writes
    the formatted content to a file.
    The function handles dynamic slicing of content based on page number:
    - Page 1: removes first 5 lines and last 8 lines
    - Pages 2-5: removes first 5 lines and last 9 lines
    - Pages 6+: removes first 5 lines and last 12 lines
    Stops processing if:
    - The target element is not found on a page
    - A timeout occurs while waiting for page content to load
    - Any other exception is encountered during processing
    Raises:
        PlaywrightTimeoutError: When page content fails to load within timeout period.
        Exception: For any other errors during page processing.
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        i = 1

        with open(ARQUIVO, "a", encoding="utf-8") as f:
            while i < 15:
                url = f"{LINK}{i}/"
                print(f"Acessando: {url}")
                page.goto(url, wait_until="domcontentloaded")

                try:
                    if i == 1:
                        final = -7 - i
                    elif i <= 5:
                        final = -7 - i - 1
                    else:
                        final = -12

                    elemento = page.wait_for_selector(
                        SELECTOR["noticia"], timeout=5000)
                    if not elemento:
                        print("Elemento não encontrado, encerrando.")
                        break

                    content_raw = elemento.inner_text().split("\n")
                    content = '\n'.join(content_raw[5:final])

                    # print(content)
                    f.write(f"=== Página {i} ===\n" + content + "\n")

                    i += 1

                except PlaywrightTimeoutError:
                    print("Timeout — sem mais páginas disponíveis.")
                    break
                except Exception as e:
                    print(f"Erro ao processar página {i}: {e}")
                    break

        browser.close()


if __name__ == "__main__":
    main()
