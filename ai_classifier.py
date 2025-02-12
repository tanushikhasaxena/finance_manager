import re


expense_categories = {
    "Food": ["Pizza", "Burger", "Coffee", "Meal", "Restaurant", "Dominos", "Subway", "McDonalds", "Zomato", "Swiggy", "food panda"],
    "Clothes": ["Shirt", "T-shirt", "Jeans", "Sweater", "Jacket", "Dress", "Clothing", "Footwear", "Shoes","HnM", "trends","zudio","zara"],
    "Games": ["PS5", "Xbox", "Game", "Steam", "PUBG", "Gaming", "PlayStation", "Nintendo","cricket","football","tennis","badminton","soccer"],
    "Study": ["Books", "Notebook", "Stationery", "Pen", "Tuition", "Course", "Exam", "Library"],
    "Mandatory": ["Rent", "Electricity", "Water", "Internet", "Gas", "Phone Bill","petrol","diesel","medical","hospital","healthcare","path lab"],
    "Others": ["Miscellaneous", "Entertainment", "Recharge", "Shopping","movie","pvr","inox","imax"]
}

def extract_amount(text):
    """Extract the total amount from OCR text"""
    amount_pattern = r"(?i)(total|amount|grand total|payable|net)[:\s]*[\$₹€]?\s*([\d,.]+)"
    matches = re.findall(amount_pattern, text)

    if matches:
        return matches[-1][1]  # Last match is usually the final total amount
    else:
        return "Amount not found"

def classify_expense(extracted_text):
    """Category Classification Based on Keywords"""
    matched_category = "Others"  # Default category
    matched_keywords = []

    for category, keywords in expense_categories.items():
        for keyword in keywords:
            if keyword.lower() in extracted_text.lower():
                matched_category = category
                matched_keywords.append(keyword)

    return matched_category, matched_keywords

