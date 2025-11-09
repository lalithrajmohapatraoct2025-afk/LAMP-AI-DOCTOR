import streamlit as st
import pandas as pd

# Load Excel data
df = pd.read_excel("Diseases123.xlsx")

st.title("Lamp AI Doctor")

# Ask user for basic info
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=1, max_value=120)
gender = st.selectbox("Select gender", ["Male", "Female", "Other"])

st.write("---")

st.subheader("Disease Information Assistant")

# Dropdown of diseases
disease_list = df["Disease"].dropna().unique()

selected_disease = st.selectbox("Select a disease", disease_list)

# Display details of selected disease
if selected_disease:
    info = df[df["Disease"] == selected_disease].iloc[0]

    st.write("### Disease Details")
    st.write(f"**Category:** {info['Category']}")
    st.write(f"**Common Symptoms:** {info['Common Symptoms']}")
    st.write(f"**Specialist to Consult:** {info['Specialist to Consult']}")


