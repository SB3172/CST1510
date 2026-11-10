# Handle nonnumeric values without crashing.
raw_line = "srv-01,used=unknown,total=100"
hostname_part, rest = raw_line.split(",", 1)
print("Hostname:", hostname_part.strip())
for piece in rest.split(","):
    key, value = piece.split("=", 1)
    key = key.strip()
    value = value.strip()
    try:
        print(key, float(value))
    except ValueError:
        print(f"{key}: invalid number ({value})")
