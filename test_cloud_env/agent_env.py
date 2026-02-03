
import os
import sys
val = os.environ.get("TEST_ENV_KEY")
if val:
    print(f"FOUND: {val}")
else:
    print("NOT FOUND")
