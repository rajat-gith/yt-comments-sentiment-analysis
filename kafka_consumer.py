import os
from kafka import KafkaConsumer
from dotenv import load_dotenv
import json

from utilities import *
from generate_sentiment import *
from process_data import *

load_dotenv()

BOOTSTRAP_SERVER = os.environ.get("BOOTSTRAP_SERVER")


TOPIC = os.environ.get("TOPIC")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVER,
    group_id='my-group',
    auto_offset_reset='earliest'
)


for message in consumer:
    combined_data = message.value
    combined_data_dict = json.loads(combined_data)
    video_data = combined_data_dict.get("video_data")
    comments_data = combined_data_dict.get("comments_data")
    

    print("consumerside",comments_data)
    if video_data and comments_data:
        video_df = process_video_data(video_data)
        comments_df = process_comments_data(comments_data)
        plot_sentiment_distribution(comments_df)
        plot_sentiment_trends(comments_df)