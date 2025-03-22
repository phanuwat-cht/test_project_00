import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import base64
from io import BytesIO
import pandas as pd
from streamlit_option_menu import option_menu
import streamlit_nested_layout
import streamlit_javascript as st_js
import random

# Set page config
st.set_page_config(
    page_title="Roomlab - Interior Design Solutions",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define color palette
colors = {
    "primary": "#2D3142",    # Dark blue-gray
    "secondary": "#4F5D75",  # Medium blue-gray
    "accent": "#F46036",     # Orange
    "light": "#EEF2F5",      # Light gray
    "white": "#FFFFFF",      # White
    "success": "#4CAF50",    # Green
    "warning": "#FFC107",    # Yellow
    "danger": "#F44336"      # Red
}

# Custom CSS
def local_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700&display=swap');
        
        * {{
            font-family: 'Nunito', sans-serif;
        }}
        
        .main {{
            background-color: {colors["light"]};
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: {colors["primary"]};
            font-weight: 600;
        }}
        
        .stButton > button {{
            background-color: {colors["accent"]};
            color: {colors["white"]};
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
            font-weight: 600;
        }}
        
        .stButton > button:hover {{
            background-color: {colors["secondary"]};
        }}
        
        .card {{
            background-color: {colors["white"]};
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }}
        
        .nav-link {{
            color: {colors["primary"]};
            font-weight: 600;
        }}
        
        .nav-link:hover {{
            color: {colors["accent"]};
        }}
        
        .footer {{
            background-color: {colors["primary"]};
            color: {colors["white"]};
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            margin-top: 30px;
        }}
        
        .form-container {{
            background-color: {colors["white"]};
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .portfolio-item {{
            background-color: {colors["white"]};
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
        }}
        
        .portfolio-item:hover {{
            transform: translateY(-5px);
        }}
        
        .btn-primary {{
            background-color: {colors["accent"]};
            color: {colors["white"]};
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
            font-weight: 600;
            cursor: pointer;
        }}
        
        .btn-secondary {{
            background-color: {colors["secondary"]};
            color: {colors["white"]};
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
            font-weight: 600;
            cursor: pointer;
        }}
        
        .btn-outline {{
            background-color: transparent;
            color: {colors["accent"]};
            border-radius: 5px;
            border: 1px solid {colors["accent"]};
            padding: 10px 20px;
            font-weight: 600;
            cursor: pointer;
        }}
        
        .btn-outline:hover {{
            background-color: {colors["accent"]};
            color: {colors["white"]};
        }}
        
        @media (max-width: 768px) {{
            .card {{
                padding: 15px;
            }}
            
            .stButton > button {{
                padding: 8px 15px;
                font-size: 14px;
            }}
        }}
        
        /* Custom Dashboard styling */
        .dashboard-card {{
            background-color: {colors["white"]};
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            height: 100%;
        }}
        
        .dashboard-stat {{
            text-align: center;
            padding: 15px;
        }}
        
        .dashboard-stat h3 {{
            margin-bottom: 5px;
            font-size: 24px;
        }}
        
        .dashboard-stat p {{
            color: {colors["secondary"]};
            margin-top: 0;
        }}
        
        /* Design Token Card */
        .token-card {{
            background-color: {colors["light"]};
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin: 10px;
        }}
        
        .token-card h3 {{
            color: {colors["primary"]};
        }}
        
        .token-card h2 {{
            color: {colors["accent"]};
            font-size: 28px;
            margin: 15px 0;
        }}
        
        .token-card ul {{
            list-style-type: none;
            padding: 0;
            text-align: left;
        }}
        
        .token-card ul li {{
            padding: 5px 0;
        }}
        
        .token-card ul li:before {{
            content: "✓";
            color: {colors["accent"]};
            margin-right: 8px;
        }}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for page navigation and user data
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'name': '',
        'email': '',
        'property_type': '',
        'floor_count': 0,
        'room_types': [],
        'space_size': '',
        'style': '',
        'family_requirements': '',
        'budget': '',
        'designs': [],
        'tokens': 0,
        'projects': []
    }

# Helper function to detect device type
def get_device_type():
    try:
        width = st_js.st_javascript("window.innerWidth")
        if width < 768:
            return "mobile"
        return "desktop"
    except:
        return "desktop"  # Default to desktop if detection fails

# Navigation function
def navigate_to(page):
    st.session_state.page = page
    st.experimental_rerun()

# Mock function for social login
def social_login(platform):
    st.session_state.logged_in = True
    st.session_state.user_data['name'] = f'Test User ({platform})'
    st.session_state.user_data['email'] = f'testuser_{random.randint(1000, 9999)}@example.com'
    navigate_to('dashboard')

# Function to display the navbar
def display_navbar():
    device = get_device_type()
    
    if device == "desktop":
        cols = st.columns([1, 2, 1])
        with cols[0]:
            st.markdown(f'<h2 style="color:{colors["accent"]}; font-weight:700;">ROOMLAB</h2>', unsafe_allow_html=True)
        with cols[1]:
            selected = option_menu(
                menu_title=None,
                options=["Home", "Portfolio", "Services", "Pricing", "Contact"],
                icons=["house", "images", "tools", "calculator", "envelope"],
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": colors["accent"], "font-size": "14px"},
                    "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "--hover-color": colors["light"]},
                    "nav-link-selected": {"background-color": colors["accent"], "color": colors["white"]},
                }
            )
            
            if selected and selected.lower() != st.session_state.page:
                navigate_to(selected.lower())
        
        with cols[2]:
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.logged_in:
                    if st.button("Dashboard"):
                        navigate_to('dashboard')
                else:
                    if st.button("Login"):
                        navigate_to('login')
            with col2:
                if not st.session_state.logged_in:
                    if st.button("Register"):
                        navigate_to('register')
                else:
                    if st.button("Logout"):
                        st.session_state.logged_in = False
                        navigate_to('home')
    else:
        # Mobile navbar
        st.markdown(f'<h2 style="color:{colors["accent"]}; font-weight:700; text-align:center;">ROOMLAB</h2>', unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Home", "Portfolio", "Services", "Pricing", "Contact", "Account"],
            icons=["house", "images", "tools", "calculator", "envelope", "person"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": colors["accent"], "font-size": "14px"},
                "nav-link": {"font-size": "12px", "text-align": "center", "margin":"0px", "--hover-color": colors["light"], "padding": "5px"},
                "nav-link-selected": {"background-color": colors["accent"], "color": colors["white"]},
            }
        )
        
        if selected == "Account":
            if st.session_state.logged_in:
                navigate_to('dashboard')
            else:
                navigate_to('login')
        elif selected and selected.lower() != st.session_state.page:
            navigate_to(selected.lower())

# Function to display the footer
def display_footer():
    st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
            <div style="min-width: 200px;">
                <h3>ROOMLAB</h3>
                <p>Your one-stop solution for interior design</p>
            </div>
            <div style="min-width: 200px;">
                <h4>Quick Links</h4>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li><a href="#" style="color: white;">Home</a></li>
                    <li><a href="#" style="color: white;">Portfolio</a></li>
                    <li><a href="#" style="color: white;">Services</a></li>
                    <li><a href="#" style="color: white;">Pricing</a></li>
                </ul>
            </div>
            <div style="min-width: 200px;">
                <h4>Contact Us</h4>
                <p>Email: info@roomlab.com</p>
                <p>Phone: +66 2 123 4567</p>
                <p>Address: Bangkok, Thailand</p>
            </div>
        </div>
        <hr style="border-color: rgba(255,255,255,0.2);">
        <p style="text-align: center;">© 2025 Roomlab. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

# Pages
def home_page():
    device = get_device_type()
    
    # Hero section
    st.markdown(f"""
    <div style="background-color: {colors['primary']}; padding: 40px; border-radius: 10px; color: white; text-align: center; margin-bottom: 30px;">
        <h1>Transform Your Space with Roomlab</h1>
        <p style="font-size: 1.2rem; margin: 20px 0;">Professional interior design and furniture arrangement for your dream home</p>
        <button class="btn-primary" onclick="Streamlit.setComponentValue('get_started')">Get Started</button>
    </div>
    """, unsafe_allow_html=True)
    
    # How it works section
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>How It Works</h2>", unsafe_allow_html=True)
    
    if device == "desktop":
        cols = st.columns(3)
        
        with cols[0]:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <h3 style="color: #4F5D75;">1. Share Your Vision</h3>
                <p>Tell us about your space, preferences, and requirements</p>
                <p>🏠</p>
            </div>
            """, unsafe_allow_html=True)
            
        with cols[1]:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <h3 style="color: #4F5D75;">2. Get 3D Designs</h3>
                <p>Our AI creates detailed 3D renders of your space</p>
                <p>🎨</p>
            </div>
            """, unsafe_allow_html=True)
            
        with cols[2]:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <h3 style="color: #4F5D75;">3. Bring It To Life</h3>
                <p>Shop furniture from our recommendations and transform your space</p>
                <p>✨</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="text-align: center; margin-bottom: 15px;">
            <h3 style="color: #4F5D75;">1. Share Your Vision</h3>
            <p>Tell us about your space, preferences, and requirements</p>
            <p>🏠</p>
        </div>
        
        <div class="card" style="text-align: center; margin-bottom: 15px;">
            <h3 style="color: #4F5D75;">2. Get 3D Designs</h3>
            <p>Our AI creates detailed 3D renders of your space</p>
            <p>🎨</p>
        </div>
        
        <div class="card" style="text-align: center; margin-bottom: 15px;">
            <h3 style="color: #4F5D75;">3. Bring It To Life</h3>
            <p>Shop furniture from our recommendations and transform your space</p>
            <p>✨</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Featured designs
    st.markdown("<h2 style='text-align: center; margin: 40px 0 30px 0;'>Featured Designs</h2>", unsafe_allow_html=True)
    
    if device == "desktop":
        cols = st.columns(3)
        rooms = ["Living Room", "Kitchen", "Bathroom"]
        
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"""
                <div class="portfolio-item">
                    <div style="height: 200px; background-color: #ddd; display: flex; align-items: center; justify-content: center;">
                        <span style="color: #777;">Image Placeholder</span>
                    </div>
                    <div style="padding: 15px;">
                        <h4>{rooms[i]} Design</h4>
                        <p>Modern {rooms[i].lower()} design with optimal space utilization</p>
                        <button class="btn-outline">View Details</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        rooms = ["Living Room", "Kitchen", "Bathroom"]
        
        for room in rooms:
            st.markdown(f"""
            <div class="portfolio-item" style="margin-bottom: 20px;">
                <div style="height: 200px; background-color: #ddd; display: flex; align-items: center; justify-content: center;">
                    <span style="color: #777;">Image Placeholder</span>
                </div>
                <div style="padding: 15px;">
                    <h4>{room} Design</h4>
                    <p>Modern {room.lower()} design with optimal space utilization</p>
                    <button class="btn-outline">View Details</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Testimonials
    st.markdown("<h2 style='text-align: center; margin: 40px 0 30px 0;'>What Our Clients Say</h2>", unsafe_allow_html=True)
    
    if device == "desktop":
        cols = st.columns(2)
        
        with cols[0]:
            st.markdown("""
            <div class="card">
                <p style="font-style: italic;">"Roomlab transformed my apartment completely. The 3D designs were so realistic, and the furniture recommendations fit perfectly with my style and budget."</p>
                <p><strong>- Somchai P., Bangkok</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
        with cols[1]:
            st.markdown("""
            <div class="card">
                <p style="font-style: italic;">"I was skeptical about online interior design services, but Roomlab exceeded my expectations. The process was smooth, and the results were amazing!"</p>
                <p><strong>- Pranee S., Chiang Mai</strong></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="margin-bottom: 15px;">
            <p style="font-style: italic;">"Roomlab transformed my apartment completely. The 3D designs were so realistic, and the furniture recommendations fit perfectly with my style and budget."</p>
            <p><strong>- Somchai P., Bangkok</strong></p>
        </div>
        
        <div class="card" style="margin-bottom: 15px;">
            <p style="font-style: italic;">"I was skeptical about online interior design services, but Roomlab exceeded my expectations. The process was smooth, and the results were amazing!"</p>
            <p><strong>- Pranee S., Chiang Mai</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown(f"""
    <div style="background-color: {colors['accent']}; padding: 30px; border-radius: 10px; color: white; text-align: center; margin: 40px 0;">
        <h2>Ready to Transform Your Space?</h2>
        <p style="margin: 15px 0;">Get started with Roomlab today and see your dream interior come to life!</p>
        <button class="btn-secondary" onclick="Streamlit.setComponentValue('start_project')">Start Your Project</button>
    </div>
    """, unsafe_allow_html=True)

def portfolio_page():
    st.markdown("<h1 style='text-align: center;'>Our Portfolio</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Explore our collection of stunning interior designs for various spaces</p>", unsafe_allow_html=True)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        room_type = st.selectbox("Room Type", ["All", "Living Room", "Kitchen", "Bathroom", "Bedroom", "Office"])
    with col2:
        style = st.selectbox("Style", ["All", "Modern", "Minimalist", "Scandinavian", "Industrial", "Classic", "Thai Contemporary"])
    with col3:
        sort_by = st.selectbox("Sort By", ["Newest", "Most Popular", "Budget: Low to High", "Budget: High to Low"])
    
    # Portfolio grid
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    device = get_device_type()
    
    if device == "desktop":
        # Desktop: 3 columns
        for row in range(3):
            cols = st.columns(3)
            for col in cols:
                with col:
                    st.markdown(f"""
                    <div class="portfolio-item">
                        <div style="height: 200px; background-color: #ddd; display: flex; align-items: center; justify-content: center;">
                            <span style="color: #777;">Design Image</span>
                        </div>
                        <div style="padding: 15px;">
                            <h4>{"Modern Living Room" if row % 2 == 0 else "Minimalist Kitchen"}</h4>
                            <p>{"Spacious design with optimal lighting" if row % 2 == 0 else "Clean lines with functional storage"}</p>
                            <button class="btn-outline">View Details</button>
                        </div>
                    </div>
                    <div style="height: 20px;"></div>
                    """, unsafe_allow_html=True)
    else:
        # Mobile: 1 column
        for i in range(6):
            st.markdown(f"""
            <div class="portfolio-item" style="margin-bottom: 20px;">
                <div style="height: 180px; background-color: #ddd; display: flex; align-items: center; justify-content: center;">
                    <span style="color: #777;">Design Image</span>
                </div>
                <div style="padding: 15px;">
                    <h4>{"Modern Living Room" if i % 2 == 0 else "Minimalist Kitchen"}</h4>
                    <p>{"Spacious design with optimal lighting" if i % 2 == 0 else "Clean lines with functional storage"}</p>
                    <button class="btn-outline">View Details</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Pagination
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-top: 30px;">
        <button class="btn-outline" style="margin: 0 5px;">Previous</button>
        <button class="btn-primary" style="margin: 0 5px;">1</button>
        <button class="btn-outline" style="margin: 0 5px;">2</button>
        <button class="btn-outline" style="margin: 0 5px;">3</button>
        <button class="btn-outline" style="margin: 0 5px;">Next</button>
    </div>
    """, unsafe_allow_html=True)

def services_page():
    st.markdown("<h1 style='text-align: center;'>Our Services</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Comprehensive interior design solutions for your home or office</p>", unsafe_allow_html=True)
    
    device = get_device_type()
    
    # Service offerings
    if device == "desktop":
        for i in range(3):
            cols = st.columns([1, 3])
            with cols[0]:
                st.markdown(f"""
                <div style="height: 200px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                    <span style="color: #777;">Image {i+1}</span>
                </div>
                """, unsafe_allow_html=True)
            with cols[1]:
                services = [
                    {
                        "title": "3D Interior Design Visualization",
                        "desc": "Get photorealistic 3D renderings of your space with our AI-powered design tool. Visualize different styles, layouts, and furniture arrangements before making any purchasing decisions."
                    },
                    {
                        "title": "Furniture Selection & Arrangement",
                        "desc": "Our expert system will recommend the perfect furniture pieces that match your style, space dimensions, and budget. We help you optimize your space for both functionality and aesthetics."
                    },
                    {
                        "title": "Complete Room Transformation",
                        "desc": "From concept to completion, we handle everything. Get a comprehensive design package including 3D visualizations, furniture recommendations, color schemes, and a detailed bill of quantities."
                    }
                ]
                
                st.markdown(f"""
                <div class="card">
                    <h2>{services[i]["title"]}</h2>
                    <p>{services[i]["desc"]}</p>
                    <button class="btn-primary">Learn More</button>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    else:
        services = [
            {
                "title": "3D Interior Design Visualization",
                "desc": "Get photorealistic 3D renderings of your space with our AI-powered design tool."
            },
            {
                "title": "Furniture Selection & Arrangement",
                "desc": "Our expert system will recommend the perfect furniture pieces that match your style and budget."
            },
            {
                "title": "Complete Room Transformation",
                "desc": "From concept to completion, we handle everything with a comprehensive design package."
            }
        ]
        
        for service in services:
            st.markdown(f"""
            <div class="card" style="margin-bottom: 20px;">
                <div style="height: 150px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px; margin-bottom: 15px;">
                    <span style="color: #777;">Service Image</span>
                </div>
                <h3>{service["title"]}</h3>
                <p>{service["desc"]}</p>
                <button class="btn-primary">Learn More</button>
            </div>
            """, unsafe_allow_html=True)
    
    # How our service works
    st.markdown("<h2 style='text-align: center; margin: 40px 0 30px 0;'>Our Process</h2>", unsafe_allow_html=True)
    
    if device == "desktop":
        cols = st.columns(4)
        steps = [
            {"title": "Share Your Requirements", "icon": "📋"},
            {"title": "AI Generates Designs", "icon": "🎨"},
            {"title": "Review & Refine", "icon": "👁️"},
            {"title": "Implementation", "icon": "🏠"}
        ]
        
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"""
                <div class="card" style="text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 15px;">{steps[i]["icon"]}</div>
                    <h4 style="margin-bottom: 10px;">Step {i+1}</h4>
                    <h3 style="margin-top: 0;">{steps[i]["title"]}</h3>
                </div>
                """, unsafe_allow_html=True)
    else:
        steps = [
            {"title": "Share Your Requirements", "icon": "📋"},
            {"title": "AI Generates Designs", "icon": "🎨"},
            {"title": "Review & Refine", "icon": "👁️"},
            {"title": "Implementation", "icon": "🏠"}
        ]
        
        for i, step in enumerate(steps):
            st.markdown(f"""
            <div class="card" style="text-align: center; margin-bottom: 15px;">
                <div style="font-size: 2.5rem; margin-bottom: 15px;">{step["icon"]}</div>
                <h4 style="margin-bottom: 10px;">Step {i+1}</h4>
                <h3 style="margin-top: 0;">{step["title"]}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    # Design tokens
    st.markdown("<h2 style='text-align: center; margin: 40px 0 30px 0;'>Design Tokens</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Purchase tokens to generate multiple design variations for your space</p>", unsafe_allow_html=True)
    
    if device == "desktop":
        cols = st.columns(3)
        packages = [
            {"title": "Starter", "price": "1,500฿", "tokens": "3 tokens", "features": ["3 design variations", "1 room type", "Basic furniture recommendations", "Valid for 30 days"]},
            {"title": "Pro", "price": "3,500฿", "tokens": "8 tokens", "features": ["8 design variations", "Up to 3 room types", "Detailed furniture recommendations", "Shopping list with budget options", "Valid for 60 days"]},
            {"title": "Premium", "price": "6,000฿", "tokens": "15 tokens", "features": ["15 design variations", "Unlimited room types", "Premium furniture selections", "Personalized shopping list", "Priority support", "Valid for 90 days"]}
        ]
        
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"""
                <div class="token-card" style="{'transform: scale(1.05); border: 2px solid ' + colors['accent'] if i == 1 else ''}">
                    <h3>{packages[i]["title"]} Package</h3>
                    <h2>{packages[i]["price"]}</h2>
                    <p>{packages[i]["tokens"]}</p>
                    <ul>
                        {"".join(f"<li>{feature}</li>" for feature in packages[i]["features"])}
                    </ul>
                    <button class="{'btn-primary' if i == 1 else 'btn-outline'}" style="width: 100%; margin-top: 15px;">Purchase</button>
                </div>
                """, unsafe_allow_html=True)
    else:
        packages = [
            {"title": "Starter", "price": "1,500฿", "tokens": "3 tokens", "features": ["3 design variations", "1 room type", "Basic furniture recommendations", "Valid for 30 days"]},
            {"title": "Pro", "price": "3,500฿", "tokens": "8 tokens", "features": ["8 design variations", "Up to 3 room types", "Detailed furniture recommendations", "Shopping list with budget options", "Valid for 60 days"]},
            {"title": "Premium", "price": "6,000฿", "tokens": "15 tokens", "features": ["15 design variations", "Unlimited room types", "Premium furniture selections", "Personalized shopping list", "Priority support", "Valid for 90 days"]}
        ]
        
        for i, package in enumerate(packages):
            st.markdown(f"""
            <div class="token-card" style="margin-bottom: 20px; {'border: 2px solid ' + colors['accent'] if i == 1 else ''}">
                <h3>{package["title"]} Package</h3>
                <h2>{package["price"]}</h2>
                <p>{package["tokens"]}</p>
                <ul>
                    {"".join(f"<li>{feature}</li>" for feature in package["features"])}
                </ul>
                <button class="{'btn-primary' if i == 1 else 'btn-outline'}" style="width: 100%; margin-top: 15px;">Purchase</button>
            </div>
            """, unsafe_allow_html=True)

def pricing_page():
    st.markdown("<h1 style='text-align: center;'>Pricing Estimation</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Get an estimate for your interior design project</p>", unsafe_allow_html=True)
    
    device = get_device_type()
    
    # Estimation form
    st.markdown("""
    <div class="form-container">
        <h3>Project Details</h3>
        <p>Fill in the information below to get an estimate for your project</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        property_type = st.selectbox("Property Type", ["Condominium", "House", "Townhouse", "Commercial Space"])
        room_type = st.multiselect("Room Types", ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Dining Room", "Office"])
        style_preference = st.selectbox("Design Style", ["Modern", "Minimalist", "Scandinavian", "Industrial", "Classic", "Thai Contemporary"])
    
    with col2:
        floor_count = st.number_input("Number of Floors", min_value=1, max_value=10, value=1)
        space_size = st.selectbox("Space Size (sqm)", ["Less than 30", "30-50", "50-80", "80-120", "120-200", "More than 200"])
        budget_range = st.select_slider("Budget Range (฿)", options=["50,000-100,000", "100,000-300,000", "300,000-500,000", "500,000-1,000,000", "More than 1,000,000"])
    
    additional_requirements = st.text_area("Additional Requirements or Specific Needs")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("Calculate Estimate", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Sample estimation result (hidden by default, would be shown after calculation)
    with st.expander("View Estimation Result", expanded=False):
        if device == "desktop":
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="card">
                    <h3>Project Summary</h3>
                    <p><strong>Property Type:</strong> Condominium</p>
                    <p><strong>Room Types:</strong> Living Room, Bedroom, Kitchen</p>
                    <p><strong>Number of Floors:</strong> 1</p>
                    <p><strong>Space Size:</strong> 50-80 sqm</p>
                    <p><strong>Design Style:</strong> Modern</p>
                    <p><strong>Budget Range:</strong> 300,000-500,000฿</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="card">
                    <h3>Estimated Costs</h3>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>Design Fee:</span>
                        <span style="font-weight: bold;">15,000฿</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>Construction/Renovation:</span>
                        <span style="font-weight: bold;">180,000฿</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>Furniture & Fixtures:</span>
                        <span style="font-weight: bold;">120,000฿</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>Accessories & Decor:</span>
                        <span style="font-weight: bold;">35,000฿</span>
                    </div>
                    <hr>
                    <div style="display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: bold; color: {colors['accent']};">
                        <span>Total Estimate:</span>
                        <span>350,000฿</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card" style="margin-bottom: 20px;">
                <h3>Project Summary</h3>
                <p><strong>Property Type:</strong> Condominium</p>
                <p><strong>Room Types:</strong> Living Room, Bedroom, Kitchen</p>
                <p><strong>Number of Floors:</strong> 1</p>
                <p><strong>Space Size:</strong> 50-80 sqm</p>
                <p><strong>Design Style:</strong> Modern</p>
                <p><strong>Budget Range:</strong> 300,000-500,000฿</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="card">
                <h3>Estimated Costs</h3>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span>Design Fee:</span>
                    <span style="font-weight: bold;">15,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span>Construction/Renovation:</span>
                    <span style="font-weight: bold;">180,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span>Furniture & Fixtures:</span>
                    <span style="font-weight: bold;">120,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span>Accessories & Decor:</span>
                    <span style="font-weight: bold;">35,000฿</span>
                </div>
                <hr>
                <div style="display: flex; justify-content: space-between; font-size: 1.2rem; font-weight: bold; color: {colors['accent']};">
                    <span>Total Estimate:</span>
                    <span>350,000฿</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Purchase Design Tokens", use_container_width=True)
        with col2:
            st.button("Request Detailed Quote", use_container_width=True)
    
    # FAQ section
    st.markdown("<h2 style='text-align: center; margin: 40px 0 30px 0;'>Frequently Asked Questions</h2>", unsafe_allow_html=True)
    
    faq_items = [
        {
            "question": "How accurate is the pricing estimation?",
            "answer": "Our pricing estimation tool provides a rough approximation based on typical costs in Thailand. The actual costs may vary depending on specific requirements, materials chosen, and current market prices."
        },
        {
            "question": "Do I need to pay for the estimation?",
            "answer": "No, the pricing estimation tool is completely free to use. You only pay when you decide to proceed with your project or purchase design tokens."
        },
        {
            "question": "What's included in the design fee?",
            "answer": "The design fee covers 3D visualizations, furniture layout plans, color schemes, and material recommendations. It also includes up to two rounds of revisions based on your feedback."
        },
        {
            "question": "Can I get a more detailed breakdown of costs?",
            "answer": "Yes, you can request a detailed quote after receiving the initial estimation. Our team will analyze your requirements in more depth and provide a comprehensive breakdown of all costs involved."
        }
    ]
    
    for item in faq_items:
        with st.expander(item["question"]):
            st.write(item["answer"])

def contact_page():
    st.markdown("<h1 style='text-align: center;'>Contact Us</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Get in touch with our team for inquiries or support</p>", unsafe_allow_html=True)
    
    device = get_device_type()
    
    if device == "desktop":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="form-container">
                <h3>Send Us a Message</h3>
                <p>Fill out the form below and we'll get back to you as soon as possible</p>
            """, unsafe_allow_html=True)
            
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            subject = st.selectbox("Subject", ["General Inquiry", "Project Consultation", "Support", "Partnership", "Other"])
            message = st.text_area("Message")
            
            st.button("Send Message", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="card">
                <h3>Contact Information</h3>
                <p><strong>Email:</strong> info@roomlab.com</p>
                <p><strong>Phone:</strong> +66 2 123 4567</p>
                <p><strong>Office Hours:</strong> Monday to Friday, 9:00 AM - 6:00 PM</p>
                <p><strong>Address:</strong> 123 Sukhumvit Road, Bangkok 10110, Thailand</p>
                
                <h4 style="margin-top: 30px;">Connect With Us</h4>
                <div style="display: flex; gap: 10px;">
                    <button class="btn-outline" style="padding: 5px 10px;">Facebook</button>
                    <button class="btn-outline" style="padding: 5px 10px;">Instagram</button>
                    <button class="btn-outline" style="padding: 5px 10px;">Line</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="form-container" style="margin-bottom: 20px;">
            <h3>Send Us a Message</h3>
            <p>Fill out the form below and we'll get back to you as soon as possible</p>
        """, unsafe_allow_html=True)
        
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        subject = st.selectbox("Subject", ["General Inquiry", "Project Consultation", "Support", "Partnership", "Other"])
        message = st.text_area("Message")
        
        st.button("Send Message", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>Contact Information</h3>
            <p><strong>Email:</strong> info@roomlab.com</p>
            <p><strong>Phone:</strong> +66 2 123 4567</p>
            <p><strong>Office Hours:</strong> Monday to Friday, 9:00 AM - 6:00 PM</p>
            <p><strong>Address:</strong> 123 Sukhumvit Road, Bangkok 10110, Thailand</p>
            
            <h4 style="margin-top: 20px;">Connect With Us</h4>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <button class="btn-outline" style="padding: 5px 10px; margin-bottom: 10px;">Facebook</button>
                <button class="btn-outline" style="padding: 5px 10px; margin-bottom: 10px;">Instagram</button>
                <button class="btn-outline" style="padding: 5px 10px; margin-bottom: 10px;">Line</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # FAQ
    st.markdown("<h3 style='margin-top: 40px;'>Frequently Asked Questions</h3>", unsafe_allow_html=True)
    
    with st.expander("How long does it take to respond to inquiries?"):
        st.write("We typically respond to all inquiries within 24 hours during business days.")
    
    with st.expander("Do you offer on-site consultations?"):
        st.write("Yes, we do offer on-site consultations for projects in Bangkok and surrounding areas. Additional fees may apply for locations outside our service area.")
    
    with st.expander("Can I schedule a video call consultation?"):
        st.write("Absolutely! We offer video consultations via Line, Zoom, or Google Meet. You can select this option when filling out the contact form.")

def login_page():
    st.markdown("<h1 style='text-align: center;'>Login to Your Account</h1>", unsafe_allow_html=True)
    
    device = get_device_type()
    
    if device == "desktop":
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="form-container">
                <h3>Login with Email</h3>
            """, unsafe_allow_html=True)
            
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            st.checkbox("Remember me")
            st.button("Login", use_container_width=True)
            
            st.markdown("<p style='text-align: center; margin-top: 10px;'><a href='#'>Forgot password?</a></p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="form-container">
                <h3>Social Login</h3>
                <p>Login quickly with your social account</p>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Line", use_container_width=True):
                    social_login("Line")
            with col2:
                if st.button("Google", use_container_width=True):
                    social_login("Google")
            with col3:
                if st.button("Facebook", use_container_width=True):
                    social_login("Facebook")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; margin-top: 20px;'>Don't have an account? <a href='#' onclick='Streamlit.setComponentValue(\"navigate_register\")'>Register now</a></p>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="form-container" style="margin-bottom: 20px;">
            <h3>Login with Email</h3>
        """, unsafe_allow_html=True)
        
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        st.checkbox("Remember me")
        st.button("Login", use_container_width=True)
        
        st.markdown("<p style='text-align: center; margin-top: 10px;'><a href='#'>Forgot password?</a></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="form-container">
            <h3>Social Login</h3>
            <p>Login quickly with your social account</p>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Line", use_container_width=True):
                social_login("Line")
        with col2:
            if st.button("Google", use_container_width=True):
                social_login("Google")
        with col3:
            if st.button("Facebook", use_container_width=True):
                social_login("Facebook")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; margin-top: 20px;'>Don't have an account? <a href='#' onclick='Streamlit.setComponentValue(\"navigate_register\")'>Register now</a></p>", unsafe_allow_html=True)

def register_page():
    st.markdown("<h1 style='text-align: center;'>Create Your Account</h1>", unsafe_allow_html=True)
    
    device = get_device_type()
    
    if device == "desktop":
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="form-container">
                <h3>Register with Email</h3>
            """, unsafe_allow_html=True)
            
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            st.checkbox("I agree to the Terms of Service and Privacy Policy")
            st.button("Register", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="form-container">
                <h3>Social Registration</h3>
                <p>Register quickly with your social account</p>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Line", use_container_width=True):
                    social_login("Line")
            with col2:
                if st.button("Google", use_container_width=True):
                    social_login("Google")
            with col3:
                if st.button("Facebook", use_container_width=True):
                    social_login("Facebook")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; margin-top: 20px;'>Already have an account? <a href='#' onclick='Streamlit.setComponentValue(\"navigate_login\")'>Login now</a></p>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="form-container" style="margin-bottom: 20px;">
            <h3>Register with Email</h3>
        """, unsafe_allow_html=True)
        
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        st.checkbox("I agree to the Terms of Service and Privacy Policy")
        st.button("Register", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="form-container">
            <h3>Social Registration</h3>
            <p>Register quickly with your social account</p>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Line", use_container_width=True):
                social_login("Line")
        with col2:
            if st.button("Google", use_container_width=True):
                social_login("Google")
        with col3:
            if st.button("Facebook", use_container_width=True):
                social_login("Facebook")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; margin-top: 20px;'>Already have an account? <a href='#' onclick='Streamlit.setComponentValue(\"navigate_login\")'>Login now</a></p>", unsafe_allow_html=True)

def dashboard_page():
    st.markdown("<h1 style='text-align: center;'>Your Dashboard</h1>", unsafe_allow_html=True)
    
    device = get_device_type()
    
    # User info and stats
    if device == "desktop":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="dashboard-card dashboard-stat">
                <h3>3</h3>
                <p>Active Projects</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="dashboard-card dashboard-stat">
                <h3>5</h3>
                <p>Design Tokens</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="dashboard-card dashboard-stat">
                <h3>2</h3>
                <p>Completed Projects</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="dashboard-card dashboard-stat">
                <h3>3</h3>
                <p>Active Projects</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="dashboard-card dashboard-stat">
                <h3>5</h3>
                <p>Design Tokens</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="dashboard-card dashboard-stat">
            <h3>2</h3>
            <p>Completed Projects</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Dashboard tabs
    tab1, tab2, tab3 = st.tabs(["My Projects", "Design Tokens", "Account Settings"])
    
    with tab1:
        # My Projects
        st.markdown("<h3>Active Projects</h3>", unsafe_allow_html=True)
        
        for i in range(3):
            with st.expander(f"Project #{i+1} - {'Living Room Redesign' if i == 0 else 'Kitchen Renovation' if i == 1 else 'Bathroom Makeover'}", expanded=(i==0)):
                if device == "desktop":
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="height: 150px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                            <span style="color: #777;">Design Preview</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div style="padding: 0 15px;">
                            <h4 style="margin-top: 0;">{'Living Room Redesign' if i == 0 else 'Kitchen Renovation' if i == 1 else 'Bathroom Makeover'}</h4>
                            <p><strong>Status:</strong> {'Design Review' if i == 0 else 'In Progress' if i == 1 else 'Quote Generation'}</p>
                            <p><strong>Created:</strong> {'March 15, 2025' if i == 0 else 'March 10, 2025' if i == 1 else 'March 5, 2025'}</p>
                            <p><strong>Style:</strong> {'Modern' if i == 0 else 'Scandinavian' if i == 1 else 'Minimalist'}</p>
                            <div style="display: flex; gap: 10px; margin-top: 10px;">
                                <button class="btn-primary" style="padding: 5px 10px;">View Details</button>
                                <button class="btn-outline" style="padding: 5px 10px;">Modify Design</button>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="height: 120px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px; margin-bottom: 15px;">
                        <span style="color: #777;">Design Preview</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div>
                        <h4 style="margin-top: 0;">{'Living Room Redesign' if i == 0 else 'Kitchen Renovation' if i == 1 else 'Bathroom Makeover'}</h4>
                        <p><strong>Status:</strong> {'Design Review' if i == 0 else 'In Progress' if i == 1 else 'Quote Generation'}</p>
                        <p><strong>Created:</strong> {'March 15, 2025' if i == 0 else 'March 10, 2025' if i == 1 else 'March 5, 2025'}</p>
                        <p><strong>Style:</strong> {'Modern' if i == 0 else 'Scandinavian' if i == 1 else 'Minimalist'}</p>
                        <div style="display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap;">
                            <button class="btn-primary" style="padding: 5px 10px; margin-bottom: 10px;">View Details</button>
                            <button class="btn-outline" style="padding: 5px 10px; margin-bottom: 10px;">Modify Design</button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='margin-top: 30px;'>Completed Projects</h3>", unsafe_allow_html=True)
        
        for i in range(2):
            with st.expander(f"Project #{i+1} - {'Home Office Setup' if i == 0 else 'Dining Area Redesign'}", expanded=False):
                if device == "desktop":
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="height: 150px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                            <span style="color: #777;">Design Preview</span>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div style="padding: 0 15px;">
                            <h4 style="margin-top: 0;">{'Home Office Setup' if i == 0 else 'Dining Area Redesign'}</h4>
                            <p><strong>Status:</strong> Completed</p>
                            <p><strong>Completed On:</strong> {'February 20, 2025' if i == 0 else 'January 15, 2025'}</p>
                            <p><strong>Style:</strong> {'Industrial' if i == 0 else 'Thai Contemporary'}</p>
                            <div style="display: flex; gap: 10px; margin-top: 10px;">
                                <button class="btn-primary" style="padding: 5px 10px;">View Details</button>
                                <button class="btn-outline" style="padding: 5px 10px;">Order Similar</button>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="height: 120px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px; margin-bottom: 15px;">
                        <span style="color: #777;">Design Preview</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div>
                        <h4 style="margin-top: 0;">{'Home Office Setup' if i == 0 else 'Dining Area Redesign'}</h4>
                        <p><strong>Status:</strong> Completed</p>
                        <p><strong>Completed On:</strong> {'February 20, 2025' if i == 0 else 'January 15, 2025'}</p>
                        <p><strong>Style:</strong> {'Industrial' if i == 0 else 'Thai Contemporary'}</p>
                        <div style="display: flex; gap: 10px; margin-top: 10px; flex-wrap: wrap;">
                            <button class="btn-primary" style="padding: 5px 10px; margin-bottom: 10px;">View Details</button>
                            <button class="btn-outline" style="padding: 5px 10px; margin-bottom: 10px;">Order Similar</button>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            st.button("Start New Project", use_container_width=True)
    
    with tab2:
        # Design Tokens
        st.markdown("<h3>Current Token Balance: 5</h3>", unsafe_allow_html=True)
        
        # Token usage history
        st.markdown("<h4 style='margin-top: 20px;'>Token Usage History</h4>", unsafe_allow_html=True)
        
        token_data = [
            {"date": "March 15, 2025", "project": "Living Room Redesign", "tokens": "-1", "balance": "5"},
            {"date": "March 10, 2025", "project": "Kitchen Renovation", "tokens": "-2", "balance": "6"},
            {"date": "March 5, 2025", "project": "Bathroom Makeover", "tokens": "-1", "balance": "8"},
            {"date": "March 1, 2025", "project": "Token Purchase (Pro Package)", "tokens": "+8", "balance": "9"}
        ]
        
        st.markdown("""
        <div style="background-color: white; border-radius: 10px; overflow: hidden; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background-color: #f5f5f5;">
                        <th style="padding: 10px; text-align: left; border-bottom: 1px solid #ddd;">Date</th>
                        <th style="padding: 10px; text-align: left; border-bottom: 1px solid #ddd;">Project/Transaction</th>
                        <th style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">Tokens</th>
                        <th style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">Balance</th>
                    </tr>
                </thead>
                <tbody>
        """, unsafe_allow_html=True)
        
        for item in token_data:
            token_color = "green" if "+" in item["tokens"] else "red"
            st.markdown(f"""
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{item["date"]}</td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd;">{item["project"]}</td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: center; color: {token_color};">{item["tokens"]}</td>
                    <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: center;">{item["balance"]}</td>
                </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("""
                </tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        # Purchase more tokens
        st.markdown("<h4>Purchase More Tokens</h4>", unsafe_allow_html=True)
        
        if device == "desktop":
            cols = st.columns(3)
            packages = [
                {"title": "Starter", "price": "1,500฿", "tokens": "3 tokens"},
                {"title": "Pro", "price": "3,500฿", "tokens": "8 tokens"},
                {"title": "Premium", "price": "6,000฿", "tokens": "15 tokens"}
            ]
            
            for i, col in enumerate(cols):
                with col:
                    st.markdown(f"""
                    <div class="token-card">
                        <h3>{packages[i]["title"]} Package</h3>
                        <h2>{packages[i]["price"]}</h2>
                        <p>{packages[i]["tokens"]}</p>
                        <button class="btn-outline" style="width: 100%; margin-top: 15px;">Purchase</button>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            packages = [
                {"title": "Starter", "price": "1,500฿", "tokens": "3 tokens"},
                {"title": "Pro", "price": "3,500฿", "tokens": "8 tokens"},
                {"title": "Premium", "price": "6,000฿", "tokens": "15 tokens"}
            ]
            
            for package in packages:
                st.markdown(f"""
                <div class="token-card" style="margin-bottom: 15px;">
                    <h3>{package["title"]} Package</h3>
                    <h2>{package["price"]}</h2>
                    <p>{package["tokens"]}</p>
                    <button class="btn-outline" style="width: 100%; margin-top: 15px;">Purchase</button>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        # Bathroom section
        # Account Settings
        st.markdown("<h3>Profile Information</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Full Name", value="Test User")
        with col2:
            st.text_input("Email", value="testuser@example.com")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Phone Number", value="+66 123 456 789")
        with col2:
            st.selectbox("Language Preference", ["English", "Thai"])
        
        st.text_area("Address", value="123 Sukhumvit Rd, Bangkok 10110, Thailand")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Update Profile", use_container_width=True)
        
        st.markdown("<h3 style='margin-top: 30px;'>Change Password</h3>", unsafe_allow_html=True)
        
        st.text_input("Current Password", type="password")
        st.text_input("New Password", type="password")
        st.text_input("Confirm New Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Change Password", use_container_width=True)
        
        st.markdown("<h3 style='margin-top: 30px;'>Notification Preferences</h3>", unsafe_allow_html=True)
        
        st.checkbox("Email notifications for project updates", value=True)
        st.checkbox("SMS notifications for important updates", value=False)
        st.checkbox("Marketing communications and special offers", value=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("Save Preferences", use_container_width=True)

def property_setup_page():
    st.markdown("<h1 style='text-align: center;'>Property Setup</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Let's get to know your space better</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="form-container">
        <h3>Basic Property Information</h3>
    """, unsafe_allow_html=True)
    
    property_type = st.selectbox("Property Type", ["Condominium", "House", "Townhouse", "Commercial Space"])
    floor_count = st.number_input("Number of Floors", min_value=1, max_value=10, value=1)
    
    st.markdown("<h3 style='margin-top: 20px;'>Rooms to Design</h3>", unsafe_allow_html=True)
    
    room_types = st.multiselect(
        "Select Rooms to Include in Your Design",
        ["Living Room", "Dining Room", "Kitchen", "Master Bedroom", "Bedroom", "Bathroom", "Home Office", "Balcony"]
    )
    
    # Conditional room details based on selection
    if "Living Room" in room_types:
        st.markdown("<div style='margin-top: 15px;'><strong>Living Room Details</strong></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Living Room Size (sq.m)", min_value=10, max_value=100, value=25)
        with col2:
            st.selectbox("Living Room Shape", ["Rectangular", "Square", "L-Shaped", "Open Plan"])
    
    if "Kitchen" in room_types:
        st.markdown("<div style='margin-top: 15px;'><strong>Kitchen Details</strong></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Kitchen Size (sq.m)", min_value=5, max_value=50, value=15)
        with col2:
            st.selectbox("Kitchen Type", ["Open", "Closed", "Semi-open", "Galley", "L-Shaped", "U-Shaped"])
    
    st.markdown("<h3 style='margin-top: 20px;'>Overall Space Size</h3>", unsafe_allow_html=True)
    space_size = st.slider("Total Area (sq.m)", min_value=20, max_value=500, value=80)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("Continue to Design Preferences", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def design_preferences_page():
    st.markdown("<h1 style='text-align: center;'>Design Preferences</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Help us understand your style and requirements</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="form-container">
        <h3>Style Selection</h3>
    """, unsafe_allow_html=True)
    
    # Style selection with images
    styles = ["Modern", "Minimalist", "Scandinavian", "Industrial", "Thai Contemporary", "Luxury"]
    
    device = get_device_type()
    
    if device == "desktop":
        cols = st.columns(3)
        for i, col in enumerate(cols):
            if i < len(styles):
                with col:
                    st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 20px;">
                        <div style="height: 150px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                            <span style="color: #777;">{styles[i]} Style</span>
                        </div>
                        <div style="margin-top: 10px;">
                            <strong>{styles[i]}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, col in enumerate(cols):
            i += 3
            if i < len(styles):
                with col:
                    st.markdown(f"""
                    <div style="text-align: center; margin-bottom: 20px;">
                        <div style="height: 150px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                            <span style="color: #777;">{styles[i]} Style</span>
                        </div>
                        <div style="margin-top: 10px;">
                            <strong>{styles[i]}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        cols = st.columns(2)
        for i in range(0, len(styles), 2):
            for j in range(2):
                idx = i + j
                if idx < len(styles):
                    with cols[j]:
                        st.markdown(f"""
                        <div style="text-align: center; margin-bottom: 20px;">
                            <div style="height: 120px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                                <span style="color: #777;">{styles[idx]} Style</span>
                            </div>
                            <div style="margin-top: 10px;">
                                <strong>{styles[idx]}</strong>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    selected_style = st.selectbox("Select Your Preferred Style", styles)
    
    st.markdown("<h3 style='margin-top: 30px;'>Color Preferences</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        color_palette = st.selectbox("Color Palette", ["Neutral", "Warm", "Cool", "Vibrant", "Monochrome", "Earthy"])
    with col2:
        accent_color = st.selectbox("Accent Color", ["None", "Blue", "Green", "Orange", "Red", "Yellow", "Purple"])
    
    st.markdown("<h3 style='margin-top: 30px;'>Family Requirements</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        household_size = st.selectbox("Household Size", ["1 person", "2 people", "3-4 people", "5+ people"])
    with col2:
        children = st.selectbox("Children", ["No children", "Toddlers", "School-age children", "Teenagers", "Mixed ages"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Seniors", ["No seniors", "Seniors living in the home"])
    with col2:
        st.selectbox("Pets", ["No pets", "Dogs", "Cats", "Multiple types of pets"])
    
    special_requirements = st.text_area("Special Requirements or Accessibility Needs")
    
    st.markdown("<h3 style='margin-top: 30px;'>Budget Considerations</h3>", unsafe_allow_html=True)
    
    budget_range = st.select_slider(
        "Overall Budget Range",
        options=["Economy", "Standard", "Premium", "Luxury"]
    )
    
    priority_areas = st.multiselect(
        "Priority Areas (where would you like to allocate more budget)",
        ["Furniture", "Lighting", "Flooring", "Wall Treatments", "Storage Solutions", "Decorative Elements"]
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("Continue to Design Generation", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def design_generation_page():
    st.markdown("<h1 style='text-align: center;'>Design Generation</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Creating your personalized 3D designs</p>", unsafe_allow_html=True)
    
    # Progress indicator
    st.progress(0.75)
    st.markdown("<p style='text-align: center;'>Generating designs based on your preferences...</p>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Living Room", "Kitchen", "Bathroom"])
    
    with tab1:
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div style="height: 300px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                <span style="color: #777;">3D Rendering of Living Room</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("Regenerate Design", use_container_width=True)
        
        with st.expander("Design Details", expanded=True):
            st.markdown("""
            <div>
                <h4>Modern Living Room Design</h4>
                <p>This design features a spacious layout with optimal natural lighting. The furniture arrangement promotes conversation while maintaining good flow. Key elements include:</p>
                <ul>
                    <li>Comfortable 3-seater sofa with chaise lounge</li>
                    <li>Minimalist coffee table with storage</li>
                    <li>Media console with integrated storage</li>
                    <li>Accent chair for additional seating</li>
                    <li>Smart lighting system with both ambient and task lighting</li>
                    <li>Built-in bookshelves</li>
                </ul>
                <p>The color scheme includes neutral walls with accent colors through decorative elements. Furniture pieces focus on comfort while maintaining the modern aesthetic.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div style="height: 300px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                <span style="color: #777;">3D Rendering of Kitchen</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("Regenerate Design ", use_container_width=True)
        
        with st.expander("Design Details", expanded=False):
            st.markdown("""
            <div>
                <h4>Modern Kitchen Design</h4>
                <p>This kitchen design maximizes functionality while maintaining a clean, modern aesthetic. The layout follows the efficient work triangle principle. Key features include:</p>
                <ul>
                    <li>Custom cabinetry with soft-close mechanisms</li>
                    <li>Quartz countertops for durability and easy maintenance</li>
                    <li>Kitchen island with breakfast bar seating</li>
                    <li>Under-cabinet LED lighting</li>
                    <li>Premium appliances with energy-efficient ratings</li>
                    <li>Smart storage solutions to maximize space</li>
                </ul>
                <p>The design incorporates a neutral color palette with wood accents for warmth. All materials are selected for durability and ease of cleaning.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <div style="height: 300px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                <span style="color: #777;">3D Rendering of Bathroom</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("Regenerate Design  ", use_container_width=True)
        
        with st.expander("Design Details", expanded=False):
            st.markdown("""
            <div>
                <h4>Modern Bathroom Design</h4>
                <p>This bathroom design balances luxury with functionality. The layout maximizes the available space while creating a spa-like atmosphere. Key features include:</p>
                <ul>
                    <li>Walk-in shower with rainfall showerhead</li>
                    <li>Floating vanity with integrated sink</li>
                    <li>Large mirror with integrated LED lighting</li>
                    <li>Storage solutions including medicine cabinet and under-sink storage</li>
                    <li>Porcelain tile flooring with underfloor heating</li>
                    <li>Water-efficient fixtures</li>
                </ul>
                <p>The design uses a monochromatic color scheme with textural elements to add visual interest while maintaining a clean, uncluttered look.</p>
            </div>
            """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("Review Previous Step", use_container_width=True)
    with col2:
        st.button("Continue to Quote", use_container_width=True)

def quote_page():
    st.markdown("<h1 style='text-align: center;'>Project Quote</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Summary and pricing for your interior design project</p>", unsafe_allow_html=True)
    
    # Project summary
    st.markdown("""
    <div class="card">
        <h3>Project Overview</h3>
        <table style="width: 100%;">
            <tr>
                <td style="width: 40%; padding: 8px 0;"><strong>Property Type:</strong></td>
                <td style="padding: 8px 0;">Condominium</td>
            </tr>
            <tr>
                <td style="padding: 8px 0;"><strong>Rooms:</strong></td>
                <td style="padding: 8px 0;">Living Room, Kitchen, Bathroom</td>
            </tr>
            <tr>
                <td style="padding: 8px 0;"><strong>Total Area:</strong></td>
                <td style="padding: 8px 0;">80 sq.m</td>
            </tr>
            <tr>
                <td style="padding: 8px 0;"><strong>Design Style:</strong></td>
                <td style="padding: 8px 0;">Modern</td>
            </tr>
            <tr>
                <td style="padding: 8px 0;"><strong>Budget Range:</strong></td>
                <td style="padding: 8px 0;">Standard</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Room breakdowns
    st.markdown("<h3 style='margin-top: 30px;'>Room Breakdown</h3>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Living Room", "Kitchen", "Bathroom"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            <div style="height: 200px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                <span style="color: #777;">Living Room Design</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="card" style="height: 100%;">
                <h4 style="margin-top: 0;">Living Room Costs</h4>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Furniture:</span>
                    <span style="font-weight: bold;">85,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Lighting:</span>
                    <span style="font-weight: bold;">15,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Flooring:</span>
                    <span style="font-weight: bold;">25,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Wall Treatments:</span>
                    <span style="font-weight: bold;">18,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Accessories:</span>
                    <span style="font-weight: bold;">12,000฿</span>
                </div>
                <hr>
                <div style="display: flex; justify-content: space-between; font-weight: bold; color: {colors['accent']};">
                    <span>Subtotal:</span>
                    <span>155,000฿</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            <div style="height: 200px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                <span style="color: #777;">Kitchen Design</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="card" style="height: 100%;">
                <h4 style="margin-top: 0;">Kitchen Costs</h4>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Cabinetry:</span>
                    <span style="font-weight: bold;">75,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Countertops:</span>
                    <span style="font-weight: bold;">35,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Appliances:</span>
                    <span style="font-weight: bold;">50,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Fixtures & Plumbing:</span>
                    <span style="font-weight: bold;">15,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Flooring & Backsplash:</span>
                    <span style="font-weight: bold;">25,000฿</span>
                </div>
                <hr>
                <div style="display: flex; justify-content: space-between; font-weight: bold; color: {colors['accent']};">
                    <span>Subtotal:</span>
                    <span>200,000฿</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            <div style="height: 200px; background-color: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                <span style="color: #777;">Bathroom Design</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="card" style="height: 100%;">
                <h4 style="margin-top: 0;">Bathroom Costs</h4>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Fixtures & Sanitaryware:</span>
                    <span style="font-weight: bold;">45,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Tiling & Flooring:</span>
                    <span style="font-weight: bold;">30,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Shower/Bath:</span>
                    <span style="font-weight: bold;">25,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Vanity & Storage:</span>
                    <span style="font-weight: bold;">18,000฿</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span>Lighting & Accessories:</span>
                    <span style="font-weight: bold;">12,000฿</span>
                </div>
                <hr>
                <div style="display: flex; justify-content: space-between; font-weight: bold; color: {colors['accent']};">
                    <span>Subtotal:</span>
                    <span>130,000฿</span>
                </div>
            </div>
            """
