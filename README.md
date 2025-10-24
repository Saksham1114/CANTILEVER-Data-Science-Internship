This repository contains two separate Python web applications built with Flask, demonstrating different data processing techniques: web scraping and Optical Character Recognition (OCR).

Table of Contents

Project 1: Web Scraper Dashboard

Project 2: OCR (Image-to-Text) App

General Setup Instructions

Step 1: Tesseract OCR Engine (Required for Project 2)

Step 2: Python Environment & Libraries

How to Run

Project 1: Web Scraper Dashboard

File: app.py

Dependencies: requirements.txt

This is a Flask application that simulates scraping e-commerce product data. It displays the data in a clean UI, provides a search bar to filter products, and uses Matplotlib/Seaborn to generate a bar chart of average prices by category.

Note: This app currently uses mock data. To use it for real scraping, you will need to uncomment and modify the scrape_ecommerce_site function within app.py to target a real website's HTML structure.

Features

Product search functionality.

Data visualization (Avg. Price by Category) embedded in the page.

Data loaded into a Pandas DataFrame.

Commented-out code to save data to Excel.

Modern UI styled with Tailwind CSS.

Project 2: OCR (Image-to-Text) App

File: ocr_app.py

Dependencies: ocr_requirements.txt

This is a Flask application that allows users to upload an image file (PNG, JPG, etc.). It uses the Tesseract OCR engine to process the image, extract any detectable text, and display the text on the page alongside a preview of the uploaded image.

Features

File upload interface.

Image preview.

Text extraction using pytesseract and the TlL library.

Handles common errors, such as "Tesseract not found."

General Setup Instructions

Step 1: Tesseract OCR Engine (Required for Project 2)

This is the most critical step for the OCR App. pytesseract is just a Python wrapper; it requires the Tesseract engine to be installed on your system.

Windows: Download and run the installer from Tesseract at UB Mannheim. Important: During installation, make sure to check the box to "Add Tesseract to system PATH."

macOS: Install via Homebrew: brew install tesseract

Linux (Ubuntu/Debian): Install via apt: sudo apt install tesseract-ocr

Step 2: Python Environment & Libraries

Clone this repository (or ensure all files are in the same directory).

Create a virtual environment (recommended):

python -m venv venv


Activate the virtual environment:

On Windows: .\venv\Scripts\activate

On macOS/Linux: source venv/bin/activate

Install the required Python libraries.
You can install the libraries for one or both projects:

To run BOTH projects:

pip install -r requirements.txt -r ocr_requirements.txt


To run ONLY the Web Scraper:

pip install -r requirements.txt


To run ONLY the OCR App:

pip install -r ocr_requirements.txt


How to Run

Make sure your virtual environment is activated. You can only run one app at a time, as both default to the same port.

To Run the Web Scraper Dashboard:

python app.py


Open your browser and go to: http://127.0.0.1:5000

To Run the OCR (Image-to-Text) App:

python ocr_app.py


Open your browser and go to: http://1s.0.0.1:5000
