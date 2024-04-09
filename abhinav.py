import random
import pandas as pd
import csv
import os.path

# Dummy user profile
dummy_user = {
    'name': 'Abhinav',
    'email': 'Abhinav@example.com',
    'age': 25,
    'gender': 'Male',
    'location': 'New York, USA',
    'income_level': 'Medium',
    'occupation': 'Software Engineer',
    'marital_status': 'Single',
    'family_size': 1,
    'interests': ['technology', 'gaming', 'fitness'],
    'language_preference': 'English',
    'purchase_frequency': 'Monthly',
    'preferred_brands': ['Apple', 'Nike'],
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
