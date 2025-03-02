import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# ตั้งค่าหน้าเพจ
st.set_page_config(
    page_title="RoomLab - ออกแบบภายในด้วย AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# เก็บสถานะและข้อมูลผู้ใช้ใน session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = True
if 'username' not in st.session_state:
    st.session_state.username = "คุณสมชาย"
if 'tokens' not in st.session_state:
    st.session_state.tokens = 10
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "create_design"
if 'design_step' not in st.session_state:
    st.session_state.design_step = 1  # เริ่มต้นที่ขั้นตอนแรก
if 'projects' not in st.session_state:
    st.session_state.projects = []
if 'generated_images' not in st.session_state:
    # เก็บรูปภาพที่ถูก generate ไว้
    st.session_state.generated_images = {
        1: "https://via.placeholder.com/750x500?text=Generated+Design+View+1",
        2: "https://via.placeholder.com/750x500?text=Generated+Design+View+2",
        3: "https://via.placeholder.com/750x500?text=Generated+Design+View+3",
        4: "https://via.placeholder.com/750x500?text=Generated+Design+View+4"
    }
if 'design_details' not in st.session_state:
    # ข้อมูลการออกแบบ
    st.session_state.design_details = {
        "project_name": "ออกแบบห้องนั่งเล่นบ้านคุณสมชาย",
        "room_type": "ห้องนั่งเล่น",
        "room_size": "35 ตร.ม.",
        "room_shape": "สี่เหลี่ยมผืนผ้า",
        "design_style": "โมเดิร์น",
        "color_theme": "เอิร์ธโทน",
        "main_furniture": "โซฟาขนาดใหญ่ 3 ที่นั่ง, โต๊ะกลางทรงสี่เหลี่ยม, ชั้นวางทีวีติดผนัง",
        "additional_furniture": "เก้าอี้พักผ่อน, โคมไฟตั้งพื้น, พรม",
        "decor_level": "ระดับ 3",
        "created_date": "02/03/2025",
        "status": "เสร็จสมบูรณ์",
        "tokens_used": 1
    }
if 'saved_notes' not in st.session_state:
    st.session_state.saved_notes = []  # เก็บบันทึกของผู้ใช้
if 'comments' not in st.session_state:
    st.session_state.comments = []  # เก็บความคิดเห็นของผู้ใช้
if 'regenerate_count' not in st.session_state:
    st.session_state.regenerate_count = 0  # จำนวนครั้งที่ regenerate

# ฟังก์ชันช่วยเหลือ
def change_tab(tab):
    st.session_state.active_tab = tab

def set_design_step(step):
    st.session_state.design_step = step

def set_result_tab(tab):
    st.session_state.result_tab = tab

def set_selected_view(view):
    st.session_state.selected_view = view

def regenerate_design():
    # จำลองการสร้างรูปภาพใหม่
    if st.session_state.tokens >= 1:
        st.session_state.tokens -= 1
        st.session_state.regenerate_count += 1
        
        # สร้างลิงก์ URL สำหรับรูปภาพใหม่ (ในที่นี้เป็นเพียงการปรับ timestamp เพื่อให้ดูเหมือนเปลี่ยนรูป)
        timestamp = int(time.time())
        for i in range(1, 5):
            st.session_state.generated_images[i] = f"https://via.placeholder.com/750x500?text=Regenerated+Design+View+{i}+({st.session_state.regenerate_count})"
        
        return True
    else:
        return False

def save_design_data(data):
    # บันทึกข้อมูลการออกแบบ
    if 'design_data' not in st.session_state:
        st.session_state.design_data = {}
    
    st.session_state.design_data.update(data)
    return True

def calculate_total_price():
    # สมมติว่ามีข้อมูล BOQ items
    boq_items = [
        {"category": "เฟอร์นิเจอร์", "item": "โซฟา 3 ที่นั่ง", "brand": "IKEA", "model": "KIVIK", "price": 25000, "quantity": 1},
        {"category": "เฟอร์นิเจอร์", "item": "โต๊ะกลาง", "brand": "IKEA", "model": "LACK", "price": 3500, "quantity": 1},
        {"category": "เฟอร์นิเจอร์", "item": "ชั้นวางทีวี", "brand": "IKEA", "model": "BESTA", "price": 12000, "quantity": 1},
        {"category": "เฟอร์นิเจอร์", "item": "เก้าอี้พักผ่อน", "brand": "IKEA", "model": "POÄNG", "price": 8500, "quantity": 1},
        {"category": "ของตกแต่ง", "item": "โคมไฟตั้งพื้น", "brand": "IKEA", "model": "HEKTAR", "price": 2500, "quantity": 1},
        {"category": "ของตกแต่ง", "item": "พรม", "brand": "IKEA", "model": "VINDUM", "price": 6000, "quantity": 1},
    ]
    total = 0
    for item in boq_items:
        total += item["price"] * item["quantity"]
    return total

# CSS สำหรับจัดรูปแบบเว็บไซต์
def load_css():
    return """
    <style>
    /* หน้าโดยรวม */
    .main {
        background-color: #f8f9fa;
    }
    
    /* แก้ไข CSS สำหรับ header */
    .stApp header {
        background-color: #ffffff;
        border-bottom: 1px solid #dee2e6;
    }
    
    /* แก้ไข CSS สำหรับ sidebar ให้เป็นสีเทาเข้ม #212130 */
    [data-testid="stSidebar"] {
        background-color: #212130;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-color: #212130;
    }
    [data-testid="stSidebar"] .stButton button {
        background-color: #2d2d3e;
        color: white;
        border: none;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #3d3d4f;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #ffffff;
    }
    [data-testid="stSidebar"] button[kind="secondary"] {
        background-color: #2d2d3e;
        color: white;
        border: none;
    }
    [data-testid="stSidebar"] hr {
        border-color: #3d3d4f;
    }
    
    /* สถานะการทำงาน */
    .progress-tracker {
        display: flex;
        align-items: center;
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .progress-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-right: 1rem;
    }
    .step-circle {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: #e9ecef;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #343a40;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .step-circle.active {
        background-color: #6d63ff;
        color: white;
    }
    .step-circle.completed {
        background-color: #28a745;
        color: white;
    }
    .step-connector {
        height: 2px;
        width: 50px;
        background-color: #dee2e6;
        margin: 0 0.5rem;
    }
    .step-connector.active {
        background-color: #28a745;
    }
    
    /* สไตล์การ์ด */
    .card {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    /* รูปภาพผลลัพธ์ */
    .result-image {
        width: 100%;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* ตัวเลือกมุมมอง */
    .view-selector {
        display: flex;
        background-color: #f8f9fa;
        border-radius: 30px;
        margin: 1rem 0;
        overflow: hidden;
    }
    .view-option {
        flex: 1;
        text-align: center;
        padding: 0.75rem 1rem;
        cursor: pointer;
    }
    .view-option.active {
        background-color: #6d63ff;
        color: white;
    }
    
    /* แท็บรายละเอียด */
    .detail-tabs {
        display: flex;
        border-bottom: 1px solid #dee2e6;
        margin-bottom: 1.5rem;
    }
    .detail-tab {
        padding: 0.75rem 1.5rem;
        cursor: pointer;
        border-bottom: 3px solid transparent;
    }
    .detail-tab.active {
        border-bottom-color: #6d63ff;
        font-weight: bold;
        color: #6d63ff;
    }
    
    /* ข้อมูลรายละเอียด */
    .detail-row {
        display: flex;
        margin-bottom: 1rem;
        align-items: flex-start;
    }
    .detail-label {
        font-weight: bold;
        width: 180px;
        margin-right: 1rem;
    }
    .detail-value {
        flex: 1;
    }
    
    /* สถานะ */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.85rem;
    }
    .status-completed {
        background-color: #d4edda;
        color: #155724;
    }
    .status-processing {
        background-color: #fff3cd;
        color: #856404;
    }
    
    /* บันทึกและความคิดเห็น */
    .notes-panel {
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        height: 100%;
    }
    .note-card {
        background-color: #f8f9fa;
        border-radius: 0.25rem;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
    }
    .add-note {
        text-align: center;
        border: 1px dashed #dee2e6;
        border-radius: 0.25rem;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        cursor: pointer;
    }
    
    /* ปุ่มสไตล์เดียวกับที่ใช้หน้าอื่น */
    .stButton button {
        border-radius: 0.25rem;
    }
    
    /* สไตล์ด้านบน (header) */
    .roomlab-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    .roomlab-logo {
        font-size: 1.75rem;
        font-weight: bold;
        color: #6d63ff;
    }
    .roomlab-subtitle {
        font-size: 1rem;
        color: #6c757d;
    }
    
    /* สไตล์ Token ด้านบน */
    .token-display {
        display: inline-block;
        background-color: #f0f4f8;
        padding: 0.5rem 1rem;
        border-radius: 1rem;
        font-weight: bold;
        color: #6d63ff;
    }
    
    /* BOQ ตาราง */
    .boq-table {
        width: 100%;
        border-collapse: collapse;
    }
    .boq-table th, .boq-table td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #dee2e6;
        text-align: left;
    }
    .boq-table th {
        background-color: #f8f9fa;
        font-weight: bold;
    }
    .category-header {
        background-color: #e9ecef;
        font-weight: bold;
    }
    </style>
    """

# แบรนด์ RoomLab
def display_brand_header():
    st.markdown(f"""
    <div class="roomlab-header">
        <div>
            <div class="roomlab-logo">RoomLab</div>
            <div class="roomlab-subtitle">ออกแบบภายในที่ตอบโจทย์ด้วย AI</div>
        </div>
        <div class="token-display">
            💎 {st.session_state.tokens} Tokens คงเหลือ
        </div>
    </div>
    """, unsafe_allow_html=True)

# ฟังก์ชันสำหรับ sidebar
def render_sidebar():
    with st.sidebar:
        # โลโก้และข้อมูลผู้ใช้
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown('<div style="background-color: #6d63ff; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px;">RL</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f"**{st.session_state.username}**")
            st.markdown(f"<span style='color: #6d63ff;'>{st.session_state.tokens} Tokens</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # เมนูหลัก
        menu_items = {
            "home": "🏠 หน้าหลัก",
            "create_design": "🎨 สร้างดีไซน์",
            "my_projects": "📂 โปรเจคของฉัน",
            "buy_token": "🪙 ซื้อ Token",
            "pricing": "💰 คำนวณราคา",
            "history": "📊 ประวัติการใช้งาน",
            "settings": "⚙️ ตั้งค่าบัญชี"
        }
        
        for key, label in menu_items.items():
            if st.button(label, key=f"menu_{key}", use_container_width=True, 
                       type="primary" if st.session_state.active_tab == key else "secondary"):
                change_tab(key)
                st.experimental_rerun()
        
        # ออกจากระบบที่ด้านล่าง
        st.markdown('<div style="position: fixed; bottom: 60px; width: 17%;"></div>', unsafe_allow_html=True)
        st.markdown("---")
        if st.button("📤 ออกจากระบบ", use_container_width=True):
            st.session_state.logged_in = False
            st.experimental_rerun()

# ฟังก์ชันสำหรับแสดงสถานะการทำงาน
def render_progress_tracker():
    steps = [
        {"num": 1, "name": "ข้อมูล", "status": "active" if st.session_state.design_step == 1 else ("completed" if st.session_state.design_step > 1 else "")},
        {"num": 2, "name": "สไตล์", "status": "active" if st.session_state.design_step == 2 else ("completed" if st.session_state.design_step > 2 else "")},
        {"num": 3, "name": "เฟอร์นิเจอร์", "status": "active" if st.session_state.design_step == 3 else ("completed" if st.session_state.design_step > 3 else "")},
        {"num": 4, "name": "ผลลัพธ์", "status": "active" if st.session_state.design_step == 4 else ("completed" if st.session_state.design_step > 4 else "")},
        {"num": 5, "name": "BOQ", "status": "active" if st.session_state.design_step == 5 else ""}
    ]
    
    st.markdown("""
    <div class="progress-tracker">
    """, unsafe_allow_html=True)
    
    for i, step in enumerate(steps):
        status_class = ""
        content = str(step["num"])
        
        if step["status"] == "completed":
            status_class = "completed"
            content = "✓"
        elif step["status"] == "active":
            status_class = "active"
        
        connector_class = "active" if i < len(steps) - 1 and (steps[i]["status"] == "completed" or steps[i+1]["status"] == "active" or steps[i+1]["status"] == "completed") else ""
        
        st.markdown(f"""
        <div style="display: flex; align-items: center;">
            <div class="progress-step">
                <div class="step-circle {status_class}">{content}</div>
                <div class="step-name">{step["name"]}</div>
            </div>
            {f'<div class="step-connector {connector_class}"></div>' if i < len(steps) - 1 else ''}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

# ฟังก์ชันสำหรับแสดงหน้าแรกที่ลูกค้ากรอกรายละเอียด (ขั้นตอนที่ 1)
def render_first_step():
    st.markdown("<h2>สร้างดีไซน์ใหม่</h2>", unsafe_allow_html=True)
    st.markdown("<p>กรอกข้อมูลพื้นฐานเพื่อเริ่มต้นการออกแบบห้องของคุณ</p>", unsafe_allow_html=True)
    
    # Card สำหรับกรอกข้อมูลพื้นฐาน
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("ข้อมูลพื้นฐาน")
    
    with st.form("design_form_step1"):
        project_name = st.text_input("ชื่อโปรเจค", value="ออกแบบห้องนั่งเล่นบ้านคุณสมชาย")
        
        col1, col2 = st.columns(2)
        with col1:
            room_type = st.selectbox("ประเภทห้อง", 
                                   ["ห้องนั่งเล่น", "ห้องนอน", "ห้องครัว", "ห้องทำงาน", "ห้องน้ำ"])
            room_size = st.number_input("ขนาดห้อง (ตร.ม.)", min_value=1, value=35)
        
        with col2:
            room_shape = st.selectbox("รูปแบบห้อง", 
                                    ["สี่เหลี่ยมผืนผ้า", "สี่เหลี่ยมจัตุรัส", "ตัวแอล (L-Shape)", "แบบเปิดโล่ง"])
            ceiling_height = st.selectbox("ความสูงเพดาน (เมตร)", 
                                        ["2.4", "2.7", "3.0", "มากกว่า 3.0"])
        
        additional_details = st.text_area("รายละเอียดเพิ่มเติม", 
                                       "ต้องการห้องที่มีโซฟา โต๊ะกลาง ทีวี และชั้นวางหนังสือ")
        
        # ปุ่มดำเนินการ
        st.markdown("<br>", unsafe_allow_html=True)
        col3, col4, col5, col6 = st.columns([2, 1, 1, 1.5])  # แบ่งเป็น 4 คอลัมน์
        
        with col4:
            cancel_button = st.form_submit_button("ยกเลิก", use_container_width=True)
        
        with col5:
            next_button = st.form_submit_button("ถัดไป", type="primary", use_container_width=True)
        
        with col6:
            generate_button = st.form_submit_button("✨ Generate ภาพทันที", 
                                                 type="primary", 
                                                 use_container_width=True,
                                                 help="ข้ามขั้นตอนเลือกสไตล์และเฟอร์นิเจอร์")
        
        # ข้อความอธิบายการใช้ Token
        st.markdown("<div style='text-align: right; font-size: 0.8rem; color: #6d63ff; margin-top: 0.5rem;'>การ Generate ภาพทันทีจะใช้ 1 Token จากยอดคงเหลือของคุณ</div>", unsafe_allow_html=True)
            
        if next_button:
            if project_name:
                # บันทึกข้อมูล
                design_data = {
                    "project_name": project_name,
                    "room_type": room_type,
                    "room_size": room_size,
                    "room_shape": room_shape,
                    "ceiling_height": ceiling_height,
                    "additional_details": additional_details
                }
                
                if save_design_data(design_data):
                    # ไปขั้นตอนถัดไป
                    set_design_step(2)
                    st.experimental_rerun()
            else:
                st.error("กรุณากรอกชื่อโปรเจค")
        
        if generate_button:
            if project_name:
                # บันทึกข้อมูล
                design_data = {
                    "project_name": project_name,
                    "room_type": room_type,
                    "room_size": room_size,
                    "room_shape": room_shape,
                    "ceiling_height": ceiling_height,
                    "additional_details": additional_details,
                    # กำหนดค่าเริ่มต้นสำหรับข้อมูลที่ผู้ใช้ไม่ได้กำหนด
                    "design_style": "โมเดิร์น",  # สไตล์เริ่มต้น
                    "color_theme": "เอิร์ธโทน",  # โทนสีเริ่มต้น
                    "main_furniture": f"โซฟา, โต๊ะกลาง, ทีวี, ชั้นวางหนังสือ",  # เฟอร์นิเจอร์เริ่มต้น
                    "decor_level": "ระดับกลาง"  # ระดับการตกแต่งเริ่มต้น
                }
                
                if save_design_data(design_data):
                    # ตรวจสอบว่ามี Token เพียงพอหรือไม่
                    if st.session_state.tokens >= 1:
                        st.session_state.tokens -= 1  # หัก Token
                        # ข้ามไปขั้นตอนที่ 4 (ผลลัพธ์) เลย
                        set_design_step(4)
                        st.experimental_rerun()
                    else:
                        st.error("Token ไม่เพียงพอ กรุณาซื้อ Token เพิ่ม")
            else:
                st.error("กรุณากรอกชื่อโปรเจค")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # คำแนะนำการใช้งาน
    st.info("💡 เคล็ดลับ: การให้รายละเอียดเพิ่มเติมจะช่วยให้ AI สร้างการออกแบบที่ตรงกับความต้องการของคุณมากขึ้น")
    
    # ตัวอย่างผลงาน
    st.markdown("<h3>ตัวอย่างผลงานของเรา</h3>", unsafe_allow_html=True)
    
    # แสดงตัวอย่างผลงาน 3 รูป
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://via.placeholder.com/300x200?text=Example+1", use_column_width=True)
        st.markdown("<p style='text-align: center;'>ห้องนั่งเล่นสไตล์โมเดิร์น</p>", unsafe_allow_html=True)
    
    with col2:
        st.image("https://via.placeholder.com/300x200?text=Example+2", use_column_width=True)
        st.markdown("<p style='text-align: center;'>ห้องนอนสไตล์มินิมอล</p>", unsafe_allow_html=True)
    
    with col3:
        st.image("https://via.placeholder.com/300x200?text=Example+3", use_column_width=True)
        st.markdown("<p style='text-align: center;'>ห้องครัวสไตล์สแกนดิเนเวียน</p>", unsafe_allow_html=True)

# ฟังก์ชันสำหรับแสดงภาพผลลัพธ์ (ขั้นตอนที่ 4)
def render_design_results():
    if 'selected_view' not in st.session_state:
        st.session_state.selected_view = 1  # มุมมองที่เลือก (1-4)
    if 'result_tab' not in st.session_state:
        st.session_state.result_tab = "details"  # details, edit, or save
    
    st.markdown("<h2>ผลลัพธ์การออกแบบ</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # แสดงรูปภาพ
    col1, col2 = st.columns([5, 1])
    
    with col1:
        # แสดงรูปภาพที่เลือก
        selected_image = st.session_state.generated_images[st.session_state.selected_view]
        st.image(selected_image, use_column_width=True, caption=f"มุมมองที่ {st.session_state.selected_view}")
        
        # ตัวเลือกมุมมอง
        view_col1, view_col2, view_col3, view_col4 = st.columns(4)
        
        view_cols = [view_col1, view_col2, view_col3, view_col4]
        for i, col in enumerate(view_cols, 1):
            with col:
                if st.button(f"มุมมองที่ {i}", key=f"view_{i}", 
                           use_container_width=True,
                           type="primary" if st.session_state.selected_view == i else "secondary"):
                    st.session_state.selected_view = i
                    st.experimental_rerun()
    
    with col2:
        st.markdown("<div class='notes-panel'>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>บันทึก</h4>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # แสดงบันทึกที่มีอยู่
        for i, note in enumerate(st.session_state.saved_notes):
            st.markdown(f"""
            <div class="note-card">
                บันทึก {i+1}
            </div>
            """, unsafe_allow_html=True)
        
        # ปุ่มเพิ่มบันทึก
        if st.button("+ เพิ่มบันทึก", key="add_note"):
            st.session_state.saved_notes.append(f"บันทึก {len(st.session_state.saved_notes) + 1}")
        
        st.markdown("<h4 style='text-align: center; margin-top: 1rem;'>ความเห็น</h4>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ช่องเพิ่มความคิดเห็น
        comment = st.text_area("เพิ่มความเห็น", key="comment_input", label_visibility="collapsed", height=100)
        if st.button("ส่งความเห็น", key="submit_comment"):
            if comment:
                st.session_state.comments.append(comment)
                st.experimental_rerun()
        
        # แสดงความคิดเห็นที่มีอยู่
        for comment in st.session_state.comments:
            st.markdown(f"""
            <div style="background-color: #f0f4f8; padding: 0.5rem; border-radius: 0.25rem; margin-bottom: 0.5rem; font-size: 0.85rem;">
                {comment}
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
    
    # แท็บรายละเอียด
    tabs = st.tabs(["รายละเอียดการออกแบบ", "แก้ไขและ Regenerate", "บันทึกและดำเนินการต่อ"])
    
    with tabs[0]:
        # รายละเอียดการออกแบบ
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        st.subheader("ข้อมูลการออกแบบ")
        
        details = st.session_state.design_details
        
        # แสดงข้อมูลในรูปแบบตาราง
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**ชื่อโปรเจค:**")
            st.write(details["project_name"])
            
            st.markdown("**ประเภทห้อง:**")
            st.write(details["room_type"])
            
            st.markdown("**ขนาดห้อง:**")
            st.write(details["room_size"])
            
            st.markdown("**รูปแบบห้อง:**")
            st.write(details["room_shape"])
            
            st.markdown("**สไตล์การออกแบบ:**")
            st.write(details["design_style"])
        
        with col2:
            st.markdown("**โทนสี:**")
            st.write(details["color_theme"])
            
            st.markdown("**เฟอร์นิเจอร์หลัก:**")
            st.write(details["main_furniture"])
            
            st.markdown("**เฟอร์นิเจอร์เสริม:**")
            st.write(details["additional_furniture"])
            
            st.markdown("**ระดับการตกแต่ง:**")
            st.write(details["decor_level"])
            
            st.markdown("**Token ที่ใช้:**")
            st.write(f"{details['tokens_used']} Token")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ปุ่มดำเนินการ
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("◀ ย้อนกลับ", use_container_width=True):
                set_design_step(3)  # กลับไปขั้นตอนที่ 3
                st.experimental_rerun()
        
        with col2:
            if st.button("🔄 Regenerate", use_container_width=True, type="warning"):
                st.experimental_rerun()
        
        with col3:
            if st.button("ถัดไป: ดูรายละเอียด BOQ ▶", use_container_width=True, type="primary"):
                set_design_step(5)  # ไปขั้นตอน BOQ
                st.experimental_rerun()
        
        # ข้อความแจ้งเตือน
        st.info(f"💡 การ Regenerate จะใช้ Token เพิ่มอีก 1 ดวง (คงเหลือ {st.session_state.tokens} Token)")
        st.success("⭐ เคล็ดลับ: คุณสามารถบันทึกภาพผลลัพธ์นี้และแชร์กับเพื่อนหรือครอบครัวได้")
    
    with tabs[1]:
        # แก้ไขและ Regenerate
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        st.subheader("แก้ไขพารามิเตอร์และ Regenerate")
        
        with st.form("edit_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                design_style = st.selectbox("สไตล์การออกแบบ", 
                                        ["โมเดิร์น", "มินิมอล", "ลอฟท์", "สแกนดิเนเวียน", "คลาสสิค"],
                                        index=0)
                
                color_theme = st.selectbox("โทนสี", 
                                        ["เอิร์ธโทน", "โมโนโทน", "พาสเทล", "สีฟ้า", "สีเขียว"],
                                        index=0)
                
                sofa_type = st.selectbox("โซฟา", 
                                        ["โซฟาขนาดใหญ่ 3 ที่นั่ง", "โซฟาตัว L", "โซฟาขนาดกลาง 2 ที่นั่ง", "โซฟาเดี่ยว + เก้าอี้"],
                                        index=0)
            
            with col2:
                table_type = st.selectbox("โต๊ะกลาง", 
                                        ["โต๊ะกลางทรงสี่เหลี่ยม", "โต๊ะกลางทรงกลม", "โต๊ะกลางทรงรี", "โต๊ะเล็กหลายตัว"],
                                        index=0)
                
                tv_stand = st.selectbox("ชั้นวางทีวี", 
                                    ["ชั้นวางทีวีติดผนัง", "ตู้ทีวีขนาดใหญ่", "ชั้นวางทีวีแบบลอย", "ไม่มีชั้นวางทีวี"],
                                    index=0)
                
                decor_level = st.slider("ระดับการตกแต่ง", 1, 5, 3)
            
            specific_requirements = st.text_area("ความต้องการเฉพาะเพิ่มเติม")
            
            st.markdown(f"""
            <div style="background-color: #fff3cd; border: 1px solid #ffeeba; border-radius: 0.25rem; padding: 1rem; margin: 1rem 0;">
                <b>หมายเหตุ:</b> การ Regenerate จะใช้ Token เพิ่มอีก 1 ดวง (คงเหลือ {st.session_state.tokens} Token)
            </div>
            """, unsafe_allow_html=True)
            
            col3, col4 = st.columns([1, 1])
            
            with col3:
                back_button = st.form_submit_button("กลับไปหน้ารายละเอียด", use_container_width=True)
            
            with col4:
                regenerate_button = st.form_submit_button("Regenerate", use_container_width=True, type="primary")
            
            if back_button:
                st.experimental_rerun()
            
            if regenerate_button:
                if regenerate_design():
                    # อัปเดตข้อมูลการออกแบบ
                    st.session_state.design_details["design_style"] = design_style
                    st.session_state.design_details["color_theme"] = color_theme
                    st.session_state.design_details["main_furniture"] = f"{sofa_type}, {table_type}, {tv_stand}"
                    st.session_state.design_details["decor_level"] = f"ระดับ {decor_level}"
                    st.session_state.design_details["tokens_used"] += 1
                    
                    st.success("สร้างการออกแบบใหม่สำเร็จ!")
                    st.experimental_rerun()
                else:
                    st.error("Token ไม่เพียงพอ กรุณาซื้อ Token เพิ่ม")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[2]:
        # บันทึกและดำเนินการต่อ
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        st.subheader("บันทึกและดำเนินการต่อ")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h4>ตัวเลือกการบันทึก</h4>", unsafe_allow_html=True)
            
            save_options = [
                "บันทึกเป็นรูปภาพ (JPG)",
                "บันทึกเป็นรูปภาพคุณภาพสูง (PNG)",
                "บันทึกทุกมุมมอง (ZIP)",
                "แชร์ทางอีเมล"
            ]
            
            selected_save_option = st.radio("เลือกวิธีการบันทึก", save_options)
            
            email = st.text_input("อีเมลสำหรับรับไฟล์ (ถ้ามี)")
            
            if st.button("บันทึก", type="primary", use_container_width=True):
                st.success(f"บันทึกเรียบร้อย! เลือกวิธี: {selected_save_option}")
        
        with col2:
            st.markdown("<h4>ขั้นตอนถัดไป</h4>", unsafe_allow_html=True)
            
            st.markdown("""
            <p>เลือกดำเนินการต่อเพื่อ:</p>
            <ul>
                <li>ดูรายการวัสดุและเฟอร์นิเจอร์ (BOQ)</li>
                <li>ประมาณการราคาการตกแต่ง</li>
                <li>รับใบเสนอราคาอย่างละเอียด</li>
            </ul>
            """, unsafe_allow_html=True)
            
            if st.button("ดูรายละเอียด BOQ", type="primary", use_container_width=True):
                set_design_step(5)  # ไปขั้นตอน BOQ
                st.experimental_rerun()
            
            if st.button("ขอใบเสนอราคาละเอียด", use_container_width=True):
                st.info("ทีมงานจะติดต่อกลับเพื่อให้รายละเอียดเพิ่มเติมภายใน 24 ชั่วโมง")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("สร้างดีไซน์เพิ่มเติม")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("""
            <p>หากต้องการสร้างดีไซน์เพิ่มเติม คุณสามารถ:</p>
            <ul>
                <li>สร้างห้องใหม่ด้วยข้อมูลเริ่มต้นใหม่</li>
                <li>สร้างดีไซน์ห้องอื่นๆ ในโปรเจคเดียวกัน</li>
            </ul>
            """, unsafe_allow_html=True)
            
            if st.button("สร้างดีไซน์ใหม่", use_container_width=True):
                set_design_step(1)  # กลับไปขั้นตอนแรก
                st.experimental_rerun()
        
        with col4:
            st.markdown(f"""
            <p>Token คงเหลือ:</p>
            <h3 style="color: #6d63ff;">{st.session_state.tokens} Token</h3>
            <p>ต้องการ Token เพิ่ม?</p>
            """, unsafe_allow_html=True)
            
            if st.button("ซื้อ Token เพิ่ม", type="primary", use_container_width=True):
                change_tab("buy_token")
                st.experimental_rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# ฟังก์ชันสำหรับแสดงหน้า BOQ (ขั้นตอนที่ 5)
def render_boq_page():
    st.markdown("<h2>รายละเอียด BOQ (Bill of Quantities)</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # แสดงภาพและรายละเอียดโปรเจค
    col1, col2 = st.columns([2, 3])
    
    with col1:
        selected_image = st.session_state.generated_images[1]  # ใช้ภาพแรก
        st.image(selected_image, use_column_width=True, caption="ภาพการออกแบบ")
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("ข้อมูลโปรเจค")
        
        details = st.session_state.design_details
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("**ชื่อโปรเจค:**")
            st.write(details["project_name"])
            
            st.markdown("**ประเภทห้อง:**")
            st.write(details["room_type"])
        
        with col4:
            st.markdown("**ขนาดห้อง:**")
            st.write(details["room_size"])
            
            st.markdown("**สไตล์การออกแบบ:**")
            st.write(details["design_style"])
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # แสดงรายการ BOQ
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("รายการวัสดุและเฟอร์นิเจอร์")
    
    # สร้างข้อมูลตัวอย่างสำหรับ BOQ
    boq_items = [
        {"category": "เฟอร์นิเจอร์", "item": "โซฟา 3 ที่นั่ง", "brand": "IKEA", "model": "KIVIK", "price": 25000, "quantity": 1},
        {"category": "เฟอร์นิเจอร์", "item": "โต๊ะกลาง", "brand": "IKEA", "model": "LACK", "price": 3500, "quantity": 1},
        {"category": "เฟอร์นิเจอร์", "item": "ชั้นวางทีวี", "brand": "IKEA", "model": "BESTA", "price": 12000, "quantity": 1},
        {"category": "เฟอร์นิเจอร์", "item": "เก้าอี้พักผ่อน", "brand": "IKEA", "model": "POÄNG", "price": 8500, "quantity": 1},
        {"category": "ของตกแต่ง", "item": "โคมไฟตั้งพื้น", "brand": "IKEA", "model": "HEKTAR", "price": 2500, "quantity": 1},
        {"category": "ของตกแต่ง", "item": "พรม", "brand": "IKEA", "model": "VINDUM", "price": 6000, "quantity": 1},
        {"category": "ของตกแต่ง", "item": "หมอนอิง", "brand": "IKEA", "model": "SANELA", "price": 750, "quantity": 4},
        {"category": "สี", "item": "สีผนัง", "brand": "TOA", "model": "SUPER SHIELD MATT", "price": 1200, "quantity": 2},
        {"category": "วัสดุตกแต่ง", "item": "วอลเปเปอร์", "brand": "GOODRICH", "model": "Modern Pattern", "price": 5500, "quantity": 1},
        {"category": "อื่นๆ", "item": "ค่าติดตั้ง", "brand": "-", "model": "-", "price": 15000, "quantity": 1}
    ]
    
    # จัดกลุ่มรายการตามหมวดหมู่
    boq_by_category = {}
    for item in boq_items:
        category = item["category"]
        if category not in boq_by_category:
            boq_by_category[category] = []
        boq_by_category[category].append(item)
    
    # สร้างตาราง BOQ
    for category, items in boq_by_category.items():
        st.markdown(f"#### {category}")
        
        # สร้างตาราง
        data = []
        for item in items:
            total_price = item["price"] * item["quantity"]
            data.append({
                "รายการ": item["item"],
                "แบรนด์": item["brand"],
                "รุ่น": item["model"],
                "จำนวน": item["quantity"],
                "ราคาต่อหน่วย": f"{item['price']:,} บาท",
                "ราคารวม": f"{total_price:,} บาท"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # คำนวณและแสดงราคารวม
    total_price = sum(item["price"] * item["quantity"] for item in boq_items)
    st.markdown(f"#### ราคารวมทั้งหมด: {total_price:,} บาท")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ปุ่มดำเนินการต่อ
    col5, col6, col7 = st.columns([1, 1, 2])
    
    with col5:
        if st.button("◀ กลับไปแก้ไขดีไซน์", use_container_width=True):
            set_design_step(4)  # กลับไปขั้นตอนที่ 4
            st.experimental_rerun()
    
    with col6:
        if st.button("💾 บันทึก BOQ", use_container_width=True):
            st.success("บันทึก BOQ เรียบร้อย!")
    
    with col7:
        if st.button("📋 ขอใบเสนอราคาอย่างละเอียด", type="primary", use_container_width=True):
            st.success("ส่งคำขอใบเสนอราคาเรียบร้อย ทีมงานจะติดต่อกลับภายใน 24 ชั่วโมง")
    
    # ข้อมูลเพิ่มเติม
    st.info("ราคาที่แสดงเป็นเพียงการประมาณการเบื้องต้น ราคาและรายละเอียดอาจมีการเปลี่ยนแปลงตามความพร้อมของสินค้าและการตรวจสอบพื้นที่จริง")

# ฟังก์ชันหลักของแอปพลิเคชัน
def main():
    # โหลด CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # แสดง Header ของแบรนด์ RoomLab
    display_brand_header()
    
    # แสดง Sidebar
    render_sidebar()
    
    # ส่วนเนื้อหาหลัก
    container = st.container()
    
    with container:
        # แสดงสถานะการทำงาน
        render_progress_tracker()
        
        # แสดงเนื้อหาตามแท็บที่เลือก
        if st.session_state.active_tab == "create_design":
            # แสดงเนื้อหาตามขั้นตอน
            if st.session_state.design_step == 1:
                render_first_step()
            elif st.session_state.design_step == 4:
                render_design_results()
            elif st.session_state.design_step == 5:
                render_boq_page()
            else:
                # สำหรับขั้นตอนที่ยังไม่ได้พัฒนา (2 และ 3)
                st.info(f"กำลังอยู่ในขั้นตอนที่ {st.session_state.design_step} - อยู่ระหว่างการพัฒนา")
                # ปุ่มสำหรับการทดสอบ
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("◀ ย้อนกลับ", use_container_width=True):
                        set_design_step(st.session_state.design_step - 1)
                        st.experimental_rerun()
                with col2:
                    if st.button("ถัดไป ▶", use_container_width=True, type="primary"):
                        set_design_step(st.session_state.design_step + 1)
                        st.experimental_rerun()
        else:
            # หน้าอื่นๆ (ที่ยังไม่ได้พัฒนา)
            st.info(f"คุณอยู่ในหน้า '{st.session_state.active_tab}' - อยู่ระหว่างการพัฒนา")
            if st.button("กลับไปหน้าสร้างดีไซน์", type="primary"):
                change_tab("create_design")
                st.experimental_rerun()

if __name__ == "__main__":
    main()
