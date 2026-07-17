# Pattern: every run gets unique data so tests never collide with previous
# runs, or with everyone else practicing on the same public demo site.
import time
import random


def generate_unique_user() -> dict:
    suffix = f"{int(time.time())}_{random.randint(0, 999)}"
    return {
        "username": f"qauser_{suffix}",
        "password": f"TestPass_{suffix}!",
    }
