"""
import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
"""
import sys
import config
import pandas as pd
import numpy as np
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
materials_df = materials()

# venues function
def venues():
    df = conn.get_venues_df()
    return(df)
venues_df = venues()

# vendors funtion
def vendors():
    df = conn.get_procurement_vendor_catalog_df()
    return(df)
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
purchase_data_df = purchase_data()

# PURCHASE DATA DETAIL
def purchase_data_detail():
    
    v = venues_df
    left_df = purchase_data_df
    rightdf = materials_df

    venues_name_df = v[['venue_code','name']]
    
    df = pd.merge(
        left = left_df, 
        right = rightdf, 
        how = 'left', 
        left_on = 'material_id', 
        right_on = 'id'
        )
    df.drop(
        columns = ['id', 'group', 'unit_y', 'name', 'unit_name'], 
        inplace = True
        )
    df.rename(columns = {'unit_x': 'unit'}, inplace = True)
    df = pd.merge(left = df, right = venues_name_df, how = 'left', on = 'venue_code')
    df.rename(columns = {'name': 'venue_name'}, inplace = True)
    df = pd.merge(left = df, right = venues_name_df, how = 'left', on = 'venue_code')
    
    df.rename(columns = {'name': 'venue_name'}, inplace = True)
    return(df)
purchase_data_detail_df = purchase_data_detail()

# PURCHASE MATERIALS
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
purchase_materials_df = purchase_materials()

# PLOT 1
def data_plot1():
    df = purchase_data_detail_df.groupby(['venue_name', 'vendor_negotiation_type']).size().unstack(fill_value=0).reset_index()
    df = pd.melt(
        df, 
        id_vars = 'venue_name', 
        var_name = 'vendor_negotiation_type', 
        value_name = 'count'
        )
    return(df)
data_plot1_df = data_plot1()

# PLOT 2
def data_plot2():
    df = pd.crosstab(
        index=purchase_data_df['venue_code'],
        columns=purchase_data_df['vendor_negotiation_type'],
        normalize="index"
        )
    return(df)
data_plot2_df = data_plot2()

#PLOT 3
def data_plot3():
    df = purchase_data_detail_df
    return(df)
data_plot3_df = data_plot3()

# PLOT 4 DATA
#
def unit98():
    df = purchase_data_detail_df[purchase_data_detail_df['unit_price'] <= np.percentile(purchase_data_detail_df['unit_price'], 95)]
    return(df)
purchase_data_detail_unit98 = unit98()
 #
def net98():
    df = purchase_data_detail_df[purchase_data_detail_df['net_value'] <= np.percentile(purchase_data_detail_df['net_value'], 95)]
    return(df)
purchase_data_detail_net98 = net98()
#
def quant98():
    df = purchase_data_detail_df[purchase_data_detail_df['quantity'] <= np.percentile(purchase_data_detail_df['quantity'], 98)]
    return(df)
purchase_data_detail_quant98 = quant98()

# top10groups_local_corporate_data
#def top10():
#    top10groups_local_corporate_data = purchase_data_detail_df[
 #       purchase_data_detail_df['group_name'].isin(df.columns)
 #       ]
 #   return

# PLOT 5
def local_groups_purchase_detail():
    df = purchase_data_detail_df[purchase_data_detail_df['vendor_negotiation_type'] == 'Local']
    return(df)
local_groups_purchase_detail_df = local_groups_purchase_detail()

def corporate_groups_purchase_detail():
    df = purchase_data_detail_df[purchase_data_detail_df['vendor_negotiation_type'] == 'Corporate']
    return(df)
corporate_groups_purchase_detail_df = corporate_groups_purchase_detail()

def local_groups_top10():
    df = local_groups_purchase_detail_df['group_name'].value_counts().rename_axis('group_name').reset_index(name='counts')
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
    return(df)
local_groups_top10_df = local_groups_top10()

def local():
    df = local_groups_purchase_detail_df[local_groups_purchase_detail_df['group_name'].isin(local_groups_top10)]
    return(df)
local_df = local()

def corporate_groups_top10():
    df = corporate_groups_purchase_detail_df['group_name'].value_counts().rename_axis('group_name').reset_index(name='counts')
    df = [
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
    return(df)
corporate_groups_top10_df = corporate_groups_top10()

def corporate():
    df = corporate_groups_purchase_detail_df[corporate_groups_purchase_detail_df['group_name'].isin(corporate_groups_top10)]
    return(df)
corporate_df = corporate()

def joint():
    df = pd.concat([local_df,corporate_df])
    return(df)
joint_df = joint()


def data_plot5():

    df = pd.crosstab(
        index=joint_df['vendor_negotiation_type'],
        columns=joint_df['group_name'],
        normalize="index"
        )
    top10groups_local_corporate_data = purchase_data_detail_df[
        purchase_data_detail_df['group_name'].isin(df.columns)
        ]
    df = pd.crosstab(
        index=top10groups_local_corporate_data['vendor_negotiation_type'],
        columns=top10groups_local_corporate_data['group_name'],
        normalize="index"
        )
    return(df)
data_plot5_df = data_plot5()

def top10groups_local_corporate_data():
    d = pd.crosstab(index=joint_df['vendor_negotiation_type'],columns=joint_df['group_name'],normalize="index")
    df = purchase_data_detail_df[purchase_data_detail_df['group_name'].isin(d.columns)]
    return(df)
top10groups_local_corporate_data_df = top10groups_local_corporate_data()

# PLOT 6
def data_plot6():
    
    corporate_groups = top10groups_local_corporate_data_df[
        top10groups_local_corporate_data_df['vendor_negotiation_type'] == 'Corporate'
        ]
    local_groups = top10groups_local_corporate_data_df[
        top10groups_local_corporate_data_df['vendor_negotiation_type'] == 'Local'
        ]
    corporate_groups_mean = corporate_groups['unit_price'].groupby(corporate_groups['group_name']).agg('mean').rename_axis('group_name').reset_index(name = 'Promedio')
    corporate_groups_mean['vendor_negotiation_type'] = 'Corporate'
    local_groups_mean = local_groups['unit_price'].groupby(local_groups['group_name']).agg('mean').rename_axis('group_name').reset_index(name = 'Promedio')
    local_groups_mean['vendor_negotiation_type'] = 'Local'
    df = pd.concat([corporate_groups_mean, local_groups_mean])
    return(df)
data_plot6_df = data_plot6()

# PLOT 7
def data_plot7():

    df = pd.crosstab(
        index=top10groups_local_corporate_data_df['venue_code'],
        columns=top10groups_local_corporate_data_df['group_name'],
        normalize="index"
        )
    return(df)
data_plot7_df = data_plot7()

# PLOT 8
def data_plot8():

    table_data = []
    venuesdf = venues_df
    venues_activos = venuesdf[venuesdf['status_name'] == 'Activo']
    
    for venue_code in venues_activos['venue_code'].unique():
        venue_df = top10groups_local_corporate_data_df[top10groups_local_corporate_data_df['venue_code'].isin([venue_code])]
        for group_name in data_plot5_df.columns:
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
    return(table_df)
data_plot8_df = data_plot8()

