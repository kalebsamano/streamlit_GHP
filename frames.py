"""
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
"""
import sys
import config
import pandas as pd
from ghp_suite_api import GHPSuiteApiConnector

# connection
conn = GHPSuiteApiConnector(config.api_key)
r = conn.test_connection()
if r != '':
    sys.exit('Connection failed. ' + r)

"""
# static data
materials = conn.get_procurement_material_catalog_df().to_csv('./data/materials.csv')
venues = conn.get_venues_df().to_csv('./data/venues.csv')
vendors = conn.get_procurement_vendor_catalog_df().to_csv('./data/vendors.csv')
"""

# functions that return static data

# materials function
def materials():
    df = conn.get_procurement_material_catalog_df()
    return(df)
# result
materials_df = materials()

# venues function
def venues():
    df = conn.get_venues_df()
    return(df)
# result
venues_df = venues()

# vendors funtion
def vendors():
    df = conn.get_procurement_vendor_catalog_df()
    return(df)
# result
vendors_df = vendors()

# purchase data function
def purchase_data():

    #pmc = materials_df
    venues = venues_df
    venues_activos = venues[venues['status_name'] == 'Activo']
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
            df = pd.concat([df, purchase_data1, purchase_data2, purchase_data3, purchase_data4, purchase_data5])
        elif count == 0:
            purchase_data1 = conn.get_procurement_purchase_orders_df(venue_code, fecha1, fecha2)
            purchase_data2 = conn.get_procurement_purchase_orders_df(venue_code, fecha3, fecha4)
            purchase_data3 = conn.get_procurement_purchase_orders_df(venue_code, fecha5, fecha6)
            purchase_data4 = conn.get_procurement_purchase_orders_df(venue_code, fecha7, fecha8)
            purchase_data5 = conn.get_procurement_purchase_orders_df(venue_code, fecha9, fecha10)
            df = pd.concat([purchase_data1, purchase_data2, purchase_data3, purchase_data4, purchase_data5])
            count += 1
    df['quantity'] = df['quantity'].astype(float)
    df['unit_price'] = df['unit_price'].astype(float)
    df['net_value'] = df['net_value'].astype(float)
    return(df)
# result
purchase_data_df = purchase_data()

# cross tab function
def purchase_vendors():
    purchase_data = purchase_data_df
    df = pd.crosstab(
        index=purchase_data['venue_code'],
        columns=purchase_data['vendor_negotiation_type'],
        normalize="index"
        )

    return(df)
#result
purchase_vendors_df = purchase_vendors()

def purchase_materials():
    
    purchase_data = purchase_data_df
    materials = materials_df
    purchase_data_detail = pd.merge(
        left = purchase_data, 
        right = materials, 
        how = 'left', 
        left_on = 'material_id', 
        right_on = 'id'
        )

    purchase_data_detail.drop(columns = ['id', 'group', 'unit_y', 'name', 'unit_name'], inplace = True)
    purchase_data_detail.rename(columns = {'unit_x': 'unit'}, inplace = True)

    group_name = purchase_data_detail['group_name'].value_counts().rename_axis('group_name').reset_index(name='counts')
    group_name = group_name.head(10)
    top10_groups = group_name['group_name'].unique()

    groups_purchase_detail_df = purchase_data_detail[purchase_data_detail['group_name'].isin(top10_groups)]

    df = pd.crosstab(index=groups_purchase_detail_df['venue_code'],
                                columns=groups_purchase_detail_df['group_name'],
                                normalize="index")
    return(df)
# result
purchase_materials_df = purchase_materials()
