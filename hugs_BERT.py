#!/usr/bin/env python
# coding: utf-8

# # Hugging Face (Pre-trained Model) BERT Twitter Stock Sentiment Analysis

# In[1]:



# !pip install yahoo_fin
# !pip install transformers
# !pip install tweepy

import time
import datetime
import tweepy
import pandas as pd
from tweepy import OAuthHandler
from transformers import pipeline
from statistics import mean
from yahoo_fin import stock_info as si
from pandas_datareader import data as pdr


specific_model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")


# Variables

tickers = si.tickers_sp500()[0:30]
tickers = [item.replace(".", "-") for item in tickers] # Yahoo Finance uses dashes instead of dots
index_name = '^GSPC' # S&P 500
start_date = datetime.datetime.now() - datetime.timedelta(days=7)
end_date = datetime.date.today()
exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA", "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])
returns_multiples = []

# Index Returns
index_df = pdr.get_data_yahoo(index_name, start_date, end_date)
index_df['Percent Change'] = index_df['Adj Close'].pct_change()
index_return = (index_df['Percent Change'] + 1).cumprod()[-1]

# Find top 30% performing stocks (relative to the S&P 500)
for ticker in tickers:
    # Download historical data as CSV for each stock (makes the process faster)
    df = pdr.get_data_yahoo(ticker, start_date, end_date)
#     df.to_csv(f'{ticker}.csv')

    # Calculating returns relative to the market (returns multiple)
    df['Percent Change'] = df['Adj Close'].pct_change()
    stock_return = (df['Percent Change'] + 1).cumprod()[-1]
    
    returns_multiple = round((stock_return / index_return), 2)
    returns_multiples.extend([returns_multiple])
    
    print (f'Ticker: {ticker}; Returns Multiple against S&P 500: {returns_multiple}\n')
    time.sleep(1)

# Creating dataframe of only top 30%
rs_df = pd.DataFrame(list(zip(tickers, returns_multiples)), columns=['Ticker', 'Returns_multiple'])
rs_df['RS_Rating'] = rs_df.Returns_multiple.rank(pct=True) * 100
rs_df = rs_df[rs_df.RS_Rating >= rs_df.RS_Rating.quantile(.70)]


df = rs_df.sort_values(by='Returns_multiple', ascending = False)


client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAGsRfwEAAAAA9avAVOadpyjiDUS0%2FvAjqObovwA%3DuOy52TtpkYOuabmC4iw3CgJzIdyY7k0Usl1JDoYGBJo4dqYVwM")
consumer_key = "Voa1NdvJCbxrhoPh7nipmd7NW"
consumer_secret = "o7CETkfE52fjIw02o5EVt5D8Y0ZfGYp2dO9rhMG54FtCyiKcVr"
access_key = "1520622913224798209-Tv3GwMriwTOXRygQORkGoWLWOwvWsG"
access_secret = "uYCAgUSNBOqARXOVI5cWRfYD6ceees5JgXGTPuiC3AQhg"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


# In[2]:


avgs = []
for i in df.Ticker:
    
    scores = []
    data = client.search_recent_tweets(query=f'#{i} Stock', max_results=100)

    try:
    
        for j in data.data:
            tweet = j.text
            score = specific_model(j.text[0:120])[0]['score']
            scores.append(score)

        avgs.append(mean(scores))
            
    except TypeError:
        # No tweets available, remove from dataframe
        df = df.drop(index = df[df.Ticker == i].index)
    


# In[3]:


df['RS_BERT_Score'] = df['Returns_multiple']*avgs
df = df.sort_values(by='RS_BERT_Score', ascending=False)
print(df.tail())

