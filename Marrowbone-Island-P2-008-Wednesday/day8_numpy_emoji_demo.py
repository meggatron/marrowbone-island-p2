import numpy as np

# Generate a 5x5 weather grid with random values 0–3
grid = np.random.randint(0, 4, (5, 5))

# Define symbols for weather types
symbols = {
    0: "~",   # Clear
    1: "☁️",  # Cloudy
    2: "🌧",  # Rain
    3: "🔥"   # Heat wave
}

# Print the grid with symbols
for row in grid:
    line = " ".join(symbols[val] for val in row)
    print(line)