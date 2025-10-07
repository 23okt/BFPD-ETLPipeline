import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from utils.extract import get_content, extract_fashion_data, scrape_product


# -------- TEST get_content --------
@patch("utils.extract.requests.Session.get")
def test_get_content_success(mock_get):
    mock_response = MagicMock()
    mock_response.content = b"<html></html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_content("http://dummy-url.com")
    assert result == b"<html></html>"


@patch("utils.extract.requests.Session.get")
def test_get_content_fail(mock_get):
    mock_get.side_effect = Exception("Request failed")

    result = get_content("http://dummy-url.com", retries=1)
    assert result is None


# -------- TEST extract_fashion_data --------
def test_extract_fashion_data_success():
    html = """
    <div class="collection-card">
        <h3 class="product-title">T-Shirt</h3>
        <span class="price">$10</span>
        <p>3 Colors</p>
        <p>Size: L</p>
        <p>Gender: Unisex</p>
        <p>Rating: 4.5</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    product = soup.find("div", class_="collection-card")

    result = extract_fashion_data(product)
    assert result["Title"] == "T-Shirt"
    assert result["Price"] == "$10"
    assert result["Colors"] == "3"
    assert result["Size"] == "L"
    assert result["Gender"] == "Unisex"
    assert result["Rating"] == "4.5"
    assert "Timestamp" in result


def test_extract_fashion_data_error():
    # Kirim objek kosong -> harus kembali default "Unknown"
    result = extract_fashion_data(None)
    assert result["Title"] == "Unknown Product"
    assert result["Price"] == "Unknown Price"


# -------- TEST scrape_product --------
@patch("utils.extract.get_content")
def test_scrape_product_success(mock_get_content):
    html = """
    <html>
        <div class="collection-card">
            <h3 class="product-title">Shoes</h3>
            <span class="price">$20</span>
            <p>2 Colors</p>
            <p>Size: XL</p>
            <p>Gender: Men</p>
            <p>Rating: 3.9</p>
        </div>
    </html>
    """
    mock_get_content.return_value = html

    result = scrape_product("http://dummy-url.com", max_pages=1)
    assert len(result) == 1
    assert result[0]["Title"] == "Shoes"
    assert result[0]["Price"] == "$20"


@patch("utils.extract.get_content")
def test_scrape_product_no_content(mock_get_content):
    mock_get_content.return_value = None
    result = scrape_product("http://dummy-url.com", max_pages=1)
    assert result == []
