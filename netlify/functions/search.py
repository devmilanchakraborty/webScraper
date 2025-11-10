"""
Netlify Serverless Function for DuckDuckGo Search
"""

import json
import sys
import os

# Add parent directory to path to import scrape module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from scrape import DuckDuckGoScraper

scraper = None

def get_scraper():
    """Get or create scraper instance"""
    global scraper
    if scraper is None:
        scraper = DuckDuckGoScraper()
    return scraper

def handler(event, context):
    """Netlify function handler"""
    try:
        # Handle CORS preflight
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': ''
            }
        
        # Parse request body
        body_str = event.get('body', '{}')
        if isinstance(body_str, str):
            body = json.loads(body_str)
        else:
            body = body_str if body_str else {}
        search_type = body.get('type', 'text')
        query = body.get('query', '')
        max_results = int(body.get('max_results', 10))
        region = body.get('region', 'us-en')
        deep_scrape = body.get('deep_scrape', False)
        max_pages = int(body.get('max_pages', 3)) if deep_scrape else 0
        
        if not query:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Query is required'})
            }
        
        scraper = get_scraper()
        results = []
        
        if search_type == 'text':
            results = scraper.search(query, max_results=max_results, region=region)
            if deep_scrape and results:
                results = scraper.enhance_results_with_page_content(results, max_pages=max_pages)
        elif search_type == 'images':
            results = scraper.search_images(query, max_results=max_results)
        elif search_type == 'news':
            results = scraper.search_news(query, max_results=max_results, region=region)
        elif search_type == 'videos':
            results = scraper.search_videos(query, max_results=max_results, region=region)
        else:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Invalid search type'})
            }
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': True,
                'results': results,
                'count': len(results)
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }

