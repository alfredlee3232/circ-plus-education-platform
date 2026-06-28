import streamlit as st
import sqlite3
import pandas as pd
import re

try:
    from database import create_table, insert_registration
except ImportError:
    from database import create_table, save_registration as insert_registration


# =====================================================
# SETUP
# =====================================================

create_table()
def is_valid_email(email):
    email = email.strip()

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(pattern, email):
        return False

    if ".." in email:
        return False

    return True


def is_valid_australian_phone(phone):
    phone = phone.strip()

    # Remove spaces, brackets and dashes
    cleaned_phone = re.sub(r"[\s\-\(\)]", "", phone)

    # Convert +61 format to 0 format
    # Example: +61412345678 -> 0412345678
    if cleaned_phone.startswith("+61"):
        cleaned_phone = "0" + cleaned_phone[3:]

    # Australian mobile number: 04XXXXXXXX
    if re.match(r"^04\d{8}$", cleaned_phone):
        return True

    # Australian landline number: 02 / 03 / 07 / 08 + 8 digits
    if re.match(r"^0[2378]\d{8}$", cleaned_phone):
        return True

    return False


def clean_australian_phone(phone):
    phone = phone.strip()
    cleaned_phone = re.sub(r"[\s\-\(\)]", "", phone)

    if cleaned_phone.startswith("+61"):
        cleaned_phone = "0" + cleaned_phone[3:]

    return cleaned_phone

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
.stApp {
    background: linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
    color: #f8fafc;
}

h1, h2, h3 {
    color: #f8fafc !important;
    font-weight: 850 !important;
}

p, label, span {
    color: #e2e8f0 !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.25);
}

.hero {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.95), rgba(14, 165, 233, 0.9), rgba(16, 185, 129, 0.75));
    padding: 46px;
    border-radius: 30px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0px 18px 50px rgba(37, 99, 235, 0.35);
    border: 1px solid rgba(255,255,255,0.22);
}

.hero-title {
    font-size: 48px;
    font-weight: 900;
    margin-bottom: 10px;
    color: white !important;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 19px;
    color: #e0f2fe !important;
    line-height: 1.55;
}

.disclaimer {
    background: rgba(251, 191, 36, 0.12);
    padding: 18px;
    border-radius: 18px;
    border-left: 6px solid #f59e0b;
    color: #fde68a !important;
    margin-bottom: 18px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.18);
}

.disclaimer b {
    color: #facc15 !important;
}

.module-box {
    background: rgba(15, 23, 42, 0.82);
    border: 1px solid rgba(148, 163, 184, 0.25);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0px 12px 35px rgba(0,0,0,0.28);
    min-height: 180px;
    backdrop-filter: blur(12px);
    transition: 0.25s ease;
}

.module-box:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(56, 189, 248, 0.65);
    box-shadow: 0px 18px 45px rgba(56, 189, 248, 0.22);
}

.card-title {
    font-size: 23px;
    font-weight: 850;
    color: #ffffff !important;
    margin-bottom: 10px;
}

.card-text {
    font-size: 15.8px;
    color: #cbd5e1 !important;
    line-height: 1.55;
}

.detail-box {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.9));
    padding: 32px;
    border-radius: 28px;
    border: 1px solid rgba(56, 189, 248, 0.35);
    box-shadow: 0px 18px 45px rgba(0,0,0,0.32);
    margin-bottom: 24px;
}

.detail-title {
    font-size: 42px;
    font-weight: 900;
    color: #ffffff !important;
    margin-bottom: 8px;
}

.detail-subtitle {
    font-size: 17px;
    color: #bae6fd !important;
    line-height: 1.5;
}

[data-testid="stMetric"] {
    background: rgba(15, 23, 42, 0.86);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid rgba(56, 189, 248, 0.25);
    box-shadow: 0px 10px 28px rgba(0,0,0,0.24);
}

.stTextInput input, .stTextArea textarea {
    background-color: #111827 !important;
    color: #f8fafc !important;
    border-radius: 14px !important;
    border: 1px solid #334155 !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #111827 !important;
    color: #f8fafc !important;
    border-radius: 14px !important;
    border: 1px solid #334155 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    color: white !important;
    border: none;
    border-radius: 14px;
    padding: 0.65rem 1rem;
    font-weight: 750;
    transition: 0.2s ease;
    box-shadow: 0px 8px 22px rgba(37, 99, 235, 0.35);
}

.stButton > button:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #1d4ed8, #0891b2);
    box-shadow: 0px 12px 30px rgba(56, 189, 248, 0.35);
}

img {
    border-radius: 22px;
}

hr {
    border-color: rgba(148, 163, 184, 0.25);
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


def preferred_language_input(key):
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

    selected_language = st.selectbox(
        "Preferred Language",
        language_options,
        key=f"{key}_language_select"
    )

    if selected_language == "Other":
        custom_language = st.text_input(
            "Please type your preferred language",
            key=f"{key}_language_other",
            placeholder="Example: Greek, Italian, Punjabi, Nepali"
        )

        if custom_language.strip():
            return custom_language.strip()

        return ""

    return selected_language


def sport_interest_input(key):
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

    selected_sport = st.selectbox(
        "Sport / Fitness Interest",
        sport_options,
        key=f"{key}_sport_select"
    )

    if selected_sport == "Other":
        custom_sport = st.text_input(
            "Please type your sport or fitness interest",
            key=f"{key}_sport_other",
            placeholder="Example: Volleyball, cricket, dance, hiking"
        )

        if custom_sport.strip():
            return custom_sport.strip()

        return ""

    return selected_sport


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
    
    if st.button("🔒 Admin Dashboard", use_container_width=True):
        go_to("Admin Dashboard")

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
            <div class="hero-title">Fuel Knowledge. Train Smarter.</div>
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

    # These are outside the form so "Other" will show the typing box immediately
    final_language = preferred_language_input("individual")
    sport = sport_interest_input("individual")

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

            elif not is_valid_email(email):
                st.error("Invalid email address. Please enter a valid email. Example: name@example.com")

            elif phone and not is_valid_australian_phone(phone):
                st.error("Invalid Australian phone number. Please enter a valid number. Example: 0412345678 or +61412345678")

            elif not final_language:
                st.error("Please type your preferred language because you selected Other.")

            elif not sport:
                st.error("Please type your sport / fitness interest because you selected Other.")

            elif not consent:
                st.error("Please tick the consent box before submitting.")

            else:
                phone = clean_australian_phone(phone)

                insert_registration(
                    full_name=name.strip(),
                    email=email.strip().lower(),
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

    # These are outside the form so "Other" will show the typing box immediately
    sport_type = sport_interest_input("organisation")
    org_language = preferred_language_input("organisation")

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

            elif not is_valid_email(org_email):
                st.error("Invalid email address. Please enter a valid organisation email. Example: club@example.com")

            elif org_phone and not is_valid_australian_phone(org_phone):
                st.error("Invalid Australian phone number. Please enter a valid number. Example: 0412345678 or +61412345678")

            elif not sport_type:
                st.error("Please type the sport / community type because you selected Other.")

            elif not org_language:
                st.error("Please type the preferred language because you selected Other.")

            elif not consent:
                st.error("Please tick the consent box before submitting.")

            else:
                org_phone = clean_australian_phone(org_phone)

                insert_registration(
                    full_name=contact_person.strip(),
                    email=org_email.strip().lower(),
                    phone=org_phone,
                    preferred_language=org_language,
                    sport_interest=sport_type,
                    organisation_name=organisation_name.strip(),
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

elif st.session_state.page == "Admin Dashboard":
    st.header("🔒 Admin Dashboard")
    st.write("This page is password protected and only for viewing registration records.")

    try:
        admin_password = st.secrets["ADMIN_PASSWORD"]
    except Exception:
        st.error("Admin password is not configured yet.")
        st.info("Please add ADMIN_PASSWORD in Streamlit Secrets.")
        st.stop()

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        password_input = st.text_input("Enter admin password", type="password")

        if st.button("Login"):
            if password_input == admin_password:
                st.session_state.admin_logged_in = True
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Incorrect password.")

        st.stop()

    if st.button("Log out"):
        st.session_state.admin_logged_in = False
        st.rerun()

    st.divider()

    conn = sqlite3.connect("registrations.db")

    try:
        df = pd.read_sql_query(
            "SELECT * FROM registrations ORDER BY created_at DESC",
            conn
        )
    except Exception:
        df = pd.DataFrame()

    conn.close()

    st.subheader("Registration Overview")

    if df.empty:
        st.warning("No registrations found yet.")
    else:
        total_records = len(df)

        if "organisation_name" in df.columns:
            organisation_records = df["organisation_name"].fillna("").astype(str).str.strip().ne("").sum()
        else:
            organisation_records = 0

        individual_records = total_records - organisation_records

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Registrations", total_records)
        c2.metric("Individual Registrations", individual_records)
        c3.metric("Organisation Leads", organisation_records)

        st.subheader("Registration Records")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Registrations as CSV",
            data=csv,
            file_name="circ_plus_registrations.csv",
            mime="text/csv"
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
# force redeploy admin dashboard
