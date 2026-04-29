#!/bin/bash
source path/to/venv/bin/activate
rm -rf "$4"
python3 main.py "$1" "$2" "$3" "$4"