import datetime
import time

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
}


def get_content(url, retries=3, delay=3):
    """Function untuk ambil konten HTML dari URL Website"""
    session = requests.Session()
    for attempt in range(retries):
        try:
            response = session.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"[Percobaan {attempt+1}] Gagal akses {url} - {e}")
            time.sleep(delay)
        except Exception as e:
            print(f"[Error] Terjadi kesalahan tak terduga saat akses {url}: {e}")
            break
    return None

def extract_fashion_data(product):
    """Funtion data mengambil beberapa value yang ditentukan"""
    try:
        # Title
        fashion_title = product.find('h3', class_='product-title')
        title = fashion_title.text.strip() if fashion_title else "Unknown Product"

        # Price
        fashion_price = product.find('span', class_='price')
        price = fashion_price.text.strip() if fashion_price else "Unknown Price"

        # Colors → ambil angka saja
        fashion_colors = product.find('p', string=lambda text: text and "Colors" in text)
        if fashion_colors:
            colors_text = fashion_colors.text.strip()
            colors = ''.join(filter(str.isdigit, colors_text)) or "Unknown"
        else:
            colors = "Unknown"

        # Size → ambil hanya value
        fashion_size = product.find('p', string=lambda text: text and "Size" in text)
        size = fashion_size.text.replace("Size:", "").strip() if fashion_size else "Unknown"

        # Gender → ambil hanya value
        fashion_gender = product.find('p', string=lambda text: text and "Gender" in text)
        gender = fashion_gender.text.replace("Gender:", "").strip() if fashion_gender else "Unknown"

        # Rating → ambil angka rating
        fashion_rating = product.find('p', string=lambda text: text and "Rating" in text)
        if fashion_rating:
            rating_text = fashion_rating.text.strip()
            rating = ''.join(ch for ch in rating_text if ch.isdigit() or ch == '.')
        else:
            rating = "Unknown"

        # Timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp,
        }
    except Exception as e:
        print(f"[Error] Gagal extract data produk: {e}")
        return {
            "Title": "Unknown Product",
            "Price": "Unknown Price",
            "Rating": "Unknown",
            "Colors": "Unknown",
            "Size": "Unknown",
            "Gender": "Unknown",
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

def scrape_product(base_url, max_pages=50, delay=5):
    """Function untuk scraping data secara keseluruhan halaman"""
    data = []
    page_number = 1
    
    while page_number <= max_pages:
        try:
            if page_number == 1:
                current_url = base_url
            else:
                current_url = f"{base_url}page{page_number}/"

            print(f"Melakukan Scraping Halaman: {current_url}")
            content = get_content(current_url)

            if not content:
                print(f"[Warning] Tidak ada konten di {current_url}")
                break

            soup = BeautifulSoup(content, "html.parser")
            product_element = soup.find_all('div', class_='collection-card')

            if not product_element:
                print(f"[Warning] Tidak ada produk ditemukan di {current_url}")
                break

            for product in product_element:
                fashion = extract_fashion_data(product)
                data.append(fashion)

            # cek tombol next
            next_button = soup.find('li', class_='page-item next')
            if next_button:
                page_number += 1
                time.sleep(delay)
            else:
                break
        except Exception as e:
            print(f"[Error] Gagal scraping {current_url}: {e}")
            break
        
    return data
