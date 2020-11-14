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

# Timezone for USA:
timezone_list = [
    "US/Central",
    "US/Eastern",
    "US/Pacific",
    "US/Mountain",
    "US/Alaska",
    "US/Hawaii",
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

    i += 1

