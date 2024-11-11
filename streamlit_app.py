# Import required packages
import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col

# Define Snowflake connection parameters using nested Streamlit secrets
connection_parameters = {
    "account": st.secrets["connections"]["snowflake"]["account"],
    "user": st.secrets["connections"]["snowflake"]["user"],
    "password": st.secrets["connections"]["snowflake"]["password"],
    "role": st.secrets["connections"]["snowflake"]["role"],
    "warehouse": st.secrets["connections"]["snowflake"]["warehouse"],
    "database": st.secrets["connections"]["snowflake"]["database"],
    "schema": st.secrets["connections"]["snowflake"]["schema"]
}

# Establish Snowflake session
session = Session.builder.configs(connection_parameters).create()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("**Choose the fruits you want in your custom Smoothie!**")

# Input for the name on the smoothies
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Fetch fruit options from Snowflake
my_dataframe = session.table("fruit_options").select(col("FRUIT_NAME")).to_pandas()

# Ingredients selection
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'],
    max_selections=5
)

# Concatenate selected ingredients into a single string and create SQL insert statement
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    st.write("Selected ingredients:", ingredients_string)

    # Create the insert statement with the selected ingredients and name
    my_insert_stmt = f"INSERT INTO smoothies.public.orders(name_on_order, ingredients) VALUES ('{name_on_order}', '{ingredients_string}')"

# Button to submit the order
time_to_insert = st.button('Submit Order')

# Execute the insert statement in Snowflake when button is pressed
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f"Awesome choice! '{name_on_order}' smoothie is now in the works. Enjoy!", icon="✅")
