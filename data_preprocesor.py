import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler

data_file = Path('data') / 'raspberrypi_aws_truck_raw_simulated.csv'
csv = pd.read_csv(data_file)
csv = csv.drop_duplicates()

csv['aws_ingest_ts_utc'] = pd.to_datetime(csv['aws_ingest_ts_utc'], errors='coerce')

# The raw file uses decimal comma in some numeric fields (e.g. -34,5583).
csv['lat'] = pd.to_numeric(csv['lat'].astype(str).str.replace(',', '.', regex=False), errors='coerce')
csv['lon'] = pd.to_numeric(csv['lon'].astype(str).str.replace(',', '.', regex=False), errors='coerce')
csv['gross_weight_kg'] = pd.to_numeric(csv['gross_weight_kg'], errors='coerce')
csv['payload_kg'] = pd.to_numeric(csv['payload_kg'], errors='coerce')
csv = csv.dropna(subset=['aws_ingest_ts_utc', 'lat', 'lon', 'gross_weight_kg', 'payload_kg'])

scaler = StandardScaler()
# scaled_values = scaler.fit_transform(csv[ 'gross_weight_kg'])
# csv[ 'gross_weight_kg'] = scaled_values

new_csv = csv[['truck_id', 'aws_ingest_ts_utc', 'lat', 'lon', 'gross_weight_kg', 'payload_kg']]

# Crear tabla única de coordenadas (sin repetidos)
coords_unicas = (
    csv[["lat", "lon"]]
    .drop_duplicates()
    .sort_values(["lat", "lon"])
    .reset_index(drop=True)
)

# Asignar nombre: bin1, bin2, bin3...
coords_unicas["bin_name"] = ["bin" + str(i + 1) for i in coords_unicas.index]

print(coords_unicas.head())

print(new_csv.head())


new_csv.to_csv(Path('data') / 'raspberrypi_aws_truck_preprocessed.csv', index=False)
coords_unicas.to_csv(Path('data') / 'raspberrypi_aws_truck_preprocessed_bins.csv', index=False)