import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def generate_recommendations(user_interactions, product_df):
    # Convert user interactions to DataFrame
    browsing_history_df = pd.DataFrame(user_interactions['browsing_history'])
    purchase_history_df = pd.DataFrame(user_interactions['purchases'])

    # Concatenate browsing and purchase history
    user_interactions_df = pd.concat([browsing_history_df, purchase_history_df], ignore_index=True)

    # Calculate similarity matrix between products based on features (e.g., price, rating)
    product_features = product_df[['price', 'rating']].values
    product_similarity_matrix = cosine_similarity(product_features)

    # Function to recommend products based on user interactions
    def recommend_products(user_interactions_df):
        recommended_products = []
        for index, row in user_interactions_df.iterrows():
            product_id = row['id']
            similar_indices = product_similarity_matrix[product_id].argsort()[-2:][::-1]
            similar_products = product_df.iloc[similar_indices]
            recommended_products.extend(similar_products.to_dict('records'))
        return recommended_products

    # Generate recommendations based on combined interactions
    recommendations = recommend_products(user_interactions_df)

    return recommendations
