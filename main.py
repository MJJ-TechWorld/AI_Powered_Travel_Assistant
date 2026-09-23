import streamlit as st
from datetime import date, timedelta
from dotenv import load_dotenv
load_dotenv()
from google import genai
client = genai.Client()

st.set_page_config(page_title="AI Powered Travel Assistant", page_icon="✈️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');
html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: 
        linear-gradient(180deg, rgba(255,255,255,0.55) 0%, rgba(255,255,255,0.94) 50%, rgba(240,245,255,0.82) 100%),
        url("https://images.unsplash.com/photo-1488085061387-422e29b40080?w=1920&q=80&auto=format&fit=crop") no-repeat center top;
    background-size: cover;
    background-attachment: fixed;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: url("https://images.unsplash.com/photo-1500835556837-99ac94a94552?w=1920&q=60&auto=format&fit=crop") no-repeat center;
    background-size: cover;
    opacity: 0.12;
    pointer-events: none;
    z-index: 0;
}

.hero {
    text-align: center;
    padding: 2.8rem 1rem 2rem 1rem;
    position: relative;
    z-index: 2;
    background: rgba(255,255,255,0.88);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 24px;
    margin: 18px auto 24px auto;
    max-width: 860px;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.6rem;
    font-weight: 800;
    letter-spacing: -2px;
    background: linear-gradient(100deg, #0f172a 0%, #6366f1 55%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: #6366f1;
    font-size: 1.15rem;
    font-weight: 600;
    max-width: 620px;
    margin: 10px auto 0 auto;
    line-height: 1.5;
}

.card {
    background: rgba(255,255,255,0.95);
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 18px;
    position: relative;
    z-index: 2;
}
.card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    background: linear-gradient(90deg, #6366f1 0%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 16px;
}

label, .stSelectbox label, .stTextInput label, .stNumberInput label, .stDateInput label, .stMultiSelect label, .stRadio label {
    color: #334155 !important;
    font-weight: 600 !important;
}
div[data-testid="stWidgetLabel"] p {
    color: #1e293b !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

.stButton > button {
    background: linear-gradient(100deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
    color: white;
    border-radius: 16px;
    padding: 1.1rem 2.5rem;
    font-weight: 800;
    font-size: 1.15rem;
    border: none;
    position: relative;
    z-index: 2;
}

.itinerary-box {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 24px;
    padding: 32px;
    position: relative;
    z-index: 2;
    margin-top: 28px;
}
.itinerary-box h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(100deg, #0f172a 0%, #6366f1 60%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.itinerary-box h3 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.32rem;
    margin-top: 26px;
    margin-bottom: 10px;
}
.itinerary-box h3:nth-of-type(1) { color: #6366f1; }
.itinerary-box h3:nth-of-type(2) { color: #0ea5e9; }
.itinerary-box h3:nth-of-type(3) { color: #f59e0b; }
.itinerary-box h3:nth-of-type(4) { color: #10b981; }
.itinerary-box h3:nth-of-type(5) { color: #ec4899; }
.itinerary-box h3:nth-of-type(6) { color: #8b5cf6; }
.itinerary-box h3:nth-of-type(7) { color: #ef4444; }
.itinerary-box h3:nth-of-type(8) { color: #06b6d4; }
.itinerary-box p { color: #334155; font-size: 1.05rem; line-height: 1.8; font-weight: 500; }
.itinerary-box li { color: #1e293b; font-size: 1.05rem; line-height: 1.8; font-weight: 500; }
.itinerary-box strong, .itinerary-box b { color: #6366f1; font-weight: 700; }
.itinerary-box li strong { color: #0ea5e9; }
.itinerary-box li em { color: #ec4899; font-style: normal; font-weight: 600; }

.footer-pro {
    text-align: center;
    padding: 44px 20px 28px 20px;
    position: relative;
    z-index: 2;
    background: rgba(255,255,255,0.92);
    border-top: 1px solid #e2e8f0;
    margin-top: 60px;
    border-radius: 20px 20px 0 0;
}
.footer-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    background: linear-gradient(90deg, #0f172a 0%, #6366f1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 1.15rem;
}
.footer-sub { color: #6366f1; font-size: 0.92rem; margin-top: 8px; font-weight: 600; line-height: 1.5; }
.footer-copy { color: #64748b; font-size: 0.82rem; margin-top: 14px; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>AI Powered Travel Assistant</h1>
    <p>Your Personal AI Assistant That Plans Your Entire Trip With Best Hotels, Best Places, Best Restaurants And Full Schedule</p>
</div>
""", unsafe_allow_html=True)

AGE_GROUP_SINGLE = ["Mostly Young Adults (18-29)", "Mostly Adults (30-59)", "With Seniors (60+)", "Family with Kids (Kids + Adults)", "Kids Only (0-12)", "Teens (13-17)", "Mixed Group (All Ages)", "All of the Above (Mixed Ages)"]
OCCASION_OPTIONS = ["None", "Honeymoon", "Anniversary", "Birthday", "Family Vacation", "Graduation", "Bachelor/Bachelorette Party", "Workation", "Other (Custom)"]
TRAVEL_MODE_OPTIONS = ["Flight", "Train", "Bus", "Car / Self-Drive", "Cruise", "Mix (Flight + Local)"]
FOOD_OPTIONS = ["Vegetarian", "Non-Vegetarian", "Eggetarian"]
ATTRACTION_OPTIONS = ["Beaches & Islands", "Mountains & Hills", "Historical Monuments", "Temples & Spiritual Sites", "Wildlife Safari", "Scuba Diving", "Snorkeling", "Paragliding", "River Rafting", "Trekking / Hiking", "City Sightseeing", "Museums & Art Galleries", "Shopping Markets", "Nightlife & Bars", "Food Tour / Cooking Class", "Spa & Wellness", "Photography Spots", "Adventure Parks", "Cultural Shows", "Boating / Cruises", "Other (Custom)"]
AVOID_OPTIONS = ["No Trekking / Hiking", "No Long Walks", "No Crowded Places", "No Night Travel", "No Adventure Sports", "No Non-Veg Food Areas", "No Alcohol Places", "No Early Mornings", "No Shopping", "Other (Custom)"]
MEDICAL_OPTIONS = ["None", "Knee / Joint Pain", "Back Pain", "Asthma / Breathing Issue", "Heart Condition", "Diabetes", "Cannot Walk Long Distances", "Wheelchair Support Needed", "Pregnancy", "Motion Sickness", "Other (Custom)"]
FOOD_ALLERGY_OPTIONS = ["None", "Peanuts", "Dairy / Lactose", "Gluten", "Shellfish / Seafood", "Eggs", "Soy", "Other (Custom)"]

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="card"><div class="card-title">Destination & Dates</div>', unsafe_allow_html=True)
    destination = st.text_input("What is your intended destination?", placeholder="e.g. Bali, Switzerland, Kerala")
    departure_city = st.text_input("What is your city of departure?", placeholder="e.g. Mumbai, Delhi")
    travel_dates = st.date_input("What are your preferred travel dates? (Start & End)", value=(date.today(), date.today() + timedelta(days=4)), format="DD/MM/YYYY")
    if isinstance(travel_dates, tuple) and len(travel_dates) == 2:
        trip_duration = (travel_dates[1] - travel_dates[0]).days + 1
        if trip_duration <= 0: trip_duration = 1
    else:
        trip_duration = 1
    st.success(f"Trip Duration Auto-Calculated: {trip_duration} Days")
    dates_flexible = st.selectbox("Are your travel dates flexible?", ["Yes, Flexible", "No, Fixed", "Flexible by 2-3 Days"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Travel Mode</div>', unsafe_allow_html=True)
    main_transport_mode = st.selectbox("Select your main travel mode", TRAVEL_MODE_OPTIONS)
    flight_class = None
    flights_included = "No"
    train_class = None
    bus_type = None
    if main_transport_mode in ["Flight", "Mix (Flight + Local)"]:
        flights_included = st.radio("Should flights be included in the budget?", ["Yes", "No"], horizontal=True, key="flight_inc")
        flight_class = st.selectbox("Preferred flight class?", ["Economy", "Premium Economy", "Business", "First Class"])
    elif main_transport_mode == "Train":
        train_class = st.selectbox("Preferred train class?", ["Sleeper", "3AC", "2AC", "1AC", "Chair Car"])
    elif main_transport_mode == "Bus":
        bus_type = st.selectbox("Preferred bus type?", ["Regular", "AC Sleeper", "Volvo / Luxury"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Budget Details</div>', unsafe_allow_html=True)
    budget = st.number_input("What is your total estimated budget?", min_value=0, value=80000, step=5000)
    budget_type = st.radio("Is your budget per person or for whole group?", ["Per Person", "For Whole Group"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><div class="card-title">Travellers</div>', unsafe_allow_html=True)
    num_travellers = st.number_input("How many travellers are there?", min_value=1, max_value=10, value=2)
    traveller_relationship = st.selectbox("What is the relationship between travellers?", ["Solo", "Couple", "Family", "Friends", "Honeymoon", "Business Group"])
    overall_age_group = st.selectbox("What is the overall age group of your travellers? (One idea for all)", AGE_GROUP_SINGLE)
    nationality = st.text_input("What is your nationality?", placeholder="e.g. Indian")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Occasion & Stay Preferences</div>', unsafe_allow_html=True)
    special_occasion = st.selectbox("Are you celebrating a special occasion?", OCCASION_OPTIONS)
    special_occasion_custom = ""
    if "Other" in special_occasion and "Custom" in special_occasion:
        special_occasion_custom = st.text_input("Please specify your occasion", placeholder="e.g. Proposal...")
    accommodation_category = st.selectbox("Preferred accommodation category?", ["3-Star Hotel", "4-Star Hotel", "5-Star Hotel", "Boutique Stay", "Villa", "Homestay", "Hostel", "Resort"])
    room_sharing = st.selectbox("Room sharing preference?", ["Double Room", "Twin Room", "Single Rooms", "Family Suite", "Separate Rooms"])
    local_transport = st.selectbox("Preferred mode of local transport?", ["Private Car with Driver", "Public Transport", "Self-Drive", "Mix of All", "Bike / Scooter"])
    travel_pace = st.selectbox("What is your preferred travel pace?", ["Very Relaxed", "Relaxed", "Balanced", "Fast-Paced"])
    trip_purpose = st.selectbox("What is the main purpose of your trip?", ["Leisure", "Honeymoon", "Family Vacation", "Adventure", "Culture & Heritage", "Relaxation", "Spiritual"])
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card"><div class="card-title">Journey Experiences</div>', unsafe_allow_html=True)
je1, je2 = st.columns(2)
with je1:
    travel_interests = st.multiselect("What are your primary travel interests? ", ["Nature", "Beaches", "Mountains", "History & Culture", "Wildlife", "Nightlife", "Food", "Shopping", "Spiritual", "Photography", "Adventure", "Relaxation"])
    must_do = st.multiselect("Must-do attractions? (Best places)", ATTRACTION_OPTIONS)
    must_do_custom = ""
    if any("Other" in x and "Custom" in x for x in must_do):
        must_do_custom = st.text_input("Specify custom attractions", placeholder="e.g. Hot Air Balloon", key="must_custom")
    avoid_activities = st.multiselect("Activities you want to strictly avoid?", AVOID_OPTIONS)
    avoid_custom = ""
    if any("Other" in x and "Custom" in x for x in avoid_activities):
        avoid_custom = st.text_input("Specify what to avoid", placeholder="e.g. Heights", key="avoid_custom")
with je2:
    food_preferences = st.selectbox("What are your food preferences?", FOOD_OPTIONS)
    food_allergies = st.multiselect("Food allergies?", FOOD_ALLERGY_OPTIONS)
    food_allergies_custom = ""
    if any("Other" in x and "Custom" in x for x in food_allergies):
        food_allergies_custom = st.text_input("Specify allergy", placeholder="e.g. Mushroom", key="allergy_custom")
    medical_concerns = st.multiselect("Medical or mobility concerns?", MEDICAL_OPTIONS)
    medical_custom = ""
    if any("Other" in x and "Custom" in x for x in medical_concerns):
        medical_custom = st.text_input("Specify medical concern", placeholder="e.g. Vertigo", key="med_custom")
    visa_assistance = st.radio("Need visa assistance?", ["Yes", "No"], horizontal=True)
    travel_insurance = st.radio("Need travel insurance?", ["Yes", "No"], horizontal=True)
    need_guide = st.radio("Need a tour guide?", ["Yes", "No"], horizontal=True)
    guide_language = st.selectbox("Preferred language for guide?", ["English", "Hindi", "English + Hindi", "Local Language"])
st.markdown('</div>', unsafe_allow_html=True)

if st.button("Craft My Premium Itinerary - Plan My Entire Trip", use_container_width=True):
    final_occasion = special_occasion_custom if special_occasion_custom else special_occasion
    final_must_do = ", ".join(must_do) + (f", {must_do_custom}" if must_do_custom else "")
    final_avoid = ", ".join(avoid_activities) + (f", {avoid_custom}" if avoid_custom else "")
    final_allergies = ", ".join(food_allergies) + (f", {food_allergies_custom}" if food_allergies_custom else "")
    final_medical = ", ".join(medical_concerns) + (f", {medical_custom}" if medical_custom else "")
    transport_summary = f"{main_transport_mode}"
    if flight_class: transport_summary += f" ({flight_class})"
    if train_class: transport_summary += f" ({train_class})"
    if bus_type: transport_summary += f" ({bus_type})"

    prompt = f"""
You are a WORLD-CLASS Luxury Travel Planner and Personal Guide. Your job is to plan the ENTIRE trip like a real human travel expert, not just list inputs. You must think through every input and create best recommendations.

USER INPUTS - USE EVERY SINGLE ONE:
Destination: {destination}
From: {departure_city}
Duration: {trip_duration} days ({travel_dates}) | Flexible: {dates_flexible}
Travellers: {num_travellers} ({traveller_relationship}) | Overall Age Group: {overall_age_group} | Nationality: {nationality}
Transport: Main {transport_summary} | Local {local_transport} | Flights in Budget: {flights_included}
Budget: Rs {budget} ({budget_type}) | Pace: {travel_pace} | Purpose: {trip_purpose} | Occasion: {final_occasion}
Stay: {accommodation_category} | Room: {room_sharing}
Interests: {', '.join(travel_interests) if travel_interests else 'General'}
Must-Do Best Places: {final_must_do or 'Suggest best of destination'}
Strictly Avoid: {final_avoid or 'None'}
Food: {food_preferences} | Allergies: {final_allergies or 'None'} | Medical: {final_medical or 'None'}
Services: Visa {visa_assistance} | Insurance {travel_insurance} | Guide {need_guide} ({guide_language})

NOW CREATE FULL ITINERARY WITH THESE EXACT SECTIONS, BE VERY DETAILED, BULLET POINTS, USE ALL INPUTS:

### Trip At A Glance
Give 3-4 bullets summary of destination, duration, travellers, occasion, budget.

### Why This Plan Fits You Perfectly
Explain each input in separate bullet: Why Age Group {overall_age_group} matters for pace and hotel choice, Why {traveller_relationship} matters for room, Why Budget {budget} split, Why Food {food_preferences} and Allergy {final_allergies} handled, Why Must-Do {final_must_do} placed, Why Avoid {final_avoid} removed completely, Why Medical {final_medical} considered with low walks and clinics.

### Best Hotels For You (Based on Budget {budget}, {accommodation_category}, {overall_age_group}, {final_occasion}, {room_sharing})
Give 3 BEST hotels: Name, Exact Location, Price per night (calculate from budget), Why perfect for {overall_age_group} and {traveller_relationship} and {final_occasion}, Amenities for {final_medical}, Food {food_preferences} restaurant availability, Room type {room_sharing}.

### Best Places To Visit (Based on {', '.join(travel_interests) if travel_interests else 'interests'} and {final_must_do})
Give 6-8 best places: Name, Best time to visit, Entry fee, Why matches your interests, How it avoids {final_avoid}, Suitable for {overall_age_group}.

### Best Restaurants (100% {food_preferences}, Allergy Safe {final_allergies})
Give 4-5 best restaurants: Name, Cuisine, Must-try {food_preferences} dish, Price, How they handle {final_allergies}, Why good for {overall_age_group}.

### Full Day-Wise Schedule Day 1 to Day {trip_duration}
For EACH day create:
Day X - Title
- Morning (9 AM - 12 PM): Activity, Place, Why for {overall_age_group}, Cost, Transport {local_transport}
- Afternoon (12 PM - 5 PM): Activity, Restaurant for {food_preferences} lunch, Rest for {final_medical}
- Evening (5 PM - 9 PM): Activity, Dinner spot, Sunset or cultural show
- Tips for {final_medical} and {overall_age_group}

### Budget Breakdown (Rs {budget} - {budget_type})
Give table bullets: Transport {transport_summary} 35%, Stay {accommodation_category} 40%, Food {food_preferences} 15%, Activities 10% with exact rupee calculation.

### Packing, Safety & Local Tips For {destination} and {nationality}
Based on {final_medical}, {overall_age_group}, {destination} weather, Visa {visa_assistance} for {nationality}, Local transport {local_transport} tips, Guide {guide_language}.

### Final Checklist - No Doubts Left
Bullet checklist covering booking {transport_summary} from {departure_city} to {destination}, hotel {accommodation_category} with {room_sharing}, {food_preferences} restaurants list, medical kit for {final_medical}, insurance {travel_insurance}, guide {need_guide}.

RULES: NEVER suggest {final_avoid}, Food MUST be strictly {food_preferences}, Consider {overall_age_group} for intensity and walk limits, Be LONG, detailed, attractive, bullet points. Plan like a pro human guide.
"""

    with st.spinner("Planning your entire trip with best hotels, places, restaurants and full schedule using powerful AI tools..."):
        try:
            interaction = client.interactions.create(
                model="gemini-3.5-flash-lite",
                input=prompt
            )
            itinerary_text = interaction.output_text
        except Exception as e:
            itinerary_text = f"API Key not found in .env or error: {e}\n\nFallback Plan for {destination or 'Trip'} - {trip_duration} Days - {overall_age_group} - {food_preferences} - Avoid {final_avoid} - Budget {budget} - Best hotels, places, restaurants will be planned once API key is set in .env file."

    st.markdown(f"""
    <div class="itinerary-box">
        <h2>Your Entire Trip Planned - {destination or 'Your Dream Destination'}</h2>
        <p>{trip_duration} Days • {num_travellers} Travellers • {overall_age_group} • {main_transport_mode} • {food_preferences} • Best Hotels, Places & Restaurants</p>
        <hr style="margin:20px 0; border:none; border-top:1px solid #e2e8f0;">
        <div style="white-space: pre-wrap;">{itinerary_text}</div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="Download Your Complete Itinerary",
        data=itinerary_text,
        file_name=f"{destination or 'Trip'}_Full_Plan.txt",
        mime="text/plain",
        use_container_width=True
    )
    st.balloons()

st.markdown("""
<div class="footer-pro">
    <div class="footer-title">Travel Assistant</div>
    <div class="footer-sub">Crafted For Explorers, Designed By MJJ-TechWorld</div>
    <div class="footer-sub">Your Data Is Safe & Private • Secure, Encrypted & Trusted By Sanket Dodya Sir</div>
    <div class="footer-copy">© 2026 Travel Planner. All Rights Reserved. | Terms Of Service | Privacy Policy | Cookie Policy | Disclaimer<br>Designed & Developed By MJJ-TechWorld • Made In India • Support: support@mjjtechworld.com • Version 2.0</div>
</div>
""", unsafe_allow_html=True)
