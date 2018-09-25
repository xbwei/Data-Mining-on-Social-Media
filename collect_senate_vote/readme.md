# Collect Senators' Votes

The [collect_vote.py](./collect_vote.py) can collect votes from the [Senate](https://www.senate.gov/legislative/votes.htm) website.

## Code Parameter
1. Define the url in `url_str = ''`, e..g, `url = 'https://www.senate.gov/legislative/LIS/roll_call_lists/roll_call_vote_cfm.cfm?congress=115&session=2&vote=00214'`
2. Defin the location of the database in `db_file = ''`

## Sample Query
1. A [sample](./query.sql) SQL is also provided.

<img src="./query_result.PNG" width="200">


## Database
Here is an example of collected data:
![collected data](./collected_data.PNG)

The python code uses an Access table. The tables include:
1. ![senator table](./vote_table.PNG )
2. ![vote table](./vote_table.PNG )

The relationship is defined as:

3. ![relation ship](./relationship.PNG )

