import streamlit as st # type: ignore
import pandas as pd # type: ignore
import plotly.express as px # type: ignore
from datetime import datetime
import random

# Set page config
st.set_page_config(page_title="Shrimp Lab Management", layout="wide")

# Generate sample data for growths and harvests
def generate_sample_data():
    tanks = [f"Tank{i}" for i in range(1, 16)]
    months = ["January", "February", "March"]
    data = []

    for month in months:
        total = 50  # Total millions for the month
        for tank in tanks:
            amount = random.randint(1, 10)  # Random amount between 1 and 10 million
            total -= amount
            if total < 0:
                amount += total  # Adjust last amount if we've gone over 50
                total = 0
            data.append({"tank": tank, "gross_millions": amount, "production_month": month})
        if total > 0:  # Distribute any remaining amount
            data[-1]["gross_millions"] += total

    return pd.DataFrame(data)

# Generate sample data
df = generate_sample_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Growths and Harvests", "Feed Costs per Run", "Events Timeline"])

# Function to check for unread emails (placeholder)
def check_unread_emails():
    # This is a placeholder. You'd need to implement actual email checking logic here.
    return random.randint(0, 10)

# Home page
if page == "Home":
    st.title("Shrimp Larvae Production Lab")
    st.header("Welcome to the Lab Management System")
    
    # User information
    st.subheader("User Information")
    user_name = "John Doe"  # This would be dynamic in a real app
    st.write(f"Logged in as: {user_name}")
    
    # Email notification
    unread_emails = check_unread_emails()
    st.info(f"You have {unread_emails} unread emails.")
    
    # Quick links or shortcuts
    st.subheader("Quick Links")
    if st.button("View Latest Growth Data"):
        st.session_state.page = "Growths and Harvests"
    if st.button("Check Feed Costs"):
        st.session_state.page = "Feed Costs per Run"
    if st.button("Log New Event"):
        st.session_state.page = "Events Timeline"

# Growths and Harvests page
elif page == "Growths and Harvests":
    st.title("Growths and Harvests")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    # Use uploaded file if available, otherwise use sample data
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.info("Using sample data. Upload a CSV file to use your own data.")
    
    # Month selection
    months = df['production_month'].unique()
    selected_month = st.selectbox("Select Production Month", months)
    
    # Filter data for selected month
    filtered_df = df[df['production_month'] == selected_month]
    
    # Display filtered data
    st.subheader(f"Production Data for {selected_month}")
    st.write(filtered_df)
    
    # Bar chart
    fig_bar = px.bar(filtered_df, x='tank', y='gross_millions', 
                     title=f'Gross Millions by Tank for {selected_month}')
    st.plotly_chart(fig_bar)
    
    # Distribution plot
    fig_dist = px.histogram(filtered_df, x='gross_millions', nbins=20,
                            title=f'Distribution of Gross Millions for {selected_month}')
    st.plotly_chart(fig_dist)
    
    # Box plot
    fig_box = px.box(filtered_df, y='gross_millions', 
                     title=f'Distribution of Gross Millions for {selected_month}')
    st.plotly_chart(fig_box)

# Feed Costs per Run page
elif page == "Feed Costs per Run":
    st.title("Feed Costs per Run")
    
    # Simulated data - replace with actual data in a real app
    months = ["January", "February", "March"]
    selected_month = st.selectbox("Select Production Month", months)
    
    # Simulated cost data
    costs = {
        "Feed1": random.randint(1000, 5000),
        "Feed2": random.randint(1000, 5000),
        "Feed3": random.randint(1000, 5000),
        "Brine Shrimp": random.randint(500, 2000),
        "Probiotics": random.randint(200, 1000),
        "Vitamin C": random.randint(100, 500)
    }
    
    # Display costs
    st.subheader(f"Costs for {selected_month}")
    for product, cost in costs.items():
        st.write(f"{product}: ${cost}")
    
    # Create a bar chart of costs
    fig = px.bar(x=list(costs.keys()), y=list(costs.values()), title=f"Product Costs for {selected_month}")
    st.plotly_chart(fig)

# Events Timeline page
elif page == "Events Timeline":
    st.title("Events Timeline")
    
    # Event input form
    st.subheader("Log New Event")
    event_date = st.date_input("Event Date")
    event_time = st.time_input("Event Time")
    event_description = st.text_area("Event Description")
    event_image = st.file_uploader("Upload Image (optional)", type=["png", "jpg", "jpeg"])
    
    if st.button("Log Event"):
        # Here you would typically save this to a database
        st.success("Event logged successfully!")
    
    # Display events (this is a placeholder, you'd typically load this from a database)
    st.subheader("Recent Events")
    events = [
        {"date": "2024-05-01", "time": "10:00", "description": "Power outage affected tanks 1-5"},
        {"date": "2024-04-15", "time": "14:30", "description": "New feed supplier onboarded"},
        {"date": "2024-03-22", "time": "09:15", "description": "Maintenance performed on filtration system"}
    ]
    
    for event in events:
        st.write(f"{event['date']} {event['time']}: {event['description']}")
