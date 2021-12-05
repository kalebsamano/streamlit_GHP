import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from frames import data_plot1_df, data_plot2_df, data_plot3_df, purchase_data_detail_unit98, purchase_data_detail_net98, purchase_data_detail_quant98, data_plot5_df, data_plot6_df, data_plot7_df, data_plot8_df

def get_vendor_analysis_interface2():

    # page format
    st.title('Analisis de vendedores')
    pd.set_option('display.max_columns', None)

    # PLOT 1
    fig = px.scatter(
        data_plot1_df, 
        y="venue_name", 
        x="count", 
        color="vendor_negotiation_type", 
        template = 'plotly_white', 
        color_discrete_map={"Corporate": "#BF9F63", "Local": "#0C3140"})
    fig.update_traces(marker_size=10)
    fig.update_layout(
        title = 'Número de compras con tipo de proveedor', 
        height = 800, 
        width = 1200
        )
    st.plotly_chart(fig)

    # PLOT 2
    fig = go.Figure(data_plot2_df)
    fig.update_layout(
        barmode = 'stack', 
        title='Proporción de compras por hotel y por tipo de proveedor', 
        plot_bgcolor = 'white'
        )
    st.plotly_chart(fig)

    # PLOT 3
    fig = go.Figure()  
    fig.add_trace( 
        go.Indicator(
        title = {'text': "Precio por unidad"},
        mode = "number",
        value = np.percentile(data_plot3_df['unit_price'], 95),
        number = {'prefix': "$"},
        domain = {'row': 1, 'column': 0},
        title_font_color = '#BF9460'))
    fig.add_trace( 
        go.Indicator(
        title = {'text': "Importe total de compra"},
        mode = "number",
        value = np.percentile(data_plot3_df['net_value'], 95),
        number = {'prefix': "$"},
        domain = {'row': 1, 'column': 1},
        title_font_color = '#EF7C20'))
    fig.add_trace( 
        go.Indicator(
        title = {'text': "Cantidad"},
        mode = "number",
        value = np.percentile(data_plot3_df['quantity'], 95),
        domain = {'row': 1, 'column': 2},
        title_font_color = '#0D0D0D'))
    fig.update_layout(
        title = 'Percentil 95%: Límite en donde 95% de los datos son menores', 
        paper_bgcolor = "white", 
        grid = {'rows': 1, 'columns': 3}
        )
    st.plotly_chart(fig)

    # PLOT 4
    fig = make_subplots(
        rows=1, 
        cols=3, 
        subplot_titles=('Precio de cada unidad', 'Cantidad', 'Importe total de compra')
        )
    fig.add_trace(
        go.Box(
            y = purchase_data_detail_unit98['unit_price'], 
            x = purchase_data_detail_unit98['vendor_negotiation_type'], 
            marker_color = '#BF9460',
            name = 'Precio de cada unidad'
            ),
        row = 1, col = 1    
    )
    fig.add_trace(
        go.Box(
            y = purchase_data_detail_quant98['quantity'], 
            x = purchase_data_detail_quant98['vendor_negotiation_type'], 
            marker_color = '#EF7C20',
            name = 'Cantidad'
            ),
        row = 1, col = 2
    )
    fig.add_trace(
        go.Box(
            y = purchase_data_detail_net98['net_value'], 
            x = purchase_data_detail_net98['vendor_negotiation_type'], 
            marker_color = '#0D0D0D',
            name = 'Importe total de compra'
            ),
        row = 1, col = 3
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gainsboro')
    fig.update_layout(
        title_text="Comparación de variables por tipo de proveedor", 
        height = 700, 
        plot_bgcolor='white'
        )
    st.plotly_chart(fig)

    # PLOT 5
    colors = {
        'Fruits & Vegetables':'#bfa48a', 
        'Cleaning accesories':'#1b1715', 
        'Dairy Products':'#5f4d3d', 
        'Meats':'#4d3525',
        'Food and Beverages Supplies':'#ded7c5', 
        'Poultry':'#4d6881', 
        'Bakery':'#b26603', 
        'Cereals and Legumes':'#855832',
        'Sausages':'#efd8ac', 
        'Office Supplies':'#27394f', 
        'Tortillas': 'darkorange', 
        'Soft Drinks':'dimgray', 
        'Hardware Store':'darkblue', 
        'Amenities':'lightblue', 
        'Juices':'lightsteelblue'
        }
    # initiate data list for figure
    data = []
    #use for loop on every zoo name to create bar data
    for x in data_plot5_df.columns:
        data.append(
            go.Bar(
                name=str(x), 
                x=data_plot5_df.index, 
                y=data_plot5_df[x], 
                marker_color = colors[x]
                )
            )
    fig = go.Figure(data)
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=0.1, 
        gridcolor='gainsboro'
        )
    fig.update_layout(
        height = 600, 
        width = 1000, 
        barmode = 'stack', 
        plot_bgcolor='white', 
        title_text="Porcentaje de compras de grupo por tipo de proveedor"
        )
    st.plotly_chart(fig)

    # PLOT 6
    fig = px.bar(
        data_plot6_df, 
        x="group_name", 
        y="Promedio",
        color='vendor_negotiation_type', 
        barmode='group',
        color_discrete_sequence = ["#BF9F63", "#0C3140"],
        height=400
        )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=0.1, 
        gridcolor='gainsboro'
        )
    fig.update_layout(
        title = 'Promedio de precio unitario por grupo', 
        plot_bgcolor = 'white'
        )
    st.plotly_chart(fig)

    # PLOT 7
    data = []
    colors = {
        'Fruits & Vegetables':'#bfa48a', 
        'Cleaning accesories':'#1b1715', 
        'Dairy Products':'#5f4d3d', 
        'Meats':'#4d3525',
        'Food and Beverages Supplies':'#ded7c5', 
        'Poultry':'#4d6881', 
        'Bakery':'#b26603', 
        'Cereals and Legumes':'#855832',
        'Sausages':'#efd8ac', 
        'Office Supplies':'#27394f', 
        'Tortillas': 'darkorange', 
        'Soft Drinks':'dimgray', 
        'Hardware Store':'darkblue', 
        'Amenities':'lightblue', 
        'Juices':'lightsteelblue'
        }
    for x in data_plot7_df.columns:
        data.append(
            go.Bar(
                name=str(x), 
                x=data_plot7_df.index, 
                y=data_plot7_df[x], 
                marker_color = colors[x]
                )
            )
    fig = go.Figure(data)
    fig.update_layout(
        barmode = 'stack', 
        plot_bgcolor = 'white'
        )
    #For you to take a look at the result use
    st.plotly_chart(fig)

    # PLOT 8
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(data_plot8_df.columns),
                    fill_color='#27394f',
                    font=dict(color='white'),
                    align='left'
                    ),
                cells=dict(
                    values=[
                        data_plot8_df.venue_code, 
                        data_plot8_df.group_name, 
                        data_plot8_df.corporate_unitprice_mean, 
                        data_plot8_df.local_unitprice_mean, 
                        data_plot8_df.corporateIsHigher
                        ],
                    fill_color='#efd8ac',
                    align='left'
                    )
                )
            ]
        )
    st.plotly_chart(fig)

if __name__ == "__main__":
    get_vendor_analysis_interface2()