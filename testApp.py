# Data visualization project for GHP
# 
# By: Jose, Rafael and Diego

# libraries
import streamlit as st
#from interfaces2.Vendors2 import get_vendors_interface
from interfaces2.Materials2 import get_materials_interface
#from interfaces2.Purchases2 import get_purchases_interface
from  interfaces2.Vendor_Analysis2 import get_vendor_analysis_interface2

############################################################################################
#Barside
############################################################################################
st.set_page_config(layout="wide")

#barside helpers
st.sidebar.image('src/img/ghp.png', width=200)
st.sidebar.header('Menu')

# title
#st.title('Abastecimiento general')

# menu
menu = st.sidebar.radio(
    "",
    ('Materiales','Vendor Analysis'),
)

# sidebar
st.sidebar.markdown('---')
st.sidebar.write('Jose Gonzalez | Diego Samano | Rafa Velasco | Diciembre 2021')

# menu options
if menu == 'Materiales':
    get_materials_interface()
elif menu == 'Vendor Analysis':
    get_vendor_analysis_interface2()
#elif menu == 'Proveedores':
     #get_vendors_interface()
#elif menu == 'Compras':
    #get_purchases_interface()