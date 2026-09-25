""" Requests
    Enviar solicitudes HTTP para interactuar con web services y traer datos de páginas web.
    Ideal para acceder a APIs, decargar contenido o intectuar con websites.
"""
import requests

URL = "https://example.com"
TIMEOUT = 10


def requests_demo():
    try:
        response = requests.get(URL, timeout=TIMEOUT)
    except requests.RequestException as e:
        print(f"No se pudo acceder a {URL}: {e}")
        return

    if response.ok:
        print(response.text)
    else:
        print(f"Fallo al acceder a la pagina. Codigo de estado: {response.status_code}")


""" Selenium
    Auomatizar navegadores web simulando interacciones usuarios reales (clicking, scrolling, llenar formularios).
    Útil para automatizar tareas repetitivas, hacer testeo y acceder a contenido de páginas.

    Otras opciones son:
        - Playwright para automatización de páginas modernas.
        - Pyppeteer: Automatizar especialmente cuando el renderizado de código de Javascript es critico.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HEADLESS = True


def selenium_demo():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(URL)
        element = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        print("Page Heading:", element.text)
    except Exception as e:
        print("Error during Selenium execution:", e)
    finally:
        driver.quit()


""" Scrappy
    Obtencion y almacenamiento de los datos extraidos de paginas web.
    Proyectos de extracción de datos mas estructurados y escalables.
"""
import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = [URL]
    allowed_domains = ["example.com"]

    def parse(self, response):
        yield {"title": response.css("title::text").get()}


def main():
    requests_demo()
    selenium_demo()


if __name__ == "__main__":
    main()
