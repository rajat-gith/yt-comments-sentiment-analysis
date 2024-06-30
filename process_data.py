import pandas as pd

from generate_sentiment import get_sentiment

def process_consumed_video_data(video_data):

    video_info = {
        "title": video_data["title"],
        "description": video_data["description"],
        "publishedAt": video_data["publishedAt"],
        "viewCount": int(video_data.get("viewCount", 0)),
        "likeCount": int(video_data.get("likeCount", 0)),
        "dislikeCount": int(video_data.get("dislikeCount", 0)),
        "commentCount": int(video_data.get("commentCount", 0))
    }
    return video_info



def process_video_data(video_data):
    video_snippet = video_data["items"][0]["snippet"]
    video_stats = video_data["items"][0]["statistics"]
    video_info = {
        "title": video_snippet["title"],
        "description": video_snippet["description"],
        "publishedAt": video_snippet["publishedAt"],
        "viewCount": int(video_stats.get("viewCount", 0)),
        "likeCount": int(video_stats.get("likeCount", 0)),
        "dislikeCount": int(video_stats.get("dislikeCount", 0)),
        "commentCount": int(video_stats.get("commentCount", 0))
    }
    return video_info



def process_comments_data(comments_data):
    comments_list = []
    for item in comments_data['items']:
        top_comment = item["snippet"]["topLevelComment"]["snippet"]
        comments_list.append(top_comment)
        total_replies = item["snippet"]["totalReplyCount"]
        if total_replies > 0:
            replies = item.get('replies', {}).get('comments', [])
            for reply in replies:
                comments_list.append(reply["snippet"])

    comments_df = pd.DataFrame(comments_list)    
    comments_df['sentiment'] = comments_df['textDisplay'].apply(get_sentiment)
    comments_df['publishedAt'] = (comments_df['publishedAt'])
    
    comments_df['sentiment_category'] = comments_df['sentiment'].apply(
        lambda x: 'positive' if x > 0 else 'negative' if x < 0 else 'neutral'
    )
    
    return comments_df



