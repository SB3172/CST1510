# Split only at the first equals sign so the value may contain "=".
piece = "note=server=east"
key, value = piece.split("=", 1)
print(key, value)
