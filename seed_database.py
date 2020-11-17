"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime
from faker import Faker

import crud
import model
import server

os.system("dropdb sleeps")  # NOTE: Correct naming database variable
os.system("createdb sleeps")

model.connect_to_db(server.app)
model.db.create_all()

# TODO Uncomment out other timezones!!!
# Timezone for USA:
timezone_list = [
    "US/Central",
    # "US/Eastern",
    # "US/Pacific",
    # "US/Mountain",
    # "US/Alaska",
    # "US/Hawaii",
]

# Use Faker to generate and seed database:
fake = Faker()

# NOTE: Random emails don't match user first and last name...might want to change this design?
# Part 1: Generate 10 Users
i = 0
while i < 5:
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.unique.email()
    password = fake.unique.building_number()
    timezone = choice(timezone_list)

    user = crud.create_user(first_name, last_name, email, password, timezone)

    # Seed the database with fake sleep log data
    # user_sleep_log = crud.create_sleep_log(user_id = 7, )

    i += 1

i = 0
while i < 1:

    # Seed the database with fake sleep log data
    with open("sleep_logs.txt") as file:
        for line in file:
            words = line.split("|")
            user_sleep_log = crud.create_sleep_log(
                words[0], words[1], words[2], words[3]
            )

    #     data_file = open(filename)
    # for line in data_file:
    #     words = line.split("|")
    #     houses.add(words[2])
    # user_sleep_log = crud.create_sleep_log(user_id = 7, )

    i += 1

