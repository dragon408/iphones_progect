import re


def normalize_product_name(raw_name):
    name = raw_name.lower()

    # Викидаємо бренд і зайві слова
    remove_words = [
        "apple", "смартфон", "мобільний телефон", "в інтернет магазині",
        "купить в киеве", "цена и отзывы", "оригінал", "телефон", "мобільний"
    ]
    for word in remove_words:
        name = name.replace(word, "")

    # Викидаємо артикули (типу MYX13, MYX13SX/A тощо)
    name = re.sub(r"\(.*?\)", "", name)

    # Викидаємо все зайве (сильна чистка)
    name = re.sub(r"[^\w\s]", "", name).strip()

    # Міняємо синоніми на єдиний формат
    synonyms = {
        "гб": "gb",
        "синій": "blue",
        "чорний": "black",
        "білий": "white",
        "зелений": "green",
        "рожевий": "pink",
        "фіолетовий": "purple",
        "про": "pro",
        "макс": "max",
        "титановий": "titanium"
    }
    for k, v in synonyms.items():
        name = name.replace(k, v)

    # Витягуємо дані через патерн
    match = re.search(r"iphone\s*(\d{2})\s*(pro max|pro|max|mini|)\s*(\d{2,4})\s*gb\s*(\w+)?", name)

    if not match:
        return raw_name.strip(), None  # Якщо не розпарсилось, повертаємо як є

    model = match.group(1)
    version = match.group(2).strip() if match.group(2) else ""
    storage = match.group(3)
    color = match.group(4) if match.group(4) else ""

    normalized_name = f"iphone {model} {version} {storage}gb {color}".strip()
    product_key = normalized_name.replace(" ", "_")

    return normalized_name, product_key


def preprocess_foxtrot_name(name):
    # Прибираємо "Смартфон APPLE" або "APPLE"
    name = re.sub(r"(?i)\b(смартфон\s*)?apple\b", "", name).strip()

    # Видаляємо все в дужках (типу (MYX43SX/A))
    name = re.sub(r"\(.*?\)", "", name).strip()

    return name
