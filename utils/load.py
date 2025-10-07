import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def store_to_csv(df: pd.DataFrame, filename: str = "scraping_result.csv"):
    """
    Menyimpan DataFrame ke file CSV.
    """
    try:
        df.to_csv(filename, index=False)
        print(f"Data berhasil disimpan ke file: {filename}")
    except Exception as e:
        print(f"Gagal menyimpan data ke CSV: {e}")

def store_to_google_sheets(df: pd.DataFrame, spreadsheet_id: str, range_name: str):
    """Upload dataframe ke Google Sheets"""
    try:
        # Setup credentials
        creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Convert dataframe ke list of lists
        values = [df.columns.tolist()] + df.values.tolist()

        body = {"values": values}
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()

        print(f"Data berhasil dimuat ke Google Sheets: {result.get('updatedCells')} sel ter-update")
    except Exception as e:
        print(f"Error load ke Google Sheets: {e}")

def store_to_postgre(data, db_url):
    """Fungsi untuk menyimpan data ke dalam PostgreSQL."""
    try:
        # Buat engine database
        engine = create_engine(db_url)
        with engine.connect() as con:
            data.to_sql('product', con=con, if_exists='append', index=False)
            print("Data berhasil ditambahkan!")
        
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")