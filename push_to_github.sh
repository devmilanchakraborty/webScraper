#!/bin/bash

# Script to push to GitHub
# Replace YOUR_USERNAME and REPO_NAME with your actual values

echo "🚀 Pushing to GitHub..."
echo ""
echo "Make sure you've:"
echo "1. Created a repo on GitHub.com"
echo "2. Copied the repository URL"
echo ""

# Get repository URL from user
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ No URL provided. Exiting."
    exit 1
fi

# Check if remote already exists
if git remote get-url origin &>/dev/null; then
    echo "⚠️  Remote 'origin' already exists. Removing it..."
    git remote remove origin
fi

# Add remote
echo "📡 Adding remote repository..."
git remote add origin "$REPO_URL"

# Rename branch to main if needed
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    echo "🔄 Renaming branch to 'main'..."
    git branch -M main
fi

# Push
echo "⬆️  Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Your code is now on GitHub!"
    echo "🌐 View it at: ${REPO_URL%.git}"
else
    echo ""
    echo "❌ Push failed. You may need to authenticate."
    echo "💡 Try:"
    echo "   1. Use a Personal Access Token (GitHub → Settings → Developer settings)"
    echo "   2. Or install GitHub CLI: brew install gh && gh auth login"
fi

