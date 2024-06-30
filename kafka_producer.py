import json
from kafka import KafkaProducer
from dotenv import load_dotenv

from utilities import *
from generate_sentiment import *
from process_data import *

load_dotenv()

TOPIC = os.environ.get("TOPIC")
BOOTSTRAP_SERVER = os.environ.get("BOOTSTRAP_SERVER")

def fetch_and_produce_data(video_id,producer):
    
    video_data = fetch_video_data(video_id)
    comments_data = fetch_comments(video_id)

    if video_data and comments_data:
        combined_data = {
            "video_data": video_data,
            "comments_data": comments_data
        }
        print("Producerside",comments_data)
        record_value = json.dumps(combined_data)
        producer.send(TOPIC, key=video_id.encode('utf-8'), value=record_value.encode('utf-8'))
        print(f"Sent combined data to Kafka topic {TOPIC}")
        #    sW9_SseyjEo 
def main():
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER)
    video_id = input("Enter the video Id: ")    
    fetch_and_produce_data(video_id, producer)

main()