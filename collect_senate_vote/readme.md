# Collect Senators' Votes

The [collect_vote.py](./collect_vote.py) can collect votes from the [Senate](https://www.senate.gov/legislative/votes.htm) website.

## Code Parameter
1. Define the url in `url_str = ''`, e..g, `url = 'https://www.senate.gov/legislative/LIS/roll_call_lists/roll_call_vote_cfm.cfm?congress=115&session=2&vote=00214'`
2. Defin the location of the database in `db_file = ''`

## Sample Query
A [sample](./query.sql) SQL is  provided.

<img src="./query_result.PNG" width="200">


## Database
Here is an example of collected data:

<img src="./collected_data.PNG" width="400">


The python code uses an Access table. The tables include:

1. A senator table:

<img src="./senator_table.PNG" width="300">

2. A vote table:

<img src="./vote_table.PNG" width="300">


The relationship is defined as:

<img src="./relationship.PNG" width="300">


