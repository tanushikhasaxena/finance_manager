# 🧾 Smart Expense Tracker with OCR

An intelligent expense tracking system that uses Optical Character Recognition (OCR) to scan and extract data from receipts, turning messy slips into structured, visualized expense records — no manual entry needed.

## 🔍 Features

- 📸 Upload receipt images (JPG/PNG/PDF)
- 🔎 Extract key data (date, merchant, total amount) using OCR
- 🧠 Preprocess and clean OCR output with image processing and regex
- 📊 Visualize expenses interactively using **Plotly**
- 🧾 Manually add/edit/delete entries
- 📁 Export expense reports as CSV

## 🧠 Tech Stack

- **Python** – Core logic
- **Tesseract OCR** – Text extraction from receipts
- **OpenCV** – Image preprocessing (grayscale, noise removal, etc.)
- **Pandas** – Data management
- **Plotly** – Interactive charts (bar, pie, time series)
- **Streamlit / Flask** – Optional frontend for interface

## 📈 Visualizations with Plotly

- Pie chart of expenses by category (e.g., food, travel, shopping)
- Bar chart of expenses by merchant
- Time series line graph for expense trends

## 🛠️ How It Works

1. Upload your receipt image.
2. Image gets cleaned and passed through Tesseract OCR.
3. Data is extracted using regex and stored with Pandas.
4. Plotly generates beautiful charts to show spending habits.
5. Users can interact with data or export it.

## Future Improvements
Use NLP for better receipt parsing

Add login & multi-user support

Connect to real bank APIs for auto-fetching transactions

Store data in a cloud database (Firebase, MongoDB, etc.)


## 📦 Setup Instructions

```bash
git clone https://github.com/tanushikhasaxena/finance_manager.git
cd finance_manager
pip install -r requirements.txt
python main.py

