from src.gemini_ai import ask_gemini

question = "Which product has the highest sales?"

data_summary = """
Total Sales: ₹39,837,950
Total Profit: ₹12,837,643
Total Orders: 1000
Top Product: Laptop
Top Region: West
Top Category by Profit: Electronics
Top Customer: Vikas Kumar
"""

answer = ask_gemini(question, data_summary)

print("\n========== GEMINI AI RESPONSE ==========\n")
print(answer)