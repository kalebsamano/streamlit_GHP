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

############################################################################################

# purchase data function
def purchase_data():

    #pmc = materials_df
    venues = venues_df
    venues_activos = venues[venues['status_name'] == 'Activo']
    count = 0
    fecha1 = '2020-10-06'
    fecha2 = '2020-11-02'
    fecha3 = '2020-11-03'
    fecha4 = '2021-02-01'
    fecha5 = '2021-02-02'
    fecha6 = '2021-05-03'
    fecha7 = '2021-05-04'
    fecha8 = '2021-08-02'
    fecha9 = '2021-08-03'
    fecha10 = '2021-10-06'
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
    
    df = pd.merge(left = left_df, right = rightdf, how = 'left', left_on = 'material_id', right_on = 'id')
    df.drop(columns = ['id', 'group', 'unit_y', 'name', 'unit_name'], inplace = True)
    df.rename(columns = {'unit_x': 'unit'}, inplace = True)
    df = pd.merge(left = df, right = venues_name_df, how = 'left', on = 'venue_code')
    df.rename(columns = {'name': 'venue_name'}, inplace = True)
    return(df)
purchase_data_detail_df = purchase_data_detail()

############################################################################################

# PLOT 1
def data_plot1():
    data = purchase_data_detail_df
    df = data.groupby(['venue_name', 'vendor_negotiation_type']).size().unstack(fill_value=0).reset_index()
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
    data = purchase_data_df
    df = pd.crosstab(
        index=data['venue_code'],
        columns=data['vendor_negotiation_type'],
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
    data = local_groups_purchase_detail_df
    top10 = local_groups_top10_df
    df = data[data['group_name'].isin(top10)]
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
    data = corporate_groups_purchase_detail_df
    top10 = corporate_groups_top10_df
    df = data[data['group_name'].isin(top10)]
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

# PLOT 6
def top10groups_local_corporate_data():
    d = pd.crosstab(index=joint_df['vendor_negotiation_type'],columns=joint_df['group_name'],normalize="index")
    df = purchase_data_detail_df[purchase_data_detail_df['group_name'].isin(d.columns)]
    return(df)
top10groups_local_corporate_data_df = top10groups_local_corporate_data()

def data_plot6():

    t = top10groups_local_corporate_data_df
    p = purchase_data_detail_df

    corporate_data = p[p['vendor_negotiation_type'] == 'Corporate']
    local_data = p[p['vendor_negotiation_type'] == 'Local']

    a_set = set(corporate_data['material_description'].unique())
    b_set = set(local_data['material_description'].unique())

    a = (a_set & b_set)
    common_items = list(a)

    t = t[t['material_description'].isin(common_items)]
    t.drop_duplicates(subset = ['material_description', 'vendor_negotiation_type'], inplace = True)

    corporate_groups = t[t['vendor_negotiation_type'] == 'Corporate']
    local_groups = t[t['vendor_negotiation_type'] == 'Local']

    corporate_groups_mean = corporate_groups['unit_price'].groupby(corporate_groups['group_name']).agg('mean').rename_axis('group_name').reset_index(name = 'Promedio')
    corporate_groups_mean['vendor_negotiation_type'] = 'Corporate'
    local_groups_mean = local_groups['unit_price'].groupby(local_groups['group_name']).agg('mean').rename_axis('group_name').reset_index(name = 'Promedio')
    local_groups_mean['vendor_negotiation_type'] = 'Local'
    df = pd.concat([corporate_groups_mean, local_groups_mean])

    return(df)
data_plot6_df = data_plot6()

# PLOT 7
def data_plot7():

    cross_tab2 = data_plot5_df
    d = purchase_data_detail_df

    t = d[d['group_name'].isin(cross_tab2.columns)]

    df = pd.crosstab(
        index=t['venue_code'],
        columns=t['group_name'],
        normalize="index"
        )
    return(df)
data_plot7_df = data_plot7()

# PLOT 8
def common_items():
    
    p = purchase_data_detail_df
    
    corporate_data = p[p['vendor_negotiation_type'] == 'Corporate']
    local_data = p[p['vendor_negotiation_type'] == 'Local']

    a_set = set(corporate_data['material_description'].unique())
    b_set = set(local_data['material_description'].unique())

    a = (a_set & b_set)
    df = list(a)
    return(df)
common_items_df = common_items()

def data_plot8():
    c = common_items_df
    t = top10groups_local_corporate_data_df
    p = purchase_data_detail_df

    t = t[t['material_description'].isin(c)]
    t.drop_duplicates(subset = ['material_description', 'vendor_negotiation_type'], inplace = True)

    table_data = []

    for group_name in p['group_name'].unique():
        group_info = []
        group_df = p[p['group_name'] == group_name]
        corporate_groups = group_df[group_df['vendor_negotiation_type'] == 'Corporate']
        local_groups = group_df[group_df['vendor_negotiation_type'] == 'Local']
        group_info.append(group_name)
        group_info.append(corporate_groups['unit_price'].mean())
        group_info.append(local_groups['unit_price'].mean())
        table_data.append(group_info)

    table_df = pd.DataFrame(
        table_data, 
        columns = ['group_name', 'corporate_unitprice_mean', 'local_unitprice_mean']
        )
    table_df.dropna(how = 'any', inplace = True)
    table_df['corporateIsHigher'] = np.where(table_df['corporate_unitprice_mean']>table_df['local_unitprice_mean'], 'Yes', 'No')
    table_df['corporate_unitprice_mean'] = table_df['corporate_unitprice_mean'].round(decimals = 2)
    table_df['local_unitprice_mean'] = table_df['local_unitprice_mean'].round(decimals = 2)
    table_df = table_df[table_df['corporateIsHigher']== 'Yes']
    table_df.sort_values(by = 'corporate_unitprice_mean',ascending = True, inplace = True)

    return(table_df)
data_plot8_df = data_plot8()

############################################################################################

def purchase_data_detail2():
    data = purchase_data_df
    m = materials_df
    df = pd.merge(
        left = data, 
        right = m, 
        how = 'left', 
        left_on = 'material_id', 
        right_on = 'id'
        )
    df.drop(columns = ['id', 'group', 'unit_y', 'name', 'unit_name'], inplace = True)
    df.rename(columns = {'unit_x': 'unit'}, inplace = True)
    v = venues_df
    df = pd.merge(left = df, right = v, how = 'left', on = 'venue_code')
    df.rename(columns = {'name': 'venue_name'}, inplace = True)
    df['month'] = pd.DatetimeIndex(df['date']).month
    df['day'] = pd.DatetimeIndex(df['date']).day
    df['week'] = pd.DatetimeIndex(df['date']).week
    df['day_name'] = pd.DatetimeIndex(df['date']).dayofweek
    df['day_type'] = np.where(df['day_name'] > 4, 'Weekend', 'Weekday')
    day_names = {0: 'Monday', 1: 'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5: 'Saturday', 6: 'Sunday'}
    df['day_name'].replace(day_names, inplace = True)
    return(df)
purchase_data_detail2_df = purchase_data_detail2()

# PLOT 9
def data_plot9():
    data = purchase_data_detail_df
    df = data['net_value'].groupby(data['group_name']).agg('sum').rename_axis('group_name').reset_index(name = 'net_value_sum')
    df.sort_values(by = 'net_value_sum', ascending = False, inplace = True)
    df = df.head(10)
    return(df)
data_plot9_df = data_plot9()

# PLOT 10
def data_plot10():
    
    food_colors = {
        'Fruits & Vegetables':'#bfa48a', 
        'Meats':'#1b1715', 
        'Poultry':'#4d6881', 
        'Dairy Products':'#4d3525', 
        'Food and Beverages Supplies':'#ded7c5'
        }

    group_mean_data = []
    data = purchase_data_detail2_df

    for group in food_colors.keys():
        for day in data['day'].unique():
            row = []
            group_df = data[data['group_name'] == group]
            fecha_df = group_df[group_df['day'] == day]
            group_mean = fecha_df['unit_price'].mean()
            row.append(group)
            row.append(day)
            row.append(group_mean)
            group_mean_data.append(row)

    group_mean_data = pd.DataFrame(group_mean_data, columns = ['group_name', 'day', 'group_mean'])
    group_mean_data.sort_values(by = ['group_name','day'], ascending = True, inplace = True)
    return(group_mean_data)
data_plot10_df = data_plot10()

# PLOT 11
def data_plot11():

    data = purchase_data_detail2_df
    air_df = data[data['group_name'] == 'Air Conditioning Maintenance']
    good_materials = []

    for material_description in air_df['material_description'].unique():
        material_df = air_df[air_df['material_description'] == material_description]
        if len(material_df['month'].unique()) >= 8:
            good_materials.append(material_description)
    
    air_mean_data = air_df[air_df['material_description'].isin(good_materials)]
    
    final_data = []

    for material_description in air_mean_data['material_description'].unique():
        material_df = air_mean_data[air_mean_data['material_description'] == material_description]
        for month in material_df['month'].unique():
            row = []
            fecha_df = material_df[material_df['month'] == month]
            month_mean = fecha_df['unit_price'].mean()
            row.append(material_description)
            row.append(month)
            row.append(month_mean)
            final_data.append(row)

    air_mean_df = pd.DataFrame(final_data, columns = ['material_description', 'month', 'month_mean'])
    air_mean_df.sort_values(by = ['material_description','month'], ascending = True, inplace = True)

    return(air_mean_df)
data_plot11_df = data_plot11()

# PLOT 12
def data_plot12():
    data = purchase_data_detail2_df
    fruits_df = data[data['group_name'] == 'Fruits & Vegetables']
    fruits_df_top10 = fruits_df['net_value'].groupby(fruits_df['material_description']).agg('sum').reset_index()
    fruits_df_top10.sort_values(by = 'net_value', ascending = False, inplace = True)
    fruits_df_top10 = fruits_df_top10.head(10)
    fruits_top10 = fruits_df_top10['material_description'].unique()
    fruits_df_top10 = data[data['material_description'].isin(fruits_top10)]
    fruits_df_top10 = fruits_df_top10.groupby(['material_description','month']).agg({'unit_price':'mean'}).reset_index()
    return(fruits_df_top10)
data_plot12_df = data_plot12()

# OCCUPATION MERGE
def ocupation_data():
    count = 0

    fecha1 = '2020-10-06'
    fecha2 = '2020-11-02'
    fecha3 = '2020-11-03'
    fecha4 = '2021-02-01'
    fecha5 = '2021-02-02'
    fecha6 = '2021-05-03'
    fecha7 = '2021-05-04'
    fecha8 = '2021-08-02'
    fecha9 = '2021-08-03'
    fecha10 = '2021-10-06'

    v = venues_df
    venues_activos = v[v['status_name'] == 'Activo']

    for venue_code in venues_activos['venue_code'].unique():
        if count == 1:
            try:
                ocupation_data1 = conn.get_market_daily_df(venue_code, fecha1, fecha2)
            except:
                ocupation_data1 = pd.DataFrame()
            try:
                ocupation_data2 = conn.get_market_daily_df(venue_code, fecha3, fecha4)
            except:
                ocupation_data2 = pd.DataFrame()
            try:
                ocupation_data3 = conn.get_market_daily_df(venue_code, fecha5, fecha6)
            except:
                ocupation_data3 = pd.DataFrame()
            try:
                ocupation_data4 = conn.get_market_daily_df(venue_code, fecha7, fecha8)
            except:
                ocupation_data4 = pd.DataFrame()
            try:
                ocupation_data5 = conn.get_market_daily_df(venue_code, fecha9, fecha10)
            except:
                ocupation_data5 = pd.DataFrame()  
            df = pd.concat(
                                        [
                                            df, 
                                            ocupation_data1, 
                                            ocupation_data2, 
                                            ocupation_data3, 
                                            ocupation_data4, 
                                            ocupation_data5
                                            ]
                                        )
        elif count == 0:
            ocupation_data1 = conn.get_market_daily_df(venue_code, fecha1, fecha2)
            ocupation_data2 = conn.get_market_daily_df(venue_code, fecha3, fecha4)
            ocupation_data3 = conn.get_market_daily_df(venue_code, fecha5, fecha6)
            ocupation_data4 = conn.get_market_daily_df(venue_code, fecha7, fecha8)
            ocupation_data5 = conn.get_market_daily_df(venue_code, fecha9, fecha10)
            df = pd.concat(
                                        [
                                            ocupation_data1, 
                                            ocupation_data2, 
                                            ocupation_data3, 
                                            ocupation_data4, 
                                            ocupation_data5
                                            ]
                                        )
            count += 1
    
    df['month'] = pd.DatetimeIndex(df['date']).month    

    return(df)
ocupation_data_df = ocupation_data()

# OCCUPATION MERGE
def ocupation_merge():
    data = ocupation_data_df
    df = data['rooms_occupied'].groupby(data['month']).agg('sum').rename_axis('month').reset_index(name = 'rooms_occupied')
    return(df)
ocupation_merge_df = ocupation_merge()

# PLOT 14
def data_plot14():
    data = purchase_data_detail2_df
    elev_df = data[data['group_name'] == 'Elevator Maintenance']
    elev_df = elev_df[elev_df['material_description'].isin(['Mtto Preventivo Elevadores', 'Mtto Correctivo Elevadores'])]
    elev_df = elev_df.groupby(['material_description','month']).agg({'unit_price':'mean'}).reset_index()
    return(elev_df)
data_plot14_df = data_plot14()

# COMPARATION DF
def comparation():
    data = purchase_data_detail2_df
    elev_df = data[data['group_name'] == 'Elevator Maintenance']
    elev_df = elev_df[elev_df['material_description'].isin(['Mtto Preventivo Elevadores', 'Mtto Correctivo Elevadores'])]
    df = elev_df.groupby(['venue_code','material_description']).agg({'quantity':'sum'}).reset_index()
    return(df)
comparation_df = comparation()

# PREVENTIVO DF
def preventivo():
    data = purchase_data_detail2_df
    df = data[data['material_description'] == 'Mtto Preventivo Elevadores']
    return(df)
preventivo_df = preventivo()


