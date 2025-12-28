#!/bin/bash

# Quick deployment script
# Run this after setting up GitHub, Render, and Vercel

echo "🚀 Technoaiamaze Deployment Helper"
echo "===================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📌 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Ready for deployment"
else
    echo "✅ Git repository already initialized"
fi

# Show current status
echo ""
echo "📊 Current Status:"
echo "- Git: ✅ Initialized"
echo "- Files: ✅ Ready"
echo ""

# Next steps
echo "📝 Next Steps:"
echo ""
echo "1. Create GitHub repository at: https://github.com/new"
echo "2. Run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
echo "   git push -u origin main"
echo ""
echo "3. Deploy backend to Render: https://render.com"
echo "4. Deploy frontend to Vercel: https://vercel.com"
echo ""
echo "See DEPLOYMENT.md for complete guide!"
echo ""
