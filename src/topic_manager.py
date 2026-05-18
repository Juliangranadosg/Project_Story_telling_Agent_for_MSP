import random


topics = [
    "Why clarity does not come from more thinking",
    "How mental space affects decision-making",
    "Why people feel stuck during transitions",
    "How internal structure influences leadership presence",
    "How relationship patterns can be represented in mental space"
]


def get_next_topic():
    return random.choice(topics)