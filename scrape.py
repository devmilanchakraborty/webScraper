"""
DuckDuckGo Web Scraper
A simple web scraper to search and extract results from DuckDuckGo
"""

from ddgs import DDGS
try:
    from ddgs.exceptions import RatelimitException
except ImportError:
    # Create a simple exception class if import fails
    class RatelimitException(Exception):
        pass
import json
from typing import List, Dict, Optional
import traceback
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class DuckDuckGoScraper:
    """A scraper for DuckDuckGo search results"""
    
    def __init__(self):
        """Initialize the scraper"""
        try:
            self.ddgs = DDGS()
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
        except Exception as e:
            print(f"Error initializing DDGS: {e}")
            traceback.print_exc()
            raise
    
    def search(self, query: str, max_results: int = 10, region: str = 'us-en') -> List[Dict]:
        """
        Search DuckDuckGo and return results
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return (default: 10)
            region: Region/language code (default: 'us-en')
        
        Returns:
            List of dictionaries containing title, url, and snippet for each result
        """
        results = []
        try:
            # Perform the search - DDGS.text() returns a generator
            search_results = self.ddgs.text(
                query,
                max_results=max_results,
                region=region
            )
            
            # Extract ALL available fields from results
            count = 0
            for result in search_results:
                if count >= max_results:
                    break
                
                # Extract all available data fields
                result_data = {
                    'title': result.get('title', result.get('Title', '')),
                    'url': result.get('href', result.get('url', result.get('URL', ''))),
                    'snippet': result.get('body', result.get('Body', result.get('snippet', ''))),
                    'raw_data': dict(result)  # Store all raw data
                }
                
                # Extract additional fields if available
                if 'date' in result:
                    result_data['date'] = result.get('date')
                if 'category' in result:
                    result_data['category'] = result.get('category')
                if 'hostname' in result:
                    result_data['hostname'] = result.get('hostname')
                else:
                    # Extract hostname from URL
                    try:
                        parsed = urlparse(result_data['url'])
                        result_data['hostname'] = parsed.netloc
                    except:
                        pass
                
                results.append(result_data)
                count += 1
            
            return results
            
        except Exception as e:
            print(f"Error during search: {e}")
            traceback.print_exc()
            return []
    
    def search_images(self, query: str, max_results: int = 10, retry_delay: float = 2.0) -> List[Dict]:
        """
        Search for images on DuckDuckGo
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            retry_delay: Delay in seconds before retrying after rate limit (default: 2.0)
        
        Returns:
            List of dictionaries containing image information
        """
        results = []
        max_retries = 10
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # DDGS.images() returns a generator
                image_results = self.ddgs.images(
                    query,
                    max_results=max_results
                )
                
                count = 0
                for result in image_results:
                    if count >= max_results:
                        break
                    # Extract all available image data
                    img_data = {
                        'title': result.get('title', ''),
                        'url': result.get('image', ''),
                        'thumbnail': result.get('thumbnail', ''),
                        'source': result.get('url', ''),
                        'raw_data': dict(result)  # Store all raw data
                    }
                    
                    # Extract additional image metadata if available
                    if 'width' in result:
                        img_data['width'] = result.get('width')
                    if 'height' in result:
                        img_data['height'] = result.get('height')
                    if 'size' in result:
                        img_data['size'] = result.get('size')
                    if 'format' in result:
                        img_data['format'] = result.get('format')
                    
                    results.append(img_data)
                    count += 1
                
                return results
                
            except RatelimitException as e:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"Rate limit hit. Waiting {retry_delay} seconds before retry {retry_count}/{max_retries-1}...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print(f"Error: Rate limit exceeded after {max_retries} attempts. Please try again later.")
                    return []
            except Exception as e:
                print(f"Error during image search: {e}")
                traceback.print_exc()
                return []
        
        return []
    
    def scrape_page_content(self, url: str, timeout: int = 10) -> Optional[Dict]:
        """
        Scrape detailed content from a web page
        
        Args:
            url: URL of the page to scrape
            timeout: Request timeout in seconds
        
        Returns:
            Dictionary with extracted page data or None if failed
        """
        try:
            response = self.session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract comprehensive page data
            page_data = {
                'url': url,
                'title': '',
                'description': '',
                'keywords': [],
                'author': '',
                'content': '',
                'images': [],
                'links': [],
                'meta_tags': {},
                'headings': {},
                'text_content': '',
                'language': '',
                'charset': '',
                'canonical_url': ''
            }
            
            # Extract title
            if soup.title:
                page_data['title'] = soup.title.string.strip() if soup.title.string else ''
            
            # Extract meta tags
            for meta in soup.find_all('meta'):
                name = meta.get('name', '').lower()
                property_attr = meta.get('property', '').lower()
                content = meta.get('content', '')
                
                if name == 'description' or property_attr == 'og:description':
                    page_data['description'] = content
                elif name == 'keywords':
                    page_data['keywords'] = [k.strip() for k in content.split(',')]
                elif name == 'author':
                    page_data['author'] = content
                elif property_attr == 'og:title':
                    page_data['title'] = content if not page_data['title'] else page_data['title']
                elif property_attr == 'og:url':
                    page_data['canonical_url'] = content
                
                # Store all meta tags
                if name:
                    page_data['meta_tags'][name] = content
                if property_attr:
                    page_data['meta_tags'][property_attr] = content
            
            # Extract language and charset
            html_tag = soup.find('html')
            if html_tag:
                page_data['language'] = html_tag.get('lang', '')
            
            meta_charset = soup.find('meta', charset=True)
            if meta_charset:
                page_data['charset'] = meta_charset.get('charset', '')
            
            # Extract headings
            for level in range(1, 7):
                headings = soup.find_all(f'h{level}')
                page_data['headings'][f'h{level}'] = [h.get_text().strip() for h in headings]
            
            # Extract images
            for img in soup.find_all('img'):
                img_info = {
                    'src': img.get('src', ''),
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                }
                if img_info['src']:
                    page_data['images'].append(img_info)
            
            # Extract links
            for link in soup.find_all('a', href=True):
                page_data['links'].append({
                    'url': link.get('href', ''),
                    'text': link.get_text().strip()[:100]
                })
            
            # Extract main text content (remove scripts and styles)
            for script in soup(["script", "style", "meta", "link"]):
                script.decompose()
            
            page_data['text_content'] = soup.get_text(separator=' ', strip=True)
            page_data['content'] = page_data['text_content'][:5000]  # Limit content size
            
            return page_data
            
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'status': 'failed'
            }
    
    def search_news(self, query: str, max_results: int = 10, region: str = 'us-en') -> List[Dict]:
        """
        Search for news articles on DuckDuckGo
        
        Args:
            query: Search query string
            max_results: Maximum number of results
            region: Region/language code
        
        Returns:
            List of dictionaries containing news article information
        """
        results = []
        try:
            news_results = self.ddgs.news(
                query,
                max_results=max_results,
                region=region
            )
            
            count = 0
            for result in news_results:
                if count >= max_results:
                    break
                
                news_data = {
                    'title': result.get('title', ''),
                    'url': result.get('url', result.get('href', '')),
                    'snippet': result.get('body', result.get('snippet', '')),
                    'raw_data': dict(result)
                }
                
                # Extract news-specific fields
                if 'date' in result:
                    news_data['date'] = result.get('date')
                if 'source' in result:
                    news_data['source'] = result.get('source')
                if 'image' in result:
                    news_data['image'] = result.get('image')
                
                # Extract hostname
                try:
                    parsed = urlparse(news_data['url'])
                    news_data['hostname'] = parsed.netloc
                except:
                    pass
                
                results.append(news_data)
                count += 1
            
            return results
            
        except Exception as e:
            print(f"Error during news search: {e}")
            traceback.print_exc()
            return []
    
    def search_videos(self, query: str, max_results: int = 10, region: str = 'us-en') -> List[Dict]:
        """
        Search for videos on DuckDuckGo
        
        Args:
            query: Search query string
            max_results: Maximum number of results
            region: Region/language code
        
        Returns:
            List of dictionaries containing video information
        """
        results = []
        try:
            video_results = self.ddgs.videos(
                query,
                max_results=max_results,
                region=region
            )
            
            count = 0
            for result in video_results:
                if count >= max_results:
                    break
                
                video_data = {
                    'title': result.get('title', ''),
                    'url': result.get('url', result.get('href', '')),
                    'snippet': result.get('description', result.get('body', '')),
                    'raw_data': dict(result)
                }
                
                # Extract video-specific fields
                if 'thumbnail' in result:
                    video_data['thumbnail'] = result.get('thumbnail')
                if 'duration' in result:
                    video_data['duration'] = result.get('duration')
                if 'channel' in result:
                    video_data['channel'] = result.get('channel')
                if 'views' in result:
                    video_data['views'] = result.get('views')
                if 'published' in result:
                    video_data['published'] = result.get('published')
                
                # Extract hostname
                try:
                    parsed = urlparse(video_data['url'])
                    video_data['hostname'] = parsed.netloc
                except:
                    pass
                
                results.append(video_data)
                count += 1
            
            return results
            
        except Exception as e:
            print(f"Error during video search: {e}")
            traceback.print_exc()
            return []
    
    def enhance_results_with_page_content(self, results: List[Dict], max_pages: int = 5) -> List[Dict]:
        """
        Enhance search results by scraping page content from URLs
        
        Args:
            results: List of search result dictionaries
            max_pages: Maximum number of pages to scrape (default: 5)
        
        Returns:
            List of enhanced result dictionaries with page content
        """
        enhanced = []
        scraped = 0
        
        for result in results:
            if scraped >= max_pages:
                enhanced.append(result)
                continue
            
            url = result.get('url', '')
            if url:
                print(f"  Scraping content from: {url[:60]}...")
                page_content = self.scrape_page_content(url)
                if page_content and 'error' not in page_content:
                    result['page_content'] = page_content
                    scraped += 1
                    time.sleep(1)  # Be respectful with requests
        
            enhanced.append(result)
        
        return enhanced
    
    def save_results(self, results: List[Dict], filename: str = 'search_results.json'):
        """
        Save search results to a JSON file
        
        Args:
            results: List of result dictionaries
            filename: Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def print_results(self, results: List[Dict], detailed: bool = False):
        """
        Pretty print search results to console
        
        Args:
            results: List of result dictionaries
            detailed: If True, print all available fields
        """
        if not results:
            print("No results found.")
            return
        
        print(f"\n{'='*80}")
        print(f"Found {len(results)} results:")
        print(f"{'='*80}\n")
        
        for i, result in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"  Title: {result.get('title', 'N/A')}")
            print(f"  URL: {result.get('url', 'N/A')}")
            print(f"  Snippet: {result.get('snippet', 'N/A')[:100]}...")
            
            if detailed:
                if result.get('hostname'):
                    print(f"  Hostname: {result.get('hostname')}")
                if result.get('date'):
                    print(f"  Date: {result.get('date')}")
                if result.get('category'):
                    print(f"  Category: {result.get('category')}")
                if result.get('page_content'):
                    pc = result['page_content']
                    print(f"  Page Title: {pc.get('title', 'N/A')}")
                    print(f"  Page Description: {pc.get('description', 'N/A')[:80]}...")
                    print(f"  Images Found: {len(pc.get('images', []))}")
                    print(f"  Links Found: {len(pc.get('links', []))}")
            
            print("-" * 80)


def print_header():
    """Print a nice header for the UI"""
    print("\n" + "="*80)
    print(" " * 25 + "DuckDuckGo Web Scraper")
    print("="*80 + "\n")


def print_menu():
    """Print the main menu"""
    print("\n" + "-"*80)
    print(" MAIN MENU")
    print("-"*80)
    print("1. Text Search")
    print("2. Image Search")
    print("3. News Search")
    print("4. Video Search")
    print("5. Deep Scrape (Text + Page Content)")
    print("6. Exit")
    print("-"*80)


def get_input(prompt: str, default: str = None, input_type: type = str):
    """Get user input with optional default value"""
    if default:
        full_prompt = f"{prompt} (default: {default}): "
    else:
        full_prompt = f"{prompt}: "
    
    while True:
        try:
            user_input = input(full_prompt).strip()
            if not user_input and default:
                return default
            if not user_input:
                print("This field is required. Please enter a value.")
                continue
            return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            return None


def text_search_ui(scraper: DuckDuckGoScraper):
    """Interactive text search UI"""
    print("\n" + "="*80)
    print(" TEXT SEARCH")
    print("="*80)
    
    query = get_input("Enter your search query")
    if query is None:
        return
    
    max_results = get_input("Number of results", "10", int)
    if max_results is None:
        return
    
    region = get_input("Region (e.g., us-en, uk-en, de-de)", "us-en")
    if region is None:
        return
    
    deep_scrape = get_input("Scrape page content? (y/n)", "n")
    deep_scrape = deep_scrape and deep_scrape.lower() == 'y'
    
    print(f"\n🔍 Searching for '{query}'...")
    print("Please wait...\n")
    
    results = scraper.search(query, max_results=max_results, region=region)
    
    if deep_scrape and results:
        max_pages = get_input("How many pages to scrape? (1-10)", "3", int)
        if max_pages:
            print("\n📄 Scraping page content (this may take a while)...")
            results = scraper.enhance_results_with_page_content(results, max_pages=max_pages)
    
    scraper.print_results(results, detailed=deep_scrape)
    
    if results:
        save = get_input("\nSave results to file? (y/n)", "n")
        if save and save.lower() == 'y':
            filename = get_input("Enter filename", f"search_results_{int(time.time())}.json")
            if filename:
                scraper.save_results(results, filename)
    
    input("\nPress Enter to continue...")


def image_search_ui(scraper: DuckDuckGoScraper):
    """Interactive image search UI"""
    print("\n" + "="*80)
    print(" IMAGE SEARCH")
    print("="*80)
    
    query = get_input("Enter your image search query")
    if query is None:
        return
    
    max_results = get_input("Number of images", "10", int)
    if max_results is None:
        return
    
    print(f"\n🖼️  Searching for images of '{query}'...")
    print("Please wait (this may take a moment)...\n")
    
    image_results = scraper.search_images(query, max_results=max_results)
    
    if image_results:
        print(f"\n{'='*80}")
        print(f"Found {len(image_results)} images:")
        print(f"{'='*80}\n")
        
        for i, img in enumerate(image_results, 1):
            print(f"Image {i}:")
            print(f"  Title: {img.get('title', 'N/A')}")
            print(f"  Image URL: {img.get('url', 'N/A')}")
            if img.get('thumbnail'):
                print(f"  Thumbnail: {img.get('thumbnail', 'N/A')}")
            print(f"  Source: {img.get('source', 'N/A')}")
            print("-" * 80)
        
        save = get_input("\nSave results to file? (y/n)", "n")
        if save and save.lower() == 'y':
            filename = get_input("Enter filename", f"image_results_{int(time.time())}.json")
            if filename:
                scraper.save_results(image_results, filename)
    else:
        print("No images found or search failed.")
    
    input("\nPress Enter to continue...")


def news_search_ui(scraper: DuckDuckGoScraper):
    """Interactive news search UI"""
    print("\n" + "="*80)
    print(" NEWS SEARCH")
    print("="*80)
    
    query = get_input("Enter your news search query")
    if query is None:
        return
    
    max_results = get_input("Number of results", "10", int)
    if max_results is None:
        return
    
    region = get_input("Region (e.g., us-en, uk-en, de-de)", "us-en")
    if region is None:
        return
    
    print(f"\n📰 Searching for news about '{query}'...")
    print("Please wait...\n")
    
    results = scraper.search_news(query, max_results=max_results, region=region)
    
    if results:
        print(f"\n{'='*80}")
        print(f"Found {len(results)} news articles:")
        print(f"{'='*80}\n")
        
        for i, article in enumerate(results, 1):
            print(f"Article {i}:")
            print(f"  Title: {article.get('title', 'N/A')}")
            print(f"  URL: {article.get('url', 'N/A')}")
            print(f"  Snippet: {article.get('snippet', 'N/A')[:100]}...")
            if article.get('date'):
                print(f"  Date: {article.get('date')}")
            if article.get('source'):
                print(f"  Source: {article.get('source')}")
            if article.get('hostname'):
                print(f"  Hostname: {article.get('hostname')}")
            print("-" * 80)
        
        save = get_input("\nSave results to file? (y/n)", "n")
        if save and save.lower() == 'y':
            filename = get_input("Enter filename", f"news_results_{int(time.time())}.json")
            if filename:
                scraper.save_results(results, filename)
    else:
        print("No news articles found.")
    
    input("\nPress Enter to continue...")


def video_search_ui(scraper: DuckDuckGoScraper):
    """Interactive video search UI"""
    print("\n" + "="*80)
    print(" VIDEO SEARCH")
    print("="*80)
    
    query = get_input("Enter your video search query")
    if query is None:
        return
    
    max_results = get_input("Number of results", "10", int)
    if max_results is None:
        return
    
    region = get_input("Region (e.g., us-en, uk-en, de-de)", "us-en")
    if region is None:
        return
    
    print(f"\n🎥 Searching for videos about '{query}'...")
    print("Please wait...\n")
    
    results = scraper.search_videos(query, max_results=max_results, region=region)
    
    if results:
        print(f"\n{'='*80}")
        print(f"Found {len(results)} videos:")
        print(f"{'='*80}\n")
        
        for i, video in enumerate(results, 1):
            print(f"Video {i}:")
            print(f"  Title: {video.get('title', 'N/A')}")
            print(f"  URL: {video.get('url', 'N/A')}")
            print(f"  Description: {video.get('snippet', 'N/A')[:100]}...")
            if video.get('duration'):
                print(f"  Duration: {video.get('duration')}")
            if video.get('channel'):
                print(f"  Channel: {video.get('channel')}")
            if video.get('views'):
                print(f"  Views: {video.get('views')}")
            if video.get('published'):
                print(f"  Published: {video.get('published')}")
            if video.get('hostname'):
                print(f"  Hostname: {video.get('hostname')}")
            print("-" * 80)
        
        save = get_input("\nSave results to file? (y/n)", "n")
        if save and save.lower() == 'y':
            filename = get_input("Enter filename", f"video_results_{int(time.time())}.json")
            if filename:
                scraper.save_results(results, filename)
    else:
        print("No videos found.")
    
    input("\nPress Enter to continue...")


def deep_scrape_ui(scraper: DuckDuckGoScraper):
    """Interactive deep scraping UI"""
    print("\n" + "="*80)
    print(" DEEP SCRAPE (Text Search + Page Content)")
    print("="*80)
    
    query = get_input("Enter your search query")
    if query is None:
        return
    
    max_results = get_input("Number of search results", "5", int)
    if max_results is None:
        return
    
    max_pages = get_input("How many pages to scrape? (1-10)", "3", int)
    if max_pages is None:
        return
    
    region = get_input("Region (e.g., us-en, uk-en, de-de)", "us-en")
    if region is None:
        return
    
    print(f"\n🔍 Searching for '{query}'...")
    print("Please wait...\n")
    
    results = scraper.search(query, max_results=max_results, region=region)
    
    if results:
        print(f"\n📄 Scraping content from top {max_pages} pages (this may take a while)...")
        results = scraper.enhance_results_with_page_content(results, max_pages=max_pages)
        
        scraper.print_results(results, detailed=True)
        
        save = get_input("\nSave results to file? (y/n)", "n")
        if save and save.lower() == 'y':
            filename = get_input("Enter filename", f"deep_scrape_{int(time.time())}.json")
            if filename:
                scraper.save_results(results, filename)
    else:
        print("No results found to scrape.")
    
    input("\nPress Enter to continue...")


def main():
    """Main interactive UI"""
    print_header()
    
    try:
        print("Initializing scraper...")
        scraper = DuckDuckGoScraper()
        print("✓ Scraper ready!\n")
    except Exception as e:
        print(f"❌ Error initializing scraper: {e}")
        return
    
    while True:
        print_menu()
        choice = get_input("\nSelect an option (1-6)", "1", str)
        
        if choice is None:
            break
        
        if choice == "1":
            text_search_ui(scraper)
        elif choice == "2":
            image_search_ui(scraper)
        elif choice == "3":
            news_search_ui(scraper)
        elif choice == "4":
            video_search_ui(scraper)
        elif choice == "5":
            deep_scrape_ui(scraper)
        elif choice == "6":
            print("\n👋 Thank you for using DuckDuckGo Web Scraper!")
            print("Goodbye!\n")
            break
        else:
            print("\n❌ Invalid option. Please select 1-6.")
            time.sleep(1)


if __name__ == "__main__":
    main()



