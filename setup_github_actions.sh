#!/bin/bash
# Setup script for GitHub Actions - Linux/Mac

echo "=========================================="
echo "GitHub Actions Setup Script"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "✅ Git is installed"

# Check if already a git repository
if [ -d ".git" ]; then
    echo "✅ Git repository already initialized"
else
    echo "Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
fi

# Check for GitHub remote
if git remote | grep -q "origin"; then
    echo "✅ Remote 'origin' already configured"
    git remote -v
else
    echo ""
    echo "No remote repository configured."
    echo "Please enter your GitHub repository URL:"
    echo "Example: https://github.com/username/public-health-data-dashboard.git"
    read -p "Repository URL: " repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote 'origin' added: $repo_url"
    else
        echo "⚠️  No repository URL provided. You can add it later with:"
        echo "   git remote add origin <url>"
    fi
fi

# Check for staged changes
echo ""
echo "Checking for changes..."
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "✅ No uncommitted changes"
else
    echo "📝 Uncommitted changes detected"
    echo ""
    echo "Would you like to commit all changes? (y/n)"
    read -p "Commit? " commit_choice
    
    if [ "$commit_choice" = "y" ] || [ "$commit_choice" = "Y" ]; then
        git add .
        git commit -m "Add GitHub Actions workflows for automated testing"
        echo "✅ Changes committed"
    fi
fi

# Push to GitHub
echo ""
echo "Would you like to push to GitHub now? (y/n)"
read -p "Push? " push_choice

if [ "$push_choice" = "y" ] || [ "$push_choice" = "Y" ]; then
    # Get current branch
    current_branch=$(git branch --show-current)
    
    if [ -z "$current_branch" ]; then
        # No branch yet, create main branch
        git branch -M main
        current_branch="main"
    fi
    
    echo "Pushing to branch: $current_branch"
    git push -u origin "$current_branch"
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pushed to GitHub!"
        echo ""
        echo "=========================================="
        echo "Next Steps:"
        echo "=========================================="
        echo "1. Go to your GitHub repository"
        echo "2. Click on the 'Actions' tab"
        echo "3. You should see workflows running automatically"
        echo "4. Update badge URLs in README.md with your username"
        echo ""
        echo "Workflows configured:"
        echo "  • Run Tests (Multi-platform, Multi-version)"
        echo "  • Quick Test (Fast feedback)"
        echo "  • Linting (Code quality)"
        echo ""
        echo "For more details, see GITHUB_ACTIONS_SETUP.md"
        echo "=========================================="
    else
        echo "❌ Failed to push. Please check your credentials and remote URL."
    fi
else
    echo "⚠️  Skipped push. You can push later with:"
    echo "   git push -u origin main"
fi

echo ""
echo "✅ Setup complete!"

