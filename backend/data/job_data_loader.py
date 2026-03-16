import pandas as pd
import os

def load_jobs():

    current_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(current_dir, "..", "..", "datasets", "jobs.csv")

    df = pd.read_csv(dataset_path)

    return df