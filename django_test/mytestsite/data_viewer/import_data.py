from pathlib import Path

import pandas as pd

from data_viewer.models import DataEntry, bin as BinModel


def import_data(clear_existing=False):
    base_dir = Path(__file__).resolve().parents[3]
    csv_file_path = base_dir / 'data' / 'raspberrypi_aws_truck_preprocessed.csv'
    csv_bins_file_path = base_dir / 'data' / 'raspberrypi_aws_truck_preprocessed_bins.csv'

    df = pd.read_csv(csv_file_path)
    df_bins = pd.read_csv(csv_bins_file_path)
    df['aws_ingest_ts_utc'] = pd.to_datetime(df['aws_ingest_ts_utc'], errors='coerce', utc=True)
    df = df.dropna(subset=['truck_id', 'aws_ingest_ts_utc', 'lat', 'lon', 'gross_weight_kg', 'payload_kg'])
    df_bins = df_bins.dropna(subset=['bin_name', 'lat', 'lon'])
    df_bins = df_bins.dropna(subset=['bin_name', 'lat', 'lon'])

    if clear_existing:
        DataEntry.objects.all().delete()

    entries = [
        DataEntry(
            truck_id=row['truck_id'],
            timestamp=row['aws_ingest_ts_utc'].to_pydatetime(),
            latitude=float(row['lat']),
            longitude=float(row['lon']),
            weight=float(row['gross_weight_kg']),
            payload_kg=float(row['payload_kg']) if 'payload_kg' in row and not pd.isna(row['payload_kg']) else None,
        )
        for _, row in df.iterrows()

    ]

    entries_bins = [
        BinModel(
            bin_id=row['bin_name'],
            lat=float(row['lat']),
            lon=float(row['lon']),
        )
        for _, row in df_bins.iterrows()
    ]

    DataEntry.objects.bulk_create(entries, batch_size=2000)
    BinModel.objects.bulk_create(entries_bins, batch_size=2000)
    return len(entries)