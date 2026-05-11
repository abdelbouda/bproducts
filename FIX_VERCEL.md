# 🔧 Vercel Config Fix

## Probleem
Vercel kan de serverless function niet vinden met de huidige `vercel.json` configuratie.

## Oplossing

### Stap 1: Update vercel.json in GitHub
Ga naar https://github.com/abdelbouda/bproducts en open `vercel.json`. 
Vervang de inhoud met:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.js",
      "use": "@vercel/node"
    },
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.js"
    },
    {
      "src": "/(.*)",
      "dest": "/dist/$1"
    }
  ],
  "env": {
    "NODE_ENV": "production"
  }
}
```

### Stap 2: Upload nieuwe api/index.js
Ik heb `api/index.js` aangemaakt met de juiste Vercel structuur. 
Upload dit bestand naar GitHub (naast de bestaande `api/server.js`).

### Stap 3: Deploy opnieuw in Vercel
1. Ga naar https://vercel.com/new
2. Importeer `abdelbouda/bproducts`
3. Settings:
   - Framework: `Other`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Deploy

## Waarom dit werkt
- `api/index.js` is de standaard naam die Vercel verwacht
- `builds` configuratie is explicieter voor Vercel
- Routes sturen API requests correct naar de function

**🎉 Dit zou de deployment fout moeten oplossen!**
