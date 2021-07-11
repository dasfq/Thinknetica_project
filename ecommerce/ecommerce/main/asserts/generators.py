import random


def generate_code(digits_qty):
    from_ = 0
    to = 9
    return "".join([str(random.randint(from_, to)) for x in range(digits_qty)])


def generate_cache_key(object):
    model_name = object.__class__.__name__
    id = object.id
    return f"{model_name}_{id}"
