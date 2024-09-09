import streamlit as st
import mysql.connector

# Database connection parameters
db_user = "ty376miw198qbdtc"
db_password = "mpnls4nyljjqrswz"
db_host = "q7cxv1zwcdlw7699.chr7pe7iynqr.eu-west-1.rds.amazonaws.com"
db_port = 3306
db_database = "dn924vi9c6asl4zf"

# Function to connect to the database
def connect_to_database():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )

# Function to get patients from the database
def get_patients():
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, name FROM patients"
    cursor.execute(query)
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return patients

# Function to get patient history
def get_patient_history(patient_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT history FROM patients WHERE id = %s"
    cursor.execute(query, (patient_id,))
    history = cursor.fetchone()
    cursor.close()
    conn.close()
    return history['history'] if history else ""

# Function to get patient email
def get_patient_email(patient_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT email FROM patients WHERE id = %s"
    cursor.execute(query, (patient_id,))
    email = cursor.fetchone()
    cursor.close()
    conn.close()
    return email['email'] if email else ""

# Function to get exercises based on difficulty
def get_exercises(difficulty):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT exercise_name, youtube_link FROM exercises WHERE difficulty = %s"
    cursor.execute(query, (difficulty,))
    exercises = cursor.fetchall()
    cursor.close()
    conn.close()
    return exercises

# Function to get YouTube thumbnail URL
def get_thumbnail_url(youtube_link):
    video_id = youtube_link.split('v=')[-1]
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

st.set_page_config(
    page_title="Physio Exercise Assignment App",
    page_icon="🏋️‍♂️",
)

st.title("Patient Exercise Assignment Tool")

# Fetch and display patient data
patients = get_patients()
patient_names = [patient['name'] for patient in patients]
patient_id_map = {patient['name']: patient['id'] for patient in patients}

# Patient selection
patient_name = st.selectbox('Select Patient', patient_names)

if patient_name:
    patient_id = patient_id_map[patient_name]
    history = get_patient_history(patient_id)
    email = get_patient_email(patient_id)
    st.write(f"Patient History for {patient_name}:")
    st.write(history)  # Display the full history string directly

    st.write(f"Patient Email: {email}")  # Display the patient's email

    # Button to view patient data
    if st.button('View Patient Data'):
        st.write(f"Viewing additional data for {patient_name}:")
        # Display additional patient data here or trigger an action
        st.write(f"Full history or other relevant data for {patient_name} can be displayed here.")

# Fetch and display exercises based on difficulty
difficulty = st.selectbox('Select Difficulty Level', ['Beginner', 'Intermediate', 'Advanced'])
exercises = get_exercises(difficulty)
exercise_names = [exercise['exercise_name'] for exercise in exercises]

st.write(f"Select Exercises for {difficulty} level:")
selected_exercises = st.multiselect('Choose exercises', exercise_names)

# Display thumbnails for selected exercises
for exercise_name in selected_exercises:
    for exercise in exercises:
        if exercise['exercise_name'] == exercise_name:
            thumbnail_url = get_thumbnail_url(exercise['youtube_link'])
            st.image(thumbnail_url, caption=exercise_name, use_column_width=True)
            break

# Slider for repetitions
reps = st.slider('Select Repetitions', min_value=1, max_value=15, value=(8, 12), step=1)
st.write(f"Repetitions: {reps[0]} - {reps[1]}")

# Counter for sets
sets = st.number_input('Select Number of Sets', min_value=1, value=1, step=1)

# Additional notes box
additional_notes = st.text_area('Additional Notes', '')

# Button to assign exercises
if st.button('Send Exercises'):
    if patient_name and selected_exercises:
        exercise_list = ", ".join(selected_exercises)
        st.write(f"Successfully sent the following exercises to {email}:")
        st.write(exercise_list)
        st.write(f"Repetitions: {reps[0]} - {reps[1]}")
        st.write(f"Sets: {sets}")
        st.write(f"Additional Notes: {additional_notes}")
    else:
        st.write("Please select a patient and choose exercises.")
