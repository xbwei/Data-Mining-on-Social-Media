# Collect Senate Vote

The [collect_vote.py](https://github.com/xbwei/Data-Mining-on-Social-Media/blob/master/collect_senate_vote/collect_vote.py) can collect votes from the [Senate](https://www.senate.gov/legislative/votes.htm) website.

## Code Parameter
1. Define the url in `url_str = ''`, e..g, `url = 'https://www.senate.gov/legislative/LIS/roll_call_lists/roll_call_vote_cfm.cfm?congress=115&session=2&vote=00214'`
2. Defin the location of the database in `db_file = ''`

## Database
The python code uses an Access table. The tables include:
1. ![senator table](https://github.com/xbwei/Data-Mining-on-Social-Media/blob/master/collect_senate_vote/vote_table.PNG=100x20)
2. ![vote table](https://github.com/xbwei/Data-Mining-on-Social-Media/blob/master/collect_senate_vote/vote_table.PNG=100x20)

The relationship is defined as:

3. ![relation ship](https://github.com/xbwei/Data-Mining-on-Social-Media/blob/master/collect_senate_vote/relationship.PNG=100x20)

