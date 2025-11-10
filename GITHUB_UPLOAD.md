# Upload to GitHub - Step by Step

## Step 1: Create Repository on GitHub

1. Go to [github.com](https://github.com) and **sign in** (or create account)
2. Click the **"+"** icon in top right → **"New repository"**
3. Fill in:
   - **Repository name**: `duckduckgo-scraper` (or any name you want)
   - **Description**: "DuckDuckGo Web Scraper with UI"
   - **Visibility**: Choose Public or Private
   - **DO NOT** check "Initialize with README" (we already have files)
4. Click **"Create repository"**

## Step 2: Copy the Repository URL

After creating, GitHub will show you a page with commands. You'll see a URL like:
- `https://github.com/YOUR_USERNAME/duckduckgo-scraper.git`

**Copy this URL!** You'll need it in the next step.

## Step 3: Push Your Code

Run these commands in your terminal:

```bash
cd "/Users/dev/Documents/Vs Code/wab scraper"

# Check if git is initialized
git status

# If not initialized, run:
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - DuckDuckGo Scraper"

# Add your GitHub repo (replace with YOUR actual URL)
git remote add origin https://github.com/YOUR_USERNAME/duckduckgo-scraper.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Authentication

When you run `git push`, GitHub will ask for authentication:

**Option A: Personal Access Token (Recommended)**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name, select `repo` scope
4. Copy the token
5. When prompted for password, paste the token (not your password)

**Option B: GitHub CLI**
```bash
# Install GitHub CLI (if you want)
brew install gh
gh auth login
```

## Troubleshooting

**"Repository not found" error:**
- Check the URL is correct
- Make sure you created the repo on GitHub first
- Check your username is correct

**"Permission denied" error:**
- You need to authenticate (see Step 4)
- Use a Personal Access Token

**"Already exists" error:**
```bash
git remote remove origin
git remote add origin YOUR_NEW_URL
```

## Quick Check

After pushing, refresh your GitHub repo page. You should see all your files!

