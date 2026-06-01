#!/bin/bash

if [ "$#" -ne 1 ]; then #check number of args
    echo "Usage: $0 <output-dir-of-html-files>"
    echo "Example: $0 pages"
    exit 1
fi

HTML_DIR=$1
INDEX_DIR="./index_dir"
VENV_PATH="venv"

echo "=== Starting CS 172 Search Engine Indexer ==="

if [ -d "$VENV_PATH" ]; then #activate virtual environment
    echo "Activating virtual environment..."
    source "$VENV_PATH/bin/activate"
else
    echo "ERROR: Virtual environment '$VENV_PATH' not found."
    echo "Please run 'python3 -m venv venv' and install requirements first."
    exit 1
fi

if [ -f "index.py" ]; then #run index.py with expected flags
    echo "Running indexer on: $HTML_DIR"
    echo "Output index directory will be: $INDEX_DIR"
    
    python3 index.py --input "$HTML_DIR" --index "$INDEX_DIR"
    
else
    echo "ERROR: index.py not found in the current directory."
    deactivate
    exit 1
fi

echo "Indexing complete. Deactivating virtual environment." #deactivate environment
deactivate
echo "=============================================="