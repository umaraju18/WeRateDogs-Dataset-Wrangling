# WeRateDogs-Dataset-Wrangling

Introduction: 

The dataset we analyzed (and analyzing and visualizing) is the tweet archive of Twitter user @dog_rates, also known as WeRateDogs. WeRateDogs is a Twitter account that rates people's dogs with a humorous comment about the dog. These ratings almost always have a denominator of 10. The numerators, though? Almost always greater than 10. 11/10, 12/10, 13/10, etc. Why? Because "they're good dogs Brent." WeRateDogs has over 4 million followers and has received international media coverage. WeRateDogs downloaded their Twitter archive and sent it to Udacity via email exclusively for you to use in this project. This archive contains basic tweet data (tweet ID, timestamp, text, etc.) for all 5000+ of their tweets as they stood on August 1, 2017. More on this soon.

This section describes about the wrangling procedure followed for WeRateDog Project. The wrangling process includes following steps:
(1) Gathering data (2) Assessing data (3) Cleaning data

Gathering Data:

There are three different type of dataset used in this project.
(1) Twitter_archive_enhanced.csv – The WeRateDogs Twitter archive. We manually downloaded this file.
(2) Image_predictions.tsv – The tweet image predictions, i.e., what breed of dog (or other object, animal, etc.) is present in each tweet according to a neural network. This file is hosted on Udacity’s servers and should be downloaded programmatically using Requests library and the following URL:
(3) tweet_json.txt – Each tweet’s retweet count, favorite and any additional data we found interesting. Using the tweet IDs in the WERateDogs twitter archive, we could query the twitter API for each tweet’s JSON data using Python’s Tweepy library and store each tweet’s entire set of JSON data in a file called tweet_json.txt file. Each tweet’s JSON data stored in a line

