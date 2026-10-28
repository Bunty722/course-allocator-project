import os
import numpy as np

# 1. Master Seed (Requirement Step 4 & 10)
# This guarantees that every time we run the script, we get the exact same numbers.
RANDOM_SEED = 20261022

# Initialize the random number generator
rng = np.random.default_rng(RANDOM_SEED)

# 2. Volume Scales (Requirement Step 4)
# We parameterize this so we can test with a small batch before running the full 20,000.
SCALES = {
    "starter": {
        "programs": 10,
        "courses": 100,
        "faculty": 50,
        "student_plans": 2000
    },
    "full": {
        "programs": 100,
        "courses": 1000,
        "faculty": 500,
        "student_plans": 20000
    }
}

# 3. File Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)