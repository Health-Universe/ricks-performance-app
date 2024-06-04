import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize in-memory data
if 'data' not in st.session_state:
    st.session_state['data'] = {
        'doctors': {
            'Dr. Smith': [
                {"Patient": "John Doe", "Blood Pressure": "120/80", "Cholesterol": 180, "HA1C": 6.0},
                {"Patient": "Jane Roe", "Blood Pressure": "130/85", "Cholesterol": 190, "HA1C": 6.5},
                {"Patient": "Alice Johnson", "Blood Pressure": "140/90", "Cholesterol": 200, "HA1C": 7.0}
            ],
            'Dr. Brown': [
                {"Patient": "Bob Smith", "Blood Pressure": "115/75", "Cholesterol": 170, "HA1C": 5.8},
                {"Patient": "Charlie Black", "Blood Pressure": "135/88", "Cholesterol": 195, "HA1C": 6.3},
                {"Patient": "Diane White", "Blood Pressure": "145/92", "Cholesterol": 210, "HA1C": 7.2}
            ],
            'Dr. Johnson': [
                {"Patient": "Edward Green", "Blood Pressure": "118/78", "Cholesterol": 175, "HA1C": 5.9},
                {"Patient": "Fiona Blue", "Blood Pressure": "138/89", "Cholesterol": 185, "HA1C": 6.4},
                {"Patient": "George Yellow", "Blood Pressure": "148/94", "Cholesterol": 205, "HA1C": 7.3}
            ]
        }
    }

# Function to calculate performance metrics
def calculate_metrics(patients):
    total_patients = len(patients)
    bp_goal = sum(1 for p in patients if int(p['Blood Pressure'].split('/')[0]) < 130 and int(p['Blood Pressure'].split('/')[1]) < 80)
    cholesterol_goal = sum(1 for p in patients if p['Cholesterol'] < 200)
    ha1c_goal = sum(1 for p in patients if p['HA1C'] < 7.0)
    
    return {
        "Total Patients": total_patients,
        "BP Goal Achieved": f"{bp_goal} ({bp_goal / total_patients * 100:.1f}%)",
        "Cholesterol Goal Achieved": f"{cholesterol_goal} ({cholesterol_goal / total_patients * 100:.1f}%)",
        "HA1C Goal Achieved": f"{ha1c_goal} ({ha1c_goal / total_patients * 100:.1f}%)"
    }

# App layout
st.title("Physician Performance Metrics")
st.write("""
    This app measures physician performance metrics based on the goals for blood pressure, cholesterol, and HA1C levels. 
    The metrics are calculated for each doctor and their respective patients.
""")

# Display metrics for each doctor
for doctor, patients in st.session_state['data']['doctors'].items():
    st.header(f"Performance Metrics for {doctor}")
    metrics = calculate_metrics(patients)
    for key, value in metrics.items():
        st.write(f"**{key}:** {value}")
    
    st.subheader("Patient Data")
    df = pd.DataFrame(patients)
    st.dataframe(df)

# Form to add new patient data
st.header("Add New Patient Data")
with st.form("add_patient_form"):
    doctor = st.selectbox("Select Doctor", list(st.session_state['data']['doctors'].keys()))
    patient = st.text_input("Patient Name")
    blood_pressure = st.text_input("Blood Pressure (e.g., 120/80)")
    cholesterol = st.number_input("Cholesterol", min_value=0)
    ha1c = st.number_input("HA1C", min_value=0.0, max_value=15.0, step=0.1)
    submitted = st.form_submit_button("Add Patient")
    
    if submitted:
        new_patient = {
            "Patient": patient,
            "Blood Pressure": blood_pressure,
            "Cholesterol": cholesterol,
            "HA1C": ha1c
        }
        st.session_state['data']['doctors'][doctor].append(new_patient)
        st.success(f"Patient data added for {doctor}!")

# Display updated data
st.header("Updated Doctor and Patient Data")
for doctor, patients in st.session_state['data']['doctors'].items():
    st.subheader(f"{doctor}'s Patients")
    df = pd.DataFrame(patients)
    st.dataframe(df)
