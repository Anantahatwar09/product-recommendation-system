from user import dummy_user_interactions
from recommendation_engine import generate_recommendations
import pandas as pd

# Read product data from CSV
product_data = pd.read_csv('abhinav.csv')

# Generate recommendations for the dummy user
recommendations = generate_recommendations(dummy_user_interactions, product_data)

# Print recommendations
print("Recommendations:")
for product in recommendations:
    print(product)
