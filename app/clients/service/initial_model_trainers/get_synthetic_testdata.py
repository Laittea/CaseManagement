import pandas as pd
import numpy as np
import os

np.random.seed(42)  # For reproducibility

num_samples = 4000  # Number of rows

# Age distribution: Normal distribution centered around 30, capped between 18 and 60
age = np.random.normal(loc=30, scale=8, size=num_samples).astype(int)
age = np.clip(age, 18, 60)

# Work experience based on age (years since 18 minus some gap years)
work_experience = (age - 18) - np.random.randint(0, 4, num_samples)
work_experience = np.clip(work_experience, 0, 42)

# Canadian work experience is a fraction of total work experience
canada_workex = (work_experience * np.random.uniform(0.3, 0.9, num_samples)).astype(int)

# Education level: weighted choice
level_of_schooling = np.random.choice([6, 8, 10, 12, 14], size=num_samples, p=[0.1, 0.25, 0.3, 0.25, 0.1])

# English proficiency
fluent_english = np.random.randint(4, 10, num_samples)
reading_english = np.clip(fluent_english + np.random.randint(-1, 2, num_samples), 1, 10)
speaking_english = np.clip(fluent_english + np.random.randint(-1, 2, num_samples), 1, 10)
writing_english = np.clip(fluent_english + np.random.randint(-1, 2, num_samples), 1, 10)

# Numeracy and computer skills
numeracy = np.random.randint(3, 10, num_samples)
computer = np.random.randint(3, 10, num_samples)

# Binary features generator
binary_features = lambda: np.random.randint(0, 2, num_samples)

# Other categorical and binary features
gender = binary_features()
dep_num = np.random.randint(0, 5, num_samples)
canada_born = binary_features()
citizen_status = binary_features()
transportation_bool = binary_features()
caregiver_bool = binary_features()
housing = np.random.randint(1, 10, num_samples)
income_source = np.random.randint(1, 10, num_samples)
felony_bool = binary_features()
attending_school = binary_features()
currently_employed = binary_features()
substance_use = binary_features()
time_unemployed = np.random.randint(0, 8, num_samples)
need_mental_health_support_bool = binary_features()
employment_assistance = binary_features()
life_stabilization = binary_features()
retention_services = binary_features()
specialized_services = binary_features()
employment_related_financial_supports = binary_features()
employer_financial_supports = binary_features()
enhanced_referrals = binary_features()

# Success Rate Logic

felony_penalty = np.where(felony_bool == 1, -15, 0)
substance_penalty = np.where(substance_use == 1, -10, 0)
long_unemployed_penalty = np.where(time_unemployed >= 4, -5, 0)

bonus_services = (
    (employment_assistance + life_stabilization + retention_services + specialized_services) * 3
)

employment_bonus = np.where(currently_employed == 1, 5, 0)
education_effect = np.minimum(level_of_schooling, 12)  # Cap effect after a certain level

success_rate_base = (
    fluent_english * 2 +
    education_effect * 2 +
    computer * 2 +
    numeracy * 1.5 +
    work_experience * 1.0 +
    employment_bonus +
    bonus_services +
    felony_penalty +
    substance_penalty +
    long_unemployed_penalty +
    (np.random.randint(0, 2, num_samples) * 5)  # Random life variance
)

# Normalize and add Gaussian noise
success_rate = (success_rate_base / success_rate_base.max() * 100) + np.random.normal(0, 5, num_samples)
success_rate = np.clip(success_rate.astype(int), 0, 100)

# Create DataFrame
data = pd.DataFrame({
    "age": age,
    "gender": gender,
    "work_experience": work_experience,
    "canada_workex": canada_workex,
    "dep_num": dep_num,
    "canada_born": canada_born,
    "citizen_status": citizen_status,
    "level_of_schooling": level_of_schooling,
    "fluent_english": fluent_english,
    "reading_english_scale": reading_english,
    "speaking_english_scale": speaking_english,
    "writing_english_scale": writing_english,
    "numeracy_scale": numeracy,
    "computer_scale": computer,
    "transportation_bool": transportation_bool,
    "caregiver_bool": caregiver_bool,
    "housing": housing,
    "income_source": income_source,
    "felony_bool": felony_bool,
    "attending_school": attending_school,
    "currently_employed": currently_employed,
    "substance_use": substance_use,
    "time_unemployed": time_unemployed,
    "need_mental_health_support_bool": need_mental_health_support_bool,
    "employment_assistance": employment_assistance,
    "life_stabilization": life_stabilization,
    "retention_services": retention_services,
    "specialized_services": specialized_services,
    "employment_related_financial_supports": employment_related_financial_supports,
    "employer_financial_supports": employer_financial_supports,
    "enhanced_referrals": enhanced_referrals,
    "success_rate": success_rate
})

# Save to CSV
output_path = os.path.join(os.path.dirname(__file__), "../data_commontool_synthetic_testdata.csv")
data.to_csv(output_path, index=False)

print(f" {num_samples} diversified synthetic data rows generated and saved to data_commontool_synthetic.csv")
