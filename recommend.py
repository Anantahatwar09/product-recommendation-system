import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# Load the dataset
data = pd.read_csv('user_purchases.csv')

# Prepare the data: extracting transactions
transaction_data = data[['transaction 1', 'Striped Henley Neck Pure Cotton T-shirt']]
transaction_data.columns = ['TransactionID', 'ProductName']
grouped_transactions = transaction_data.groupby('TransactionID')['ProductName'].apply(list)
transactions_list = grouped_transactions.tolist()

# Encode transactions for the Apriori algorithm
encoder = TransactionEncoder()
transactions_encoded = encoder.fit(transactions_list).transform(transactions_list)
transactions_df = pd.DataFrame(transactions_encoded, columns=encoder.columns_)

# Apply Apriori algorithm
frequent_itemsets = apriori(transactions_df, min_support=0.01, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)

# Assuming you want to recommend a product based on the presence of another,
# let's find recommendations for a common product from your dataset.
selected_product = 'Printed Round Neck T-Shirt'  # Example product from your dataset
relevant_rules = rules[rules['antecedents'].apply(lambda x: selected_product in x)]
relevant_rules = relevant_rules.sort_values(by='confidence', ascending=False)

# Assuming we want the top recommendation
if not relevant_rules.empty:
    top_recommendation = relevant_rules.iloc[0]['consequents']

def recommend_product(category, min_price):
    # Load the CSV file to understand its structure
    products_df = pd.read_csv('products.csv')
    
    # Filter products based on the category and price range
    filtered_products = products_df[(products_df['category'] == category) &
                                    (products_df['price'] >= min_price) &
                                    (products_df['price'] <= min_price + 100)]
    
    # Sort products based on a combination of rating, ratingTotal, and discount
    sorted_products = filtered_products.sort_values(by=['rating', 'ratingTotal', 'discount'], ascending=[False, False, False])
    
    # Select only the top 10 products
    top_products = sorted_products.head(10)
    
    # Return a list of dictionaries containing details of each top product
    recommendations = []
    for index, row in top_products.iterrows():
        recommendations.append({
            'brand': row['Brand'],
            'rating': row['rating'],
            'price': row['price'],
            'description': row['description']
        })
    
    return recommendations if recommendations else "No products found matching the criteria."

recommendation = recommend_product("tshirts", 200)
print(recommendation)
