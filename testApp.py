# Data visualization project for GHP
# 
# By: Jose, Rafael and Diego

# libraries
import streamlit as st
#from interfaces2.Vendors2 import get_vendors_interface
from interfaces.Pricing_Analysis import get_pricing_analysis_interface
#from interfaces2.Purchases2 import get_purchases_interface
from  interfaces.Vendor_Analysis import get_vendor_analysis_interface2

############################################################################################
#Barside
############################################################################################
st.set_page_config(layout="centered", page_title='PRISMA')

#barside helpers
st.sidebar.image('src/img/ghp.png', width=200)
st.sidebar.header('Menu')

# menu
menu = st.sidebar.radio(
    "",
    ('Vendor Analysis', 'Pricing Analysis'),
)

# sidebar
st.sidebar.markdown('---')
st.sidebar.write('Jose Gonzalez | Diego Samano | Rafa Velasco | Diciembre 2021')

# menu options
if menu == 'Vendor Analysis':
    get_vendor_analysis_interface2()
elif menu == 'Pricing Analysis':
    get_pricing_analysis_interface()
#elif menu == 'Proveedores':
     #get_vendors_interface()
#elif menu == 'Compras':
    #get_purchases_interface()