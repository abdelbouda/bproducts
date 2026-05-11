#!/usr/bin/env python3
"""
BProducts Price Arbitrage Scraper
Scrapes product prices from multiple e-commerce platforms for arbitrage opportunities
"""

import json
import sys
import os
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spiders.bol_spider import BolSpider
from scraper.spiders.amazon_spider import AmazonSpider
from scraper.spiders.coolblue_spider import CoolblueSpider

# Target products for arbitrage analysis
TARGET_PRODUCTS = [
    {
        "id": "iphone-15-pro",
        "name": "Apple iPhone 15 Pro 128GB Natural Titanium",
        "keywords": ["iPhone 15 Pro", "128GB", "Natural Titanium"],
        "category": "electronics"
    },
    {
        "id": "airpods-pro-2",
        "name": "Apple AirPods Pro (2nd generation) with MagSafe Case",
        "keywords": ["AirPods Pro", "2nd generation", "MagSafe"],
        "category": "electronics"
    }
]

class PriceArbitrageAnalyzer:
    def __init__(self):
        self.results = {}
        
    def run_scrapers(self):
        """Run all scrapers for target products"""
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        
        # Run spiders for each platform
        process.crawl(BolSpider, products=TARGET_PRODUCTS)
        process.crawl(AmazonSpider, products=TARGET_PRODUCTS)
        process.crawl(CoolblueSpider, products=TARGET_PRODUCTS)
        
        process.start()
        
    def analyze_arbitrage(self):
        """Analyze scraped data for arbitrage opportunities"""
        # Load scraped data
        self.load_scraped_data()
        
        # Calculate arbitrage opportunities
        arbitrage_opportunities = []
        
        for product in TARGET_PRODUCTS:
            product_id = product["id"]
            if product_id in self.results:
                prices = self.results[product_id]
                if len(prices) > 1:
                    min_price = min(prices, key=lambda x: x['price'])
                    max_price = max(prices, key=lambda x: x['price'])
                    
                    if max_price['price'] - min_price['price'] > 50:  # Minimum €50 difference
                        arbitrage_opportunities.append({
                            "product": product,
                            "min_price": min_price,
                            "max_price": max_price,
                            "profit": max_price['price'] - min_price['price'],
                            "profit_percentage": ((max_price['price'] - min_price['price']) / min_price['price']) * 100
                        })
        
        return arbitrage_opportunities
    
    def load_scraped_data(self):
        """Load data from scraped JSON files"""
        for product in TARGET_PRODUCTS:
            self.results[product["id"]] = []
            
        # Load data from output files
        if os.path.exists('scraped_data.json'):
            with open('scraped_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    product_id = item.get('product_id')
                    if product_id in self.results:
                        self.results[product_id].append({
                            'platform': item.get('platform'),
                            'price': item.get('price'),
                            'url': item.get('url'),
                            'availability': item.get('availability'),
                            'timestamp': item.get('timestamp')
                        })
    
    def generate_report(self):
        """Generate arbitrage analysis report"""
        opportunities = self.analyze_arbitrage()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_opportunities": len(opportunities),
            "opportunities": opportunities,
            "summary": {
                "highest_profit": max([opp["profit"] for opp in opportunities]) if opportunities else 0,
                "average_profit": sum([opp["profit"] for opp in opportunities]) / len(opportunities) if opportunities else 0
            }
        }
        
        # Save report
        with open('arbitrage_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report

def main():
    print("🚀 Starting BProducts Price Arbitrage Scraper...")
    
    analyzer = PriceArbitrageAnalyzer()
    
    try:
        # Run scrapers
        print("📊 Scraping product prices...")
        analyzer.run_scrapers()
        
        # Generate report
        print("📈 Analyzing arbitrage opportunities...")
        report = analyzer.generate_report()
        
        print(f"✅ Found {report['total_opportunities']} arbitrage opportunities")
        print(f"💰 Highest potential profit: €{report['summary']['highest_profit']:.2f}")
        
        # Display top opportunities
        for i, opp in enumerate(report['opportunities'][:3], 1):
            print(f"\n{i}. {opp['product']['name']}")
            print(f"   Buy: {opp['min_price']['platform']} - €{opp['min_price']['price']:.2f}")
            print(f"   Sell: {opp['max_price']['platform']} - €{opp['max_price']['price']:.2f}")
            print(f"   Profit: €{opp['profit']:.2f} ({opp['profit_percentage']:.1f}%)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
