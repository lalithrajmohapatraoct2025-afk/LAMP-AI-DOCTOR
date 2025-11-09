import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO

# Load disease list
@st.cache_data
def load_diseases():
    try:
        df = pd.read_excel("Diseases123.xlsx")
        disease_list = df.iloc[:, 0].dropna().tolist()
        return disease_list
    except:
        return ["No diseases found"]

disease_list = load_diseases()

# UI
st.set_page_config(page_title="LAMP AI Doctor", layout="centered")

st.title("🩺 LAMP AI Doctor Chatbot")

# Animated doctor gif
st.markdown(
    """
    <div style='text-align:center;'>
        <img src='https://media.giphy.com/media/3oEjHI8z6FKScV9Pfy/giphy.gif' width='200'>
    </div>
    """,
    unsafe_allow_html=True
)

# User info
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=1, max_value=120)
gender = st.selectbox("Select gender", ["Male", "Female", "Other"])

st.write("---")

st.subheader(f"Hello {name}, how can I help you today?")

question = st.text_input("Ask about any disease or health issue")

if question:
    st.write("Select a disease from the list below:")
    selected_disease = st.selectbox("Diseases available:", disease_list)
    st.write(f"You selected: **{selected_disease}**")

st.write("---")
st.subheader("Find Nearest Hospital 🏥")

location = st.text_input("Enter your current location")

if location:
    maps_url = f"https://www.google.com/maps/search/hospitals+near+{location.replace(' ', '+')}"
    st.write(f"[Click to find nearest hospitals]({maps_url})")

st.write("---")
st.subheader("Generate QR Code for chatbot URL")

chatbot_url = st.text_input("Enter the deployed chatbot URL")

if chatbot_url:
    qr = qrcode.make(chatbot_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    st.image(buffer.getvalue(), caption="Scan to open chatbot")
