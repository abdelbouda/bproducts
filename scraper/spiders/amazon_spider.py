import scrapy
import json
from datetime import datetime
from urllib.parse import urljoin
from fake_useragent import UserAgent

class AmazonSpider(scrapy.Spider):
    name = 'amazon_spider'
    allowed_domains = ['amazon.nl', 'amazon.com']
    ua = UserAgent()
    
    def __init__(self, products=None, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.products = products or []
        
    def start_requests(self):
        """Generate initial search requests"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        for product in self.products:
            # Build search query
            search_query = ' '.join(product['keywords'])
            search_url = f"https://www.amazon.nl/s?k={search_query}"
            
            yield scrapy.Request(
                url=search_url,
                callback=self.parse_search_results,
                meta={'product': product},
                headers=headers
            )
    
    def parse_search_results(self, response):
        """Parse Amazon search results"""
        product = response.meta['product']
        
        # Extract product items from search results
        product_items = response.css('.s-result-item, [data-component-type="s-search-result"]')
        
        for item in product_items[:3]:  # Limit to top 3 results
            try:
                # Extract product details
                name = item.css('h2 a span::text, .a-size-medium::text').get()
                price_whole = item.css('.a-price-whole::text').get()
                price_fraction = item.css('.a-price-fraction::text').get()
                url = item.css('h2 a::attr(href)').get()
                
                if name and price_whole and url:
                    # Combine price components
                    price = self.clean_price(f"{price_whole}.{price_fraction}" if price_fraction else price_whole)
                    
                    # Check availability
                    availability = item.css('.a-color-success::text, .a-color-price::text').get() or 'Available'
                    
                    # Build full URL
                    full_url = urljoin('https://www.amazon.nl', url)
                    
                    yield {
                        'product_id': product['id'],
                        'product_name': name.strip(),
                        'platform': 'Amazon',
                        'price': price,
                        'url': full_url,
                        'availability': availability.strip(),
                        'timestamp': datetime.now().isoformat(),
                        'keywords': product['keywords']
                    }
                    
            except Exception as e:
                self.logger.error(f"Error parsing Amazon item: {e}")
                continue
    
    def clean_price(self, price_text):
        """Clean and convert price text to float"""
        if not price_text:
            return 0.0
        
        # Remove currency symbols and whitespace
        cleaned = price_text.replace('€', '').replace('$', '').replace(',', '.').strip()
        
        try:
            # Extract numeric value
            import re
            match = re.search(r'\d+\.?\d*', cleaned)
            if match:
                return float(match.group())
        except ValueError:
            pass
        
        return 0.0
