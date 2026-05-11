import scrapy
import json
from datetime import datetime
from urllib.parse import urljoin

class CoolblueSpider(scrapy.Spider):
    name = 'coolblue_spider'
    allowed_domains = ['coolblue.nl']
    start_urls = ['https://www.coolblue.nl']
    
    def __init__(self, products=None, *args, **kwargs):
        super(CoolblueSpider, self).__init__(*args, **kwargs)
        self.products = products or []
        
    def parse(self, response):
        """Parse initial page and search for products"""
        for product in self.products:
            # Build search query
            search_query = ' '.join(product['keywords'])
            search_url = f"https://www.coolblue.nl/search?query={search_query}"
            
            yield scrapy.Request(
                url=search_url,
                callback=self.parse_search_results,
                meta={'product': product}
            )
    
    def parse_search_results(self, response):
        """Parse Coolblue search results"""
        product = response.meta['product']
        
        # Extract product items from search results
        product_items = response.css('.product-card, .js-product-card')
        
        for item in product_items[:3]:  # Limit to top 3 results
            try:
                # Extract product details
                name = item.css('.product-card__title::text, h3 a::text').get()
                price_text = item.css('.sales-price__current::text, .price::text').get()
                url = item.css('a::attr(href)').get()
                
                if name and price_text and url:
                    # Clean price
                    price = self.clean_price(price_text)
                    
                    # Check availability
                    availability = item.css('.stock-indicator__text::text').get() or 'Available'
                    
                    # Build full URL
                    full_url = urljoin('https://www.coolblue.nl', url)
                    
                    yield {
                        'product_id': product['id'],
                        'product_name': name.strip(),
                        'platform': 'Coolblue',
                        'price': price,
                        'url': full_url,
                        'availability': availability.strip(),
                        'timestamp': datetime.now().isoformat(),
                        'keywords': product['keywords']
                    }
                    
            except Exception as e:
                self.logger.error(f"Error parsing Coolblue item: {e}")
                continue
    
    def clean_price(self, price_text):
        """Clean and convert price text to float"""
        if not price_text:
            return 0.0
        
        # Remove currency symbols and whitespace
        cleaned = price_text.replace('€', '').replace(',', '.').strip()
        
        try:
            # Extract numeric value
            import re
            match = re.search(r'\d+\.?\d*', cleaned)
            if match:
                return float(match.group())
        except ValueError:
            pass
        
        return 0.0
