# ИМПОРТЫ

import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import geopandas as gpd
from graphfunc import print_bar_by_sales, print_histo_rentable, print_bar_by_district_subdistrict, print_line_dynamic, \
    print_treemap_sales_district_subdistric, print_box_price_for_one, print_pie_category, print_moscow_map, \
    print_from_api_pic

# ИНИЦИАЛИЗАЦИЯ ПРИЛОЖЕНИЯ И ЗАГРУЗКА ДАННЫХ
app = Dash(__name__,
           external_stylesheets=[
               dbc.themes.BOOTSTRAP,
               'assets/css/project.css',
               'assets/css/typography.css'],
           suppress_callback_exceptions=True
           )

df = pd.read_csv('data_for_otus.csv')

# Дата начало-конец периода
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
min_date = df['OrderDate'].min()
max_date = df['OrderDate'].max()

# Начало-конец слайдера
rent_max = df['rentabel'].max()
rent_min = df['rentabel'].min()

# Канал продаж
sales_options = [{'value':col,'label':col} for col in df['Channel'].unique().tolist()]

# Округа
district_options = [{'value':col,'label':col} for col in df['District'].unique().tolist()]

# ЭЛЕМЕНТЫ

sales_channel = dcc.Dropdown(
    id='sales_channel',
    options=sales_options,
    value=[],
    clearable=False,
    placeholder='Выберите канал продаж',
    multi=True
)

rentable_slider = dcc.RangeSlider(
    id='rent_slider',
    min=rent_min,
    max=rent_max,
    value=[rent_min,rent_max],
    dots=False,
    tooltip={"placement": "bottom", "always_visible": True}
)

date_range = dcc.DatePickerRange(
    id='data_filter',
    display_format='DD-MM-YYYY',
    min_date_allowed=min_date,
    max_date_allowed=max_date,
    start_date=min_date,
    end_date=max_date)

accept_button = dbc.Button('Выполнить',id='accept_button',n_clicks=0,className='me-1',color='warning')

district_dropdown = dcc.Dropdown(
    id='district_dropdown',
    options=district_options,
    value=[],
    clearable=True,
    placeholder='Весь город',
    multi=False
)

district_school_dropdown = dcc.Dropdown(
    id='district_dropdown_for_api',
    options=district_options,
    value=[],
    clearable=True,
    placeholder='Выберите округ',
    multi=False
)

# ВЁРСТКА
app.title = 'OTUS DASH'

graph_with_filters = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H6("Канал продаж")),
                dbc.CardBody(html.Div(sales_channel))])),
            dbc.Col(dbc.Card([
                dbc.CardHeader([html.H6("Процент рентабельности")]),
                dbc.CardBody(html.Div(rentable_slider))])),
            dbc.Col(dbc.Card([
                dbc.CardHeader(html.H6("Временной период")),
                dbc.CardBody(html.Div(date_range))]))
        ]),
        dbc.Row([
            dbc.Col(accept_button),
            dbc.Col()
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H4('Продажи'),
            dbc.Row(dcc.Graph(id='product_bar'))
        ]),
        dbc.Col([
            html.H4("Количество продаж с рентабельностью"),
            dbc.Row(dcc.Graph(id='histogram'))
        ])
    ]),
    dbc.Row([
        html.H4("Динамика продаж по месяцам"),
        dcc.Graph(id='line_order')
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Card([
                dbc.CardHeader(dbc.Row(html.H6('Выберите округ'))),
                dbc.CardBody(dbc.Row(html.Div(district_dropdown)))
            ]),
            dbc.Row(html.Div(id='change_graph'))
        ])
    ])


])

graph_without_filters = html.Div([
    dbc.Row(
        html.Div([
            html.H4('Иерархия продаж по округам, районам и категориям товаров'),
            dcc.Graph(figure=print_treemap_sales_district_subdistric(df))
        ])
    ),
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H4('Распределение цен за единицу товара по округам'),
                    dcc.Graph(figure=print_box_price_for_one(df))
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H4('Доля продаж по категориям товаров'),
                    dcc.Graph(figure=print_pie_category(df))
                ])
            )
        ])
    ])
])

maps = html.Div([
    dbc.Row(
        html.Div([
            html.H4('Распределение заказов школ на карте'),
            dcc.Graph(figure=print_moscow_map(df))
        ])
    ),
    dbc.Container(
        dbc.Row([
            dbc.Card([
                dbc.CardHeader(html.H6("Отображение школ на карте в зависимости от округа")),
                dbc.CardBody([
                    dbc.Row(html.Div(district_school_dropdown)),
                    dbc.Row(html.Div(id='school_api_dropdown')),
                ]),
            ]),
            dbc.Row(html.Div(id='school_api_pic'))
        ])
    )
])


app.layout = dbc.Container(
    html.Div([
    #     HEADER
        html.Div(
            dbc.Row([
                dbc.Col(html.Img(
                    src=app.get_asset_url("images/logo_black.png"),
                    style={'width':'200px','margin-top':'10px','margin-bottom':'10px'}),
                style={'width':'200px'}),
                dbc.Col(html.Div(html.H1('BI-dashboard on Dash')))]),className='app-header'
        ),
    # BODY
        html.Div([
            dbc.Card([
                dbc.CardHeader(
                    dbc.Tabs([
                        dbc.Tab(label='Графика с фильтрами', tab_id='graph_with_filters'),
                        dbc.Tab(label='Графика без фильтров', tab_id='graph_without_filters'),
                        dbc.Tab(label='Картографическая информация', tab_id='maps'),
                    ],
                        id='card-tabs',
                        active_tab='graph_with_filters')),
                dbc.CardBody(html.Div(id='card-content'))
            ]),
        ]),
    # FOOTER
        html.Div(
            dbc.Row([
                dbc.Col(html.Img(src=app.get_asset_url("images/logo-small_black.png"),style={'width':'200px'})),
                dbc.Col(html.Div(html.H3('OTUS. Курс «BI-аналитика»')),align='center'),
                dbc.Col(html.P("Колесник Андрей, 2024 г.")),
        ],align='center'),
        className='app-footer')
    ])
)

# CALLBACK'S (ФУНКЦИИ ОБРАТНОГО ВЫЗОВА)

@app.callback(
    Output(component_id='card-content',component_property='children'),
    Input(component_id='card-tabs',component_property='active_tab')
)
def tab_content(active_tab):
    if active_tab == 'graph_with_filters':
        return graph_with_filters
    if active_tab == 'graph_without_filters':
        return graph_without_filters
    if active_tab == 'maps':
        return maps

@app.callback(
    Output(component_id='product_bar',component_property='figure'),
    Input(component_id='accept_button',component_property='n_clicks'),
    State(component_id='sales_channel',component_property='value'),
    State(component_id='data_filter',component_property='start_date'),
    State(component_id='data_filter',component_property='end_date'),
    State(component_id='rent_slider',component_property='value')
)
def sales_channel_filter(n_clicks, value_sales_channel, start_date, end_date, range_value):

    if bool(value_sales_channel):
        f_data = df.copy(deep=True)
        f_data = f_data[f_data['Channel'].isin(value_sales_channel)]
    else:
        f_data = df.copy(deep=True)

    f_data = f_data[(f_data['rentabel'] >= range_value[0]) & (f_data['rentabel'] <= range_value[-1])]

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    f_data = f_data[(f_data['OrderDate'] >= start_date) & (f_data['OrderDate'] <= end_date)]

    return print_bar_by_sales(f_data)

@app.callback(
    Output(component_id='histogram',component_property='figure'),
    Input(component_id='rent_slider',component_property='value')
)
def one_filter_renta(range_value):
    f_data = df.copy(deep=True)
    f_data = f_data[(f_data['rentabel'] >= range_value[0]) & (f_data['rentabel'] <= range_value[-1])]
    return print_histo_rentable(f_data)

@app.callback(
    Output(component_id='change_graph',component_property='children'),
    Input(component_id='district_dropdown',component_property='value')
)
def sales_bar_by_district(value):
    f_data = df.copy(deep=True)

    if ctx.triggered[0]['value'] is None:
        return html.Div([
            html.H4('Сумма продаж по округам'),
            dcc.Graph(figure=print_bar_by_district_subdistrict(f_data, type_layout='district'))])
    else:
        f_data = f_data[f_data['District'].isin([value])].reset_index(drop=True)
        return html.Div([
            html.H4('Сумма продаж по районам'),
            dcc.Graph(figure=print_bar_by_district_subdistrict(f_data, type_layout='subdistrict'))])

@app.callback(
    Output(component_id='line_order',component_property='figure'),
    Input(component_id='sales_channel',component_property='value'),
    Input(component_id='data_filter',component_property='start_date'),
    Input(component_id='data_filter',component_property='end_date')
)
def sales_dynamic_my_month(value_sales_channel,start_date, end_date):

    if bool(value_sales_channel):
        f_data = df.copy(deep=True)
        f_data = f_data[f_data['Channel'].isin(value_sales_channel)]
    else:
        f_data = df.copy(deep=True)

    f_data = f_data[(f_data['OrderDate'] >= start_date) & (f_data['OrderDate'] <= end_date)]

    f_data['OrderDate_month'] = f_data['OrderDate'].dt.to_period('M')
    f_data['OrderDate_month'] = f_data['OrderDate_month'].astype(str)
    data_grouped = f_data.groupby('OrderDate_month')['Line Total'].sum().reset_index()

    return print_line_dynamic(data_grouped)

@app.callback(
    Output(component_id='school_api_dropdown',component_property='children'),
    Input(component_id='district_dropdown_for_api',component_property='value')
)
def print_api_dropdown(value):
    f_data = df.copy(deep=True)

    f_data = f_data[f_data['District'].isin([value])]

    school_option = [{'value':col,'label':col} for col in f_data['SchoolCustomer'].unique().tolist()]

    school_dropdown = dcc.Dropdown(
        id='school_dropdown',
        options=school_option,
        value=[],
        clearable=True,
        placeholder='Выберите школу',
        multi=False
    )

    if ctx.triggered[0]['value'] is None:
        return ''

    return school_dropdown

@app.callback(
    Output(component_id='school_api_pic',component_property='children'),
    Input(component_id='school_dropdown',component_property='value'),
    prevent_initial_call=True
)
def print_api_picture(value):
    if (ctx.triggered[0]['value'] is None):
        return ''
    if (len(ctx.triggered[0]['value']) == 0):
        return ''
    f_data = df.copy(deep=True)
    f_data = f_data[f_data['SchoolCustomer'].isin([ctx.triggered[0]['value']])].reset_index(drop=True)

    return html.Div([
        html.H4(f"Школа: {ctx.triggered[0]['value']}"),
        print_from_api_pic(f_data)
    ])

# ЗАПУСК ПРИЛОЖЕНИЯ

if __name__ == '__main__':
    app.run_server(debug=True)