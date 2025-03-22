import praw
import random
import threading
from time import sleep
from prawcore.exceptions import Forbidden, ServerError, RequestException

# Reddit API Authentication
reddit = praw.Reddit(
    client_id="Your_Client_id",
    client_secret="Your_Cliend_Secret",
    password="Your_password",
    user_agent="G-Bot v2.0 (by u/G-Bot-9000)",
    username="Bot_Username",
)

active_subreddits = ["TheLetterG"]  # Modify this list as needed

bot_statement = "\n\n^(I am a bot. This action was performed automatically.)"

def post_g_comment(submission):
    try:
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            if comment.author == reddit.user.me():
                return  

        sleep(random.randint(10, 30))  # Avoid bot detection
        submission.reply("G" + bot_statement)
        print(f"Replied 'G' to post: {submission.title}")

    except Forbidden:
        print(f"Bot is banned from r/{submission.subreddit}. Skipping...")
    except Exception as e:
        print(f"Error while commenting: {e}")
        
def restart():
    print("Restarting bot...")
    
    os.execv(sys.executable, ['python3'] + sys.argv)
def submission_stream():
    while True:
        try:
            for submission in reddit.subreddit("+".join(active_subreddits)).stream.submissions(skip_existing=True):
                post_g_comment(submission)
        except RequestException:
            print("Reddit API limit reached. Sleeping for 60 seconds...")
            sleep(60)
        except ServerError:
            print("Reddit server error. Retrying in 30 seconds...")
            sleep(30)
        except Exception as e:
            print(f"Stream Error: {e}. Restarting in 30 seconds...")
            sleep(30)

submission_thread = threading.Thread(target=submission_stream)
submission_thread.start()
