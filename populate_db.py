import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from faker import Faker
import random
from datetime import datetime, timedelta
from events.models import Category, Event, Participant



def populate_db():
    # Initialize Faker
    fake = Faker()

    # Create Categories
    categories = [Category.objects.create(
        name=name,
        description=fake.sentence()
    ) for name in ['Tech', 'Workshop', 'Seminar', 'Webinar', 'Networking']]
    print(f"Created {len(categories)} categories.")

    # Create Events
    events = []
    for _ in range(15):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            date=fake.date_between(start_date='-7d', end_date='+30d'),
            time=fake.time_object(),
            location=fake.city(),
            category=random.choice(categories)
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # Create Participants
    participants = []
    for _ in range(25):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.email()
        )
        participant.event.set(random.sample(events, k=random.randint(1, 4)))
        participants.append(participant)
    print(f"Created {len(participants)} participants.")

    print("Populated TaskDetails for all tasks.")
    print("Database populated successfully!")

# Run it
if __name__ == "__main__":
    populate_db()
