def camel_clase(snake_case: str):
    init, *temp = snake_case.lower().split('_')
    # using map() to get all words other than 1st
    # and titlecasing them
    res = ''.join([init.lower(), *map(str.title, temp)])

    return res