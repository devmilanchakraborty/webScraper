"""
Flask Web Application for DuckDuckGo Scraper
A modern web UI for the scraper with image viewing capabilities
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from scrape import DuckDuckGoScraper
import json
import os
import time
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/results'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize scraper
scraper = None

def get_scraper():
    """Get or create scraper instance"""
    global scraper
    if scraper is None:
        scraper = DuckDuckGoScraper()
    return scraper

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def api_search():
    """Text search API endpoint"""
    try:
        data = request.json
        query = data.get('query', '')
        max_results = int(data.get('max_results', 10))
        region = data.get('region', 'us-en')
        deep_scrape = data.get('deep_scrape', False)
        max_pages = int(data.get('max_pages', 3)) if deep_scrape else 0
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        scraper = get_scraper()
        results = scraper.search(query, max_results=max_results, region=region)
        
        if deep_scrape and results:
            results = scraper.enhance_results_with_page_content(results, max_pages=max_pages)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/images', methods=['POST'])
def api_search_images():
    """Image search API endpoint"""
    try:
        data = request.json
        query = data.get('query', '')
        max_results = int(data.get('max_results', 10))
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        scraper = get_scraper()
        results = scraper.search_images(query, max_results=max_results)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/news', methods=['POST'])
def api_search_news():
    """News search API endpoint"""
    try:
        data = request.json
        query = data.get('query', '')
        max_results = int(data.get('max_results', 10))
        region = data.get('region', 'us-en')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        scraper = get_scraper()
        results = scraper.search_news(query, max_results=max_results, region=region)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search/videos', methods=['POST'])
def api_search_videos():
    """Video search API endpoint"""
    try:
        data = request.json
        query = data.get('query', '')
        max_results = int(data.get('max_results', 10))
        region = data.get('region', 'us-en')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        scraper = get_scraper()
        results = scraper.search_videos(query, max_results=max_results, region=region)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save', methods=['POST'])
def api_save():
    """Save results to file"""
    try:
        data = request.json
        results = data.get('results', [])
        filename = data.get('filename', f'results_{int(time.time())}.json')
        
        if not results:
            return jsonify({'error': 'No results to save'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting DuckDuckGo Scraper Web UI...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

