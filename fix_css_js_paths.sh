#!/bin/bash

# Fix CSS paths in all HTML files
find . -name "*.html" -exec sed -i 's|href="css/styles.css"|href="CSS/styles.css"|g' {} \;

# Fix JS paths in all HTML files
find . -name "*.html" -exec sed -i 's|src="js/script.js"|src="JS/script.js"|g' {} \;

echo "Path references updated in all HTML files." 