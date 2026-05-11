# ⚡ Quick Deploy Guide - BProducts

## 🚀 Snelste Manier (5 minuten)

### Stap 1: GitHub Repository (2 min)
1. Ga naar https://github.com/new
2. Repository naam: `bproducts`
3. Owner: `abdelbouda`
4. **NIET** README aanvinken
5. Click "Create repository"

### Stap 2: Upload Bestanden (2 min)
1. In de nieuwe repository, click "uploading an existing file"
2. Sleep alle bestanden uit `C:\Users\Laptop\CascadeProjects\bproducts` naar de browser
3. Of upload de folder als ZIP:
   - Selecteer alles in `bproducts` folder
   - Right-click → Send to → Compressed (zipped) folder
   - Upload de ZIP file

### Stap 3: Vercel Deploy (1 min)
1. Ga naar https://vercel.com/new
2. Importeer GitHub repository: `abdelbouda/bproducts`
3. Settings:
   - Framework Preset: `Other`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`
4. Click "Deploy"

## 🎯 Resultaat
- **Live URL**: `https://bproducts.vercel.app`
- **API**: `https://bproducts.vercel.app/api/arbitrage-data`

## 📁 Benodigde Bestanden
Alle bestanden zijn al klaar in `C:\Users\Laptop\CascadeProjects\bproducts`:

```
bproducts/
├── src/
│   ├── pages/index.astro
│   ├── layouts/Layout.astro
│   └── styles/global.css
├── api/server.js
├── scraper/ (Python scraping code)
├── package.json
├── astro.config.mjs
├── tailwind.config.js
├── vercel.json
├── .gitignore
└── README.md
```

## 🔥 Alternative: Direct Vercel Deploy
Als je GitHub niet wilt gebruiken:

1. Ga naar https://vercel.com/new
2. Kies "Other" als import methode
3. Upload de `bproducts` folder
4. Gebruik zelfde settings hierboven

## ⚠️ Belangrijk
- Gebruik **exact** deze settings voor Vercel
- Het project is production-ready met mock data
- API endpoints werken out-of-the-box

**🎉 Binnen 5 minuten live!**
