import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from frames import purchase_materials_df, purchase_vendors_df

#@st.cache(suppress_st_warning=True)
def get_purchases_interface():

    # page format
    st.title('Compras')
    pd.set_option('display.max_columns', None)
    
    # data calls
    cross_tab = purchase_materials_df
    cross_tab2 = purchase_vendors_df

    # PLOT 1
    data = []
    for x in cross_tab.columns:
        data.append(go.Bar(name=str(x), x=cross_tab.index, y=cross_tab[x]))
        figure = go.Figure(data)
        figure.update_layout(
            barmode = 'stack', 
            title=dict(
                text='<b>Proporcion de compras por material</b>',
                font=dict(family="Arial", size=20, color='#000000')
            ),
            autosize=False,
            width=1100,
            height=800
            )

    figure.update_yaxes(automargin=True)
    st.plotly_chart(figure)
    
    # PLOT 2
    data = []
    for x in cross_tab2.columns:
        data.append(go.Bar(name=str(x), x=cross_tab2.index, y=cross_tab2[x]))
    figure = go.Figure(data)
    figure.update_layout(
        barmode = 'stack',
        title=dict(
                text='<b>Proporcion de compras por proveedor</b>',
                font=dict(family="Arial", size=20, color='#000000')
            ),
        autosize=False,
        width=1000,
        height=800
        )
    figure.update_yaxes(automargin=True)
    st.plotly_chart(figure)

if __name__ == "__main__":
    get_purchases_interface()