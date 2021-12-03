import json
import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
from frames import vendors_df

#@st.cache(suppress_st_warning=True)
def get_vendors_interface():
    
    st.title('Proveedores')
    pd.set_option('display.max_columns', None)
    
    vendors = vendors_df
    
    # display data
    with st.expander('Vendors'):
        st.write(vendors)

    # providers map
    vendors_map = vendors.groupby(['region_name'], as_index=False)['name'].count()
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
        title='Proveedores GHP',
        font=dict(
            family="Ubuntu",
            size=18,
            color='#7f7f7f')
            )
    # display
    st.plotly_chart(fig)

if __name__ == "__main__":
    get_vendors_interface()