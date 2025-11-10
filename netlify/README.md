# Netlify Deployment

Your scraper is ready to deploy to Netlify! 🚀

## Quick Deploy

### Option 1: Netlify CLI

```bash
# Install Netlify CLI (if needed)
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd "/Users/dev/Documents/Vs Code/wab scraper"
netlify deploy --prod
```

### Option 2: Netlify Dashboard

1. Go to [app.netlify.com](https://app.netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect your Git repository
4. Set build settings:
   - **Publish directory**: `netlify/public`
   - **Build command**: (leave empty)
5. Deploy!

## File Structure

```
netlify/
├── functions/
│   ├── search.py          # Serverless function
│   ├── scrape.py          # Scraper module
│   └── requirements.txt   # Dependencies
├── public/
│   └── index.html         # Frontend
└── netlify.toml           # Config
```

## Important Notes

⚠️ **Limitations:**
- Free tier: 10-second function timeout
- Pro tier: 26-second timeout
- Deep scraping may timeout with many pages

💡 **Tips:**
- Keep `max_pages` low (1-3) for deep scraping
- Functions are stateless (scraper recreated each request)
- CORS is already handled

## Testing Locally

```bash
netlify dev
```

This runs the site locally with function support.

