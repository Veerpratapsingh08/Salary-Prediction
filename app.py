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
    st.set_page_config(page_title="Salary Predictor", layout="centered")
    st.title("Salary Predictor")
    st.markdown("This app predicts annual salary in LPA from simple employee details.")

    load_data(DATA_PATH)

    age = st.number_input("Age", min_value=18, max_value=70, value=30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    education = st.selectbox("Education", ["Bachelor", "Diploma", "Master", "PhD"])
    experience = st.number_input("Experience (Years)", min_value=0, max_value=40, value=5)
    department = st.selectbox("Department", ["HR", "IT", "Marketing", "Operations", "Sales"])
    job_level = st.selectbox("Job Level", ["Junior", "Mid", "Senior", "Lead", "Manager"])
    performance_rating = st.number_input("Performance Rating", min_value=1, max_value=5, value=3)
    certifications = st.number_input("Certifications", min_value=0, max_value=10, value=2)
    overtime_hours = st.number_input("Overtime Hours", min_value=0, max_value=100, value=10)
    remote_work = st.selectbox("Remote Work", ["No", "Yes"])
    company_tenure = st.number_input("Company Tenure", min_value=0, max_value=30, value=3)
    projects_completed = st.number_input("Projects Completed", min_value=0, max_value=50, value=5)
    skill_score = st.number_input("Skill Score", min_value=0, max_value=100, value=70)

    if st.button("Predict"):
        prediction = simple_salary_estimate(
            {
                "Age": age,
                "Gender": gender,
                "Education": education,
                "Experience_Years": experience,
                "Department": department,
                "Job_Level": job_level,
                "Performance_Rating": performance_rating,
                "Certifications": certifications,
                "Overtime_Hours": overtime_hours,
                "Remote_Work": remote_work,
                "Company_Tenure": company_tenure,
                "Projects_Completed": projects_completed,
                "Skill_Score": skill_score,
            }
        )
        st.success(f"Predicted Salary: {prediction:.2f} LPA")


if __name__ == "__main__":
    main()
