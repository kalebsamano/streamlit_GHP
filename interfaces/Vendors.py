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
from ghp_suite_api import GHPSuiteApiConnector # Importing the librar

def get_vendors_interface():
    # coverage_stats = shared_state.coverage_stats
    # connection
    conn = GHPSuiteApiConnector(config.api_key)
    r = conn.test_connection()
    if r != '':
        sys.exit('Connection failed. ' + r)
    
    st.header("Vendors")
    st.title('GHP Data  Project')
    pd.set_option('display.max_columns', None)
    vendors_df = conn.get_procurement_vendor_catalog_df()
    
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
    get_vendors_interface()