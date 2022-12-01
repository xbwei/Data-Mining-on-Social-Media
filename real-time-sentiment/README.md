
# A serverless dashboard to analyze and visualize social media data in real-time

## Create Lambda functions

* Open AWS Console. Search and open AWS Lambda Service. 
* Create the first Lambda function
o Name: collect_tweets
o Runtime: python 3.9
o Execution role: the Exiting LabRole
o Leave everything else as default, and create the function
o Upload the collect_tweets.zip
o In Configuration/General configuration:
* Memory: 500 MB
* Ephemeral storage: 1000 MB
* Timeout: 1 min
o In Configuration/Environment variables, create the following variables and provide corresponding values:
* api_key
* api_secret
* access_token
* access_secret
* mongodb_connect
* database_name
* geocode
* q_parameter
o In Test, create a new event to test the function. 
o If the test is successful, add a trigger:
* Source: EventBridge
* Create a new rule
* Name: every5min 
* Schedule expression: rate(5 minutes)
* Create the second Lambda function
o Name: sentiment_tweets
o Runtime: python 3.9
o Execution role: the Exiting LabRole
o Leave everything else as default, and create the function
o Upload the sentiment_tweets.zip
o In Configuration/General configuration:
* Memory: 500 MB
* Ephemeral storage: 1000 MB
* Timeout: 1 min
o In Configuration/Environment variables, create the following variables and provide corresponding values:
* mongodb_connect
* database_name
* lang
o In Test, create a new event to test the function. 
o If the test is successful, add a trigger:
* Source: EventBridge
* Use existing rule: every5min 

## Create MongoDB dashboard

* Log in to the MongoDB website and find the final project database that contains the collected tweets. 
* Open MongoDB Chart and add a dashboard. Use the final project database as the data resource. Create the following charts and add filters to all charts to show the data from the last 60 mins. 
o A number chart to show the total number of collected Tweets
o A line chart to show the number of Tweets in different sentiments over time. Use the local time zone. 
o A word cloud to show the top 50 popular hashtags
o A bar chart to show the top 10 active Twitter users
o A table to show the Twitter texts, number of favorites, positive scores, and negative scores. 
