from faker import Faker

fake = Faker(locale="ru_RU")


def make_new_fake_user_and_return_data():
    fake_email = fake.ascii_free_email()
    fake_password = fake.job()
    fake_name = fake.first_name()

    payload = {
        "email": fake_email,
        "password": fake_password,
        "name": fake_name
    }

    return payload
