import pytest
from unittest.mock import MagicMock, patch
from src.data.crawler import SearchEngineScraper, RetailerScraper
import os

@pytest.fixture
def mock_dataset_dir(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    return str(d)

def test_search_engine_scraper_init(mock_dataset_dir):
    scraper = SearchEngineScraper(mock_dataset_dir)
    assert scraper.dataset_dir == mock_dataset_dir

@patch('src.data.crawler.BingImageCrawler')
def test_search_engine_scraper_scrape(mock_bing, mock_dataset_dir):
    scraper = SearchEngineScraper(mock_dataset_dir)
    coral_classes = {"acropora": ["acropora colony"]}
    images_per_keyword = 5
    
    # Mock crawler behavior
    mock_instance = mock_bing.return_value
    mock_instance.downloader.fetched_num = 5
    
    scraper.scrape(coral_classes, images_per_keyword)
    
    # Verify BingImageCrawler was called correctly
    mock_bing.assert_called()
    mock_instance.crawl.assert_called_with(keyword="acropora colony", max_num=5)
    assert os.path.exists(os.path.join(mock_dataset_dir, "acropora"))

def test_retailer_scraper_init(mock_dataset_dir):
    scraper = RetailerScraper(mock_dataset_dir)
    assert scraper.dataset_dir == mock_dataset_dir
    assert 'User-Agent' in scraper.headers

@patch('requests.get')
def test_retailer_scraper_scrape_wwc(mock_get, mock_dataset_dir):
    scraper = RetailerScraper(mock_dataset_dir)
    
    # Mock Shopify products.json response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "products": [
            {"images": [{"src": "http://example.com/img1.jpg"}]}
        ]
    }
    # Second call returns empty to break loop
    mock_response_empty = MagicMock()
    mock_response_empty.status_code = 200
    mock_response_empty.json.return_value = {"products": []}
    
    mock_get.side_effect = [mock_response, mock_response_empty, MagicMock(content=b"fake_image_data")]
    
    scraper.scrape_wwc("acropora", "acropora")
    
    assert os.path.exists(os.path.join(mock_dataset_dir, "acropora"))
    # Check if download was attempted (requests.get for image)
    assert mock_get.call_count >= 3 

@patch('requests.get')
def test_retailer_scraper_scrape_tidal_gardens(mock_get, mock_dataset_dir):
    scraper = RetailerScraper(mock_dataset_dir)
    
    # Mock HTML response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<div class="product-item"><img class="product-image-photo" data-src="https://tidalgardens.com/media/catalog/product/test.jpg"></div><a class="pages-item-next">Next</a>'
    
    # Second call returns empty or different text to break loop
    mock_response_empty = MagicMock()
    mock_response_empty.status_code = 200
    mock_response_empty.text = '<html></html>'
    
    mock_image_response = MagicMock()
    mock_image_response.content = b"fake_image_data"
    
    mock_get.side_effect = [mock_response, mock_response_empty, mock_image_response]
    
    scraper.scrape_tidal_gardens("https://tidalgardens.com/test", "acropora")
    
    assert os.path.exists(os.path.join(mock_dataset_dir, "acropora"))
    assert mock_get.call_count >= 3
