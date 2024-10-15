# Clean the scraped data in a modular way.
# Create functions for text cleaning and emoji removal.

import re

def clean_comments(text):

    # Convert text to lowercase
    text = text.lower()

    # Normalize bullet characters
    text = re.sub(r'[\u2022\u2023\u2043\u25CB\u25CF\u25B6\u25C6]', '•', text)
    text = re.sub(r'â€¢', '•', text)
    
    # Normalize apostrophes and quotes
    text = re.sub(r'[’‘`]', "'", text)
    text = re.sub(r'[“”]', '"', text)

    # Remove emojis
    emoji_pattern = re.compile(
        "[" 
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"  # miscellaneous symbols
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # Remove URLs
    text = re.sub(r'https?:\/\/\S+', '', text)

    # Remove mentions (@user), hashtags (#hashtag), and retweet (RT)
    text = re.sub(r'[@#RT]', '', text)

    # Remove non-ASCII characters (optional)
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    # Replace multiple periods with a single period
    text = re.sub(r'\.\.\.+', '.', text)

    # Remove extra whitespace (including newlines and tabs)
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def clean_data(df):
    preprocessed_data = df['data'].apply(clean_comments)
    return preprocessed_data

if __name__ == "__main__":
    import pandas as pd
    reddit_df = pd.read_csv('data/reddit_data.csv')
    cleaned_df = clean_data(reddit_df)
    cleaned_df.to_csv('data/reddit_data_cleaned.csv', index=False)
