#!/bin/bash

echo "Creating virtual environment called 'env'"
python3 -m venv env
source env/bin/activate
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
  echo "Failed to install dependencies."
  exit 1
fi

echo "Starting the FastAPI server..."
uvicorn app.main:app --reload