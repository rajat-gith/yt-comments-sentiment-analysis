import requests
import os
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("API_KEY")

def fetch_comments(video_id):
    comments_url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={API_KEY}&maxResults=100'
    response = requests.get(comments_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching comments data: {response.status_code}, {response.text}")
        return None
    

def fetch_video_data(video_id):
    video_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={API_KEY}'
    response = requests.get(video_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching video data: {response.status_code}, {response.text}")
        return None
    

def plot_sentiment_distribution(pandas_df):
    sentiment_counts = pandas_df['sentiment_category'].value_counts()
    sentiment_counts.plot.pie(autopct='%1.1f%%', colors=['green', 'gray', 'red'], labels=['Positive', 'Neutral', 'Negative'])
    plt.title('Sentiment Distribution of YouTube Comments')
    plt.ylabel('')
    plt.show()


def plot_sentiment_trends(pandas_df):
    
    pandas_df['date'] = pd.to_datetime(pandas_df['publishedAt']).dt.date
    sentiment_trends = pandas_df.groupby(['date', 'sentiment_category']).size().unstack(fill_value=0)
    sentiment_trends.plot(kind='line', stacked=False)
    plt.title('Sentiment Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Comments')
    plt.show()

