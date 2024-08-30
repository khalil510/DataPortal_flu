
# from django.urls import path

# from data_visualization.views import visualize_data, choose_table

# urlpatterns = [
#     path('viz/<str:table_name>/', visualize_data, name='visualize_data'),
#     path('choose_table/', choose_table, name='choose_table'),
# ]
from django.urls import path
from data_visualization.views import visualize_data

urlpatterns = [
    path('data_visualization/', visualize_data, name='visualize_data'),
]
