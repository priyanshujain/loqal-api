from random import choice as random_choice


def random_string_generator(size=10, chars=ascii_lowercase + digits):
    return "".join(random_choice(chars) for _ in range(size))
