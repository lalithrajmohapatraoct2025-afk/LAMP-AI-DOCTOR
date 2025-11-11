import streamlit as st
import pandas as pd
import requests

# ----------------------- LOAD DATA -----------------------
disease_data = pd.read_excel("Diseases123.xlsx")
disease_data = disease_data.loc[:, ~disease_data.columns.str.contains('^Unnamed')]

# ----------------------- GOOGLE MAPS API KEY -----------------------
GOOGLE_MAPS_API_KEY = "AIzaSyDLmzBXn6sQlfMu0zZhfVkXIJ9_2X7Dt24"

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(page_title="AI Doctor Assistant", page_icon="🩺")

st.markdown("<h1 style='text-align:center;'>🩺 AI Doctor Assistant</h1>", unsafe_allow_html=True)

# ----------------------- USER DETAILS -----------------------
st.subheader("👤 Patient Details")

user_name = st.text_input("Name:")
user_age = st.number_input("Age:", min_value=1, max_value=120)
user_gender = st.selectbox("Gender:", ["Male", "Female", "Other"])

st.write(f"✅ Details saved for: **{user_name}**, Age: **{user_age}**, Gender: **{user_gender}**")

# ----------------------- DISEASE SEARCH -----------------------
st.subheader("🔍 Find Disease Information")

disease_list = ["--- Select ---"] + sorted(disease_data["Disease"].unique().tolist())
selected_disease = st.selectbox("Choose a disease:", disease_list)

search_input = st.text_input("Or search disease/symptom:")

# Pick highest priority result
final_query = selected_disease if selected_disease != "--- Select ---" else search_input


# ----------------------- JAVASCRIPT AUTO LOCATION -----------------------
def get_location():
    js_code = """
    <script>
    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const coords = pos.coords.latitude + "," + pos.coords.longitude;
            window.parent.postMessage({location: coords}, "*");
        },
        (err) => {
            window.parent.postMessage({location: null}, "*");
        });
    </script>
    """
    st.components.v1.html(js_code, height=0)

get_location()

location_coords = st.session_state.get("location_coords", None)

# Script listener
import streamlit.components.v1 as components

components.html("""
<script>
  window.addEventListener("message", (event) => {
      const loc = event.data.location;
      if (loc) {
          window.parent.postMessage({set_location: loc}, "*");
      }
  });
</script>
""", height=0)

# ----------------------- Capture Browser Location -----------------------
loc_event = st.experimental_get_query_params()

if "set_location" in loc_event:
    st.session_state["location_coords"] = loc_event["set_location"][0]

location_display = (
    f"📍 Your location detected: {st.session_state['location_coords']}"
    if st.session_state.get("location_coords")
    else "⚠️ Auto location not detected. Please enter manually."
)

st.subheader("📍 Location")
st.write(location_display)

manual_location = st.text_input("Or enter your city:")

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

        # ----------------------- HOSPITAL SEARCH -----------------------
        st.subheader("🏥 Nearby Hospitals")

        # Choose coordinates
        if st.session_state.get("location_coords"):
            lat, lng = st.session_state["location_coords"].split(",")
        else:
            location = manual_location
            if not location:
                st.warning("Enter a location to search hospitals.")
                lat = lng = None

        if st.session_state.get("location_coords") or manual_location:
            if st.session_state.get("location_coords"):
                # reverse geocode
                places_url = (
                    f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
                    f"location={lat},{lng}&radius=5000&type=hospital&key={GOOGLE_MAPS_API_KEY}"
                )
            else:
                # normal geocode
                geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={manual_location}&key={GOOGLE_MAPS_API_KEY}"
                geo_resp = requests.get(geocode_url).json()

                if geo_resp.get("status") == "OK":
                    lat = geo_resp["results"][0]["geometry"]["location"]["lat"]
                    lng = geo_resp["results"][0]["geometry"]["location"]["lng"]
                else:
                    st.error("Could not find this location.")
                    lat = lng = None

            if lat and lng:
                places_url = (
                    f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
                    f"location={lat},{lng}&radius=5000&type=hospital&key={GOOGLE_MAPS_API_KEY}"
                )
                places_response = requests.get(places_url).json()

                hospitals = places_response.get("results", [])

                if hospitals:
                    for h in hospitals:
                        st.write(f"🏥 **{h['name']}**")
                        st.write(h.get("vicinity", "Address unavailable"))
                        st.write("---")
                else:
                    st.error("No hospitals found.")


# ----------------------- FOOTER -----------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.write("Made with ❤️ using Streamlit")
