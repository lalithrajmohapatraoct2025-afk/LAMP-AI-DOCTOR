import streamlit as st
import pandas as pd
import requests

# ----------------------- LOAD DATA -----------------------
disease_data = pd.read_excel("Diseases123.xlsx")
disease_data = disease_data.loc[:, ~disease_data.columns.str.contains('^Unnamed')]

# ----------------------- GOOGLE API KEY -----------------------
GOOGLE_MAPS_API_KEY = "AIzaSyDLmzBXn6sQlfMu0zZhfVkXIJ9_2X7Dt24"

# ----------------------- AUTO LOCATION -----------------------
def auto_detect_city():
    try:
        response = requests.get("https://ipinfo.io").json()
        return response.get("city", None)
    except:
        return None


# ----------------------- HOSPITAL FINDER -----------------------
def find_hospitals(location):
    try:
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}"
        geocode_response = requests.get(geocode_url).json()

        if geocode_response.get("status") != "OK":
            return None, None, []

        lat = geocode_response["results"][0]["geometry"]["location"]["lat"]
        lng = geocode_response["results"][0]["geometry"]["location"]["lng"]

        places_url = (
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
            f"location={lat},{lng}&radius=5000&type=hospital&key={GOOGLE_MAPS_API_KEY}"
        )
        places_response = requests.get(places_url).json()

        hospitals = []
        for place in places_response.get("results", []):
            hospitals.append({
                "name": place["name"],
                "address": place.get("vicinity", "Address unavailable")
            })

        return lat, lng, hospitals
    except:
        return None, None, []


# ----------------------- PAGE UI -----------------------
st.set_page_config(page_title="AI Doctor Assistant", page_icon="🩺")

st.markdown("<h1 style='text-align:center;'>🩺 AI Doctor Assistant</h1>", unsafe_allow_html=True)

# ----------------------- DROPDOWN + SEARCH BOX -----------------------
st.subheader("🔍 Find Disease Information")

disease_list = ["--- Select ---"] + sorted(disease_data["Disease"].unique().tolist())
selected_disease = st.selectbox("Choose a disease:", disease_list)

search_input = st.text_input("Or search disease/symptom:")

# Determine final disease value
final_query = None
if selected_disease != "--- Select ---":
    final_query = selected_disease
elif search_input:
    final_query = search_input


# ----------------------- DISPLAY DISEASE INFO -----------------------
if final_query:
    result_df = disease_data[disease_data["Disease"].str.contains(final_query, case=False, na=False)]

    if result_df.empty:
        st.warning("No matching disease found.")
    else:
        row = result_df.iloc[0]

        st.subheader("✅ Disease Information")
        st.write(f"**Disease:** {row['Disease']}")
        st.write(f"**Category:** {row['Category']}")
        st.write(f"**Common Symptoms:** {row['Common Symptoms']}")
        st.write(f"**Specialist to Consult:** {row['Specialist to Consult']}")

        # ----------------------- AUTO LOCATION -----------------------
        st.subheader("📍 Nearby Hospitals")

        auto_city = auto_detect_city()
        st.write(f"Auto-detected location: **{auto_city}**" if auto_city else "Location detection failed.")

        location_input = st.text_input("Enter your city (or keep auto-detected):", value=auto_city)

        if location_input:
            lat, lng, hospitals = find_hospitals(location_input)

            if hospitals:
                st.success("✅ Hospitals Found Nearby")
                for h in hospitals:
                    st.write(f"🏥 **{h['name']}**")
                    st.write(h["address"])
                    st.write("---")
            else:
                st.error("Could not find hospitals. Try a different location.")


# ----------------------- FOOTER -----------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.write("Made with ❤️ using Streamlit")
