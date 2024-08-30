"""
URL configuration for data_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from data_portal_app import views as views1
from data_portal_app.views import  data_records_geojson, data_records_choropleth, StaticHtmlView, upload_new_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload-csv/', views1.upload_csv, name='upload_csv'),
    path('', views1.map_datatable_view, name='map_datatable'),
    path('summary-json/', views1.summary_json, name='summary_json'),
    path('', include('data_visualization.urls')), 
    path('data-records-geojson/', data_records_geojson, name='data_records_geojson'),
    path('data-records-choropleth/', data_records_choropleth, name='data_records_choropleth'),
    path('static-html/', StaticHtmlView.as_view(), name='static_html_view'),
    path('upload-new-csv/', upload_new_csv, name='upload_new_csv'),
]
