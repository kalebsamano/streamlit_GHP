import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from frames import venues_df, purchase_data_detail_df, purchase_vendors_df

def get_vendor_analysis_interface():

    # page format
    st.title('Analisis de vendedores')
    pd.set_option('display.max_columns', None)
    
    # DOT PLOT
    dot_data = purchase_data_detail_df.groupby(['venue_name', 'vendor_negotiation_type']).size().unstack(fill_value=0).reset_index()
    dot_data = pd.melt(
        dot_data, 
        id_vars = 'venue_name', 
        var_name = 'vendor_negotiation_type', 
        value_name = 'count'
        )
    fig = px.scatter(
        dot_data, 
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

    # PLOT 2 (CROSS TAB)
    cross_tab = purchase_vendors_df
    colors = {"Corporate": "#BF9F63", "Local": "#0C3140"}
    data = []
    for x in cross_tab.columns:
        data.append(
            go.Bar(
                name=str(x), 
                x=cross_tab.index, 
                y=cross_tab[x], 
                marker_color=colors[x]
                )
            )
    fig = go.Figure(data)
    fig.update_layout(
        barmode = 'stack', 
        title='Proporción de compras por hotel y por tipo de proveedor', 
        plot_bgcolor = 'white'
        )
    st.plotly_chart(fig)

    # PLOT 3 (VARIABLES MONETARIAS)
    purchase_data_detail = purchase_data_detail_df
    fig = go.Figure()  
    fig.add_trace( 
        go.Indicator(
        title = {'text': "Precio por unidad"},
        mode = "number",
        value = np.percentile(purchase_data_detail['unit_price'], 95),
        number = {'prefix': "$"},
        domain = {'row': 1, 'column': 0},
        title_font_color = '#BF9460'))
    fig.add_trace( 
        go.Indicator(
        title = {'text': "Importe total de compra"},
        mode = "number",
        value = np.percentile(purchase_data_detail['net_value'], 95),
        number = {'prefix': "$"},
        domain = {'row': 1, 'column': 1},
        title_font_color = '#EF7C20'))
    fig.add_trace( 
        go.Indicator(
        title = {'text': "Cantidad"},
        mode = "number",
        value = np.percentile(purchase_data_detail['quantity'], 95),
        domain = {'row': 1, 'column': 2},
        title_font_color = '#0D0D0D'))
    fig.update_layout(
        title = 'Percentil 95%: Límite en donde 95% de los datos son menores', 
        paper_bgcolor = "white", 
        grid = {'rows': 1, 'columns': 3}
        )
    st.plotly_chart(fig)

    #PLOT 4
    purchase_data_detail_unit98 = purchase_data_detail[purchase_data_detail['unit_price'] <= np.percentile(purchase_data_detail['unit_price'], 95)]
    purchase_data_detail_net98 = purchase_data_detail[purchase_data_detail['net_value'] <= np.percentile(purchase_data_detail['net_value'], 95)]
    purchase_data_detail_quant98 = purchase_data_detail[purchase_data_detail['quantity'] <= np.percentile(purchase_data_detail['quantity'], 98)]
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
    local_groups_purchase_detail_df = purchase_data_detail[
        purchase_data_detail['vendor_negotiation_type'] == 'Local'
        ]
    corporate_groups_purchase_detail_df = purchase_data_detail[
        purchase_data_detail['vendor_negotiation_type'] == 'Corporate'
        ]
    local_groups_top10 = local_groups_purchase_detail_df['group_name'].value_counts().rename_axis('group_name').reset_index(name='counts')
    local_groups_top10 = [
        'Fruits & Vegetables', 
        'Dairy Products', 
        'Tortillas', 
        'Meats',
        'Hardware Store', 
        'Bakery', 
        'Office Supplies', 
        'Poultry', 
        'Juices', 
        'Soft Drinks'
        ]
    local_df = local_groups_purchase_detail_df[
        local_groups_purchase_detail_df['group_name'].isin(local_groups_top10)
        ]
    corporate_groups_top10 = corporate_groups_purchase_detail_df['group_name'].value_counts().rename_axis('group_name').reset_index(name='counts')
    corporate_groups_top10 = [
        'Fruits & Vegetables',
        'Cleaning accesories', 
        'Dairy Products',
        'Food and Beverages Supplies',
        'Meats',
        'Poultry',
        'Cereals and Legumes',
        'Sausages',
        'Bakery',
        'Amenities'
        ]
    corporate_df = corporate_groups_purchase_detail_df[
        corporate_groups_purchase_detail_df['group_name'].isin(corporate_groups_top10)
        ]
    joint_df = pd.concat([local_df,corporate_df])

    cross_tab2 = pd.crosstab(
        index=joint_df['vendor_negotiation_type'],
        columns=joint_df['group_name'],
        normalize="index"
        )
    top10groups_local_corporate_data = purchase_data_detail[
        purchase_data_detail['group_name'].isin(cross_tab2.columns)
        ]
    cross_tab2 = pd.crosstab(
        index=top10groups_local_corporate_data['vendor_negotiation_type'],
        columns=top10groups_local_corporate_data['group_name'],
        normalize="index"
        )
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
    for x in cross_tab2.columns:
        data.append(
            go.Bar(
                name=str(x), 
                x=cross_tab2.index, 
                y=cross_tab2[x], 
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
    #For you to take a look at the result use
    st.plotly_chart(fig)

    # PLOT 6
    corporate_groups = top10groups_local_corporate_data[
        top10groups_local_corporate_data['vendor_negotiation_type'] == 'Corporate'
        ]
    local_groups = top10groups_local_corporate_data[
        top10groups_local_corporate_data['vendor_negotiation_type'] == 'Local'
        ]
    corporate_groups_mean = corporate_groups['unit_price'].groupby(corporate_groups['group_name']).agg('mean').rename_axis('group_name').reset_index(name = 'Promedio')
    corporate_groups_mean['vendor_negotiation_type'] = 'Corporate'
    local_groups_mean = local_groups['unit_price'].groupby(local_groups['group_name']).agg('mean').rename_axis('group_name').reset_index(name = 'Promedio')
    local_groups_mean['vendor_negotiation_type'] = 'Local'
    group_means = pd.concat([corporate_groups_mean, local_groups_mean])
    fig = px.bar(
        group_means, 
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
    cross_tab3 = pd.crosstab(
        index=top10groups_local_corporate_data['venue_code'],
        columns=top10groups_local_corporate_data['group_name'],
        normalize="index"
        )
    # initiate data list for figure
    data = []
    #use for loop on every zoo name to create bar data
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
    for x in cross_tab3.columns:
        data.append(
            go.Bar(
                name=str(x), 
                x=cross_tab3.index, 
                y=cross_tab3[x], 
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
    table_data = []
    venues = venues_df
    venues_activos = venues[venues['status_name'] == 'Activo']
    for venue_code in venues_activos['venue_code'].unique():
        venue_df = top10groups_local_corporate_data[top10groups_local_corporate_data['venue_code'].isin([venue_code])]
        for group_name in cross_tab2.columns:
            venue_info = []
            group_df = venue_df[venue_df['group_name'] == group_name]
            corporate_groups = group_df[group_df['vendor_negotiation_type'] == 'Corporate']
            local_groups = group_df[group_df['vendor_negotiation_type'] == 'Local']
            venue_info.append(venue_code)
            venue_info.append(group_name)
            venue_info.append(corporate_groups['unit_price'].mean())
            venue_info.append(local_groups['unit_price'].mean())
            table_data.append(venue_info) 
    table_df = pd.DataFrame(
        table_data, 
        columns = [
            'venue_code', 
            'group_name', 
            'corporate_unitprice_mean', 
            'local_unitprice_mean'
            ]
        )
    table_df.dropna(how = 'any', inplace = True)
    table_df['corporateIsHigher'] = np.where(
        table_df['corporate_unitprice_mean']>table_df['local_unitprice_mean'], 'Yes', 'No'
        )
    table_df['corporate_unitprice_mean'] = table_df['corporate_unitprice_mean'].round(decimals = 2)
    table_df['local_unitprice_mean'] = table_df['local_unitprice_mean'].round(decimals = 2)
    table_df = table_df[table_df['corporateIsHigher']== 'Yes']
    table_df.sort_values(
        by = 'corporate_unitprice_mean',
        ascending = True, 
        inplace = True
        )
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(table_df.columns),
                    fill_color='#27394f',
                    font=dict(color='white'),
                    align='left'
                    ),
                cells=dict(
                    values=[
                        table_df.venue_code, 
                        table_df.group_name, 
                        table_df.corporate_unitprice_mean, 
                        table_df.local_unitprice_mean, 
                        table_df.corporateIsHigher
                        ],
                    fill_color='#efd8ac',
                    align='left'
                    )
                )
            ]
        )
    st.plotly_chart(fig)


if __name__ == "__main__":
    get_vendor_analysis_interface()
