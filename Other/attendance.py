'''
I make attendance for 1/2 of classes.
This script will decide whether or not I should
make attendance for today's class.
'''

import random
from datetime import datetime
random.seed(datetime.now())


print (datetime.now())

result = random.randrange(1,3)

if result ==1:
    print ('Make attendance!')
else:
    print ('No, Python loves you :)')
