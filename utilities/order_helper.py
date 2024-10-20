from utilities.generator_data import generate_random_string

valid_ingredients = {"ingredients": ['61c0c5a71d1f82001bdaaa70', '61c0c5a71d1f82001bdaaa6c']}
empty_ingredients = {'ingredients': []}
invalid_ingredients = {"ingredients": ['61c0c5a711bdaaa70', '61c0c5a001bdaaa6c']}


def generate_user_data():
    user = {
        "email": f"{generate_random_string(8)}@yandex.ru",
        "password": generate_random_string(10),
        "name": generate_random_string(8)
    }
    return user
