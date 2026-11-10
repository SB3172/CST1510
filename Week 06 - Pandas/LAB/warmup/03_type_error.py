# Convert numeric text to numbers before dividing.
import pandas as pd

df = pd.DataFrame({"value": ["87", "120", "45"], "limit": [100, 100, 100]})
df["value"] = pd.to_numeric(df["value"])
df["percent"] = (df["value"] / df["limit"]) * 100
print(df)
