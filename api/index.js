const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from the build directory
app.use(express.static(path.join(__dirname, '../dist')));

// Mock data for development
const mockData = {
  timestamp: new Date().toISOString(),
  total_opportunities: 2,
  opportunities: [
    {
      product: {
        id: "iphone-15-pro",
        name: "Apple iPhone 15 Pro 128GB Natural Titanium",
        category: "electronics"
      },
      min_price: {
        platform: "Bol.com",
        price: 1099.00,
        url: "https://bol.com/iphone-15-pro",
        availability: "In stock"
      },
      max_price: {
        platform: "Coolblue",
        price: 1199.00,
        url: "https://coolblue.nl/iphone-15-pro",
        availability: "In stock"
      },
      profit: 100.00,
      profit_percentage: 9.1
    },
    {
      product: {
        id: "airpods-pro-2",
        name: "Apple AirPods Pro (2nd generation) with MagSafe Case",
        category: "electronics"
      },
      min_price: {
        platform: "Amazon",
        price: 249.00,
        url: "https://amazon.nl/airpods-pro-2",
        availability: "In stock"
      },
      max_price: {
        platform: "Coolblue",
        price: 299.00,
        url: "https://coolblue.nl/airpods-pro-2",
        availability: "In stock"
      },
      profit: 50.00,
      profit_percentage: 20.1
    }
  ],
  summary: {
    highest_profit: 100.00,
    average_profit: 75.00
  }
};

// API Routes
app.get('/api/arbitrage-data', async (req, res) => {
  try {
    // Check if we have recent scraped data
    const dataPath = path.join(__dirname, '../arbitrage_report.json');
    
    if (fs.existsSync(dataPath)) {
      const stats = fs.statSync(dataPath);
      const fileAge = Date.now() - stats.mtime.getTime();
      
      // If file is less than 5 minutes old, use it
      if (fileAge < 5 * 60 * 1000) {
        const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
        return res.json(data);
      }
    }
    
    // Otherwise, try to scrape new data (in production)
    if (process.env.NODE_ENV === 'production') {
      try {
        await runScraper();
        if (fs.existsSync(dataPath)) {
          const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
          return res.json(data);
        }
      } catch (error) {
        console.error('Scraper failed:', error);
      }
    }
    
    // Fallback to mock data
    res.json(mockData);
    
  } catch (error) {
    console.error('Error fetching arbitrage data:', error);
    res.status(500).json({ error: 'Failed to fetch arbitrage data' });
  }
});

// Product details endpoint
app.get('/api/product-details/:productId', async (req, res) => {
  try {
    const { productId } = req.params;
    
    // Find product in opportunities
    const product = mockData.opportunities.find(p => p.product.id === productId);
    
    if (!product) {
      return res.status(404).json({ error: 'Product not found' });
    }
    
    // Enhanced product details with price analysis
    const productDetails = {
      ...product,
      price_analysis: {
        cheapest: product.min_price,
        most_expensive: product.max_price,
        average_price: ((product.min_price.price + product.max_price.price) / 2).toFixed(2),
        price_difference: product.profit,
        price_difference_percentage: product.profit_percentage,
        savings_opportunity: product.profit
      },
      platforms: [
        {
          name: product.min_price.platform,
          price: product.min_price.price,
          url: product.min_price.url,
          availability: product.min_price.availability,
          type: 'cheapest'
        },
        {
          name: product.max_price.platform,
          price: product.max_price.price,
          url: product.max_price.url,
          availability: product.max_price.availability,
          type: 'most_expensive'
        }
      ],
      last_updated: new Date().toISOString(),
      currency: 'EUR'
    };
    
    res.json(productDetails);
    
  } catch (error) {
    console.error('Error fetching product details:', error);
    res.status(500).json({ error: 'Failed to fetch product details' });
  }
});

app.get('/api/refresh', async (req, res) => {
  try {
    await runScraper();
    const dataPath = path.join(__dirname, '../arbitrage_report.json');
    
    if (fs.existsSync(dataPath)) {
      const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
      res.json({ 
        success: true, 
        message: 'Data refreshed successfully',
        data 
      });
    } else {
      res.status(404).json({ 
        success: false, 
        message: 'No data available after refresh' 
      });
    }
  } catch (error) {
    console.error('Error refreshing data:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Failed to refresh data' 
    });
  }
});

app.get('/api/products', (req, res) => {
  res.json([
    {
      id: "iphone-15-pro",
      name: "Apple iPhone 15 Pro 128GB Natural Titanium",
      category: "electronics",
      keywords: ["iPhone 15 Pro", "128GB", "Natural Titanium"]
    },
    {
      id: "airpods-pro-2",
      name: "Apple AirPods Pro (2nd generation) with MagSafe Case",
      category: "electronics",
      keywords: ["AirPods Pro", "2nd generation", "MagSafe"]
    }
  ]);
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV || 'development'
  });
});

// Function to run the Python scraper
function runScraper() {
  return new Promise((resolve, reject) => {
    const scraperPath = path.join(__dirname, '../scraper');
    
    // Check if Python is available and scraper exists
    if (!fs.existsSync(path.join(scraperPath, 'main.py'))) {
      return reject(new Error('Scraper not found'));
    }
    
    const python = spawn('python', ['main.py'], {
      cwd: scraperPath,
      stdio: 'pipe'
    });
    
    let output = '';
    let errorOutput = '';
    
    python.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    python.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });
    
    python.on('close', (code) => {
      if (code === 0) {
        console.log('Scraper completed successfully');
        resolve(output);
      } else {
        console.error('Scraper failed with code:', code);
        console.error('Error output:', errorOutput);
        reject(new Error(`Scraper failed with code ${code}: ${errorOutput}`));
      }
    });
    
    python.on('error', (error) => {
      console.error('Failed to start scraper:', error);
      reject(error);
    });
    
    // Timeout after 2 minutes
    setTimeout(() => {
      python.kill();
      reject(new Error('Scraper timeout'));
    }, 120000);
  });
}

// Serve the frontend for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../dist/index.html'));
});

// Start server
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`🚀 BProducts API Server running on port ${PORT}`);
    console.log(`📊 API available at http://localhost:${PORT}/api`);
    console.log(`🌐 Frontend available at http://localhost:${PORT}`);
  });
}

module.exports = app;
