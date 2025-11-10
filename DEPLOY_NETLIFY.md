# Deploy to Netlify (No npm needed!)

## Method 1: Netlify Web Dashboard (Easiest - No CLI needed!)

### Step 1: Prepare Your Files
Make sure your `netlify/` folder is ready with:
- `netlify/functions/search.py`
- `netlify/functions/scrape.py`
- `netlify/functions/requirements.txt`
- `netlify/public/index.html`
- `netlify.toml`

### Step 2: Create a Git Repository (if you haven't)
```bash
cd "/Users/dev/Documents/Vs Code/wab scraper"
git init
git add .
git commit -m "Initial commit"
```

### Step 3: Push to GitHub/GitLab/Bitbucket
1. Create a new repository on GitHub (github.com)
2. Push your code:
```bash
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 4: Deploy on Netlify
1. Go to [app.netlify.com](https://app.netlify.com)
2. Sign up/Login (free account)
3. Click **"Add new site"** → **"Import an existing project"**
4. Connect to **GitHub** (or GitLab/Bitbucket)
5. Select your repository
6. Configure build settings:
   - **Base directory**: Leave empty
   - **Build command**: Leave empty
   - **Publish directory**: `netlify/public`
7. Click **"Deploy site"**

That's it! Your site will be live in a few minutes.

---

## Method 2: Manual Drag & Drop (No Git needed!)

1. Go to [app.netlify.com](https://app.netlify.com)
2. Sign up/Login
3. Click **"Add new site"** → **"Deploy manually"**
4. Drag and drop your `netlify/public` folder
5. **BUT** - This won't work for functions! You need Git for serverless functions.

---

## Method 3: Install npm (Optional - for CLI)

If you want to use the CLI later:

**On macOS:**
```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Then install Node.js (which includes npm)
brew install node
```

But you don't need it! The web dashboard works perfectly.

---

## Quick Summary

✅ **Easiest way**: Use Netlify web dashboard with GitHub
✅ **No npm needed** for web dashboard
✅ **Functions require Git** (GitHub/GitLab/Bitbucket)
❌ **Manual drag & drop won't work** for serverless functions

Your site will get a URL like: `https://your-site-name.netlify.app`

