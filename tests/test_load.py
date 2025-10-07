import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from utils.load import store_to_csv, store_to_google_sheets, store_to_postgre


# ------- FIXTURE DUMMY DATA -------
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Title": ["Item A", "Item B"],
        "Price": [1000, 2000],
        "Rating": [4.5, 3.9],
        "Colors": [3,5],
        "Size": ["M","L"],
        "Gender": ["Men", "Women"],
    })


# ------- TEST store_to_csv -------
def test_store_to_csv(tmp_path, sample_df):
    filename = tmp_path / "test.csv"
    store_to_csv(sample_df, filename)

    assert os.path.exists(filename)
    df_loaded = pd.read_csv(filename)
    assert df_loaded.shape == sample_df.shape


# ------- TEST store_to_google_sheets -------
@patch("utils.load.build")
@patch("utils.load.Credentials.from_service_account_file")
def test_store_to_google_sheets(mock_creds, mock_build, sample_df):
    # Mock service dan spreadsheets
    mock_service = MagicMock()
    mock_sheets = MagicMock()
    mock_service.spreadsheets.return_value = mock_sheets
    mock_build.return_value = mock_service

    mock_sheets.values.return_value.update.return_value.execute.return_value = {
        "updatedCells": 10
    }

    store_to_google_sheets(sample_df, "dummy-id", "Sheet1!A1")

    mock_build.assert_called_once()
    mock_sheets.values.return_value.update.assert_called_once()


# ------- TEST store_to_postgre -------
@patch("pandas.DataFrame.to_sql")
@patch("utils.load.create_engine")
def test_store_to_postgre(mock_engine, mock_to_sql, sample_df):
    # Mock connection
    mock_conn = MagicMock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

    # Panggil fungsi
    store_to_postgre(sample_df, "postgresql://user:pass@localhost:5432/dbname")

    # Cek apakah to_sql dipanggil sekali
    mock_to_sql.assert_called_once_with(
        'product', con=mock_conn, if_exists='append', index=False
    )
