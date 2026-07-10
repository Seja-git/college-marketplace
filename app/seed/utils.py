import random
def choose_condition():

    return random.choice([
        "Like New",
        "Excellent",
        "Good",
        "Fair"
    ])

CONDITION_MULTIPLIER = {
    "Like New": 0.95,
    "Excellent": 0.85,
    "Good": 0.70,
    "Fair": 0.55
}

def generate_price(price_range, condition):
    base_price = random.randint(
        price_range[0],
        price_range[1]
    )

    return int(base_price * CONDITION_MULTIPLIER[condition])

def generate_views():

    return random.randint(0,500)

def generate_likes():

    return random.randint(0,50)

def random_bool():

    return random.choice([True,False])

def random_rating():

    return round(random.uniform(3.5,5.0),1)

def generate_quantity():

    return random.randint(1,5)