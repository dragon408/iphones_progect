from scrap import Scraper

# Тестові URL (заміни на реальні, якщо вони змінились)
test_urls = {
    "ctrs": "https://www.ctrs.com.ua/smartfony/iphone-16-pro-max-512gb-white-titanium-apple-752241.html?gad_source=1&gclid=Cj0KCQiA2oW-BhC2ARIsADSIAWoPLW3FLtSmWmagc2eSMEXhPN1C6eaLfJNtK4HublI0Ha6KN8e_ZvAaAuKfEALw_wcB",
    "rozetka": "https://rozetka.com.ua/ua/apple-myx13sx-a/p448428632/",
    "foxtrot": "https://www.foxtrot.com.ua/uk/shop/smartfoniy-i-mobilniye-telefoniy-apple-iphone-16-pro-max-512gb-white-titanium.html?utm_source=google&utm_medium=cpc&utm_campaign=1-[regular]-[Srch]-[Pro-Audit]-[feed]-[PMax]-[DIG]-[Top-Perform]_pr_mpc_reg_&utm_content=17568238518&gad_source=1&gclid=Cj0KCQiA2oW-BhC2ARIsADSIAWrufcFJ6Ld-2gEvxQZWmyYYXl9gOwFeNanm5UIgtcFIxIz2wRgqymgaAsKDEALw_wcB",
    "moyo": "https://www.moyo.ua/smartfon_apple_iphone_16_pro_max_512gb_white_titanium/600497.html?srsltid=AfmBOoqH8d-r2J_PXf3Bu3NE9olDktByX5y4DHYZgzLKKOAPuMT9r7h6",
    "comfy": "https://comfy.ua/ua/smartfon-apple-iphone-16-pro-max-512gb-white-titanium.html"
}

# Перевіряємо кожен магазин
for store, url in test_urls.items():
    print(f"Тестуємо {store}...")
    scraper = Scraper(url, store)
    result = scraper.scrape()
    print(result)
    print("-" * 50)
