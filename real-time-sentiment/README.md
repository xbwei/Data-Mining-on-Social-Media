
# A serverless dashboard to analyze and visualize social media data in real-time

## Create Lambda functions

1.	Open AWS Console. Search and open AWS Lambda Service. 
2.	Create the first Lambda function
    1.	Name: `collect_tweets`
    2.	Runtime: `python 3.9`
    3.	Leave everything else as default, and create the function
    4.	Upload the [collect_tweets.zip](https://github.com/xbwei/Data-Mining-on-Social-Media/blob/master/real-time-sentiment/collect_tweets.zip)
    5.	In Configuration/General configuration:
        - Memory: `500 MB`
        - Ephemeral storage: `1000 MB`
        - Timeout: `1 min`
    6.	In Configuration/Environment variables, create the following variables and provide corresponding values:
        - `api_key`
        - `api_secret`
        - `access_token`
        - `access_secret`
        - `mongodb_connect`
        - `database_name`
        - `geocode`
        - `q_parameter`
    7.	In Test, create a new event to test the function. 
    8.	If the test is successful, add a trigger:
        - Source: `EventBridge`
        - Create a new rule
        - Name: `every5min`
        - Schedule expression: `rate(5 minutes)`
3.	Create the second Lambda function
    1.	Name: `sentiment_tweets`
    2.	Runtime: `python 3.9`
    3.	Leave everything else as default, and create the function
    4.	Upload the [sentiment_tweets.zip](https://github.com/xbwei/Data-Mining-on-Social-Media/blob/master/real-time-sentiment/sentiment_tweets.zip)
    5.	In Configuration/General configuration:
        - Memory: `500 MB`
        - Ephemeral storage: `1000 MB`
        - Timeout: `1 min`
    6.	In Configuration/Environment variables, create the following variables and provide corresponding values:
        - `mongodb_connect`
        - `database_name`
        - `lang`
    7.	In Test, create a new event to test the function. 
    8.	If the test is successful, add a trigger:
        - Source: `EventBridge`
        - Use existing rule: `every5min`

## Create MongoDB dashboard

4.	Log in to the MongoDB website and find the final project database that contains the collected tweets. 
5.	Open MongoDB Chart and add a dashboard. Use the final project database as the data resource. Create the following charts and add filters to all charts to show the data from the last 60 mins. 
    1.	A number chart to show the total number of collected Tweets
    2.	A line chart to show the number of Tweets in different sentiments over time. Use the local time zone. 
    3.	A word cloud to show the top 50 popular hashtags
    4.	A bar chart to show the top 10 active Twitter users
    5.	A table to show the Twitter texts, number of favorites, positive scores, and negative scores. 

