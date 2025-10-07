import pandas as pd


import pandas as pd

def transform_dataframe(data):
    """Mengubah hasil scraping menjadi dataframe."""
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"[Error] Gagal membuat DataFrame: {e}")
        return pd.DataFrame()  # fallback dataframe kosong


def transform_data(data, exchange_rate):
    """Transformasi data dengan error handling"""
    try:
        df = pd.DataFrame(data)

        # --- Step 1: Invalid value ke NaN ---
        invalid_value = [
            "Unknown Product",
            "Price Unavailable",
            "Invalid Rating / 5",
            "Not Rated",
            None
        ]
        df = df.replace(invalid_value, pd.NA).dropna(how="any")

        # --- Step 2: Price ke float (USD → IDR) ---
        try:
            df["Price"] = (
                df["Price"]
                .astype(str)
                .str.replace(r"[^0-9.]", "", regex=True)
                .replace("", pd.NA)
            )
            df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
            df = df.dropna(subset=["Price"])
            df["Price"] = df["Price"] * exchange_rate
        except Exception as e:
            print(f"[Warning] Gagal transformasi kolom Price: {e}")
            df["Price"] = pd.NA

        # --- Step 3: Rating ke float ---
        df['Rating'] = df['Rating'].str.extract(r"([\d.]+)").astype(float)

        # --- Step 4: Colors ke int ---
        try:
            df["Colors"] = pd.to_numeric(df["Colors"], errors="coerce").astype("Int64")
        except Exception as e:
            print(f"[Warning] Gagal transformasi kolom Colors: {e}")
            df["Colors"] = pd.NA

        # --- Step 5: Drop duplikasi ---
        df = df.drop_duplicates()

        return df

    except Exception as e:
        print(f"[Error] Gagal transformasi data: {e}")
        return pd.DataFrame()