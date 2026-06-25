import streamlit as st
import sqlite3
import pandas as pd

try:
    from database import create_table, insert_registration
except ImportError:
    from database import create_table, save_registration as insert_registration


# =====================================================
# SETUP
# =====================================================

create_table()

st.set_page_config(
    page_title="CIRC+ Education Platform",
    page_icon="🏃",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "Home"


def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()


# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* =========================
   GLOBAL PREMIUM STYLE
========================= */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(59, 130, 246, 0.35), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(34, 197, 94, 0.24), transparent 25%),
        radial-gradient(circle at 50% 90%, rgba(168, 85, 247, 0.18), transparent 30%),
        linear-gradient(135deg, #020617 0%, #08111f 45%, #020617 100%);
    color: #f8fafc;
}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 4rem;
    max-width: 1280px;
}

/* =========================
   TEXT
========================= */

h1, h2, h3 {
    color: #ffffff !important;
    font-weight: 900 !important;
    letter-spacing: -0.8px;
}

h1 {
    font-size: 2.7rem !important;
}

h2 {
    margin-top: 1.2rem;
}

p, label, span, div {
    color: #e2e8f0;
}

/* =========================
   SIDEBAR
========================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(2, 6, 23, 0.98), rgba(15, 23, 42, 0.96)),
        radial-gradient(circle at top, rgba(37, 99, 235, 0.28), transparent 40%);
    border-right: 1px solid rgba(56, 189, 248, 0.25);
    box-shadow: 12px 0px 45px rgba(0,0,0,0.38);
}

section[data-testid="stSidebar"] img {
    border-radius: 18px;
    box-shadow: none;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: #f8fafc !important;
}

/* =========================
   HERO SECTION
========================= */

.hero {
    background:
        linear-gradient(135deg, rgba(15, 23, 42, 0.35), rgba(37, 99, 235, 0.72), rgba(6, 182, 212, 0.58)),
        url("https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg");
    background-size: cover;
    background-position: center;
    padding: 64px 54px;
    border-radius: 38px;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.25);
    box-shadow:
        0px 28px 80px rgba(37, 99, 235, 0.35),
        inset 0px 1px 0px rgba(255,255,255,0.22);
}

.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        linear-gradient(90deg, rgba(2, 6, 23, 0.72), rgba(2, 6, 23, 0.12));
    z-index: 0;
}

.hero::after {
    content: "";
    position: absolute;
    top: -100px;
    right: -80px;
    width: 280px;
    height: 280px;
    background: rgba(255,255,255,0.14);
    border-radius: 50%;
    filter: blur(2px);
}

.hero-title,
.hero-subtitle {
    position: relative;
    z-index: 1;
}

.hero-title {
    font-size: 62px;
    font-weight: 950;
    margin-bottom: 16px;
    color: white !important;
    letter-spacing: -2px;
    line-height: 1.02;
    text-shadow: 0px 5px 22px rgba(0,0,0,0.35);
    word-break: keep-all !important;
    overflow-wrap: normal !important;
    hyphens: none !important;
}

.no-break-word {
    white-space: nowrap !important;
    display: inline-block;
}

.hero-subtitle {
    font-size: 21px;
    color: #e0f2fe !important;
    line-height: 1.65;
    max-width: 820px;
    text-shadow: 0px 2px 12px rgba(0,0,0,0.28);
}

/* =========================
   DISCLAIMER
========================= */

.disclaimer {
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.15), rgba(249, 115, 22, 0.10));
    padding: 20px 22px;
    border-radius: 22px;
    border: 1px solid rgba(251, 191, 36, 0.35);
    border-left: 7px solid #f59e0b;
    color: #fde68a !important;
    margin-bottom: 24px;
    box-shadow: 0px 16px 38px rgba(0,0,0,0.25);
    backdrop-filter: blur(14px);
}

.disclaimer b {
    color: #facc15 !important;
}

/* =========================
   GLASS MODULE CARDS
========================= */

.module-box {
    background:
        linear-gradient(180deg, rgba(15, 23, 42, 0.88), rgba(30, 41, 59, 0.66));
    border: 1px solid rgba(148, 163, 184, 0.26);
    border-radius: 30px;
    padding: 28px;
    box-shadow:
        0px 20px 45px rgba(0,0,0,0.36),
        inset 0px 1px 0px rgba(255,255,255,0.08);
    min-height: 200px;
    backdrop-filter: blur(18px);
    transition: all 0.26s ease;
    position: relative;
    overflow: hidden;
}

.module-box::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: linear-gradient(90deg, #2563eb, #06b6d4, #22c55e, #a855f7);
}

.module-box::after {
    content: "";
    position: absolute;
    top: -70px;
    right: -70px;
    width: 150px;
    height: 150px;
    background: rgba(56, 189, 248, 0.10);
    border-radius: 50%;
    filter: blur(3px);
}

.module-box:hover {
    transform: translateY(-9px) scale(1.015);
    border: 1px solid rgba(56, 189, 248, 0.75);
    box-shadow:
        0px 28px 70px rgba(56, 189, 248, 0.25),
        inset 0px 1px 0px rgba(255,255,255,0.14);
}

.card-title {
    font-size: 25px;
    font-weight: 900;
    color: #ffffff !important;
    margin-bottom: 13px;
    letter-spacing: -0.3px;
}

.card-text {
    font-size: 16px;
    color: #cbd5e1 !important;
    line-height: 1.7;
}

/* =========================
   DETAIL PAGE
========================= */

.detail-box {
    background:
        radial-gradient(circle at top left, rgba(37, 99, 235, 0.33), transparent 42%),
        linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(30, 41, 59, 0.9));
    padding: 40px;
    border-radius: 34px;
    border: 1px solid rgba(56, 189, 248, 0.42);
    box-shadow:
        0px 24px 68px rgba(0,0,0,0.42),
        inset 0px 1px 0px rgba(255,255,255,0.09);
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}

.detail-box::after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -90px;
    bottom: -110px;
    background: rgba(16, 185, 129, 0.13);
    border-radius: 50%;
}

.detail-title {
    font-size: 48px;
    font-weight: 950;
    color: #ffffff !important;
    margin-bottom: 12px;
    letter-spacing: -1.3px;
}

.detail-subtitle {
    font-size: 18px;
    color: #bae6fd !important;
    line-height: 1.65;
}

/* =========================
   METRICS
========================= */

/* =========================
   METRICS - CLEANER SIZE
========================= */

[data-testid="stMetric"] {
    background:
        linear-gradient(180deg, rgba(15, 23, 42, 0.88), rgba(30, 41, 59, 0.72));
    padding: 18px 20px;
    border-radius: 22px;
    border: 1px solid rgba(56, 189, 248, 0.22);
    box-shadow:
        0px 12px 30px rgba(0,0,0,0.25),
        inset 0px 1px 0px rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    min-height: 120px;
}

[data-testid="stMetricLabel"] {
    color: #93c5fd !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 850 !important;
    font-size: 30px !important;
    line-height: 1.1 !important;
    white-space: normal !important;
}

/* =========================
   FORMS
========================= */

.stTextInput input,
.stTextArea textarea {
    background: rgba(15, 23, 42, 0.94) !important;
    color: #f8fafc !important;
    border-radius: 18px !important;
    border: 1px solid rgba(148, 163, 184, 0.38) !important;
    box-shadow: inset 0px 1px 0px rgba(255,255,255,0.06);
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border: 1px solid #38bdf8 !important;
    box-shadow: 0px 0px 0px 3px rgba(56,189,248,0.20) !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: rgba(15, 23, 42, 0.94) !important;
    color: #f8fafc !important;
    border-radius: 18px !important;
    border: 1px solid rgba(148, 163, 184, 0.38) !important;
}

.stCheckbox label {
    color: #e2e8f0 !important;
}

/* =========================
   BUTTONS
========================= */

/* =========================
   BUTTONS - MORE PREMIUM LESS BRIGHT
========================= */

.stButton > button {
    background: linear-gradient(135deg, #1e40af, #0f766e);
    color: white !important;
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 16px;
    padding: 0.72rem 1.05rem;
    font-weight: 800;
    transition: all 0.22s ease;
    box-shadow: 0px 8px 22px rgba(15, 23, 42, 0.45);
}

.stButton > button:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #1d4ed8, #0f766e);
    border: 1px solid rgba(56, 189, 248, 0.35);
    box-shadow: 0px 12px 30px rgba(15, 23, 42, 0.55);
}

.stFormSubmitButton > button {
    background: linear-gradient(135deg, #166534, #0f766e) !important;
    color: white !important;
    border-radius: 16px !important;
    font-weight: 850 !important;
    border: 1px solid rgba(148, 163, 184, 0.25) !important;
    padding: 0.75rem 1.1rem !important;
    box-shadow: 0px 10px 24px rgba(15, 23, 42, 0.45);
}

.stFormSubmitButton > button:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #15803d, #0f766e) !important;
    box-shadow: 0px 14px 32px rgba(15, 23, 42, 0.55);
}

/* =========================
   IMAGES
========================= */

img {
    border-radius: 30px;
    box-shadow:
        0px 18px 44px rgba(0,0,0,0.32),
        inset 0px 1px 0px rgba(255,255,255,0.08);
}

/* =========================
   ALERTS / INFO BOXES
========================= */

div[data-testid="stAlert"] {
    border-radius: 22px;
    border: 1px solid rgba(56, 189, 248, 0.28);
    box-shadow: 0px 14px 34px rgba(0,0,0,0.25);
}

/* =========================
   DIVIDERS / CAPTIONS
========================= */

hr {
    border-color: rgba(148, 163, 184, 0.22);
    margin-top: 2.2rem;
    margin-bottom: 2.2rem;
}

.stCaption,
caption {
    color: #94a3b8 !important;
}

/* =========================
   MOBILE RESPONSIVE
========================= */

@media (max-width: 768px) {
    .hero-title {
        font-size: 40px;
    }

    .hero {
        padding: 34px;
    }

    .detail-title {
        font-size: 34px;
    }

    .module-box {
        min-height: auto;
    }
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_source():
    try:
        return st.query_params.get("source", "Website")
    except Exception:
        return "Website"


def load_counts():
    conn = sqlite3.connect("registrations.db")

    try:
        df = pd.read_sql_query("SELECT * FROM registrations", conn)
        total = len(df)

        if "organisation_name" in df.columns:
            org_count = df["organisation_name"].fillna("").astype(str).str.strip().ne("").sum()
        else:
            org_count = 0

    except Exception:
        total = 0
        org_count = 0

    conn.close()
    return total, org_count


def language_selector(key):
    language_options = [
        "English",
        "Mandarin Chinese",
        "Cantonese",
        "Malay",
        "Hindi",
        "Japanese",
        "Korean",
        "Vietnamese",
        "Thai",
        "Indonesian",
        "Spanish",
        "French",
        "German",
        "Arabic",
        "Tamil",
        "Other"
    ]

    selected = st.selectbox(
        "Preferred Language",
        language_options,
        key=f"{key}_language_select"
    )

    if selected == "Other":
        typed_language = st.text_input(
            "Please type your preferred language",
            key=f"{key}_language_other",
            placeholder="Example: Greek, Italian, Punjabi, Nepali"
        )
        return typed_language.strip()

    return selected


def sport_selector(key):
    sport_options = [
        "Gym / Fitness",
        "Running",
        "Cycling",
        "Swimming",
        "Football / Soccer",
        "Basketball",
        "Tennis",
        "Badminton",
        "Martial Arts",
        "Yoga / Pilates",
        "Bodybuilding",
        "General Active Lifestyle",
        "Sports Club / Organisation",
        "Other"
    ]

    selected = st.selectbox(
        "Sport / Fitness Interest",
        sport_options,
        key=f"{key}_sport_select"
    )

    if selected == "Other":
        typed_sport = st.text_input(
            "Please type your sport or fitness interest",
            key=f"{key}_sport_other",
            placeholder="Example: Volleyball, cricket, dance, hiking"
        )
        return typed_sport.strip()

    return selected


def module_card(icon, title, text, button_label, page_name, key):
    st.markdown(f"""
    <div class="module-box">
        <div class="card-title">{icon} {title}</div>
        <div class="card-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(button_label, key=key, use_container_width=True):
        go_to(page_name)


source = get_source()
total_registrations, organisation_count = load_counts()


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.image("usana_logo.jpg", width=150)
    st.title("CIRC+ Platform")

    if st.button("🏠 Home", use_container_width=True):
        go_to("Home")

    if st.button("📚 Education Modules", use_container_width=True):
        go_to("Education")

    if st.button("📝 Individual Registration", use_container_width=True):
        go_to("Individual Registration")

    if st.button("🏟️ Sports Organisation Form", use_container_width=True):
        go_to("Organisation Registration")

    if st.button("🤖 AI & Gamification Plan", use_container_width=True):
        go_to("AI Gamification")

    st.divider()
    st.caption("Developed by Hoe Weng Lee")
    st.caption("ATW306 Work Integrated Learning")


# =====================================================
# HEADER
# =====================================================

col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.image("usana_logo.jpg", width=120)

with col_title:
    st.title("CIRC+ Sports Nutrition Education Platform")
    st.caption(
        "Professional digital platform for sports nutrition education, nitric oxide awareness, "
        "seminar registration and sports community engagement."
    )


# =====================================================
# HOME PAGE
# =====================================================

if st.session_state.page == "Home":
    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("""
        <div class="hero">
            <div class="hero-title">  CIRC+ Digital<br>
               Education Platform</div>
            <div class="hero-subtitle"> 
                A sports-tech education platform for CIRC+, nitric oxide awareness,
                multilingual learning, seminar registration, AI engagement and
                data-driven community outreach.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer">
            <b>Education only:</b> This website provides general sports nutrition education only.
            It does not provide medical advice, diagnosis or treatment. Users should consult a qualified
            health professional before using supplements, especially if they have a medical condition
            or take medication.
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.image("circ_pack.webp", use_container_width=True)

    st.header("Platform Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Registrations", total_registrations)
    c2.metric("Organisation Leads", organisation_count)
    c3.metric("Education Modules", "6")
    c4.metric("Project Stage", "Stage 1")

    st.caption(f"Traffic source detected: {source}")

    st.divider()

    st.header("Who This Platform Supports")

    p1, p2, p3 = st.columns(3)

    with p1:
        st.image(
            "https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg",
            caption="Sports communities",
            use_container_width=True
        )
        st.subheader("Sports Communities")
        st.write("Designed for clubs, gyms, university sport groups and active lifestyle communities.")

    with p2:
        st.image(
            "https://images.pexels.com/photos/3764011/pexels-photo-3764011.jpeg",
            caption="Seminar attendees",
            use_container_width=True
        )
        st.subheader("Seminar Attendees")
        st.write("Supports users who want structured education before attending a seminar.")

    with p3:
        st.image(
            "https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg",
            caption="Active individuals",
            use_container_width=True
        )
        st.subheader("Active Individuals")
        st.write("Helps users learn about hydration, nutrition, recovery and nitric oxide awareness.")

    st.divider()

    st.header("Explore Education Modules")
    st.write("Click a module below to open a detailed education page.")

    m1, m2, m3 = st.columns(3)

    with m1:
        module_card(
            "🩸",
            "Nitric Oxide",
            "Understand general nitric oxide awareness and its role in active lifestyle education.",
            "Learn More",
            "Nitric Oxide",
            "home_no"
        )

    with m2:
        module_card(
            "💧",
            "Hydration",
            "Learn why hydration awareness matters for sport, training and recovery.",
            "Learn More",
            "Hydration",
            "home_hydration"
        )

    with m3:
        module_card(
            "🏃",
            "Exercise Performance",
            "Explore how nutrition, routine and recovery relate to physical activity.",
            "Learn More",
            "Performance",
            "home_performance"
        )

    m4, m5, m6 = st.columns(3)

    with m4:
        module_card(
            "❤️",
            "Circulation",
            "General education about circulation, oxygen delivery and active living.",
            "Learn More",
            "Circulation",
            "home_circulation"
        )

    with m5:
        module_card(
            "🔄",
            "Recovery",
            "Understand basic recovery concepts after exercise or training.",
            "Learn More",
            "Recovery",
            "home_recovery"
        )

    with m6:
        module_card(
            "🌏",
            "Multilingual Learning",
            "Supports users from different cultural and language backgrounds.",
            "Learn More",
            "Multilingual",
            "home_multilingual"
        )


# =====================================================
# EDUCATION PAGE
# =====================================================

elif st.session_state.page == "Education":
    st.header("Education Modules")
    st.write("Select a module below to open a detailed page.")

    col1, col2, col3 = st.columns(3)

    with col1:
        module_card(
            "🩸",
            "Nitric Oxide",
            "General education about nitric oxide awareness.",
            "Open Module",
            "Nitric Oxide",
            "edu_no"
        )

        module_card(
            "❤️",
            "Circulation",
            "Circulation and active lifestyle learning.",
            "Open Module",
            "Circulation",
            "edu_circulation"
        )

    with col2:
        module_card(
            "💧",
            "Hydration",
            "Hydration awareness for active communities.",
            "Open Module",
            "Hydration",
            "edu_hydration"
        )

        module_card(
            "🔄",
            "Recovery",
            "Basic recovery concepts after activity.",
            "Open Module",
            "Recovery",
            "edu_recovery"
        )

    with col3:
        module_card(
            "🏃",
            "Performance",
            "Nutrition, recovery and performance education.",
            "Open Module",
            "Performance",
            "edu_performance"
        )

        module_card(
            "🌏",
            "Multilingual",
            "Language access and inclusive education.",
            "Open Module",
            "Multilingual",
            "edu_multilingual"
        )


# =====================================================
# MODULE DETAIL PAGES
# =====================================================

elif st.session_state.page in [
    "Nitric Oxide",
    "Hydration",
    "Performance",
    "Circulation",
    "Recovery",
    "Multilingual"
]:
    module = st.session_state.page

    content = {
        "Nitric Oxide": {
            "title": "🩸 Nitric Oxide Education",
            "image": "https://images.pexels.com/photos/4167544/pexels-photo-4167544.jpeg",
            "body": """
Nitric oxide is commonly discussed in sport and wellness education because it is connected with circulation and oxygen delivery concepts.

This page provides general education only and does not claim to diagnose, treat or cure any health condition.

Users can learn basic concepts before registering for a seminar or asking further education-based questions.
"""
        },
        "Hydration": {
            "title": "💧 Hydration Education",
            "image": "https://images.pexels.com/photos/416528/pexels-photo-416528.jpeg",
            "body": """
Hydration is important for active individuals because fluid balance is related to training comfort, recovery awareness and general wellbeing.

This module explains hydration in a simple way for sport communities, gym members and seminar attendees.
"""
        },
        "Performance": {
            "title": "🏃 Exercise Performance Education",
            "image": "https://images.pexels.com/photos/3757954/pexels-photo-3757954.jpeg",
            "body": """
Exercise performance is affected by many lifestyle factors, including nutrition, hydration, recovery and consistency.

This module introduces these concepts in an education-first way before users attend a seminar or complete a quiz.
"""
        },
        "Circulation": {
            "title": "❤️ Circulation Support Education",
            "image": "https://images.pexels.com/photos/3757376/pexels-photo-3757376.jpeg",
            "body": """
Circulation education helps users understand basic concepts related to blood flow, oxygen delivery and active living.

This platform avoids medical claims and focuses on general wellness and sports nutrition education.
"""
        },
        "Recovery": {
            "title": "🔄 Recovery Education",
            "image": "https://images.pexels.com/photos/1552106/pexels-photo-1552106.jpeg",
            "body": """
Recovery is important after physical activity. This module introduces basic recovery concepts such as rest, hydration, routine and general nutrition awareness.

The goal is to support learning, not to provide medical advice.
"""
        },
        "Multilingual": {
            "title": "🌏 Multilingual Learning",
            "image": "https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg",
            "body": """
This project supports multilingual learning because sports communities may include people from many language backgrounds.

Users can select a common language or choose Other and type their preferred language in the registration form.
"""
        }
    }

    selected = content[module]

    if st.button("← Back to Home"):
        go_to("Home")

    st.markdown(f"""
    <div class="detail-box">
        <div class="detail-title">{selected['title']}</div>
        <div class="detail-subtitle">
            Education-first learning module for sports nutrition and active lifestyle awareness.
        </div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1.2])

    with left:
        st.image(selected["image"], use_container_width=True)

    with right:
        st.markdown(selected["body"])
        st.info(
            "Interested in learning more? Register for a seminar or submit an organisation interest form."
        )

        b1, b2 = st.columns(2)

        with b1:
            if st.button("Register as Individual", use_container_width=True):
                go_to("Individual Registration")

        with b2:
            if st.button("Register Organisation Interest", use_container_width=True):
                go_to("Organisation Registration")


# =====================================================
# INDIVIDUAL REGISTRATION
# =====================================================

elif st.session_state.page == "Individual Registration":
    st.header("Register Interest for Sports Nutrition Seminar")
    st.write("Please complete the form below.")

    final_language = language_selector("individual")
    sport = sport_selector("individual")

    with st.form("individual_registration_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        notes = st.text_area("What would you like to learn about?")

        consent = st.checkbox(
            "I agree to be contacted about this educational seminar and related learning information."
        )

        submitted = st.form_submit_button("Submit Individual Registration")

        if submitted:
            if not name or not email:
                st.error("Please enter your name and email.")
            elif not final_language:
                st.error("Please type your preferred language because you selected Other.")
            elif not sport:
                st.error("Please type your sport / fitness interest because you selected Other.")
            elif not consent:
                st.error("Please tick the consent box before submitting.")
            else:
                insert_registration(
                    full_name=name,
                    email=email,
                    phone=phone,
                    preferred_language=final_language,
                    sport_interest=sport,
                    organisation_name="",
                    contact_role="Individual",
                    seminar_interest="Individual seminar interest",
                    source=source,
                    notes=notes,
                    consent=consent
                )

                st.success("Thank you! Your registration has been saved successfully.")


# =====================================================
# ORGANISATION REGISTRATION
# =====================================================

elif st.session_state.page == "Organisation Registration":
    st.header("Sports Organisation / Club Interest Form")

    st.write(
        "This form is for sports clubs, gyms, university sport groups or community organisations "
        "interested in free sports nutrition and nitric oxide education."
    )

    sport_type = sport_selector("organisation")
    org_language = language_selector("organisation")

    with st.form("organisation_interest_form"):
        organisation_name = st.text_input("Organisation / Club Name")
        contact_person = st.text_input("Contact Person")
        contact_role = st.text_input("Role / Position")
        org_email = st.text_input("Contact Email")
        org_phone = st.text_input("Contact Phone")

        seminar_interest = st.selectbox(
            "Type of Interest",
            [
                "Free education seminar",
                "Online information session",
                "Share website with members",
                "Need more information first"
            ]
        )

        notes = st.text_area("Notes / Questions from Organisation")

        consent = st.checkbox(
            "I agree to be contacted about this educational project.",
            key="org_consent"
        )

        submitted_org = st.form_submit_button("Submit Organisation Interest")

        if submitted_org:
            if not organisation_name or not contact_person or not org_email:
                st.error("Please enter organisation name, contact person and email.")
            elif not sport_type:
                st.error("Please type the sport / community type because you selected Other.")
            elif not org_language:
                st.error("Please type the preferred language because you selected Other.")
            elif not consent:
                st.error("Please tick the consent box before submitting.")
            else:
                insert_registration(
                    full_name=contact_person,
                    email=org_email,
                    phone=org_phone,
                    preferred_language=org_language,
                    sport_interest=sport_type,
                    organisation_name=organisation_name,
                    contact_role=contact_role,
                    seminar_interest=seminar_interest,
                    source=source,
                    notes=notes,
                    consent=consent
                )

                st.success("Thank you! The organisation interest form has been saved.")


# =====================================================
# AI AND GAMIFICATION PAGE
# =====================================================

elif st.session_state.page == "AI Gamification":
    st.header("Future AI Chatbot and Gamification Plan")

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("""
### Planned AI Chatbot

The future chatbot will support education-based questions about:

- Sports nutrition
- Hydration
- Nitric oxide awareness
- Seminar information
- Language support

### Planned Gamified Quiz

The quiz will help users check basic sports nutrition knowledge and receive simple educational feedback.
""")

        st.subheader("Example Quiz")

        answer = st.radio(
            "Which factor is important for active lifestyle support?",
            [
                "Hydration",
                "Skipping all meals",
                "Ignoring recovery",
                "Never exercising"
            ]
        )

        if st.button("Check Answer"):
            if answer == "Hydration":
                st.success("Correct. Hydration is important for active lifestyle support.")
            else:
                st.warning("Try again. Hydration is one important factor for active lifestyle support.")

    with col2:
        st.image(
            "https://images.pexels.com/photos/8438923/pexels-photo-8438923.jpeg",
            caption="Future AI and digital engagement",
            use_container_width=True
        )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "CIRC+ Education Platform | Developed by Hoe Weng Lee | "
    "Bachelor of Software Engineering (Artificial Intelligence) | "
    "ATW306 Work Integrated Learning"
)