#!/bin/bash

# Build script for production deployment to GitHub Pages
# This script builds the site with the correct basepath for GitHub Pages

echo "Building site for production with GitHub Pages basepath..."
python3 src/main.py "/static-site-gen/"
echo "Production build complete!"
