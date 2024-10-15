import re
from collections import Counter
import pandas as pd
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

# Initialize the OpenAI model
def initialize_llm():
    llm = ChatOpenAI(model="gpt-4o-mini")
    # prompt_template = """
    # You are an expert in identifying data science models and algorithms, including machine learning and statistical techniques mentioned in text.
    # For each comment below, extract all the data science models and algorithms mentioned.
    # For each comment, provide a list of models or algorithms in this format:
    # 'Comment X: [list of models/algorithms]'
    
    # Here are the comments:
    # {text}
    # """
    prompt_template = """
    You are an expert in extracting travel recommendations based on discussions about the best countries to visit. 
    For each comment below, identify and list the key recommendations for countries worth visiting. 
    For each comment, provide a list in this format:
    'Comment X: [list of recommendations/suggestions]'
    
    Here are the comments:
    {text}
    """
    prompt = PromptTemplate(text=['text'], template=prompt_template)
    return LLMChain(llm=llm, prompt=prompt)

# Function to batch comments for processing
def batch_comments(comments, batch_size=10):
    for i in range(0, len(comments), batch_size):
        yield comments[i:i + batch_size]

# Function to extract models from a batch of comments
def extract_models_from_batch(llm_chain, comment_batch):
    comments_str = "\n".join([f"Comment {i+1}: {comment}" for i, comment in enumerate(comment_batch)])
    response = llm_chain.run({"text": comments_str})
    return response.strip()

# Function to clean and normalize the extracted model names
def normalize_model_names(model_list):
    cleaned_models = []
    for model in model_list:
        model = re.sub(r'[\[\]]', '', model).strip().upper()  # Remove brackets, strip spaces, and make uppercase
        if model:
            cleaned_models.append(model)
    return cleaned_models

# Main extraction function to find the most mentioned models
def extract_model_insights(cleaned_df, batch_size=10, top_n=10):
    llm_chain = initialize_llm()
    all_models = []

    # Batch process comments for model extraction
    comment_batches = batch_comments(cleaned_df, batch_size=batch_size)
    for batch in comment_batches:
        # Correctly include reddit_topic in the function call
        models_from_batch = extract_models_from_batch(llm_chain, batch)
        batch_results = models_from_batch.split('\n')

        # Extract models for each comment
        for result in batch_results:
            if 'Comment' in result:
                models = result.split(':')[1].strip().split(',')
                all_models.extend([model.strip() for model in models if model])

    # Clean and normalize model names
    cleaned_all_models = normalize_model_names(all_models)

    # Count the frequency of each model
    model_counts = Counter(cleaned_all_models)

    # Get the top N models
    top_models = model_counts.most_common(top_n)

    return top_models, model_counts

# if __name__ == "__main__":
#     import pandas as pd
#     cleaned_df = pd.read_csv('data/reddit_data_cleaned.csv')
#     df_with_models = apply_extraction(cleaned_df)
#     df_with_models.to_csv('data/reddit_data_with_models.csv', index=False)
