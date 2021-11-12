import sys
import config
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from ghp_suite_api import GHPSuiteApiConnector

def get_purchases_interface():
    # coverage_stats = shared_state.coverage_stats
    # connection
    conn = GHPSuiteApiConnector(config.api_key)
    r = conn.test_connection()
    if r != '':
        sys.exit('Connection failed. ' + r)
    # data calls
    pmc = conn.get_procurement_material_catalog_df()
    venues = conn.get_venues_df()
    # page format
    st.title('Purchases')
    pd.set_option('display.max_columns', None)
    #with st.expander('Materials'):
    #    st.write(pmc)

    # NUMERO DE ORDENES POR FECHA
    venues_activos = venues[venues['status_name'] == 'Activo']
    # date variables
    count = 0
    fecha1 = '2020-10-31'
    fecha2 = '2020-11-02'
    fecha3 = '2020-11-03'
    fecha4 = '2021-02-01'
    fecha5 = '2021-02-02'
    fecha6 = '2021-05-03'
    fecha7 = '2021-05-04'
    fecha8 = '2021-08-02'
    fecha9 = '2021-08-03'
    fecha10 = '2021-10-31'
    # for loop
    for venue_code in venues_activos['venue_code'].unique():
        if count == 1:
            try:
                purchase_data1 = conn.get_procurement_purchase_orders_df(venue_code, fecha1, fecha2)
            except:
                purchase_data1 = pd.DataFrame()
            try:
                purchase_data2 = conn.get_procurement_purchase_orders_df(venue_code, fecha3, fecha4)
            except:
                purchase_data2 = pd.DataFrame()
            try:
                purchase_data3 = conn.get_procurement_purchase_orders_df(venue_code, fecha5, fecha6)
            except:
                purchase_data3 = pd.DataFrame()
            try:
                purchase_data4 = conn.get_procurement_purchase_orders_df(venue_code, fecha7, fecha8)
            except:
                purchase_data4 = pd.DataFrame()
            try:
                purchase_data5 = conn.get_procurement_purchase_orders_df(venue_code, fecha9, fecha10)
            except:
                purchase_data5 = pd.DataFrame()   
            purchase_data = pd.concat([purchase_data, purchase_data1, purchase_data2, purchase_data3, purchase_data4, purchase_data5])
        elif count == 0:
            purchase_data1 = conn.get_procurement_purchase_orders_df(venue_code, fecha1, fecha2)
            purchase_data2 = conn.get_procurement_purchase_orders_df(venue_code, fecha3, fecha4)
            purchase_data3 = conn.get_procurement_purchase_orders_df(venue_code, fecha5, fecha6)
            purchase_data4 = conn.get_procurement_purchase_orders_df(venue_code, fecha7, fecha8)
            purchase_data5 = conn.get_procurement_purchase_orders_df(venue_code, fecha9, fecha10)
            purchase_data = pd.concat([purchase_data1, purchase_data2, purchase_data3, purchase_data4, purchase_data5])
            count += 1
    # purchase data
    purchase_data['quantity'] = purchase_data['quantity'].astype(float)
    purchase_data['unit_price'] = purchase_data['unit_price'].astype(float)
    purchase_data['net_value'] = purchase_data['net_value'].astype(float)
    purchase_agg = purchase_data['net_value'].groupby(purchase_data['date']).agg('sum').reset_index()
    # plot
    fig = px.line(purchase_agg, x="date", y="net_value", title='Número de órdenes por fecha')
    st.plotly_chart(fig)

    # VENDOR NEGOTIATON TYPE

    cross_tab = pd.crosstab(index=purchase_data['venue_code'],
                             columns=purchase_data['vendor_negotiation_type'],
                             normalize="index")
    # initiate data list for figure
    data = []
    #use for loop on every zoo name to create bar data
    for x in cross_tab.columns:
        data.append(go.Bar(name=str(x), x=cross_tab.index, y=cross_tab[x]))
    #plot
    fig = go.Figure(data)
    fig.update_layout(barmode = 'stack', title='Proporción de compras con tipo de proveedor')
    st.plotly_chart(fig)

    # PROPORCIONES GROUP NAME
    # purchase data
    purchase_data_detail = pd.merge(left = purchase_data, right = pmc, how = 'left', left_on = 'material_id', right_on = 'id')
    purchase_data_detail.drop(columns = ['id', 'group', 'unit_y', 'name', 'unit_name'], inplace = True)
    purchase_data_detail.rename(columns = {'unit_x': 'unit'}, inplace = True)
    # top 10 groups
    group_name = purchase_data_detail['group_name'].value_counts().rename_axis('group_name').reset_index(name='counts')
    group_name = group_name.head(10)
    top10_groups = group_name['group_name'].unique()
    groups_purchase_detail_df = purchase_data_detail[purchase_data_detail['group_name'].isin(top10_groups)]
    cross_tab2 = pd.crosstab(index=groups_purchase_detail_df['venue_code'],
                             columns=groups_purchase_detail_df['group_name'],
                             normalize="index")
    # plot
    data = []
    #use for loop on every zoo name to create bar data
    for x in cross_tab2.columns:
        data.append(go.Bar(name=str(x), x=cross_tab2.index, y=cross_tab2[x]))

    fig = go.Figure(data)
    fig.update_layout(barmode = 'stack')
    st.plotly_chart(fig)
    

if __name__ == "__main__":
    get_purchases_interface()