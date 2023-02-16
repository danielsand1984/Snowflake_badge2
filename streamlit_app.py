import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(this_fruit):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
   return pandas.json_normalize(fruityvice_response.json())

def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
      return my_cur.fetchall()
   
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit+"')")
      return streamlit.text("Thanks for adding " + new_fruit)

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#Web page
streamlit.title('My parents now have a healthy diner')


streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
Fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
# Display the table on the page.
fruit_to_show = my_fruit_list.loc[Fruits_selected]
streamlit.dataframe(fruit_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get infromation")
  else:
    streamlit.write('The user entered ', fruit_choice)
    
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
    streamlit.error()
 
if streamlit.button('get fruit load list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   streamlit.header("The fruit load list contains")
   streamlit.dataframe(get_fruit_load_list())

add_my_fruit = streamlit.text_input("What fruit would you like to add?")

if streamlit.button('Add fruit to the list'):
   streamlit.text(insert_row_snowflake(add_my_fruit))
