from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import os

LINK = "https://www.canalrural.com.br/agricultura/page/"
SELECTOR = {
    "noticia": "body > main",
}

path = '../../src/scraping'
os.makedirs(path, exist_ok=True)
data_formated = datetime.now().strftime('%Y-%m-%d')
ARQUIVO = os.path.join(path, f'raw_scraping_{data_formated}.txt')


def main():
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

                    elemento = page.wait_for_selector(SELECTOR["noticia"], timeout=5000)
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