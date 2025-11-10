# Deploying to Netlify

## Quick Start

1. **Install Netlify CLI** (if not already installed):
   ```bash
   npm install -g netlify-cli
   ```

2. **Login to Netlify**:
   ```bash
   netlify login
   ```

3. **Deploy**:
   ```bash
   cd "/Users/dev/Documents/Vs Code/wab scraper"
   netlify deploy --prod
   ```

## Manual Deployment via Netlify Dashboard

1. Go to [netlify.com](https://netlify.com) and sign in
2. Click "Add new site" → "Import an existing project"
3. Connect your Git repository (GitHub/GitLab/Bitbucket)
4. Configure build settings:
   - **Base directory**: Leave empty or set to root
   - **Build command**: Leave empty (no build needed)
   - **Publish directory**: `netlify/public`
5. Click "Deploy site"

## Important Notes

⚠️ **Netlify Functions Limitations:**
- Functions have a 10-second timeout on free tier (26 seconds on Pro)
- Deep scraping may timeout if scraping many pages
- Functions are stateless - scraper instance is recreated on each request

## File Structure

```
netlify/
├── functions/
│   ├── search.py          # Netlify serverless function
│   ├── scrape.py          # Scraper module (copied)
│   └── requirements.txt   # Python dependencies
├── public/
│   └── index.html         # Frontend UI
└── netlify.toml           # Netlify configuration
```

## Environment Variables

No environment variables needed for basic functionality.

## Troubleshooting

- **Function timeout**: Reduce `max_pages` for deep scraping
- **Import errors**: Ensure `scrape.py` is in `netlify/functions/`
- **CORS issues**: Already handled in the function code

## Alternative: Use Netlify Dev Locally

```bash
netlify dev
```

This runs the site locally with Netlify Functions support.

