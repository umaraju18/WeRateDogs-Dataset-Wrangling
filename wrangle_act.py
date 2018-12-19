#!/usr/bin/env python
# coding: utf-8

# In[80]:


# Import the libraries that we will need in this project
import pandas as pd
import datetime as dt
import numpy as np
import requests
import tweepy
import json
import re
import time
from nltk import pos_tag


# # Gathering Data
# ## Type of Data:
# 
# ### (1) CSV
# ### (2) download from website
# ### (3) Twitter API's JSON data
# 

# ## Gathering Data - Twitter Archive (.csv)
# 

# In[81]:


# Read the twitter-archive-enhanced.csv file and store it as dataframe in archive
archive = pd.read_csv('twitter-archive-enhanced.csv', encoding = 'utf-8')
# Quick check to the file content and structure
archive.head(2)


# # Gathering Data - Image Predictions (.tsv)

# In[82]:


# Using Requests library to download a file then store it in a tsv file
import requests
import pandas as pd
url = 'https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
response = requests.get(url)

#print(response.content)
#print(url.split('/')[-1])

with open(url.split('/')[-1], mode = 'wb') as outfile:
    outfile.write(response.content)

# Read the downloaded file into a dataframe 'images'
images = pd.read_csv('image-predictions.tsv', sep = '\t', encoding = 'utf-8')
# Quick check to the file content and structure
images.head()


# # Gathering Data - Twitter Data

# In[83]:


# Autontification to twitter API

# Generate your own at https://apps.twitter.com/app
# CONSUMER_KEY = 'Consumer Key (API key)'
# CONSUMER_SECRET = 'Consumer Secret (API Secret)'
# OAUTH_TOKEN = 'Access Token'
# OAUTH_TOKEN_SECRET = 'Access Token Secret'

consumer_key = '7zBWznG6qyjSrrWWIcL1AfNZm'
consumer_secret = 'kXWuKSLinQ2lDoji0CTaGLmLHCtdRh6mF0jNxCzLthVOg7XsLO'
access_token = '1055581525524209664-LDUJp0GJdpFc13kqACu24sRyOjzJP9'
access_token_secret = '6ICuLcNIG3mUbrxpjCdIca50ttS7PHQVkH85aEtRheHCF'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Construct the API instance
api = tweepy.API(auth, 
                 parser = tweepy.parsers.JSONParser(), # Parse the result to Json Object
                 wait_on_rate_limit = True, # Automatically wait for rate limits to replenish
                 wait_on_rate_limit_notify = True) # Print a notification when Tweepy is waiting for rate limits to replenish


# In[84]:


# List of dictionaries to build and convert to a DataFrame later
df_list = []
error_list = []

# Calculate the time of excution
start = time.time()

# Get the tweet object for all the teweets in archive dataframe 
for tweet_id in archive['tweet_id']:
    try:
        page = api.get_status(tweet_id, tweet_mode = 'extended')
             
        favorites = page['favorite_count'] # How many favorites the tweet had
        retweets = page['retweet_count'] # Count of the retweet
        user_followers = page['user']['followers_count'] # How many followers the user had
        user_favourites = page['user']['favourites_count'] # How many favorites the user had
        date_time = page['created_at'] # The date and time of the creation
        
        df_list.append({'tweet_id': int(tweet_id),
                        'favorites': int(favorites),
                        'retweets': int(retweets),
                        'user_followers': int(user_followers),
                        'user_favourites': int(user_favourites),
                        'date_time': pd.to_datetime(date_time)})
    
    # Not best practice to catch all exceptions but fine for this short script
    except Exception as e:
        print(str(tweet_id)+ " _ " + str(e))
        error_list.append(tweet_id)

# Calculate the time of excution
end = time.time()
print(end - start)
# 8888202515573088257 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# 873697596434513921 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# 872668790621863937 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# 869988702071779329 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# 866816280283807744 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# 861769973181624320 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# 845459076796616705 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# 842892208864923648 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# 837012587749474308 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# Rate limit reached. Sleeping for: 714
# 827228250799742977 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# 802247111496568832 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# 775096608509886464 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# 770743923962707968 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# 754011816964026368 _ [{'code': 144, 'message': 'No status found with that ID.'}]
# Rate limit reached. Sleeping for: 733
# Rate limit reached. Sleeping for: 736
# 2631.0154485702515


# In[85]:


# lengh of the result
print("The lengh of the result", len(df_list))
# The tweet_id of the errors
print("The lengh of the errors", len(error_list))

dataframe_df_list = pd.DataFrame(df_list)
dataframe_df_list.to_csv('dataframe_df_list.csv')

dataframe_error_list = pd.DataFrame(error_list)
dataframe_error_list.to_csv('dataframe_error_list.csv')


# In[86]:


#df_list = pd.read_csv('dataframe_df_list.csv', encoding = 'utf-8')
#error_list = pd.read_csv('dataframe_error_list.csv', encoding = 'utf-8')


# In[87]:


# repeat the same process for tweet_ids that we coudln't get and append the result to df_list
ee_list = []
for e in error_list:
    try:
        favorites = page['favorite_count']
        retweets = page['retweet_count']
        user_followers = page['user']['followers_count']
        user_favourites = page['user']['favourites_count']
        date_time = page['created_at']
        
        df_list.append({'tweet_id': int(tweet_id),
                        'favorites': int(favorites),
                        'retweets': int(retweets),
                        'user_followers': int(user_followers),
                        'user_favourites': int(user_favourites),
                        'date_time': pd.to_datetime(date_time)})
        
    except Exception:
        print(str(tweet_id)+ " _ " + str(e))
        ee_list.append(e)


# In[88]:


# We can see that now the 7 errors saved in the list
# lengh of the result
print("The lengh of the result after Querying the errors separately", len(df_list))


# In[89]:


# Create DataFrames from list of dictionaries
json_tweets = pd.DataFrame(df_list, columns = ['tweet_id', 'favorites', 'retweets',
                                               'user_followers', 'user_favourites', 'date_time'])

# Save the dataFrame in file
json_tweets.to_csv('tweet_json.txt', encoding = 'utf-8', index=False)


# In[90]:


# Read the saved tweet_json.txt file into a dataframe
json_tweets = pd.read_csv('tweet_json.txt', encoding = 'utf-8')
json_tweets.head()


# ## Gathering Data Summary:
# - obtainig data from file `twitter-archive-enhanced.csv` and reading from csv file using pandas
# - downloading from internet file `image-predictions.tsv` and downloading file using requests
# - Querying an API (`tweet_json.txt`) and get JSON object of all the tweet_ids using Tweepy
# - importing all data into Jupyter notebook

# # Assessment:
# #### After gathering data from all sources, we need to assess the data for quality and tidiness for the following datasets
# - `json_tweets` which has retweet and favorite counts
# - `images` has the results of a neural network trying to identify dog breed in a tweet's picture
# - `archive` has the tweet's text, rating, and dog category
# 
# 

# ## Assessment - Archive Data

# In[91]:


# assessing by visual assessment
archive.sample(10)


# In[92]:


# assessing by programmatic assessment
archive.info()


# In[93]:


# assessing by programmatic assessment
archive.describe()


# In[94]:


# finding duplicates
archive[archive.tweet_id.duplicated()]


# In[95]:


archive.tweet_id.duplicated().value_counts()


# In[96]:


archive.rating_numerator.unique()


# In[97]:


archive.rating_numerator.value_counts()


# In[98]:


archive.rating_denominator.unique()


# In[99]:


archive.rating_denominator.value_counts()


# In[100]:


ratings = archive['text'].str.extract('((?:\d+\.)?\d+)\/(\d+)', expand=True)


# In[101]:


ratings[0].value_counts()


# In[102]:


archive.puppo.value_counts()


# In[103]:


# finding dog type NOne for all
df_dog_type = archive[(archive['doggo']=='None')& (archive['floofer']=='None') & (archive['pupper']=='None')&(archive['puppo']=='None')]
df_dog_type


# In[104]:


# checking multiple dog stages for single tweet id
archive.loc[(archive[['doggo', 'floofer', 'pupper', 'puppo']] != 'None'
                 ).sum(axis=1) > 1]


# In[105]:


archive.name.value_counts().head(5)
archive[archive['tweet_id'] == 733109485275860992]


# In[106]:


#missing url
archive[archive['expanded_urls'].isnull()]


# ## Assessment - Images data

# In[107]:


# assessing visually
images.sample(5)


# In[108]:


#assessing programmatically
images.info()


# In[109]:


images.describe()


# In[110]:


images[images['tweet_id'].duplicated()]


# In[111]:


images.img_num.value_counts()


# In[112]:


images['jpg_url'].duplicated().value_counts()


# In[113]:


images[images['jpg_url']=='https://pbs.twimg.com/media/CWza7kpWcAAdYLc.jpg']


# # Assessment - tweets Data

# In[114]:


#assessing visually
json_tweets.sample()


# In[115]:


#assessing programmatically
json_tweets.info()


# In[116]:


json_tweets.describe()


# In[117]:


json_tweets[json_tweets['tweet_id'].duplicated()]


# In[118]:


json_tweets['tweet_id'].duplicated().value_counts()


# In[119]:


# combine all data columns to find tidiness of data -programmatic assessment
all_columns = pd.Series(list(json_tweets) + list(archive) + list(images))
all_columns[all_columns.duplicated()]


# In[120]:


list(all_columns)


# # Assessing Data Summary

# ### archive dataset:
# 
# - misssing data in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id,retweeted_status_timestamp, expanded_urls 
# - timestamp, retweeted_status_timestamp are object instead of datetime
# - some dog names are invalid names such as ’None’, ‘a’ a, an, the, just, one, very, quite, not, actually, mad, space, infuriating, all, officially, 0, old, life, unacceptable, my, incredibly, by, his, such
# - few rating_numerator and rating_denominator numbers are very high numbers. For example in tweet_id 832215909146226000 has rating erroneously mentioned 75 as numerator, whereas the text has numerator as 9.75
# - in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id should be string instead of float
# - tweet_id is int instead of string
# 

# ### Images dataset:
# - tweet_id is int instead of string

# #### json_tweets dataset:
# 
# - 14 tweet_ids are duplicates.
# - date_time should be date time format instead of object
# - tweet_ids are int instead of string
# 

# ### Tidiness
# - archive dataset has too many dog breed columns. instead it could be one column with dog stage in archive dataset
# - tweet_id in other two tables need to be removed when we combine all tables
# 
# 
# 

# # Cleaning Data

# In[121]:


# copying all datasets before cleaning
archive_clean = archive.copy()
images_clean = images.copy()
json_tweets_clean = json_tweets.copy()


# ##### Define
# - misssing data in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id,retweeted_status_timestamp, expanded_urls
#     - for some tweet ids, above variables are NaN. In this project, the available values for the above variables are considered and NaN values are kept as it is.
# 

# ##### Define
# - convert tweet_id into string for all three dataset
# - convert timestamp and retweeted_status_timestamp into date time
# - in_reply_to_status_id, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id should be string instead of float
# date_time in json_tweets dataset should be datetime

# ##### Code

# In[122]:


archive_clean.tweet_id = archive_clean.tweet_id.astype(str)
json_tweets_clean.tweet_id = json_tweets_clean.tweet_id.astype(str)
images_clean.tweet_id = images_clean.tweet_id.astype(str)
archive_clean.in_reply_to_status_id = archive_clean.in_reply_to_status_id.astype(str)
archive_clean.in_reply_to_user_id = archive_clean.in_reply_to_user_id.astype(str)
archive_clean.retweeted_status_id = archive_clean.retweeted_status_id.astype(str)
archive_clean.retweeted_status_user_id = archive_clean.retweeted_status_user_id.astype(str)
json_tweets_clean.date_time = pd.to_datetime(json_tweets_clean.date_time)
archive_clean.timestamp = pd.to_datetime(archive_clean.timestamp)
archive_clean.retweeted_status_timestamp = pd.to_datetime(archive_clean.retweeted_status_timestamp)


# ##### Test

# In[123]:


archive_clean.info()


# In[124]:


images_clean.info()


# In[125]:


json_tweets_clean.info()


# ##### Define
# 14 tweet_ids in json_tweets are duplicates

# ##### code

# In[126]:


json_tweets_clean = json_tweets_clean.drop_duplicates(['tweet_id'],keep='last')


# ##### Test

# In[127]:


json_tweets_clean[json_tweets_clean['tweet_id'].duplicated()]


# In[128]:


json_tweets_clean.info()


# ##### Define
# some dog names are ’None’, ‘a’ a, an, the, just, one, very, quite, not, actually, mad, space, infuriating, all, officially, 0, old, life, unacceptable, my, incredibly, by, his, such

# ##### Code

# In[129]:


non_names = ['a', 'an', 'the', 'just', 'one', 'very', 'quite', 'not', 'actually', 
             'mad', 'space', 'infuriating', 'all', 'officially', '0', 'old', 'life',
             'unacceptable', 'my', 'incredibly', 'by', 'his', 'such']

for name in archive_clean.name:
    if name in non_names:
        archive_clean.name[archive_clean.name == name] = 'None'


# ##### Test

# In[130]:


archive_clean['name'].value_counts().head(5)


# ##### Define
# - few rating_numerator and rating_denominator numbers are very high numbers. For example in tweet_id 832215909146226000 has rating erroneously mentioned 75 as numerator, whereas the text has numerator as 9.75

# ##### Code

# In[131]:


ratings = archive_clean.text.str.extract('((?:\d+\.)?\d+)\/(\d+)', expand=True)


# In[132]:


ratings


# In[133]:


ratings.columns = ["extracted_numerator", "extracted_denominator"]
ratings["extracted_numerator"]


# In[134]:


ratings.info()
ratings['extracted_numerator']


# In[135]:


archive_clean["extracted_numerator"] = ratings["extracted_numerator"]
archive_clean["extracted_denominator"] = ratings["extracted_denominator"]
new_cols = ['tweet_id','in_reply_to_status_id','in_reply_to_user_id','timestamp','source','text','retweeted_status_id','retweeted_status_user_id','retweeted_status_timestamp','expanded_urls','rating_numerator','rating_denominator','extracted_numerator','extracted_denominator','name','doggo','floofer','pupper','puppo']
archive_clean = archive_clean[new_cols]
archive_clean[archive_clean['tweet_id'] == '786709082849828864']


# ##### Test

# #### Tidiness
# too many dog breed columns. instead it could be one column with dog stage in archive dataset

# ##### Define
# too many dog breed columns. instead it could be one column with dog stage in archive dataset

# ##### Code

# In[136]:


archive_clean = pd.melt(archive_clean,
                        id_vars=['tweet_id', 'in_reply_to_status_id', 'in_reply_to_user_id',
                                 'timestamp', 'source', 'text', 'retweeted_status_id',
                                 'retweeted_status_user_id', 'retweeted_status_timestamp',
                                 'expanded_urls', 'rating_numerator', 'rating_denominator', 'extracted_numerator', 'extracted_denominator', 'name'],
                        value_name='dog_stage')
archive_clean = archive_clean.drop('variable', axis=1)
archive_clean['dog_stage'].value_counts()


# In[137]:


# Keep one of 3 duplicates with 'None'
dup_df1 = archive_clean.drop_duplicates(subset=['tweet_id', 'dog_stage']) 
dup_df1 = archive_clean.drop_duplicates()

# Keep rows with dog stage
dup_pos = archive_clean.duplicated(subset='tweet_id', keep = False)
dup_df2 = archive_clean[dup_pos]
dup_df2 = dup_df2[dup_df2.dog_stage != 'None']

# Combine
dup_df1 = dup_df1.drop_duplicates(subset = 'tweet_id', keep = False)
dup_df_merged = dup_df1.append(dup_df2)


# In[138]:


dup_df_merged.info()


# In[139]:


remaining_dup_df = dup_df_merged[dup_df_merged.duplicated(subset='tweet_id', keep=False)]
remaining_dup_df[remaining_dup_df.tweet_id == '817777686764523521']


# In[140]:


remaining_dup_df.dog_stage = 'multiple'
dup_drops = remaining_dup_df.drop_duplicates()
dup_drops[dup_drops.tweet_id == '817777686764523521']


# In[141]:


duped_ids = set(remaining_dup_df.tweet_id)
duped_ids
for idx in dup_df_merged.tweet_id:
    if idx in duped_ids:
        dup_df_merged.dog_stage[dup_df_merged.tweet_id == idx] = 'multiple'
archive_clean = dup_df_merged.drop_duplicates()


# ##### Test

# In[142]:


archive_clean.dog_stage.value_counts()


# In[143]:


archive_clean.info()


# ##### Define
# - tweet_id in other two tables need to be removed when we combine all tables

# ##### Code

# In[144]:


# merging all data files in to one main file
df_master = pd.merge(archive_clean, images_clean, how = 'left', on = ['tweet_id'] )
df_master_clean = pd.merge(df_master, json_tweets_clean, how = 'left', on = ['tweet_id'])
df_master_clean.info()


# In[145]:


df_master_clean['user_favourites'].value_counts()


# In[146]:


df_master_clean[df_master['tweet_id'].duplicated()]


# In[147]:


df_master_clean[df_master_clean['tweet_id']=='855851453814013952']


# # Storing Data

# In[148]:


df_master_clean.to_csv('twitter_images_archive_clean.csv', encoding='utf-8', index=False)


# # Analyzing Data

# In[149]:


import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# In[150]:


f,ax = plt.subplots(figsize=(18, 18))
sns.heatmap(df_master_clean[['retweets', 'favorites', 'extracted_numerator', 'user_followers', 'user_favourites']].corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
plt.title('Correlation Map')


# In[151]:


df_master_clean.plot(kind = 'scatter', x = 'favorites', y = 'retweets', alpha = 0.5, color = 'green')
plt.xlabel('Favorites')
plt.ylabel('Retweets')
plt.title('Retweets and favorites Scatter plot')


# In[152]:


df_master_clean.info()
# Convert extracted_numerator and extracted_denominator from string to float to plot in graph
df_master_clean['extracted_numerator'] = df_master_clean['extracted_numerator'].astype(float)
df_master_clean['extracted_denominator'] = df_master_clean['extracted_denominator'].astype(float)


# In[153]:



df_master_clean.plot(x = 'timestamp', y ='extracted_numerator', ylim=[0,16], style = '.', alpha = .2)
plt.title('Rating plot over Time')
plt.xlabel('Date')
plt.ylabel('Rating')


# In[154]:


df_master_clean['dog_stage'].value_counts()


# In[155]:


# data partitioned by dog stages

dog_stage_count = list(df_master_clean[df_master_clean['dog_stage'] != 'None']['dog_stage'].value_counts())[0:5]
dog_stages = df_master_clean[df_master_clean['dog_stage'] != 'None']['dog_stage'].value_counts().index.tolist()[0:5]


explode = (0.2, 0.1, 0.1, 0.1,0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(dog_stage_count, explode = explode, labels = dog_stages, shadow = True, startangle = 90)
ax1.axis('equal') 


# In[156]:


# dog stages with ratings
df_master_clean[df_master_clean['dog_stage'] != 'None'].boxplot(column = ['extracted_numerator'], by = ['dog_stage'])
plt.title('')
plt.xlabel('Dog_stage')
plt.ylabel('Rating')


# In[ ]:




