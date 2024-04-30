import praw
import re
import pandas as pd
import openai
import os
import json
from datetime import datetime
import praw
import re
import json
from datetime import datetime

class RedditFinancialScraper:
    def __init__(self, client_id, client_secret, user_agent, ticker_file):
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        self.stock_regex = r'\b[A-Z]{2,5}(?:\.[A-Za-z]+)?\b'
        self.ticker_list = self.load_ticker_list(ticker_file)

    def load_ticker_list(self, ticker_file):
        with open(ticker_file, 'r') as file:
            ticker_data = json.load(file)
        return set([ticker['ticker'] for ticker in ticker_data.values()])

    def get_posts(self, subreddit, category='hot', limit=10):
        return getattr(self.reddit.subreddit(subreddit), category)(limit=limit)

    def find_symbols(self, text):
        pattern = self.stock_regex
        found_tickers = set(re.findall(pattern, text))
        valid_tickers = {ticker: (ticker.upper() in self.ticker_list) if ticker.upper() in self.ticker_list else False for ticker in found_tickers}
        return valid_tickers

    def extract_post_data(self, post):
        post_data = {
            "post_title": post.title,
            "post_date": post.created_utc,
            "post_body": post.selftext,
            "comments": self.extract_comments_data(post.comments)
        }
        post_data['relevant_tickers'] = self.find_symbols(post_data['post_body'])
        return post_data

    def extract_comments_data(self, comments):
        comments.replace_more(limit=None)
        comment_data = []
        for comment in comments.list():
            # if isinstance(comment, praw.models.MoreComments):
            #     continue
            comment_dict = {
                "comment_date": comment.created_utc,
                "comment_body": comment.body,
                # "relevant_tickers": list(self.find_symbols(comment.body))
            }
            comment_dict['relevant_tickers'] = self.find_symbols(comment_dict['comment_body'])
            comment_data.append(comment_dict)
        return comment_data

    def most_discussed_org(self, subreddit,limit=10,category='hot'):
        results = []
        for post in self.get_posts(subreddit, category, limit=limit):
            post_data = self.extract_post_data(post)
            results.append(post_data)
        return results
    
    def most_discussed_org_from_sticky(self, subreddit, limit=10):
        results = []
        for post in self.get_posts(subreddit, category='hot', limit=limit):
            if post.stickied:
                post_data = self.extract_post_data(post)
                results.append(post_data)
                break  # Stop after processing the first stickied post
        return results
    

# class RedditFinancialScraper:
#     def __init__(self, client_id, client_secret, user_agent, ticker_file):
#         self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
#         self.stock_regex = r'\b[A-Z]{2,5}(?:\.[A-Za-z]+)?\b'
#         self.ticker_list = self.load_ticker_list(ticker_file)

#     def load_ticker_list(self, ticker_file):
#         with open(ticker_file, 'r') as file:
#             ticker_data = json.load(file)
#         return set([ticker['ticker'] for ticker in ticker_data.values()])

#     def get_posts(self, subreddit, category='hot', limit=10):
#         return getattr(self.reddit.subreddit(subreddit), category)(limit=limit)

#     def find_symbols(self, text):
#         pattern = self.stock_regex
#         found_tickers = set(re.findall(pattern, text))
#         return found_tickers

#     def extract_post_data(self, post):
#         post_data = {
#             "post_title": post.title,
#             "post_date": post.created_utc,
#             "post_body": post.selftext,
#             "comments": self.extract_comments_data(post.comments)
#         }
#         post_data['relevant_tickers'] = list(self.find_symbols(post_data['post_body']))
#         return post_data

#     def extract_comments_data(self, comments):
#         comments.replace_more(limit=None)
#         comment_data = []
#         for comment in comments.list():
#             comment_dict = {
#                 "comment_date": comment.created_utc,
#                 "comment_body": comment.body,
#                 "relevant_tickers": list(self.find_symbols(comment.body))
#             }
#             comment_data.append(comment_dict)
#         return comment_data

#     def most_discussed_org(self, subreddit, limit=10, category='hot'):
#         results = []
#         for post in self.get_posts(subreddit, category, limit=limit):
#             post_data = self.extract_post_data(post)
#             results.append(post_data)
#         return results

#     def most_discussed_org_from_sticky(self, subreddit, limit=10):
#         results = []
#         for post in self.get_posts(subreddit, category='hot', limit=limit):
#             if post.stickied:
#                 post_data = self.extract_post_data(post)
#                 results.append(post_data)
#                 break  # Stop after processing the first stickied post
#         return results