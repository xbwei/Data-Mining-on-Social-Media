
# A serverless dashboard to analyze and visualize social media data in real-time


## Create Lambda functions
1.	Open AWS Console. Search and open AWS Lambda Service. 
2.	Create the first Lambda function
   2.1	Name: collect_tweets
    2.	Runtime: python 3.9
    3.	Execution role: the Exiting LabRole
    4.	Leave everything else as default, and create the function
    5.	Upload the collect_tweets.zip
    6.	In Configuration/General configuration:
      1. Memory: 500 MB
      2. Ephemeral storage: 1000 MB
      3. Timeout: 1 min
    7.  In Configuration/Environment variables, create the following variables and provide corresponding values:
      1. api_key
      2. api_secret
    •	access_token
    •	access_secret
    •	mongodb_connect
    •	database_name
    •	geocode
    •	q_parameter
2.8.	In Test, create a new event to test the function. 
2.9.	If the test is successful, add a trigger:
•	Source: EventBridge
•	Create a new rule
•	Name: every5min 
•	Schedule expression: rate(5 minutes)
3.	Create the second Lambda function
3.1.	Name: sentiment_tweets
3.2.	Runtime: python 3.9
3.3.	Execution role: the Exiting LabRole
3.4.	Leave everything else as default, and create the function
3.5.	Upload the sentiment_tweets.zip
3.6.	In Configuration/General configuration:
•	Memory: 500 MB
•	Ephemeral storage: 1000 MB
•	Timeout: 1 min
3.7.	In Configuration/Environment variables, create the following variables and provide corresponding values:
•	mongodb_connect
•	database_name
•	lang
3.8.	In Test, create a new event to test the function. 
3.9.	If the test is successful, add a trigger:
•	Source: EventBridge
•	Use existing rule: every5min 

## Create MongoDB dashboard

4.	Log in to the MongoDB website and find the final project database that contains the collected tweets. 
5.	Open MongoDB Chart and add a dashboard. Use the final project database as the data resource. Create the following charts and add filters to all charts to show the data from the last 60 mins. 
5.1.	A number chart to show the total number of collected Tweets
5.2.	A line chart to show the number of Tweets in different sentiments over time. Use the local time zone. 
5.3.	A word cloud to show the top 50 popular hashtags
5.4.	A bar chart to show the top 10 active Twitter users
5.5.	A table to show the Twitter texts, number of favorites, positive scores, and negative scores. 

