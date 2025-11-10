# Netlify Function Setup Check

## The Error "Unexpected token '<'"

This means Netlify is returning HTML (404 page) instead of JSON. The function isn't being found.

## Check These:

### 1. Function Location
Make sure your function is at:
```
netlify/functions/search.py
```

### 2. Netlify Dashboard Check
1. Go to Netlify Dashboard → Your Site
2. Click **"Functions"** tab
3. You should see `search` listed
4. If not, the function isn't being detected

### 3. Function Logs
1. Go to Functions → `search`
2. Click "View logs"
3. Try a search
4. Check for errors

### 4. Common Issues

**Issue**: Python functions not supported
- Netlify DOES support Python, but you need Python 3.11 runtime
- Check `netlify.toml` has `PYTHON_VERSION = "3.11"`

**Issue**: Function not detected
- Make sure `functions = "netlify/functions"` in `netlify.toml`
- Function file must be named correctly: `search.py`

**Issue**: Import errors
- Make sure `scrape.py` is in `netlify/functions/` folder
- Make sure `requirements.txt` is in `netlify/functions/` folder

## Test the Function Directly

Visit: `https://YOUR_SITE.netlify.app/.netlify/functions/search`

You should see an error (because it needs POST), but NOT a 404 page.

If you see 404, the function isn't deployed.

## Redeploy

1. Push your latest changes
2. Go to Netlify → Deploys
3. Click "Trigger deploy" → "Clear cache and deploy site"

