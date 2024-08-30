from django.shortcuts import render, redirect
from django.db import connections
import pandas as pd
import pygwalker as pyg

def get_tables():
    # Utility function to get a list of tables from PostgreSQL
    with connections['default'].cursor() as cursor:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
    return tables

def visualize_data(request):
    tables = get_tables()
    table_name = None
    walker_html = None

    if request.method == 'POST':
        # Get the selected table from the form
        table_name = request.POST.get('table')

        # Fetch data from the selected table in PostgreSQL
        with connections['default'].cursor() as cursor:
            cursor.execute(f'SELECT * FROM {table_name}')
            data = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

        # Convert data to a DataFrame
        df = pd.DataFrame(data, columns=columns)

        # Create Pygwalker visualization and generate HTML
        walker = pyg.walk(df)
        walker_html = walker.to_html()  # Use the correct method to get HTML

    # Render the template with the table list and optional visualization
    context = {
        'tables': tables,
        'table_name': table_name,
        'walker_html': walker_html,
    }
    return render(request, 'data_visualization/data_visualization.html', context)