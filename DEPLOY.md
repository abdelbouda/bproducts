# 🚀 Deployment Guide - BProducts

## GitHub Setup

### 1. Maak GitHub Repository
1. Ga naar https://github.com/new
2. Repository naam: `bproducts`
3. Owner: `abdelbouda`
4. Public/Private (naar keuze)
5. **NIET** "Initialize with README" aanvinken (we hebben al bestanden)
6. Klik op "Create repository"

### 2. Git Commands (uitvoeren in bproducts folder)
```bash
# Navigeer naar project folder
cd C:\Users\Laptop\CascadeProjects\bproducts

# Git initialiseren
git init
git add .
git commit -m "Initial commit - BProducts price arbitrage platform"

# Remote toevoegen
git remote add origin https://github.com/abdelbouda/bproducts.git
git branch -M main

# Push naar GitHub
git push -u origin main
```

## Vercel Deployment

### Optie 1: Via Vercel CLI (aanbevolen)
```bash
# Installeer Vercel CLI
npm i -g vercel

# Login naar Vercel
vercel login

# Deploy vanuit project folder
cd C:\Users\Laptop\CascadeProjects\bproducts
vercel

# Volg de prompts:
# - Link naar bestaand project? Nee
# - Project naam: bproducts
# - Directory: .
# - Instellingen bevestigen
```

### Optie 2: Via Vercel Dashboard
1. Ga naar https://vercel.com/new
2. Importeer GitHub repository: `abdelbouda/bproducts`
3. Framework Preset: `Other`
4. Build Command: `npm run build`
5. Output Directory: `dist`
6. Install Command: `npm install`
7. Klik op "Deploy"

## 🎯 Expected URLs na Deployment

- **Frontend**: `https://bproducts.vercel.app`
- **API**: `https://bproducts.vercel.app/api/arbitrage-data`
- **Health Check**: `https://bproducts.vercel.app/api/health`

## 🔧 Post-Deployment Checks

### 1. API Endpoint Test
```bash
curl https://bproducts.vercel.app/api/health
# Expected: {"status":"ok","timestamp":"...","environment":"production"}
```

### 2. Frontend Test
- Open `https://bproducts.vercel.app` in browser
- Check of live stats verschijnen
- Test refresh button
- Check responsive design

### 3. Data Refresh Test
```bash
curl https://bproducts.vercel.app/api/refresh
# Expected: {"success":true,"message":"Data refreshed successfully"}
```

## 🐛 Troubleshooting

### Git Issues
**"git is not recognized"**
- Installeer Git: https://git-scm.com/download/win
- Restart PowerShell/Command Prompt

**"Permission denied"**
- Check GitHub credentials
- Gebruik SSH key: `ssh-keygen -t ed25519 -C "your-email@example.com"`

### Vercel Issues
**Build fails**
- Check `package.json` scripts
- Verify Node.js version (20+)
- Check Vercel logs in dashboard

**API returns 404**
- Verify `vercel.json` routing
- Check file structure matches expectations

**Scraper fails in production**
- Python dependencies niet beschikbaar op Vercel
- Gebruik mock data fallback (geconfigureerd)

## 📊 Monitoring

### Vercel Analytics
- Ga naar Vercel dashboard
- Check page views, API calls
- Monitor error rates

### GitHub Actions (optioneel)
Voeg `.github/workflows/deploy.yml` toe voor automated testing.

## 🔄 Updates

### Code Changes Pushen
```bash
git add .
git commit -m "Update: description"
git push origin main
# Vercel auto-deploy
```

### Environment Variables
- Ga naar Vercel dashboard
- Project settings → Environment Variables
- Voeg toe: `NODE_ENV=production`

---

**🎉 Gefeliciteerd! Je BProducts platform is nu live!**
