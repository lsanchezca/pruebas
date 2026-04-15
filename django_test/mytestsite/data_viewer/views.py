from django.http import JsonResponse
from django.shortcuts import render

from .models import DataEntry, bin

# Create your views here.
def view_data(request):
    return render(request, 'data_viewer/view_data.html')


def view_map(request):
    return render(request, 'data_viewer/view_map.html')


def _serialize_row(entry):
    return {
        'truck_id': entry.truck_id,
        'event_ts_display': entry.timestamp.isoformat(),
        'event_type': 'telemetry',
        'lat': entry.latitude,
        'lon': entry.longitude,
        'gross_weight_kg': entry.weight,
        'payload_kg': entry.payload_kg,
    }


def api_data(request):
    queryset = DataEntry.objects.order_by('-timestamp')
    total_points = queryset.count()

    # Latest points for each truck for summary cards.
    latest_by_truck = {}
    for entry in queryset.iterator(chunk_size=2000):
        if entry.truck_id not in latest_by_truck:
            latest_by_truck[entry.truck_id] = entry

    active_trucks = len(latest_by_truck)
    avg_gross_weight = 0
    if active_trucks:
        avg_gross_weight = round(
            sum(item.weight for item in latest_by_truck.values()) / active_trucks,
            2,
        )

    rows = [_serialize_row(entry) for entry in queryset[:400]]

    return JsonResponse(
        {
            'dataset_path': 'SQLite table: data_viewer_dataentry',
            'total_points': total_points,
            'active_trucks': active_trucks,
            'avg_gross_weight': avg_gross_weight,
            'rows': rows,
        }
    )


def api_map(request):
    queryset = DataEntry.objects.order_by('-timestamp')

    latest_by_truck = {}
    for entry in queryset.iterator(chunk_size=2000):
        if entry.truck_id not in latest_by_truck:
            latest_by_truck[entry.truck_id] = entry

    markers = [
        {
            'truck_id': entry.truck_id,
            'lat': entry.latitude,
            'lon': entry.longitude,
            'gross_weight_kg': entry.weight,
            'payload_kg': entry.payload_kg,
            'event_type': 'telemetry',
            'event_ts': entry.timestamp.isoformat(),
            'marker_type': 'truck',
        }
        for entry in latest_by_truck.values()
    ]

    # Obtener todos los bins (puntos de entrega fijos)
    bins_queryset = bin.objects.all()
    bins_data = [
        {
            'bin_id': b.bin_id,
            'lat': b.lat,
            'lon': b.lon,
            'marker_type': 'bin',
        }
        for b in bins_queryset
    ]

    return JsonResponse(
        {
            'dataset_path': 'SQLite table: data_viewer_dataentry & data_viewer_bin',
            'trucks_count': len(markers),
            'bins_count': len(bins_data),
            'markers': markers,
            'bins': bins_data,
        }
    )


