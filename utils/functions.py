# FUNCTIONS

import random

# Pick random value between two given ranges
def high_low_rand(ll, lh, hl, hh):
    if random.choice([True, False]):
        return random.randint(ll, lh)
    else:
        return random.randint(hl, hh)