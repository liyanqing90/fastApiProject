x = {
    "username": "johndoe",
    "full_name": "John Doe",
    "email": "johndoe@example.com",
    "hashed_password": "fakehashedsecret",
    "disabled": False,
}

print(x)


def p(username, full_name, email, hashed_password, disabled):
    print(username, full_name)


p(**x)
