import streamlit as st
from streamlit_carousel import carousel

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "landing"

# Function to navigate between pages
def navigate_to(page):
    st.session_state.page = page

# Function to render navbar with proper navigation
def navbar():
    st.markdown("""
        <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            background-color: #333;
            padding: 10px;
        }
        .navbar button {
            color: white;
            background: none;
            border: none;
            font-size: 16px;
            padding: 10px 15px;
            cursor: pointer;
        }
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🏠 Home"):
            navigate_to("landing")
    with col2:
        if st.button("📊 Dashboard"):
            navigate_to("dashboard")

# Landing Page
def landing_page():
    navbar()
    st.image("images/team-logo.png", width=150)  
    st.title("Team Name")
    st.subheader("Welcome to Our Project!")
    st.write("Discover our journey through captivating visuals and insights.")

    if st.button("Start"):
        navigate_to("dashboard")

    if st.button("Collect Data"):
        navigate_to("dashboard")

# Dashboard Page
def dashboard_page():
    navbar()
    st.title("Dashboard")

    test_items = [
        {"title": "Slide 1", "text": "A tree in the savannah", 
         "img": "https://img.freepik.com/free-photo/wide-angle-shot-single-tree-growing-clouded-sky-during-sunset-surrounded-by-grass_181624-22807.jpg?w=1380",
         "status": "Active"},
        {"title": "Slide 2", "text": "A wooden bridge in a forest in Autumn", 
         "img": "https://img.freepik.com/free-photo/beautiful-wooden-pathway-going-breathtaking-colorful-trees-forest_181624-5840.jpg?w=1380",
         "status": "Pending"},
        {"title": "Slide 3", "text": "A distant mountain chain preceded by a sea", 
         "img": "https://img.freepik.com/free-photo/aerial-beautiful-shot-seashore-with-hills-background-sunset_181624-24143.jpg?w=1380",
         "status": "Completed"}
    ]

    selected_title = st.selectbox("Select an item:", [item["title"] for item in test_items])
    selected_item = next(item for item in test_items if item["title"] == selected_title)

    col1, col2 = st.columns([2, 3])
    with col1:
        carousel(items=test_items)

    with col2:
        st.image(selected_item["img"], caption=selected_item["title"], use_container_width=True)
        st.subheader(selected_item["title"])
        st.write(f"**Description:** {selected_item['text']}")
        st.write(f"**Status:** {selected_item['status']}")

# Page Navigation Logic
if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
