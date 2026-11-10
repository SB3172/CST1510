# The column is named "value", not "Value" (case matters).
import pandas as pd

df = pd.DataFrame({"label": ["R-001", "R-002"], "value": [87, 120], "limit": [100, 100]})
print(df["value"])
