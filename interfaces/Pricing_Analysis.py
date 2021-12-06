import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from frames import purchase_data_detail2_df, data_plot9_df, data_plot10_df, data_plot11_df, data_plot12_df, ocupation_merge_df, data_plot14_df, comparation_df

def get_pricing_analysis_interface():

    # page format
    st.title('Análisis de precios')
    pd.set_option('display.max_columns', None)
    
    # PLOT 9
    st.subheader('Gasto total por categoría: Top 10')
    fig = px.bar(
        data_plot9_df, 
        x = 'net_value_sum',
        y = 'group_name', 
        color = 'group_name', 
        color_discrete_sequence = ['#091639', '#0a1c40', '#0e264c', '#124771', '#1b75a4', '#2086b7', '#48abd5',' #8acdea', '#badff0', '#d5ebf8'],
        labels={
                "group_name": "Categoría",
                "net_value_sum": "Gasto total"
        }
        )
    fig.update_xaxes(showgrid=True, gridwidth=0.1, gridcolor='gainsboro')
    fig.update_layout(plot_bgcolor = 'white')
    st.plotly_chart(fig)

    # PLOT 10
    st.subheader('Precio unitario promedio de los grupos perecederos por día del mes')
    fig = px.line(
        data_plot10_df, 
        x = "day", 
        y = "group_mean", 
        color = "group_name", 
        width = 30, 
        markers = True,
        color_discrete_sequence = ['#4d3525','#ded7c5','#bfa48a','#1b1715','#4d6881'],
        labels={
                "day": "Día",
                "group_mean": "Precio unitario promedio",
                "group_name": "Grupo perecederos"
        }
        )
    fig.update_layout(
        plot_bgcolor = 'white',
        width = 800
        # height = 500
        )
    st.plotly_chart(fig)

    # PLOT 11
    st.subheader('Precio unitario promedio de los mantenimientos de AC a través del año')
    fig = px.line(
        data_plot11_df, 
        x = "month", 
        y = "month_mean", 
        color = "material_description", 
        width = 30, 
        markers = False,
        color_discrete_sequence = [ '#aba676', '#718271', '#cca74b', '#3c5667',  '#987f37', '#b95c04', '#d98d10','#ddbc5a'],
        labels={
                "month": "Mes",
                "month_mean": "Precio unitario promedio",
                "material_description": "Mantenimientos"
        }
        )
    fig.update_layout(
        plot_bgcolor = 'white',
        width = 800
        # height = 500
        )
    st.plotly_chart(fig)

    # PLOT 12
    st.subheader('Precio unitario promedio de frutas y verduras por mes del año')
    colors = ['#459342', '#DEBA28', 'orange', '#E0D5A2', '#DE9528', 'yellow', '#6AE366', '#E0C956', 'pink', 'red']
    fig = px.line(
        data_plot12_df, 
        x = 'month', 
        y = 'unit_price', 
        color = 'material_description', 
        color_discrete_sequence = colors, 
        markers = False,
        labels={
                "unit_price": "Precio unitario promedio",
                "month": "Mes",
                "material_description": "Frutas y verduras"
        }
        )
    fig.update_layout(
        plot_bgcolor = 'white'
        # width = 1200, 
        # height = 800
        )
    st.plotly_chart(fig)

    # PLOT 13
    st.subheader('Precio unitario de servicio de lavandería por mes del año')
    p13 = purchase_data_detail2_df
    linen_df = p13[p13['group_name'] == 'Linen Laundry']
    linen_df1 = linen_df[linen_df['material_description'].isin(['Servicio de Lavado de Manteles'])]
    linen_df2 = linen_df[linen_df['material_description'].isin(['Servicio de Lavandería de Blancos'])]
    linen_df1 = linen_df1.groupby(['material_description','month']).agg({'net_value':'mean'}).reset_index()
    linen_df2 = linen_df2.groupby(['material_description','month']).agg({'net_value':'mean'}).reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x= linen_df1['month'], 
            y=linen_df1['net_value'], 
            name='Servicio de Lavado de Manteles', 
            marker_color = '#BF9F63'
            ),
        secondary_y=False, 
        )
    fig.add_trace(
        go.Scatter(
            x= linen_df2['month'], 
            y=linen_df2['net_value'], 
            name='Servicio de Lavandería de Blancos', 
            marker_color = '#0C3140'
            ),
        secondary_y=False,
        )
    fig.add_trace(
        go.Scatter(
            x= ocupation_merge_df['month'], 
            y=ocupation_merge_df['rooms_occupied'], 
            name="Ocupación", 
            marker_color = 'gray'
            ),
        secondary_y=True,
        )
    fig.update_layout(
        plot_bgcolor = 'white'
        # width = 1200, 
        # height = 800
        )
    st.plotly_chart(fig)

    # PLOT 14
    st.subheader('Precio unitario promedio de los mantenimientos de Elevador a través del año')
    fig = px.line(
        data_plot14_df, 
        x = 'month', 
        y = 'unit_price', 
        color = 'material_description', 
        color_discrete_sequence = ['#aba676','#d98d10'], 
        markers = True,
        labels={
                "unit_price": "Precio unitario promedio",
                "month": "Mes",
                "material_description": "Mantenimientos"
        }
        )
    fig.update_layout(
        plot_bgcolor = 'white'
        # width = 1200, 
        # height = 500
        )
    st.plotly_chart(fig)

    # PLOT 15
    st.subheader('Número de mantenimientos por tipo de mantenimiento por hotel')
    fig = px.bar(
        comparation_df, 
        x = 'venue_code', 
        y = 'quantity', 
        color = 'material_description', 
        color_discrete_sequence = ['#aba676','#d98d10']
        )
    y = np.arange(0,comparation_df['quantity'].mean(),1)
    fig.add_shape(
        go.layout.Shape(
            type="line", 
            x0=-.5, 
            y0=comparation_df['quantity'].mean(),
            x1=36, 
            y1=comparation_df['quantity'].mean(),
            line=dict(color="gray", width=1, dash="dash")
            )
        )
    fig.update_layout(plot_bgcolor = 'white')
    st.plotly_chart(fig)

if __name__ == "__main__":
    get_pricing_analysis_interface()