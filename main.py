# The main script to run the entire pipeline.

from src.reddit_scraper import scrape_reddit, scrape_reddit_info
from src.reddit_cleaner import clean_data
from src.consensus_finder import extract_model_insights


import pandas as pd
import hashlib
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud
import openai
# import os


# # Function to generate a unique filename based on the URL
# def generate_filename(url):
#     url_hash = hashlib.md5(url.encode()).hexdigest()  # Hash the URL to create a unique identifier
#     return url_hash

# # Get the absolute path to the folder where main.py is located
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Create the 'data' directory if it doesn't exist
# data_dir = os.path.join(script_dir, 'data')
# if not os.path.exists(data_dir):
#     os.makedirs(data_dir)

# # Set the current working directory to the script's directory
# os.chdir(script_dir)

# Set Streamlit page configuration
st.set_page_config(page_title="Popular Topic Finder", layout="centered")

# Streamlit app title
st.markdown("<h1 style='text-align: center;'>Popular Topic Finder</h1>", unsafe_allow_html=True)

# Description
st.markdown("""
**Popular Topic Finder** is a versatile web app designed to extract and visualise key insights from discussion forums and community data. 
            Whether you're analyzing popular AI models, top travel destinations, or the most recommended restaurants, Popular Topic Finder 
            helps you discover the most frequently mentioned topics, and highlights what's popular or trending from any source, providing 
            insights in an easy-to-digest format.
""")

# Input field for the Reddit URL
url = st.text_input("Enter the URL")

# Input field for the number of top models to analyze
top_n = st.number_input("Specify the number of top results you'd like to display:", min_value=1, max_value=50, value=10)

# Button to start the scraping and model extraction
if st.button("Analyse"):
    # Check if a URL has been entered
    if url:
        # # Generate unique filenames for each URL
        # file_base = generate_filename(url)
        # scraped_csv = os.path.join(data_dir, f'{file_base}_reddit_data.csv')

        # # Scrape data (only if the file doesn't already exist)
        # if os.path.exists(scraped_csv):
        #     st.write(f"Scraped data for this URL already exists. Loading from {scraped_csv}")
        #     reddit_df = pd.read_csv(scraped_csv)
        # else:
        #     st.write(f"Scraping Reddit data for URL: {url}...")

        #     my_client_id = st.secrets["my_client_id"]
        #     my_client_secret = st.secrets["my_client_secret"]
        #     my_user_agent = st.secrets["my_user_agent"]

        #     reddit_df = scrape_reddit(url, my_client_id, my_client_secret, my_user_agent)
        #     reddit_df.columns = ['data']  # Ensure consistency by renaming the column to 'data'
        #     reddit_df.to_csv(scraped_csv, index=False)
        #     st.write(f"Data scraped and saved to {scraped_csv}")

        st.write(f"Scraping Reddit data for URL: {url}...")
        my_client_id = st.secrets["my_client_id"]
        my_client_secret = st.secrets["my_client_secret"]
        my_user_agent = st.secrets["my_user_agent"]

        reddit_df = scrape_reddit(url, my_client_id, my_client_secret, my_user_agent)
        reddit_df.columns = ['data']  # Ensure consistency by renaming the column to 'data'

        topic, subreddit = scrape_reddit_info(url, my_client_id, my_client_secret, my_user_agent)

        # reddit_df.to_csv(scraped_csv, index=False)
        # st.write(f"Data scraped and saved to {scraped_csv}")
        
        # Clean data
        cleaned_df = clean_data(reddit_df)

        # Load OpenAI Key
        openai.api_key = st.secrets["OPENAI_API_KEY"]

        # Extract insights on models commonly used
        top_consensus, model_count = extract_model_insights(cleaned_df, subreddit, topic, batch_size=50, top_n=top_n)

        # Convert the top models with percentage to a DataFrame
        visual_df = pd.DataFrame(top_consensus, columns=['Model', 'Count'])
        
        # Sort by Count in descending order
        visual_df = visual_df.sort_values(by='Count', ascending=False)

        # --- 1. Word Cloud: Model Frequency ---
        # st.subheader('Word Cloud of Data Science Models')
        st.subheader(f"Word Cloud of Most Frequently Mentioned Terms in Discussion")

        # Create a dictionary from the model counts for the word cloud
        model_dict = {model: count for model, count in model_count.items()}

        # Generate the word cloud with a more vibrant color
        wordcloud = WordCloud(width=800, height=400, background_color='black', colormap='plasma').generate_from_frequencies(model_dict)

        # Display the word cloud
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        # plt.title('Word Cloud of Data Science Models', fontsize=16)

        # Display the word cloud on Streamlit
        st.pyplot(plt)

        # --- 2. Bar Chart: Top Models ---
        # st.subheader(f"Top {len(top_consensus)} Most Common Data Science Models/Algorithms")
        st.subheader(f"Top {len(top_consensus)} Most Popular Choices in Discussion")

        plt.figure(figsize=(10, 6))
        sns.barplot(x='Count', y='Model', data=visual_df, palette='viridis')  # Using a vibrant palette
        # plt.title(f'Top {len(top_consensus)} Most Common Data Science Models/Algorithms', fontsize=16)
        plt.xlabel('Frequency of Mention', fontsize=12)
        plt.ylabel('Models/Algorithms', fontsize=12)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.tight_layout()

        # Display the bar chart on Streamlit
        st.pyplot(plt)
    else:
        st.write("Please enter a valid Reddit URL.")
