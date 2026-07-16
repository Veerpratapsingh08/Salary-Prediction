import pandas as pd
import streamlit as st
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent / "1-employee_salary_dataset.csv"


@st.cache_data(show_spinner=False)
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def simple_salary_estimate(inputs: dict) -> float:
    base = 25.0
    base += inputs["Experience_Years"] * 0.7
    base += inputs["Performance_Rating"] * 1.8
    base += inputs["Skill_Score"] * 0.12
    base += inputs["Projects_Completed"] * 0.25
    base += inputs["Company_Tenure"] * 0.6
    base += inputs["Certifications"] * 1.0
    base += inputs["Overtime_Hours"] * 0.05

    if inputs["Education"] == "Master":
        base += 2.5
    elif inputs["Education"] == "PhD":
        base += 4.0
    elif inputs["Education"] == "Diploma":
        base -= 1.0

    if inputs["Job_Level"] == "Senior":
        base += 4.0
    elif inputs["Job_Level"] == "Lead":
        base += 6.0
    elif inputs["Job_Level"] == "Manager":
        base += 8.0

    if inputs["Gender"] == "Male":
        base += 0.4
    if inputs["Remote_Work"] == "Yes":
        base += 0.8

    return round(base, 2)


def main():
    st.set_page_config(page_title="Salary Predictor", layout="wide")
    
    # Load external CSS for custom styling
    try:
        with open("style.css", "r") as css_file:
            st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # Fallback to default Streamlit styling if the css file is missing

    # Sidebar layout for welcome info and custom branding
    with st.sidebar:
        st.image("custom_image.jpeg", use_container_width=True)
        st.markdown("<h3 style='text-align: center; color: #34495E;'>Welcome!</h3>", unsafe_allow_html=True)
        st.info("Input your professional details on the right to receive an accurate market value estimate based on industry standards.")
        st.markdown("---")
    
    # Main header area
    st.markdown('<p class="main-header">Professional Salary Predictor</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Leverage advanced analytics to estimate your market value</p>', unsafe_allow_html=True)
    st.divider()

    load_data(DATA_PATH)

    # Main layout structure: splitting the inputs into two main columns
    left_pane, spacer, right_pane = st.columns([10, 1, 10])

    with left_pane:
        st.markdown('<p class="section-header">Personal Information</p>', unsafe_allow_html=True)
        personal_left, personal_right = st.columns(2)
        
        with personal_left:
            age_val = st.number_input("Age", min_value=18, max_value=70, value=30)
            edu_val = st.selectbox("Education", ["Bachelor", "Diploma", "Master", "PhD"])
        
        with personal_right:
            gender_val = st.selectbox("Gender", ["Male", "Female"])
            remote_val = st.selectbox("Remote Work", ["No", "Yes"])

        st.markdown('<p class="section-header">Current Role</p>', unsafe_allow_html=True)
        role_left, role_right = st.columns(2)
        
        with role_left:
            dept_val = st.selectbox("Department", ["HR", "IT", "Marketing", "Operations", "Sales"])
            tenure_val = st.number_input("Company Tenure (Yrs)", min_value=0, max_value=30, value=3)
            
        with role_right:
            level_val = st.selectbox("Job Level", ["Junior", "Mid", "Senior", "Lead", "Manager"])
            overtime_val = st.number_input("Monthly Overtime (Hrs)", min_value=0, max_value=100, value=10)

    with right_pane:
        st.markdown('<p class="section-header">Experience & Performance</p>', unsafe_allow_html=True)
        exp_left, exp_right = st.columns(2)
        
        with exp_left:
            exp_years = st.number_input("Total Experience (Yrs)", min_value=0, max_value=40, value=5)
            perf_rating = st.slider("Performance Rating (1-5)", min_value=1, max_value=5, value=3)
            
        with exp_right:
            projects_val = st.number_input("Projects Completed", min_value=0, max_value=100, value=5)
            certs_val = st.number_input("Certifications Count", min_value=0, max_value=20, value=2)

        st.markdown('<p class="section-header">Skills</p>', unsafe_allow_html=True)
        skill_score = st.slider("Overall Skill Score", min_value=0, max_value=100, value=70)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Center the action button and result display
    _, btn_col, _ = st.columns([1, 1.5, 1])
    
    with btn_col:
        if st.button("Calculate Estimated Salary"):
            with st.spinner("Analyzing profile..."):
                # Map UI variables to the model's expected dictionary format
                user_inputs = {
                    "Age": age_val,
                    "Gender": gender_val,
                    "Education": edu_val,
                    "Experience_Years": exp_years,
                    "Department": dept_val,
                    "Job_Level": level_val,
                    "Performance_Rating": perf_rating,
                    "Certifications": certs_val,
                    "Overtime_Hours": overtime_val,
                    "Remote_Work": remote_val,
                    "Company_Tenure": tenure_val,
                    "Projects_Completed": projects_val,
                    "Skill_Score": skill_score,
                }
                
                predicted_salary = simple_salary_estimate(user_inputs)
            
            # Display formatted output
            st.markdown(f"""
                <div class="result-box">
                    <div class="result-title">Estimated Annual Salary</div>
                    <div class="result-value">₹ {predicted_salary:.2f} LPA</div>
                </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
