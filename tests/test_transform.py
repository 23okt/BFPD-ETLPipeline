from unittest.mock import patch
import pandas as pd
from utils.transform import transform_dataframe, transform_data
import utils.transform


# ---------- TEST transform_dataframe ----------
def test_transform_dataframe_success():
    data = [{"Title": "Product A", "Price": 10.0, "Rating": 3, "Colors": 3, "Size": "M", "Gender": "Unisex"}]
    df = transform_dataframe(data)
    assert not df.empty
    assert list(df.columns) == ["Title", "Price","Rating","Colors","Size","Gender"]
    assert df.iloc[0]["Title"] == "Product A"

# ---------- TEST transform_data ----------
def test_transform_data_valid():
    data = [{"Title": "Product A", "Price": "$ 10.5", "Rating": "3", "Colors": "3", "Size": "M", "Gender": "Unisex"}]
    df = transform_data(data, exchange_rate=15000)
    assert not df.empty
    assert "Price" in df.columns
    assert df["Price"].iloc[0] == 10.5 * 15000
    assert df["Rating"].iloc[0] == 3.0
    assert df["Colors"].iloc[0] == 3
    assert df["Size"].iloc[0] == "M"
    assert df["Gender"].iloc[0] == "Unisex"


def test_transform_data_with_invalid_values():
    data = [{"Title": "Unknown Product A", "Price": "Price Unavaliable", "Rating": "Invalid Rating / 5", "Colors": 3, "Size": "M", "Gender": "Unisex"}]
    df = transform_data(data, exchange_rate=15000)
    # Book C harus hilang karena semua invalid
    assert "Unknown Product A" not in df["Title"].values
    assert pd.isna(df.loc[df["Title"] == "Unknown Product A", "Rating"]).all()
    assert pd.isna(df.loc[df["Title"] == "Unknown Product A", "Colors"]).all()


def test_transform_data_empty_input():
    df = transform_data([], exchange_rate=16000)
    assert isinstance(df, pd.DataFrame)
    assert df.empty
