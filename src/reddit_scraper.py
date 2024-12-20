# This file handles scraping data from Reddit.

import praw
import pandas as pd

def scrape_reddit(url, my_client_id, my_client_secret, my_user_agent):
    reddit = praw.Reddit(
        client_id= my_client_id,
        client_secret= my_client_secret,
        user_agent= my_user_agent
    )

    # Get the submission (post)
    submission = reddit.submission(url=url)

    # Extract the topic from the title and subreddit
    topic = submission.title
    subreddit = submission.subreddit.display_name
    
    submission.comments.replace_more(limit=None)

    comments = set()
    for top_level_comment in submission.comments:
        comments.add(top_level_comment.body)

    # Create dataframe
    reddit_df = pd.DataFrame(comments, columns=['data'])

    return reddit_df


def scrape_reddit_info(url, my_client_id, my_client_secret, my_user_agent):
    reddit = praw.Reddit(
        client_id= my_client_id,
        client_secret= my_client_secret,
        user_agent= my_user_agent
    )

    # Get the submission (post)
    submission = reddit.submission(url=url)

    # Extract the topic from the title and subreddit
    topic = submission.title
    subreddit = submission.subreddit.display_name

    return topic, subreddit


if __name__ == "__main__":
    url = 'https://www.reddit.com/r/datascience/comments/xvhiml/professional_data_scientists_what_are_the/'
    reddit_df = scrape_reddit(url)
    # reddit_df.to_csv('data/reddit_data.csv', index=False)
