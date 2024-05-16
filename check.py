from random import choice, randint, shuffle


def generate_nin():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    cert_list = []

    [cert_list.append(choice(letters)) for _ in range(6)]
    [cert_list.append(choice(numbers)) for _ in range(4)]

    shuffle(list(cert_list))
    nin = ''.join(cert_list)

    return nin


print(generate_nin())
