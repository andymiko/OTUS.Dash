# ИМПОРТЫ

import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import geopandas as gpd
from graphfunc import print_bar_by_sales

# ИНИЦИАЛИЗАЦИЯ ПРИЛОЖЕНИЯ И ЗАГРУЗКА ДАННЫХ

df = pd.read_csv('data_for_otus.csv')

app = Dash(__name__)

# ЭЛЕМЕНТЫ

# ВЁРСТКА
app.title = 'OTUS DASH'
app.layout = html.Div([
    html.H1("HELLO WORLD!"),
    dcc.Graph(figure=print_bar_by_sales(dataFrame=df))
])

# CALLBACK'S (ФУНКЦИИ ОБРАТНОГО ВЫЗОВА)

# ЗАПУСК ПРИЛОЖЕНИЯ

if __name__ == '__main__':
    app.run_server(debug=True)