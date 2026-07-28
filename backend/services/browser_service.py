from playwright.sync_api import sync_playwright

def obtener_html(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)  # Espera 3 segundos para que la página cargue completamente
        html = page.content()
        browser.close()
        return html