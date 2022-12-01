
# A serverless dashboard to analyze and visualize social media data in real-time

## Create Lambda functions

1)	Open AWS Console. Search and open AWS Lambda Service. 
2)	Create the first Lambda function
a)	Name: collect_tweets
b)	Runtime: python 3.9
c)	Execution role: the Exiting LabRole
d)	Leave everything else as default, and create the function
e)	Upload the collect_tweets.zip
f)	In Configuration/General configuration:
i)	Memory: 500 MB
ii)	Ephemeral storage: 1000 MB
iii)	Timeout: 1 min
g)	In Configuration/Environment variables, create the following variables and provide corresponding values:
i)	api_key
ii)	api_secret
iii)	access_token
iv)	access_secret
v)	mongodb_connect
vi)	database_name
vii)	geocode
viii)	q_parameter
h)	In Test, create a new event to test the function. 
i)	If the test is successful, add a trigger:
i)	Source: EventBridge
ii)	Create a new rule
iii)	Name: every5min 
iv)	Schedule expression: rate(5 minutes)
3)	Create the second Lambda function
a)	Name: sentiment_tweets
b)	Runtime: python 3.9
c)	Execution role: the Exiting LabRole
d)	Leave everything else as default, and create the function
e)	Upload the sentiment_tweets.zip
f)	In Configuration/General configuration:
i)	Memory: 500 MB
ii)	Ephemeral storage: 1000 MB
iii)	Timeout: 1 min
g)	In Configuration/Environment variables, create the following variables and provide corresponding values:
i)	mongodb_connect
ii)	database_name
iii)	lang
h)	In Test, create a new event to test the function. 
i)	If the test is successful, add a trigger:
i)	Source: EventBridge
ii)	Use existing rule: every5min 


## Create MongoDB dashboard

* Log in to the MongoDB website and find the final project database that contains the collected tweets. 
* Open MongoDB Chart and add a dashboard. Use the final project database as the data resource. Create the following charts and add filters to all charts to show the data from the last 60 mins. 
o A number chart to show the total number of collected Tweets
o A line chart to show the number of Tweets in different sentiments over time. Use the local time zone. 
o A word cloud to show the top 50 popular hashtags
o A bar chart to show the top 10 active Twitter users
o A table to show the Twitter texts, number of favorites, positive scores, and negative scores. 
