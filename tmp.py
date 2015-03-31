import os
import re
from glob import glob
from unidecode import unidecode
from datetime import datetime,date

from elly import *

usernames = [ "asdf3m", "eqrt2m", "a1m" ]

    

for u in usernames:
    print(getClassFromUsername(u))
