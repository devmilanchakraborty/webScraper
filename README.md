# DuckDuckGo Web Scraper

A Python web scraper for searching DuckDuckGo and extracting search results and images.

## Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web UI (Recommended) 🌐

Launch the modern web interface with image viewing:

```bash
source venv/bin/activate  # Activate virtual environment
python app.py
```

Then open your browser and go to: **http://localhost:5000**

The web UI features:
- **Modern Design**: Beautiful, responsive interface
- **Image Gallery**: View images in a grid with full-size modal viewer
- **Multiple Search Types**: Text, Images, News, and Videos
- **Real-time Results**: See results as they load
- **Save Functionality**: Download results as JSON files
- **Deep Scraping**: Optional page content extraction

### Command Line UI

Run the scraper with the interactive menu:

```bash
source venv/bin/activate  # Activate virtual environment
python scrape.py
```

The CLI UI provides:
- **Text Search**: Enter your query, number of results, and region
- **Image Search**: Search for images with customizable result count
- **News & Video Search**: Additional search types
- **Deep Scraping**: Full page content extraction
- **Save Results**: Option to save results to JSON files after each search

### Programmatic Usage

You can also use the scraper in your own code:

```python
from scrape import DuckDuckGoScraper

# Create scraper instance
scraper = DuckDuckGoScraper()

# Search for text
results = scraper.search("Python programming", max_results=10)
scraper.print_results(results)

# Save results to JSON
scraper.save_results(results, "my_results.json")

# Search for images
image_results = scraper.search_images("cats", max_results=5)
```

## Features

### Web Interface
- **🌐 Modern Web UI**: Beautiful, responsive design with gradient styling
- **🖼️ Image Viewer**: Click images to view full-size in modal
- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **⚡ Real-time Search**: Fast, asynchronous search operations
- **💾 Save Results**: Download search results as JSON files

### Search Capabilities
- **Text Search**: Search DuckDuckGo and get titles, URLs, snippets, and metadata
- **Image Search**: Search for images with thumbnails and full-size viewing
- **News Search**: Find news articles with dates, sources, and images
- **Video Search**: Search videos with duration, channel, views, and publish dates
- **Deep Scraping**: Extract full page content including meta tags, headings, images, and links

### Technical Features
- **Rate Limit Handling**: Automatic retry (up to 10 attempts) with exponential backoff
- **Error Handling**: Comprehensive error handling with detailed error messages
- **Input Validation**: Smart input handling with defaults and type checking
- **Metadata Extraction**: Automatically extracts hostnames, dates, categories, and more

## Methods

### `search(query, max_results=10, region='us-en')`
Performs a text search on DuckDuckGo.

**Parameters:**
- `query` (str): Search query string
- `max_results` (int): Maximum number of results (default: 10)
- `region` (str): Region/language code (default: 'us-en')

**Returns:** List of dictionaries with 'title', 'url', and 'snippet' keys

### `search_images(query, max_results=10, retry_delay=2.0)`
Searches for images on DuckDuckGo with automatic rate limit handling (up to 10 retries).

**Parameters:**
- `query` (str): Search query string
- `max_results` (int): Maximum number of results (default: 10)
- `retry_delay` (float): Initial delay in seconds before retrying after rate limit (default: 2.0)

**Returns:** List of dictionaries with 'title', 'url', 'thumbnail', and 'source' keys

### `print_results(results)`
Pretty prints search results to the console.

### `save_results(results, filename='search_results.json')`
Saves search results to a JSON file.

## Notes

- The scraper uses the `ddgs` package (the new name for `duckduckgo-search`)
- Image searches may hit rate limits if called too frequently - the scraper automatically retries up to 10 times with exponential backoff
- The interactive UI provides a smooth experience with input validation and helpful defaults
- You can cancel any operation with Ctrl+C
- Results are automatically formatted and displayed, with optional JSON export

