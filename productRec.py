import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

import os

# Read the CSV file
df = pd.read_csv('myntra202305041052.csv')

# Copy the dataframe
myntra = df.copy()

# Drop unnecessary columns
myntra.drop(['asin', 'id'], axis=1, inplace=True)

# Rename columns
myntra.rename(columns={'seller': 'Brand', 'purl': 'url'}, inplace=True)

# Add category of product
myntra['category'] = myntra['url'].apply(lambda x: x.split('/')[-5])

# Add description about product
myntra['description'] = myntra['url'].apply(lambda x: x.split('/')[-3])

# Handle missing values
myntra['name'].replace('-', np.nan, inplace=True)
myntra['name'].fillna(myntra['url'].apply(lambda x: x.split('/')[-5]), inplace=True)

# Drop url column
myntra.drop(['url'], axis=1, inplace=True)

# Handle discount column
def discount_percent(x):
    return (100*x[1]//x[0])

myntra['discount'] = myntra[['mrp', 'discount']].apply(discount_percent, axis=1)

# Handle zero ratings
df2 = myntra.groupby('description')['rating'].mean().to_dict()
myntra['rating'] = myntra['rating'].mask(myntra['rating'] == 0, myntra['description'].map(df2))

# Visualizations
sns.heatmap(myntra.corr(numeric_only=True), linewidths=0.5, linecolor="white")
sns.histplot(kde=True, data=myntra, x='mrp', bins=60, log_scale=True)
sns.histplot(kde=True, data=myntra, x='price', bins=60, log_scale=True)
sns.histplot(kde=True, data=myntra, x='discount', bins=60)
sns.histplot(kde=True, data=myntra, x='rating', bins=60)

# Product Category Counts
category_counts = myntra['category'].value_counts()
max_categories = category_counts.head(10)
min_categories = category_counts.tail(10)

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5))   
fig.subplots_adjust(bottom=0.2, left=0.2)

# Reset index before passing to barplot function
sns.barplot(data=max_categories.reset_index(), y='index', x='category', ax=axes[0])
axes[0].set_xlabel('Count')
axes[0].set_ylabel('Product Category')
axes[0].set_title('Max product Categories')

sns.barplot(data=min_categories.reset_index(), y='index', x='category', ax=axes[1])
axes[1].set_xlabel('Count')
axes[1].set_ylabel('Product Category')
axes[1].set_title('Min product Category')

plt.tight_layout(pad=2)

# User Input for Recommendations
product_category = input('Enter product category: ')
brand_name = input('Enter the brand name: ')
budget = float(input('Enter your budget: '))

def product_recom(product_category, brand_name, budget, min_support=0.01, min_confidence=0.5):
    # Filter data based on user inputs
    filtered_data = myntra[(myntra['category'] == product_category) & 
                           (myntra['Brand'] == brand_name) & 
                           (myntra['price'] <= budget)]

    if filtered_data.empty:
        print('No products found for the given criteria.')
        return

    # Convert data to transactional format
    transactions = filtered_data.groupby(['transaction_id', 'name'])['name'].count().unstack().fillna(0)

    # Apply Apriori algorithm
    frequent_itemsets = apriori(transactions, min_support=min_support, use_colnames=True)

    # Generate association rules
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_confidence)

    # Filter recommendations based on antecedents and budget
    recommendations = rules[(rules['antecedents'].apply(lambda x: brand_name in str(x))) &
                            (rules['consequents'].apply(lambda x: budget >= filtered_data[filtered_data['name'] == list(x)[0]]['price'].values[0]))]

    # Display recommendations
    if not recommendations.empty:
        print(recommendations.sort_values(by='lift', ascending=False))
    else:
        print('No recommendations found for the given criteria.')

# Call the function with user input
product_recom(product_category, brand_name, budget)
