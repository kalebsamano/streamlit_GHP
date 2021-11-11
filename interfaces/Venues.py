import sys 
import json
import config 
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
import pandas as pd
import numpy as np
from ghp_suite_api import GHPSuiteApiConnector # Importing the library


def get_venues_interface():
    # coverage_stats = shared_state.coverage_stats
    # connection
    conn = GHPSuiteApiConnector(config.api_key)
    r = conn.test_connection()
    if r != '':
        sys.exit('Connection failed. ' + r)

    st.header("Venues")
    st.title('GHP Data  Project')
    pd.set_option('display.max_columns', None)
    venues_df = conn.get_venues_df()
    materials_df = conn.get_procurement_material_catalog_df()
    vendors_df = conn.get_procurement_vendor_catalog_df()

    # VENUES
    # display data
    with st.expander('Venues'):
        st.write(venues_df)
    # sunburst venues graph
    sun_df = venues_df.loc[venues_df['status'] == 1]
    sun_df = sun_df[['region_name','state','city','venue_code','available_rooms']]
    # plot
    fig = px.sunburst(
        sun_df,
        path=['region_name','state','city','venue_code'], 
        values='available_rooms',
        color='available_rooms', 
        color_continuous_scale='Blues',
        title="GHP's venues overview",
        width=800, 
        height=800
        )
    # display
    st.plotly_chart(fig)
    # venues line chart
    # Q1
    marketPBMC_Q1 = conn.get_market_daily_df('PBCMC','2021-01-01','2021-03-31')
    # change net_value column data type from object to float
    marketPBMC_Q1['rooms_occupied'] = pd.to_numeric(marketPBMC_Q1['rooms_occupied'], downcast='integer')
    roomsPBMC_Q1 = marketPBMC_Q1[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q2
    marketPBMC_Q2 = conn.get_market_daily_df('PBCMC','2021-04-01','2021-06-30')
    # change net_value column data type from object to float
    marketPBMC_Q2['rooms_occupied'] = pd.to_numeric(marketPBMC_Q2['rooms_occupied'], downcast='integer')
    roomsPBMC_Q2 = marketPBMC_Q2[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q3
    marketPBMC_Q3 = conn.get_market_daily_df('PBCMC','2021-07-01','2021-09-29')
    # change net_value column data type from object to float
    marketPBMC_Q3['rooms_occupied'] = pd.to_numeric(marketPBMC_Q3['rooms_occupied'], downcast='integer')
    roomsPBMC_Q3 = marketPBMC_Q3[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q4
    marketPBMC_Q4 = conn.get_market_daily_df('PBCMC','2021-09-30','2021-10-31')
    # change net_value column data type from object to float
    marketPBMC_Q4['rooms_occupied'] = pd.to_numeric(marketPBMC_Q4['rooms_occupied'], downcast='integer')
    roomsPBMC_Q4 = marketPBMC_Q4[['date','rooms_occupied']]
    # concat df into one df
    PBCMC_quarters = [roomsPBMC_Q1, roomsPBMC_Q2, roomsPBMC_Q3, roomsPBMC_Q4]
    PBCMC_rooms = pd.concat(PBCMC_quarters)
    PBCMC_rooms['hotel'] = 'PBCMC'
    room_occupation = PBCMC_rooms

    ###############################################################################################################
    # Room occupation of 2021 of TLUZO
    # Q1
    marketTLUZO_Q1 = conn.get_market_daily_df('TLUZO','2021-01-01','2021-03-31')
    # change net_value column data type from object to float
    marketTLUZO_Q1['rooms_occupied'] = pd.to_numeric(marketTLUZO_Q1['rooms_occupied'], downcast='integer')
    roomsTLUZO_Q1 = marketTLUZO_Q1[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q2
    marketTLUZO_Q2 = conn.get_market_daily_df('TLUZO','2021-04-01','2021-06-30')
    # change net_value column data type from object to float
    marketTLUZO_Q2['rooms_occupied'] = pd.to_numeric(marketTLUZO_Q2['rooms_occupied'], downcast='integer')
    roomsTLUZO_Q2 = marketTLUZO_Q2[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q3
    marketTLUZO_Q3 = conn.get_market_daily_df('TLUZO','2021-07-01','2021-09-29')
    # change net_value column data type from object to float
    marketTLUZO_Q3['rooms_occupied'] = pd.to_numeric(marketTLUZO_Q3['rooms_occupied'], downcast='integer')
    roomsTLUZO_Q3 = marketTLUZO_Q3[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q4
    marketTLUZO_Q4 = conn.get_market_daily_df('TLUZO','2021-09-30','2021-10-31')
    # change net_value column data type from object to float
    marketTLUZO_Q4['rooms_occupied'] = pd.to_numeric(marketTLUZO_Q4['rooms_occupied'], downcast='integer')
    roomsTLUZO_Q4 = marketTLUZO_Q4[['date','rooms_occupied']]
    # concat df into one df
    TLUZO_quarters = [roomsTLUZO_Q1, roomsTLUZO_Q2, roomsTLUZO_Q3, roomsTLUZO_Q4]
    TLUZO_rooms = pd.concat(TLUZO_quarters)
    TLUZO_rooms['hotel'] = 'TLUZO'
    room_occupation = pd.concat([TLUZO_rooms,room_occupation])
    ###############################################################################################################
    # Room occupation of 2021 of MTYJW
    # Q1
    marketMTYJW_Q1 = conn.get_market_daily_df('MTYJW','2021-01-01','2021-03-31')
    # change net_value column data type from object to float
    marketMTYJW_Q1['rooms_occupied'] = pd.to_numeric(marketMTYJW_Q1['rooms_occupied'], downcast='integer')
    roomsMTYJW_Q1 = marketMTYJW_Q1[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q2
    marketMTYJW_Q2 = conn.get_market_daily_df('MTYJW','2021-04-01','2021-06-30')
    # change net_value column data type from object to float
    marketMTYJW_Q2['rooms_occupied'] = pd.to_numeric(marketMTYJW_Q2['rooms_occupied'], downcast='integer')
    roomsMTYJW_Q2 = marketMTYJW_Q2[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q3
    marketMTYJW_Q3 = conn.get_market_daily_df('MTYJW','2021-07-01','2021-09-29')
    # change net_value column data type from object to float
    marketMTYJW_Q3['rooms_occupied'] = pd.to_numeric(marketMTYJW_Q3['rooms_occupied'], downcast='integer')
    roomsMTYJW_Q3 = marketMTYJW_Q3[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q4
    marketMTYJW_Q4 = conn.get_market_daily_df('MTYJW','2021-09-30','2021-10-31')
    # change net_value column data type from object to float
    marketMTYJW_Q4['rooms_occupied'] = pd.to_numeric(marketMTYJW_Q4['rooms_occupied'], downcast='integer')
    roomsMTYJW_Q4 = marketMTYJW_Q4[['date','rooms_occupied']]
    # concat df into one df
    MTYJW_quarters = [roomsMTYJW_Q1, roomsMTYJW_Q2, roomsMTYJW_Q3, roomsMTYJW_Q4]
    MTYJW_rooms = pd.concat(MTYJW_quarters)
    MTYJW_rooms['hotel'] = 'MTYJW'
    room_occupation = pd.concat([MTYJW_rooms,room_occupation])
    ###############################################################################################################
    # Room occupation of 2021 of SLWHA
    # Q1
    marketSLWHA_Q1 = conn.get_market_daily_df('SLWHA','2021-01-01','2021-03-31')
    # change net_value column data type from object to float
    marketSLWHA_Q1['rooms_occupied'] = pd.to_numeric(marketSLWHA_Q1['rooms_occupied'], downcast='integer')
    roomsSLWHA_Q1 = marketSLWHA_Q1[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q2
    marketSLWHA_Q2 = conn.get_market_daily_df('SLWHA','2021-04-01','2021-06-30')
    # change net_value column data type from object to float
    marketSLWHA_Q2['rooms_occupied'] = pd.to_numeric(marketSLWHA_Q2['rooms_occupied'], downcast='integer')
    roomsSLWHA_Q2 = marketSLWHA_Q2[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q3
    marketSLWHA_Q3 = conn.get_market_daily_df('SLWHA','2021-07-01','2021-09-29')
    # change net_value column data type from object to float
    marketSLWHA_Q3['rooms_occupied'] = pd.to_numeric(marketSLWHA_Q3['rooms_occupied'], downcast='integer')
    roomsSLWHA_Q3 = marketSLWHA_Q3[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q4
    marketSLWHA_Q4 = conn.get_market_daily_df('SLWHA','2021-09-30','2021-10-31')
    # change net_value column data type from object to float
    marketSLWHA_Q4['rooms_occupied'] = pd.to_numeric(marketSLWHA_Q4['rooms_occupied'], downcast='integer')
    roomsSLWHA_Q4 = marketSLWHA_Q4[['date','rooms_occupied']]
    # concat df into one df
    SLWHA_quarters = [roomsSLWHA_Q1, roomsSLWHA_Q2, roomsSLWHA_Q3, roomsSLWHA_Q4]
    SLWHA_rooms = pd.concat(SLWHA_quarters)
    SLWHA_rooms['hotel'] = 'SLWHA'
    room_occupation = pd.concat([SLWHA_rooms,room_occupation])
    ###############################################################################################################
    # Room occupation of 2021 of SLWHA
    # Q1
    marketMTYGA_Q1 = conn.get_market_daily_df('MTYGA','2021-01-01','2021-03-31')
    # change net_value column data type from object to float
    marketMTYGA_Q1['rooms_occupied'] = pd.to_numeric(marketMTYGA_Q1['rooms_occupied'], downcast='integer')
    roomsMTYGA_Q1 = marketMTYGA_Q1[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q2
    marketMTYGA_Q2 = conn.get_market_daily_df('MTYGA','2021-04-01','2021-06-30')
    # change net_value column data type from object to float
    marketMTYGA_Q2['rooms_occupied'] = pd.to_numeric(marketMTYGA_Q2['rooms_occupied'], downcast='integer')
    roomsMTYGA_Q2 = marketMTYGA_Q2[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q3
    marketMTYGA_Q3 = conn.get_market_daily_df('MTYGA','2021-07-01','2021-09-29')
    # change net_value column data type from object to float
    marketMTYGA_Q3['rooms_occupied'] = pd.to_numeric(marketMTYGA_Q3['rooms_occupied'], downcast='integer')
    roomsMTYGA_Q3 = marketMTYGA_Q3[['date','rooms_occupied']]
    #roomsPBMC_Q1.head()
    # Q4
    marketMTYGA_Q4 = conn.get_market_daily_df('MTYGA','2021-09-30','2021-10-31')
    # change net_value column data type from object to float
    marketMTYGA_Q4['rooms_occupied'] = pd.to_numeric(marketMTYGA_Q4['rooms_occupied'], downcast='integer')
    roomsMTYGA_Q4 = marketMTYGA_Q4[['date','rooms_occupied']]
    # concat df into one df
    MTYGA_quarters = [roomsMTYGA_Q1, roomsMTYGA_Q2, roomsMTYGA_Q3, roomsMTYGA_Q4]
    MTYGA_rooms = pd.concat(MTYGA_quarters)
    MTYGA_rooms['hotel'] = 'MTYGA'
    room_occupation = pd.concat([MTYGA_rooms,room_occupation])
    # plot
    fig = px.line(room_occupation, x="date", y="rooms_occupied", title='Room occupation by hotel 2021', color='hotel')
    # display
    st.plotly_chart(fig)

    # MATERIALS
    with st.expander('Materials'):
        st.write(materials_df)
    # material units pie graph
    counts = materials_df['unit_name'].value_counts().rename_axis('unit_name').reset_index(name='counts')
    fig = px.pie(counts.head(10), values='counts', names='unit_name', title="Top 10 unidades de medición con más materiales", color_discrete_sequence = px.colors.sequential.Teal)
    fig.update_traces(textposition='inside', textinfo='value+label')
    # display
    st.plotly_chart(fig)

    # VENDORS
    # display data
    with st.expander('Vendors'):
        st.write(vendors_df)
    # providers map
    vendors_map = vendors_df.groupby(['region_name'], as_index=False)['name'].count()
    vendors_map["region_name"].replace({"Edo. de México": "México"}, inplace=True)
    vendors_map.rename(columns={'region_name':'Estado', 'name':'Proveedores'}, inplace=True)
    # get geo json
    from urllib.request import urlopen
    with urlopen('https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json') as response:
        geoMex = json.load(response)
    # plot
    fig = px.choropleth(
        data_frame=vendors_map, 
        locations='Estado',
        geojson=geoMex, 
        featureidkey='properties.name',
        color="Proveedores",
        color_continuous_scale='Teal'
        )
    fig.update_geos(
        showcountries=True, 
        showcoastlines=True, 
        showland=True, 
        fitbounds='locations'
        )
    fig.update_layout(
        title_text='Proveedores GHP',
        font=dict(
            family="Ubuntu",
            size=18,
            color='#7f7f7f')
            )
    # display
    st.plotly_chart(fig)

if __name__ == "__main__":
    get_venues_interface()