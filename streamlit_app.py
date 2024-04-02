# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col 


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input('Name On Smoothie:')
st.write('The Name On Your Smoothie will be:',name_on_order)

cnx= st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
    'Choose upto 5 ingredients'
    ,my_dataframe
    ,max_selections=5
    )

if ingredients_list:
    
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        
    #st.write(ingredients_string)  

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""
    
    
    #st.write(my_insert_stmt)
    
    time_to_insert=st.button('Submit Order')
    
    if time_to_insert:     
        session.sql(my_insert_stmt).collect()  # Execute the insert statement
        st.success(f'your Smoothie is ordered,{name_on_order}!', icon="✅")
#New section to display fruityvise nutrition information  
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
