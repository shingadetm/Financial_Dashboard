import streamlit as st

st.set_page_config(layout="wide")
st.title("�� Stock Dashboard Home")
st.write("Welcome! Use the sidebar to navigate between pages.")

## Use of st.button :  Bydefault its False, when clicked it turns to True, excecute logic and emmidiatly go back to False
animal_shelter = ['cat', 'dog', 'rabbit', 'bird']
animal = st.text_input('Type an animal')
if st.button('Check availability'):
    have_it = animal.lower() in animal_shelter
    'We have that animal!' if have_it else 'We don\'t have that animal.'


## 
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('Click me', on_click=click_button)

if st.session_state.clicked:
    # The message and nested widget will remain on the page
    st.write('Button clicked!')
    st.slider('Select a value')