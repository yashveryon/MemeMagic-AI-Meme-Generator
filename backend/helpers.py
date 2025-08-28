import random
import string
import datetime

def random_funny_caption():
    """
    Returns a random pre-defined meme-style caption.
    """
    captions = [
        "When your code finally works and you don’t know why.",
        "This is fine. Everything is fine.🔥",
        "404: Motivation not found.",
        "I’m not lazy, I’m on energy-saving mode.",
        "Debugging: removing the needles you planted.",
        "Ctrl+C & Ctrl+V are my superpowers.",
        "Just deployed, hope nothing breaks... 🤞",
        "Expectation vs Reality: always Reality 😭"
    ]
    return random.choice(captions)

def generate_unique_filename(extension=".jpg"):
    """
    Creates a unique filename using timestamp and random characters.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"meme_{timestamp}_{rand_str}{extension}"
