import datetime
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent / "1-employee_salary_dataset.csv"
TARGET_COLUMN = "Annual_Salary_LPA"


@st.cache_data(show_spinner=False)
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


@st.cache_data(show_spinner=False)
def train_model(df: pd.DataFrame):
    model_df = df.copy()
    model_df = model_df.drop(columns=["Employee_ID"], errors="ignore")

    model_df["Gender"] = model_df["Gender"].map({"Male": 1, "Female": 0})
    model_df["Remote_Work"] = model_df["Remote_Work"].map({"Yes": 1, "No": 0})

    categorical_cols = ["Education", "Department", "Job_Level", "City"]
    for col in categorical_cols:
        model_df[col] = model_df[col].astype("category").cat.codes

    X = model_df.drop(columns=[TARGET_COLUMN])
    y = model_df[TARGET_COLUMN]

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X, y)
    return model


def main():
    st.set_page_config(page_title="Salary Predictor", layout="centered")
    st.title("Salary Predictor")
    st.markdown("This app predicts annual salary in LPA from simple employee details.")

    df = load_data(DATA_PATH)
    model = train_model(df)

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
    city = st.selectbox("City", ["Chennai", "Delhi", "Hyderabad", "Mumbai"])
    company_tenure = st.number_input("Company Tenure", min_value=0, max_value=30, value=3)
    projects_completed = st.number_input("Projects Completed", min_value=0, max_value=50, value=5)
    skill_score = st.number_input("Skill Score", min_value=0, max_value=100, value=70)

    data_new = pd.DataFrame(
        {
            "Age": [age],
            "Gender": [1 if gender == "Male" else 0],
            "Education": ["Bachelor", "Diploma", "Master", "PhD"].index(education),
            "Experience_Years": [experience],
            "Department": ["HR", "IT", "Marketing", "Operations", "Sales"].index(department),
            "Job_Level": ["Junior", "Mid", "Senior", "Lead", "Manager"].index(job_level),
            "Performance_Rating": [performance_rating],
            "Certifications": [certifications],
            "Overtime_Hours": [overtime_hours],
            "Remote_Work": [1 if remote_work == "Yes" else 0],
            "City": ["Chennai", "Delhi", "Hyderabad", "Mumbai"].index(city),
            "Company_Tenure": [company_tenure],
            "Projects_Completed": [projects_completed],
            "Skill_Score": [skill_score],
        }
    )

    if st.button("Predict"):
        pred = model.predict(data_new)
        st.success(f"Predicted Salary: {pred[0]:.2f} LPA")


if __name__ == "__main__":
    main()
