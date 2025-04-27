import streamlit as st
import datetime

# Initialize Session State
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "user_type": None,
        "age": None,
        "pre_existing_conditions": False,
        "fall_details": {},
        "assessment": {},
        "outcome": None,
        "timestamp": datetime.datetime.now()
    }

def alert_caregiver():
    st.warning(f"⚠️ Alerting caregiver... Fall detected at {st.session_state.user_data['timestamp']}")

# Sections
def trigger_fall_event():
    st.title("🚨 Fall Detection and Assessment")
    st.subheader("1. Initial Trigger & User Identification")

    user_type = st.radio("Who are you?", ["Patient", "Caregiver"])
    st.session_state.user_data['user_type'] = user_type.lower()
    
    if user_type == "Patient":
        alert_caregiver()

    if st.button("Proceed to Age Question"):
        st.session_state.page = "age_branch"

def ask_age_and_branch():
    st.title("👤 Age and Pre-existing Conditions")
    age = st.number_input("Enter Age:", min_value=0, max_value=120, value=30)
    st.session_state.user_data['age'] = age

    if age >= 60:
        st.session_state.page = "detailed_fall_assessment"
    elif age < 60:
        pre_existing = st.radio("Pre-existing disabling conditions?", ["Yes", "No"])
        st.session_state.user_data['pre_existing_conditions'] = (pre_existing == "Yes")
        if st.session_state.user_data['pre_existing_conditions']:
            st.session_state.page = "detailed_fall_assessment"
        elif age < 3:
            st.session_state.page = "infant_toddler_fall_assessment"
        else:
            st.session_state.page = "younger_adult_fall_assessment"
    
    if st.button("Next Step"):
        pass

def detailed_fall_assessment():
    st.title("🧠 Detailed Fall Assessment (Older Adult / Disabling Condition)")
    
    dementia = st.radio("Is there dementia?", ["Yes", "No"])
    if dementia == "Yes":
        confusion = st.radio("Is the person more confused than normal after the fall?", ["Yes", "No"])
        commands = st.radio("Is the person responding to commands?", ["Yes", "No"])
        st.session_state.user_data['assessment']['confusion'] = confusion
        st.session_state.user_data['assessment']['responding_to_commands'] = commands

    st.session_state.user_data['assessment']['witnessed'] = st.radio("Was it a witnessed fall?", ["Yes", "No"])
    st.session_state.user_data['assessment']['trip'] = st.radio("Did you trip down?", ["Yes", "No"])
    st.session_state.user_data['assessment']['landed_safely'] = st.radio("Did you safely land on the floor?", ["Yes", "No"])

    st.subheader("Pre-Fall Symptoms")
    st.session_state.user_data['assessment']['dizzy_before'] = st.radio("Dizzy before fall?", ["Yes", "No"])
    st.session_state.user_data['assessment']['lightheaded_before'] = st.radio("Lightheaded before fall?", ["Yes", "No"])
    st.session_state.user_data['assessment']['blood_pressure'] = st.text_input("Blood Pressure Reading:")
    st.session_state.user_data['assessment']['heart_rate'] = st.text_input("Heart Rate:")

    st.subheader("Fall Impact")
    st.session_state.user_data['assessment']['time_on_ground'] = st.text_input("How long were you down?")
    memory = st.radio("Do you remember the fall?", ["Yes", "No"])
    st.session_state.user_data['assessment']['memory_of_fall'] = memory
    if memory == "No":
        st.session_state.user_data['assessment']['last_memory'] = st.text_input("Last thing you remember:")

    st.session_state.user_data['assessment']['hard_fall'] = st.radio("Was it a hard fall?", ["Yes", "No"])
    st.session_state.user_data['assessment']['hit_head'] = st.radio("Did you hit your head?", ["Yes", "No"])
    if st.session_state.user_data['assessment']['hit_head'] == "Yes":
        st.session_state.user_data['assessment']['body_parts_hit'] = st.text_input("Which body parts were hit?")

    if st.button("Determine Outcome"):
        determine_outcome()

def younger_adult_fall_assessment():
    st.title("🧍 Younger Adult Fall Assessment")

    st.session_state.user_data['assessment']['pass_out'] = st.radio("Did you pass out?", ["Yes", "No"])
    st.session_state.user_data['assessment']['trip'] = st.radio("Did you trip down?", ["Yes", "No"])
    st.session_state.user_data['assessment']['hard_fall'] = st.radio("Was it a hard fall?", ["Yes", "No"])
    st.session_state.user_data['assessment']['hit_head'] = st.radio("Did you hit your head?", ["Yes", "No"])
    st.session_state.user_data['assessment']['body_part_hit'] = st.text_input("Which body part was hit?")

    if st.button("Determine Outcome"):
        determine_outcome()

def infant_toddler_fall_assessment():
    st.title("🧸 Infant/Toddler Fall Assessment")

    st.session_state.user_data['assessment']['head_injury'] = st.radio("Did the child have a head injury?", ["Yes", "No"])
    st.session_state.user_data['assessment']['pass_out'] = st.radio("Did the child pass out?", ["Yes", "No"])
    st.session_state.user_data['assessment']['active_response'] = st.radio("Is the baby responding actively?", ["Yes", "No"])
    st.session_state.user_data['assessment']['sleepy'] = st.radio("Is the baby sleepier than usual?", ["Yes", "No"])
    st.session_state.user_data['assessment']['crying_on_movement'] = st.radio("Crying on moving a body part?", ["Yes", "No"])
    st.session_state.user_data['assessment']['sick_before_fall'] = st.radio("Was the baby sick prior?", ["Yes", "No"])

    if st.button("Determine Outcome"):
        determine_outcome()

def determine_outcome():
    st.title("🔎 Outcome Analysis")

    fatal_signs = ['pass_out', 'hard_fall', 'hit_head', 'bleeding', 'chest_pain']
    outcome = "Non-Fatal Fall (Follow-up with PCP)"

    for key in fatal_signs:
        if st.session_state.user_data['assessment'].get(key, "No") == "Yes":
            outcome = "Fatal Fall! ➡️ Go to Emergency Room immediately!"
            break

    st.session_state.user_data['outcome'] = outcome

    st.success(f"🏥 Outcome: {outcome}")

    st.subheader("📋 Fall Report")
    st.json(st.session_state.user_data)

# Main control
if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = "trigger"

    if st.session_state.page == "trigger":
        trigger_fall_event()
    elif st.session_state.page == "age_branch":
        ask_age_and_branch()
    elif st.session_state.page == "detailed_fall_assessment":
        detailed_fall_assessment()
    elif st.session_state.page == "younger_adult_fall_assessment":
        younger_adult_fall_assessment()
    elif st.session_state.page == "infant_toddler_fall_assessment":
        infant_toddler_fall_assessment()
