import streamlit as st
import pandas as pd
import plotly.express as px
from frames import materials_df

def get_materials_interface():

    # data
    pd.set_option('display.max_columns', None)
    materials = materials_df

    # page format
    st.title('Materiales')
    col1, col2 = st.columns([1,2])
    # column 1
    with col1:
        st.header('test header col1')
        st.dataframe(materials)
    # column 2
    with col2:
        st.header('test header col2')
        # Plots
        # material units pie graph
        counts = materials['unit_name'].value_counts().rename_axis('unit_name').reset_index(name='counts')
        fig = px.pie(
            counts.head(10), 
            values='counts', 
            names='unit_name', 
            title="Top 10 unidades de medición con más materiales", 
            color_discrete_sequence = px.colors.sequential.Teal
            )
        fig.update_traces(textposition='inside', textinfo='value+label')
        # display
        st.plotly_chart(fig)

if __name__ == "__main__":
    get_materials_interface()