# tw-predicter
Creating a model that classifies twitter replies.

# Background
Being a user of Twitter for many years now, it has definitely become my favourite social media platform. Most of this is due to how everyone popular in the world has some Twitter presence and how the lives of many are broadcasted through Twitter. Due to this nature of Twitter though, it makes it very easy for not so savoury opinions to get broadcasted to the world. One thing this results in is the creation of subtwitters which polarizes people and increases hostility. One place that I've seen the most hostility on is the reply section of Tweets. From experience, it's hard to read comments to even positive and wholesome tweets without someone projecting their hostile opinion. Thus, the main motivation behind this project is to see whether this is something that occurs frequently on Twitter or if it is just my selectional bias.

# Methods

First, I needed to collect data in order to train a classifier. For this, I used the Twitter API with the requests library in Python. I used the search endpoint in the API where I search for replies to a specific user. The max replies per request is 100 and using this method, sometimes I would only get 10 replies. Since this is mostly automated, I found it to be too slow. Instead, I searched replies by keyword which was much faster. 

The data collected was handlabelled and classified into 4 categories:
1. Positive/Encouraging
2. Neutral/Factual
3. Critical
4. Insulting/Obscene

# Creating the Classifier
## Preprocessing

In order for text to give the most amount of information, some preprocessing steps had to be taken. 
1. Removal of mentions, links, miscellaneous characters.
2. Removing punctuation and whitespace.
3. Removing one character words.

For example, the string 
```
@NicolleDWallace HEMP P PLANT-BASED ECONOMY  https://t.co/Jg0U0DOOEo
```
turns into 
```
hemp plant-based economy
```

I also found that puncutation such as '!' and '?' are more common in some labels than in others. I created a column/feature that determines whether a string has this punctuation or not. 

Lastly, I used the TFIDFVectorizer in order to tokenize the text.

## Training

To start, I used a dataset with 1500 entries to test this out. I tried using 3 different classifiers: XGBClassifier, Support Vector Classifier, and Multinomial Naive Bayes.
I took the average of 20 attempts using cross-validation with different train/test splits. 
