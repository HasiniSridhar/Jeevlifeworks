#!/bin/bash
# Setup script to copy all Python OOP files to python folder

echo "=========================================="
echo "Copying Python OOP Implementation Files"
echo "=========================================="

SPARK_DIR=~/Documents/faers_prr_project/spark
PYTHON_DIR=~/Documents/faers_prr_project/python

# Create python directory if it doesn't exist
mkdir -p $PYTHON_DIR

# Copy Python implementation files
echo "Copying implementation files..."
cp $SPARK_DIR/faers_prr_analyzer.py $PYTHON_DIR/
echo "✓ faers_prr_analyzer.py"

cp $SPARK_DIR/faers_examples.py $PYTHON_DIR/
echo "✓ faers_examples.py"

cp $SPARK_DIR/test_faers_prr.py $PYTHON_DIR/
echo "✓ test_faers_prr.py"

cp $SPARK_DIR/quickstart.py $PYTHON_DIR/
echo "✓ quickstart.py"

# Copy data files
echo ""
echo "Copying data files..."
cp $SPARK_DIR/drug_file.csv $PYTHON_DIR/
echo "✓ drug_file.csv"

cp $SPARK_DIR/reac_file.csv $PYTHON_DIR/
echo "✓ reac_file.csv"

# Copy documentation
echo ""
echo "Copying documentation..."
cp $SPARK_DIR/PYTHON_OOP_README.md $PYTHON_DIR/
echo "✓ PYTHON_OOP_README.md"

# Verify files
echo ""
echo "=========================================="
echo "Verification - Files in python folder:"
echo "=========================================="
ls -lh $PYTHON_DIR/

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. cd $PYTHON_DIR"
echo "2. python3 quickstart.py"
echo "3. python3 faers_prr_analyzer.py"
