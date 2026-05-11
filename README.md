# BProducts - Price Arbitrage Finder

A no-budget stack for finding price arbitrage opportunities across major e-commerce platforms. Real-time price comparison and analysis for maximum savings.

## 🚀 Features

- **Arbitrage Analysis**: Identifies profitable price differences between platforms
- **Live Dashboard**: Modern web interface with real-time updates
- **API Endpoints**: RESTful API for data access
- **Auto-refresh**: Automatic data updates every 5 minutes
- **No-budget Deployment**: Built with free/open-source technologies

## 🛠 Tech Stack

- **Frontend**: Astro + React + TailwindCSS
- **Backend**: Node.js + Express
- **Scraping**: Python + Scrapy + BeautifulSoup
- **Deployment**: Vercel (free tier) or any Node.js hosting

## 📦 Installation

### Prerequisites
- Node.js 20+
- Python 3.8+
- npm or yarn

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd bproducts
```

2. **Install frontend dependencies**
```bash
npm install
```

3. **Install Python dependencies**
```bash
cd scraper
pip install -r requirements.txt
```

## 🚀 Quick Start

### Development Mode

1. **Start the frontend**
```bash
npm run dev
```

2. **Start the API server** (in another terminal)
```bash
npm run serve-api
```

3. **Run the scraper** (optional, for fresh data)
```bash
npm run scrape
```

Visit `http://localhost:4321` to see the application.

### Production Mode

1. **Build the frontend**
```bash
npm run build
```

2. **Start the production server**
```bash
npm run preview
```

## 📊 API Endpoints

- `GET /api/arbitrage-data` - Get latest arbitrage opportunities
- `GET /api/refresh` - Force refresh of scraped data
- `GET /api/products` - Get list of tracked products
- `GET /api/health` - Health check endpoint

## 🕷️ Scraper Configuration

### Target Products

The scraper currently tracks:
- iPhone 15 Pro 128GB Natural Titanium
- AirPods Pro 2nd Generation with MagSafe

### Adding New Products

Edit `scraper/main.py` and add to `TARGET_PRODUCTS` array:

```python
{
    "id": "product-identifier",
    "name": "Product Name",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "category": "electronics"
}
```

### Platform Support

Currently supports:
- **Bol.com** - Dutch marketplace
- **Amazon NL** - Amazon Netherlands
- **Coolblue** - Dutch electronics retailer

## 🔧 Configuration

### Environment Variables

Create `.env` file in root:

```env
NODE_ENV=development
PORT=3001
```

### Scraper Settings

Edit `scraper/settings.py` to configure:
- Request delays
- Concurrent requests
- User agents
- Proxy settings

## 🚀 Deployment

### Vercel (Recommended)

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy**
```bash
vercel
```

3. **Configure serverless function**
The API will automatically deploy as serverless functions.

### Alternative Deployment

Any Node.js hosting service works:
- Railway
- Render
- DigitalOcean App Platform
- Heroku

## 📈 Monitoring

### Data Freshness

- Scraped data is cached for 5 minutes
- Auto-refresh runs every 5 minutes
- Manual refresh available via API

### Error Handling

- Fallback to mock data if scraping fails
- Timeout protection for scrapers
- Graceful degradation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Adding New Platforms

1. Create new spider in `scraper/spiders/`
2. Follow existing pattern
3. Add to main.py execution
4. Test with target products

## 📝 License

MIT License - feel free to use this project for commercial purposes.

## 🆘 Troubleshooting

### Common Issues

**Scraper fails with 403 errors**
- Add delay between requests
- Use rotating proxies
- Update user agents

**API returns mock data**
- Check scraper dependencies
- Verify Python installation
- Check logs for errors

**Build fails**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be 20+)

### Debug Mode

Enable debug logging:
```bash
DEBUG=* npm run serve-api
```

## 📞 Support

For issues and questions:
- Create GitHub issue
- Check existing documentation
- Review error logs

---

**Built with ❤️ for the arbitrage community**
