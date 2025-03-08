from bs4 import BeautifulSoup
import requests
import json
from normalizing import normalize_product_name, preprocess_foxtrot_name


class Scraper:
    HEADERS_DICT = {
        "comfy": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        },
        "ctrs": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8"
        },
        "rozetka": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8"
        },
        "foxtrot": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8"
        },
        "moyo": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8"
        }
    }

    def __init__(self, page, store):
        self.page = page
        self.store = store
        self.product_name = None
        self.price = None
        self.headers = self.HEADERS_DICT.get(store, {})

    def scrape(self):
        response = requests.get(self.page, headers=self.headers)
        if response.status_code != 200:
            return {"error": f"Не вдалося отримати сторінку, статус-код: {response.status_code}"}

        soup = BeautifulSoup(response.text, "html.parser")

        if self.store == "ctrs":
            self.extract_ctrs(soup)
        elif self.store == "rozetka":
            self.extract_rozetka(soup)
        elif self.store == "foxtrot":
            self.extract_foxtrot(soup)
        elif self.store == "moyo":
            self.extract_moyo(soup)
        elif self.store == "comfy":
            self.extract_comfy(soup)

        return self.get_data()

    def clean_price(self, price):
        if isinstance(price, str):
            return price.replace("\xa0", "").replace("₴", "").strip()
        return price

    def extract_ctrs(self, soup):
        price_element = soup.find("div", class_="Price_price__KKCnw")
        self.price = self.clean_price(price_element.get("data-price", "Ціна не знайдена")) if price_element else "Ціна не знайдена"

        title_meta = soup.find("meta", {"property": "og:title"})
        self.product_name = title_meta.get("content", "Назва не знайдена") if title_meta else "Назва не знайдена"

    def extract_rozetka(self, soup):
        title_tag = soup.find("meta", property="og:title")
        self.product_name = title_tag["content"] if title_tag else "Назва не знайдена"

        price_tag = soup.find("p", class_="product-price__big product-price__big-color-red")
        self.price = self.clean_price(price_tag.text.strip()) if price_tag else "Ціна не знайдена"

    def extract_foxtrot(self, soup):
        script = soup.find("script", {"type": "application/ld+json"})
        if script:
            try:
                data = json.loads(script.string)
                if "name" in data and "offers" in data:
                    self.product_name = data["name"]
                    self.price = self.clean_price(data["offers"].get("price", "Не вказано"))
                elif "hasVariant" in data:
                    variant = data["hasVariant"][0]
                    self.product_name = variant.get("name", "Не вказано")
                    self.price = self.clean_price(variant.get("offers", {}).get("price", "Не вказано"))
            except (json.JSONDecodeError, IndexError, TypeError):
                self.product_name = "Не вдалося розпарсити дані"
                self.price = "Не вдалося розпарсити ціну"
        else:
            self.product_name = "Назва не знайдена"
            self.price = "Ціна не знайдена"

    def extract_moyo(self, soup):
        title_tag = soup.find("meta", {"property": "og:title"})
        self.product_name = title_tag["content"] if title_tag else "Назва не знайдена"

        price_tag = soup.find("meta", {"itemprop": "price"})
        self.price = self.clean_price(price_tag["content"]) if price_tag else "Ціна не знайдена"

    def extract_comfy(self, soup):
        script_tag = soup.find("script", type="application/ld+json")
        if script_tag:
            try:
                json_data = json.loads(script_tag.string)
                self.price = self.clean_price(json_data.get("offers", {}).get("price", "Ціна не знайдена"))
                self.product_name = json_data.get("name", "Назва не знайдена")
            except json.JSONDecodeError:
                self.product_name = "Не вдалося розпарсити дані"
                self.price = "Не вдалося розпарсити ціну"
        else:
            self.product_name = "Назва не знайдена"
            self.price = "Ціна не знайдена"

    def get_data(self):
        if self.store == "foxtrot":
            self.product_name = preprocess_foxtrot_name(self.product_name)

        normalized_name, product_key = normalize_product_name(self.product_name)

        return {
            "store": self.store,
            "product_name": normalized_name,   # збережемо нормалізовану назву
            "product_key": product_key,        # це наш ключ для порівняння
            "price": self.price
        }
