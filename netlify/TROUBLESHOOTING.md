# Troubleshooting "No Results Found"

## Check Function Logs

1. Go to Netlify Dashboard → Your Site → Functions
2. Click on the function → View logs
3. Look for error messages

## Common Issues

### 1. Import Error
**Symptom**: Function fails to import `scrape` module
**Fix**: Make sure `scrape.py` is in `netlify/functions/` folder

### 2. Timeout
**Symptom**: Function times out (10 seconds on free tier)
**Fix**: 
- Reduce `max_results` (try 5 instead of 10)
- Don't use deep scraping on Netlify
- Try simpler queries first

### 3. Rate Limiting
**Symptom**: DuckDuckGo blocks requests
**Fix**: 
- Wait a few minutes between searches
- The function has retry logic built in

### 4. Empty Results
**Symptom**: Function runs but returns empty array
**Fix**:
- Check if DuckDuckGo is accessible from Netlify's servers
- Try a very simple query like "test"
- Check function logs for errors

## Test the Function Directly

You can test the function endpoint directly:

```bash
curl -X POST https://YOUR_SITE.netlify.app/.netlify/functions/search \
  -H "Content-Type: application/json" \
  -d '{"type":"text","query":"test","max_results":5}'
```

## Check Browser Console

1. Open your site
2. Press F12 (Developer Tools)
3. Go to Console tab
4. Try a search
5. Look for error messages

## Quick Fixes

1. **Redeploy**: Sometimes a fresh deploy fixes issues
2. **Check requirements.txt**: Make sure all dependencies are listed
3. **Check netlify.toml**: Verify publish directory is `netlify/public`

