# Inside data_portal_app/views.py

from django.shortcuts import render
from django.contrib import messages
from .forms import CSVUploadForm
from .models import BirdFluData
import csv
from io import TextIOWrapper
from django.http import JsonResponse
from django.db.models import Count
import os
import json
from django.views.generic import TemplateView
from .forms import NewDataCSVUploadForm
from .models import NewData
from datetime import datetime
from dateutil import parser

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
            for row in reader:
                BirdFluData.objects.create(
                    start_date_collected=row['Start date collected'],
                    end_date_collected=row['End date collected'],
                    region=row['Region'],
                    iso_code=row['ISO code'],
                    country_code=row['Country code'],
                    country=row['Country'],
                    latitude=float(row['Lat']),
                    longitude=float(row['Long']),
                    hpai_strain=row['HPAI strain'],
                    woah_classification=row['WOAH Classification'],
                    new_outbreaks=int(row['New outbreaks']),
                    cumulative_outbreaks=int(row['Cumulative outbreaks'])
                )
            messages.success(request, 'CSV file uploaded successfully.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = CSVUploadForm()
    
    return render(request, 'upload_csv.html', {'form': form})



def upload_new_csv(request):
    if request.method == 'POST':
        form = NewDataCSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
            chunk_size = 1000  # Number of rows per chunk
            chunk = []

            for row in reader:
                try:
                    date = parser.parse(row['date']).strftime('%Y-%m-%d')
                except (ValueError, KeyError):
                    messages.error(request, f"Date format error: {row['date']}")
                    continue

                try:
                    latitude_str = row['latitude'].strip()
                    longitude_str = row['longitude'].strip()

                    if latitude_str == '' or longitude_str == '':
                        continue

                    latitude = float(latitude_str)
                    longitude = float(longitude_str)
                except ValueError:
                    messages.error(request, f"Invalid float value: Latitude='{row['latitude']}', Longitude='{row['longitude']}'")
                    continue

                chunk.append(NewData(
                    fid=int(row['fid']),
                    species=row['species'],
                    latitude=latitude,
                    longitude=longitude,
                    date=date
                ))

                if len(chunk) >= chunk_size:
                    NewData.objects.bulk_create(chunk)
                    chunk = []

            if chunk:
                NewData.objects.bulk_create(chunk)

            messages.success(request, 'CSV file uploaded successfully.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = NewDataCSVUploadForm()
    
    return render(request, 'upload_new_csv.html', {'form': form})





def map_datatable_view(request):
    birdflu_data = BirdFluData.objects.all()
    context = {
        'birdflu_data': birdflu_data,
    }
    return render(request, 'data_portal_app/map_datatable.html', context)


def summary_and_data(request):
    num_countries = BirdFluData.objects.values('country').distinct().count()
    num_regions = BirdFluData.objects.values('region').distinct().count()
    num_hpai_strains = BirdFluData.objects.values('hpai_strain').distinct().count()
    num_woah_classes = BirdFluData.objects.values('woah_classification').distinct().count()
    
    context = {
        'num_countries': num_countries,
        'num_regions': num_regions,
        'num_hpai_strains': num_hpai_strains,
        'num_woah_classes': num_woah_classes,
    }
    
    return render(request, 'your_template.html', context)

def summary_json(request):
    num_countries = BirdFluData.objects.values('country').distinct().count()
    num_regions = BirdFluData.objects.values('region').distinct().count()
    num_hpai_strains = BirdFluData.objects.values('hpai_strain').distinct().count()
    num_woah_classes = BirdFluData.objects.values('woah_classification').distinct().count()
    
    summary = {
        'num_countries': num_countries,
        'num_regions': num_regions,
        'num_hpai_strains': num_hpai_strains,
        'num_woah_classes': num_woah_classes,
    }
    
    return JsonResponse(summary)

def data_records_geojson(request):
    data = {
        "type": "FeatureCollection",
        "features": []
    }

    for record in BirdFluData.objects.all():
        data["features"].append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [record.longitude, record.latitude]
            },
            "properties": {
                "hpai_strain": record.hpai_strain,
                "woah_classification": record.woah_classification,
                "country": record.country,
                "new_outbreaks": record.new_outbreaks,
                "cumulative_outbreaks": record.cumulative_outbreaks
            }
        })

    return JsonResponse(data, safe=False)

def data_records_choropleth(request):
    try:
        geojson_path = os.path.join(os.path.dirname(__file__), 'static', 'data_app', 'geojson', 'custom.geo.json')
        with open(geojson_path, encoding='utf-8') as f:
            geojson_data = json.load(f)

        data = BirdFluData.objects.values('country').annotate(hpai_count=Count('hpai_strain'))
        hpai_counts = {item['country']: item['hpai_count'] for item in data}

        for feature in geojson_data['features']:
            country_name = feature['properties'].get('name')
            feature['properties']['hpai_count'] = hpai_counts.get(country_name, 0)

        return JsonResponse(geojson_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

class StaticHtmlView(TemplateView):
    template_name = 'kepler_migration.html'
    


def new_data_geojson(request):
    data = list(NewData.objects.values('latitude', 'longitude', 'species', 'date'))
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [item['longitude'], item['latitude']]
                },
                "properties": {
                    "species": item['species'],
                    "date": item['date']
                }
            }
            for item in data
        ]
    }
    return JsonResponse(geojson)


