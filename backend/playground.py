import pandas as pd

df = pd.read_csv("data/event_performance.csv", parse_dates=["date"])

print(df.groupby("category")[["views", "registrations", "ad_spend"]].sum())