
# A serverless dashboard to analyze and visualize social media data in real-time


, open AWS Console. Search and open AWS Lambda Service. 
4.	Create the first Lambda function
4.1.	Name: collect_tweets
4.2.	Runtime: python 3.9
4.3.	Execution role: the Exiting LabRole
4.4.	Leave everything else as default, and create the function
4.5.	Upload the collect_tweets.zip
4.6.	In Configuration/General configuration:
•	Memory: 500 MB
•	Ephemeral storage: 1000 MB
•	Timeout: 1 min
4.7.	In Configuration/Environment variables, create the following variables and provide corresponding values:
•	api_key
•	api_secret
•	access_token
•	access_secret
•	mongodb_connect
•	database_name
•	geocode
•	q_parameter
4.8.	In Test, create a new event to test the function. 
4.9.	If the test is successful, add a trigger:
•	Source: EventBridge
•	Create a new rule
•	Name: every5min 
•	Schedule expression: rate(5 minutes)
5.	Create the second Lambda function
5.1.	Name: sentiment_tweets
5.2.	Runtime: python 3.9
5.3.	Execution role: the Exiting LabRole
5.4.	Leave everything else as default, and create the function
5.5.	Upload the sentiment_tweets.zip
5.6.	In Configuration/General configuration:
•	Memory: 500 MB
•	Ephemeral storage: 1000 MB
•	Timeout: 1 min
5.7.	In Configuration/Environment variables, create the following variables and provide corresponding values:
•	mongodb_connect
•	database_name
•	lang
5.8.	In Test, create a new event to test the function. 
5.9.	If the test is successful, add a trigger:
•	Source: EventBridge
•	Use existing rule: every5min 
6.	Log in to the MongoDB website and find the final project database that contains the collected tweets. 
7.	Open MongoDB Chart and add a dashboard. Use the final project database as the data resource. Create the following charts and add filters to all charts to show the data from the last 60 mins. 
7.1.	A number chart to show the total number of collected Tweets
7.2.	A line chart to show the number of Tweets in different sentiments over time. Use the local time zone. 
7.3.	A word cloud to show the top 50 popular hashtags
7.4.	A bar chart to show the top 10 active Twitter users
7.5.	A table to show the Twitter texts, number of favorites, positive scores, and negative scores. 
