import pandas as pd
import praw
import os
from dotenv import load_dotenv


load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("TOKEN_REDDIT"),
    user_agent=('sentiment_model.keras')
)

# Test de connexion
print(reddit.read_only)

##############################################################################################################

subreddit = reddit.subreddit('movies')

commentaires = []

# Récupère les 100 posts les plus récents
for post in subreddit.hot(limit=100):
    post.comments.replace_more(limit=0)  # charge tous les commentaires
    for comment in post.comments.list():
        commentaires.append({
            'post_title': post.title,
            'comment'   : comment.body,
            'score'     : comment.score,
            'date'      : comment.created_utc
        })


df_reddit = pd.DataFrame(commentaires)
print(f"{len(df_reddit):,} commentaires récupérés")
df_reddit.head()
df_reddit.to_csv('./asset/reddit_comments.csv', index=False)