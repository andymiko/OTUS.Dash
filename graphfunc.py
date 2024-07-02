import plotly.express as px

def print_bar_by_sales(dataFrame):
    filtred_data = dataFrame.groupby(['Product Name']).agg({'Line Total': 'sum'}).reset_index()
    filtred_data.sort_values(by='Line Total', ignore_index=True, inplace=True)
    fig = px.bar(filtred_data, x="Product Name", y="Line Total", title="Продажи")
    fig.update_layout(xaxis_title="Продукт", yaxis_title="Рубли")
    return fig