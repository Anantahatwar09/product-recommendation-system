import pandas as pd

def recommend_product():
    # Load the CSV file to understand its structure
    products_df = pd.read_csv('products.csv')
    
    # Prompt user for input
    category = input("Enter the category: ")
    min_price = float(input("Enter the minimum price: "))
    
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

recommendation = recommend_product()
print(recommendation)
