import random

def generate_code(digits_qty):
    from_ = 0
    to = 9
    return "".join([str(random.randint(from_, to)) for x in range(digits_qty)])