
import random
from datetime import datetime
random.seed(datetime.now())


result = random.randrange(1,4)

if result ==3:
    print ('Make attendance!')
else:
    print ('No, Python loves you :)')
