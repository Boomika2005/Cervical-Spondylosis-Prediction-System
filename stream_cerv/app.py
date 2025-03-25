import streamlit as st
import numpy as np
import joblib
import sqlite3

# Load trained model and scaler
svm_model = joblib.load("svm_model.pkl")
scaler = joblib.load("scaler.pkl")

# Initialize database connection
def create_database():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            gender TEXT,
            pain_score INTEGER,
            neck_flexibility REAL,
            neck_speed REAL,
            motion_range REAL,
            frequency_combined REAL,
            predicted_severity TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to save patient data into the database
def save_patient_data(age, gender, pain_score, neck_flexibility, neck_speed,
                      motion_range, frequency_combined, predicted_severity):
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patient_records 
        (age, gender, pain_score, neck_flexibility, neck_speed, motion_range, frequency_combined, predicted_severity) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (age, gender, pain_score, neck_flexibility, neck_speed, motion_range,
          frequency_combined, predicted_severity))
    conn.commit()
    conn.close()

# Function to fetch all patient records
def fetch_patient_data():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient_records")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Create the database (only needed once)
create_database()

# Set Streamlit page configuration
st.set_page_config(page_title="Cervical Spondylosis Prediction", page_icon="🩺", layout="wide")

# Sidebar Navigation
st.sidebar.title("🩺 Cervical Health App")
page = st.sidebar.radio("Navigation", ["Home", "Predict Severity", "Prevention methods"])

# Home Page

if page == "Home":
    # Set Background Image (Paste your own link)
    background_image_url = "https://t3.ftcdn.net/jpg/02/39/78/14/360_F_239781452_Tul0c1wT76KpBX2XT2ff7phMZqDKJWQd.jpg"
   
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("{background_image_url}");
                background-size: cover;
                background-position: center;
                
                
            }}
            .stApp * {{
                color: black !important; /* Set all text color to white */
            }}
            .info-box {{
                background-color: rgba(255, 255, 255, 0.85);
                padding: 20px;
                border-radius: 10px;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Welcome to Cervical Spondylosis Severity Prediction")
    st.write(
        "This application helps assess the severity of **cervical spondylosis** using advanced **machine learning** models. "
        "It provides personalized **prevention methods** and **lifestyle recommendations** to help manage symptoms effectively."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # About Cervical Spondylosis
    st.subheader("🔎 What is Cervical Spondylosis?")
    st.write(
        "Cervical spondylosis is an age-related condition that affects the neck’s **bones, discs, and joints**. "
        "It often results from **wear and tear** of cartilage and bones. Symptoms may include **neck pain, stiffness, headaches, and dizziness**."
    )

    st.subheader("⚙️ How This Application Works?")
    st.write("""
    1️⃣ **Enter patient details** in the **'Predict Severity'** section.  
    2️⃣ **Click Predict** to receive the severity level (**Mild, Moderate, Severe**).  
    3️⃣ **Explore prevention methods** to improve neck health and reduce discomfort.  
    """)


    # Space for adding an image (if needed)
   


# Prediction Page
elif page == "Predict Severity":
    st.title("📊 Cervical Spondylosis Severity Prediction")

    # Form layout
    with st.form(key="prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.slider("📅 Age", 18, 90, 30)
            gender = st.radio("⚤ Gender", ["Male", "Female"])
            pain_score = st.slider("😖 Pain Intensity (1-10)", 1, 10, 5)

        with col2:
            neck_flexibility = st.slider("🦴 Neck Flexibility (Low = 10, High = 90)", 10, 90, 45)
            neck_speed = st.slider("💨 Neck Speed (Slow = 1, Fast = 50)", 1, 50, 20)
            motion_range = st.slider("🔄 Motion Range (Limited = 10, Full = 90)", 10, 90, 50)

        frequency_combined = st.slider("📊 Frequency of Neck Sensations (Low = 0.1, High = 3.0)", 0.1, 3.0, 1.2)

        # Convert categorical values
        gender_numeric = 1 if gender == "Male" else 0

        # Prepare input features
        features = np.array([[age, gender_numeric, pain_score, neck_flexibility, 
                            neck_speed, motion_range, frequency_combined]])

        # Submit button
        submit_button = st.form_submit_button(label="🔍 Predict Severity")

    if submit_button:
        features_scaled = scaler.transform(features)
        prediction = svm_model.predict(features_scaled)[0]
        severity_levels = {0: "🟢 Mild", 1: "🟡 Moderate", 2: "🔴 Severe"}
        predicted_severity = severity_levels[prediction]

        # Save patient details in the database
        save_patient_data(age, gender, pain_score, neck_flexibility, neck_speed,
                          motion_range, frequency_combined, predicted_severity)

        st.success(f"Predicted Severity: {predicted_severity}")

# View Records Page
elif page == "Prevention methods":
    # Prevention Methods Section
    st.sidebar.subheader("🛡️ Get Prevention Methods")

    # Allow user to select severity level
    severity_option = st.sidebar.radio("Select Severity Level:", ["Mild", "Moderate", "Severe"])

    # Dictionary storing prevention and lifestyle changes for each severity level
    prevention_methods = {
        "Mild": {
            "Prevention Measures": [
                "✅ Maintain a proper sitting posture with back support.",
                "✅ Take frequent breaks from screen time and desk work.",
                "✅ Perform gentle neck stretches daily.",
                "✅ Sleep on a supportive pillow and a firm mattress."
            ],
            "Lifestyle Changes": [
                "🌱 Stay physically active with light exercises like yoga or walking.",
                "🌱 Avoid carrying heavy backpacks or bags on one shoulder.",
                "🌱 Stay hydrated and maintain a balanced diet.",
                "🌱 Reduce prolonged use of mobile phones with a bent neck."
            ]
        },
        "Moderate": {
            "Prevention Measures": [
                "✅ Apply heat or cold packs to relieve pain.",
                "✅ Engage in low-impact exercises like swimming or pilates.",
                "✅ Use ergonomic furniture for work and daily activities.",
                "✅ Avoid sudden neck movements and heavy lifting."
            ],
            "Lifestyle Changes": [
                "🌱 Maintain a healthy weight to reduce stress on the spine.",
                "🌱 Consult a physiotherapist for guided exercises.",
                "🌱 Use a cervical collar occasionally for support if needed.",
                "🌱 Reduce stress through meditation or breathing exercises."
            ]
        },
        "Severe": {
            "Prevention Measures": [
                "✅ Seek medical consultation for personalized treatment.",
                "✅ Consider physical therapy or chiropractic care.",
                "✅ Avoid high-impact activities that strain the neck.",
                "✅ Follow prescribed medications or treatments by a doctor."
            ],
            "Lifestyle Changes": [
                "🌱 Prioritize rest and avoid over-exertion.",
                "🌱 Use neck braces only when recommended by a specialist.",
                "🌱 Avoid prolonged head-forward posture (e.g., looking down at phone).",
                "🌱 Ensure adequate calcium and vitamin D intake for bone health."
            ]
        }
    }

    # Display the selected prevention methods and lifestyle changes
    st.subheader(f"🩹 Prevention Methods for {severity_option} Severity")
    st.write("### Prevention Measures:")
    for measure in prevention_methods[severity_option]["Prevention Measures"]:
        st.write(measure)

    st.write("### Lifestyle Changes:")
    for change in prevention_methods[severity_option]["Lifestyle Changes"]:
        st.write(change)

