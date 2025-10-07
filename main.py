from utils.extract import scrape_product
from utils.load import store_to_csv,store_to_google_sheets,store_to_postgre
from utils.transform import transform_data, transform_dataframe

SPREADSHEET_ID = "1Q0JwLiOBGnmZ89Wi0sK0ueLSgXAUghSs5cgt0Cby3w4"
RANGE_NAME = "Sheet1!A1"
DB_URL = "postgresql+psycopg2://gilang:gilang@localhost:5432/fashiondb"

def main():
    URL = "https://fashion-studio.dicoding.dev/"
    
    # 1. Extract
    all_product_data = scrape_product(base_url=URL, max_pages=50, delay=5)
    
    if not all_product_data:
        print("Tidak ada data yang ditemukan")
        return
    
    # 2. Transform ke DF dan Transformasi kolom Price
    df = transform_dataframe(all_product_data)

    df_cleaned = transform_data(df, exchange_rate=16000)
    print(df_cleaned.head())
    print(df_cleaned.info())
    
    # 3. Simpan hasil ke csv
    store_to_csv(df_cleaned, filename="scraping_result.csv")
    
    # 4. Simpan hasil ke googlesheets
    store_to_google_sheets(df_cleaned, SPREADSHEET_ID, RANGE_NAME)
    
    # 5. Simpan hasil ke postgre
    store_to_postgre(df_cleaned,DB_URL)

if __name__ == "__main__":
    main()
