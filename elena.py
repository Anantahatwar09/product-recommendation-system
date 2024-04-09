import random
import pandas as pd
import csv
import os.path

# Dummy user profile
# Dummy user profile 2
dummy_user = {
    'name': 'Elena',
    'email': 'elena@example.com',
    'age': 35,
    'gender': 'Female',
    'location': 'San Francisco, USA',
    'income_level': 'High',
    'occupation': 'Data Scientist',
    'marital_status': 'Married',
    'family_size': 2,
    'interests': ['reading', 'cooking', 'hiking'],
    'language_preference': 'English',
    'purchase_frequency': 'Weekly',
    'preferred_brands': ['Amazon', 'Adidas'],
}


# Read product data from CSV
product_data = pd.read_csv('abhinav.csv')

# Sample product instances from the CSV data
products = product_data.to_dict('records')

# Populate user purchases
# For simplicity, let's randomly select products from the dataset
dummy_purchases = random.sample(products, k=6)  # Select 3 random products for purchases

# Define a function to generate a single-line transaction
def generate_transaction(user_id, user_purchases, transaction_number):
    transactions = []
    for purchase in user_purchases:
        product_name = purchase['name']
        price = purchase['price']
        mrp = purchase['mrp']
        rating = purchase['rating']
        seller = purchase['seller']
        interaction_type = 'purchase'
        
        transaction = [user_id, f'transaction {transaction_number}', product_name, price, mrp, rating, seller, interaction_type]
        transactions.append(transaction)
    return transactions

# Save user purchases to CSV file
transaction_number = 9   # Starting transaction number
filename = f'user_purchases.csv'
 
# Check if the file exists to determine whether to write the header
write_header = not os.path.exists(filename)

with open(filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    # Write header if the file is empty
    if write_header:
        writer.writerow(['user_id', 'transaction', 'product_name', 'price', 'mrp', 'rating', 'seller', 'interaction_type'])
    
    # Write transactions
    for transaction in generate_transaction(dummy_user['email'], dummy_purchases, transaction_number):
        writer.writerow(transaction)

print(f"Transactions appended to {filename}")
