from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import BirdFluData
from .forms import CSVUploadForm
import csv
from io import TextIOWrapper

@admin.register(BirdFluData)
class BirdFluDataAdmin(admin.ModelAdmin):
    list_display = ('country', 'start_date_collected', 'end_date_collected', 'new_outbreaks', 'cumulative_outbreaks')

    def import_csv_view(self, request):
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
                self.message_user(request, "CSV file imported successfully.")
                return redirect('admin:data_portal_app_birdfludata_changelist')  # Redirect to change list view
            else:
                self.message_user(request, "Error importing CSV file: Invalid form submission.", level='error')

        else:
            form = CSVUploadForm()

        context = {
            'form': form,
            'title': 'Import CSV',
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
        }
        return render(request, 'admin/import_csv.html', context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv_view), name='import_csv'),
        ]
        return custom_urls + urls
