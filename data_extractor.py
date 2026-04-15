
import pandas as pd
from pathlib import Path

# Read CSV file into a DataFrame
csv_file_path = Path('data') / 'raspberrypi_aws_truck_preprocessed.csv'
df = pd.read_csv(csv_file_path)

# Iterate through the DataFrame and create model instances
it = 0
for index, row in df.iterrows():  # Process only a subset of rows for testing
    print("idx:", index, "row:", row)
    it += 1
    if it >= 5:  # Limit to the first 5 rows for testing    
        break

   