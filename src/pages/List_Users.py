import streamlit as st
from api.users import User

# Styles
BACKGROUND_COLOR = "#CCCCCC"

DIV_MAIN = f'''
  display: flex; 
  align-items: start; 
  justify-content: space-between; 
  padding: 10px; 
  border-radius: 5px; 
  background-color: {BACKGROUND_COLOR}; 
  color: black;
'''

DIV_CONT = f'''
  display: flex; 
  flex-direction: column; 
  max-width: 60%
'''

DIV_ELEM = f'''
  color: black
'''

USER_IMG = f'''
  height: 40%; 
  max-width: 35%; 
  margin-right: 20px;
  color: black
'''

USER_NO_IMG = f'''
  margin-top: auto;
  margin-bottom: auto;
  margin-right: 20px;
  color: black
'''

# Page

PAGE_TITLE = "List of Users"

st.set_page_config(page_title=PAGE_TITLE, layout='wide')

st.header(PAGE_TITLE)
users = User().get_users()

if users:
  for index, user in enumerate(users):
    st.markdown(
      f'<div style="{(DIV_MAIN)}">'
        f'<div style="{DIV_CONT}">'
          f'<h2 style="{DIV_ELEM}">{user.username} - {user.first_name} {user.last_name}</h2>'
          f'<h3 style="{DIV_ELEM}">{user.role}</h3>'
        f'</div>'
      f'<img src="{user.user_photo_url}" alt="User Photo" style="{USER_IMG if user.user_photo_url is not None else USER_NO_IMG}">'
      f'</div>',
      unsafe_allow_html=True
    )

    st.text('')