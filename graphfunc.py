import plotly.express as px
from dash import dcc

import requests
import imageio.v3 as iio
import io

import plotly.graph_objects as go

TEMPLATE_FONT_LEGEND = go.layout.Template(
    layout={
       "legend" : {
           'orientation':'h',
           'title_text':''
       },
        'title_font':{
            'family':'ArrialNarrow',
            'size':24
        },
    }
)

TEMPLATE_FONT = go.layout.Template(
    layout={
        'title_font':{
            'family':'ArrialNarrow',
            'size':24
        },
    }
)

def print_bar_by_sales(dataFrame):
    filtred_data = dataFrame.groupby(['Product Name']).agg({'Line Total': 'sum'}).reset_index()
    filtred_data.sort_values(by='Line Total', ignore_index=True, inplace=True)
    fig = px.bar(filtred_data, x="Product Name", y="Line Total", title="Продажи")
    fig.update_layout(xaxis_title="Продукт", yaxis_title="Рубли", template=TEMPLATE_FONT_LEGEND)
    return fig

def print_histo_rentable(dataFrame):
    filtred_data = dataFrame.copy(deep=True)
    fig = px.histogram(filtred_data, x="rentabel", color="Category", marginal="box")
    fig.update_layout(xaxis_title="Рентабельность", yaxis_title="Кол-во", template=TEMPLATE_FONT)
    return fig

def print_bar_by_district_subdistrict(dataFrame,type_layout:str):
    if type_layout == 'district':
        fig = px.histogram(dataFrame, x='District', y='Line Total')
        fig.update_layout(xaxis_title="Округ", yaxis_title="RUB", template=TEMPLATE_FONT)
        return fig
    if type_layout == 'subdistrict':
        fig = px.histogram(dataFrame, x='SubDistrict', y='Line Total')
        fig.update_layout(xaxis_title="Район", yaxis_title="RUB", template=TEMPLATE_FONT)
        return fig

def print_treemap_sales_district_subdistric(dataFrame):
    fig = px.treemap(dataFrame, path=[px.Constant("Москва"), 'District', 'SubDistrict', 'Category'],
                     values='Line Total', maxdepth=3)
    fig.update_traces(textinfo='label+percent parent')
    fig.update_layout(template=TEMPLATE_FONT)
    return fig

def print_box_price_for_one(dataFrame):
    fig = px.box(dataFrame, x='District', y='Unit Price', color="Category",)
    fig.update_layout(xaxis_title="Округ", yaxis_title="RUB", template=TEMPLATE_FONT)
    return fig

def print_pie_category(dataFrame):
    fig = px.pie(dataFrame, values='Line Total', names='Category')
    fig.update_layout(template=TEMPLATE_FONT_LEGEND)
    return fig

def print_line_dynamic(dataFrame):
    fig = px.line(dataFrame, x='OrderDate_month', y='Line Total')
    fig.update_layout(xaxis_title="Дата", yaxis_title="Всего", template=TEMPLATE_FONT)
    return fig

def print_from_api_pic(dataFrame):
    f_data_lat = str(dataFrame.loc[0, 'centroid_lat'])
    f_data_long = str(dataFrame.loc[0, 'centroid_long'])

    coord_str = ','.join([f_data_lat, f_data_long])

    url = f'https://static.maps.2gis.com/1.0?s=1024x768&c={coord_str}&z=18'

    response = requests.get(url)

    byte_stream = io.BytesIO(response.content)
    img = iio.imread(byte_stream, index=None)

    fig = px.imshow(img)
    fig.update_layout(dragmode="drawrect", width=800, height=600, template=TEMPLATE_FONT)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    config = {
        "modeBarButtonsToAdd": [
            "drawline",
            "drawopenpath",
            "drawclosedpath",
            "drawcircle",
            "drawrect",
            "eraseshape",
        ]
    }
    return dcc.Graph(figure=fig, config=config)

def print_moscow_map(dataFrame):
    fig = px.scatter_mapbox(dataFrame, lat='centroid_lat', lon='centroid_long',color='Warehouse Name', zoom=9,
                            hover_name='SchoolCustomer', mapbox_style='open-street-map')
    fig.update_layout(width=1024, height=768, template=TEMPLATE_FONT_LEGEND)
    return fig