import streamlit as st

st.title("Моё первое приложение на Streamlit 🚀")
st.write("Привет! Это тестовое приложение.")

name = st.text_input("Введите ваше имя:")
if name:
    st.write(f"Приятно познакомиться, {name}! 😊")
