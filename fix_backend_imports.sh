#!/bin/bash

# Fix import paths in Python files
find ./backend -name "*.py" -exec sed -i 's|from app\.|from App.|g' {} \;
find ./backend -name "*.py" -exec sed -i 's|from app import|from App import|g' {} \;
find ./backend -name "*.py" -exec sed -i 's|import app\.|import App.|g' {} \;

# For modules using SQLAlchemy, make sure we update to PyMongo where needed
# This would need to be customized based on the specific models and architecture

echo "Backend import paths fixed!" 