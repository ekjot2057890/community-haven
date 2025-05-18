#!/bin/bash

# Fix CSS paths in all HTML files
find . -name "*.html" -exec sed -i 's|href="css/styles.css"|href="CSS/styles.css"|g' {} \;

# Fix JavaScript paths in all HTML files
find . -name "*.html" -exec sed -i 's|src="js/script.js"|src="JS/script.js"|g' {} \;

# Fix admin CSS paths
find ./admin -name "*.html" -exec sed -i 's|href="../css/styles.css"|href="../CSS/styles.css"|g' {} \;
find ./admin -name "*.html" -exec sed -i 's|href="../css/admin.css"|href="../CSS/admin.css"|g' {} \;

# Fix admin JS paths
find ./admin -name "*.html" -exec sed -i 's|src="../js/admin.js"|src="../JS/admin.js"|g' {} \;

# Add JavaScript reference to any HTML files missing it
for file in $(find . -name "*.html" ! -path "./admin/*"); do
  if ! grep -q "script.js" $file; then
    sed -i 's|</body>|    <script src="JS/script.js"></script>\n</body>|' $file
  fi
done

echo "All paths fixed!" 