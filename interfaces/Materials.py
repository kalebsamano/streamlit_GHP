import sys
import config
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ghp_suite_api import GHPSuiteApiConnector # Importing the librar

def get_materials_interface():
    # coverage_stats = shared_state.coverage_stats
    # connection
    conn = GHPSuiteApiConnector(config.api_key)
    r = conn.test_connection()
    if r != '':
        sys.exit('Connection failed. ' + r)
    # page format
    st.title('Materiales')
    pd.set_option('display.max_columns', None)
    materials_df = conn.get_procurement_material_catalog_df()
    # Plots
    with st.expander('Materials'):
        st.write(materials_df)
    # material units pie graph
    counts = materials_df['unit_name'].value_counts().rename_axis('unit_name').reset_index(name='counts')
    fig = px.pie(counts.head(10), values='counts', names='unit_name', title="Top 10 unidades de medición con más materiales", color_discrete_sequence = px.colors.sequential.Teal)
    fig.update_traces(textposition='inside', textinfo='value+label')
    # display
    st.plotly_chart(fig)


if __name__ == "__main__":
    get_materials_interface()