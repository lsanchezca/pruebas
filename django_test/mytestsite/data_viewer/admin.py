from django.contrib import admin

from .models import DataEntry


@admin.register(DataEntry)
class DataEntryAdmin(admin.ModelAdmin):
	list_display = ('truck_id', 'timestamp', 'latitude', 'longitude', 'weight', 'payload_kg')
	search_fields = ('truck_id',)
	list_filter = ('truck_id',)
	ordering = ('-timestamp',)
