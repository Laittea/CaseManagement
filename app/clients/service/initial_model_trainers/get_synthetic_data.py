import pandas as pd
import numpy as np
import os

num_samples = 7000  # Total number of samples to generate

# Age distribution: Normal distribution centered around 30, capped between 18 and 60
age = np.random.normal(loc=30, scale=8, size=num_samples).astype(int)
age = np.clip(age, 18, 60)

# Work experience based on age (years since 18 minus some gap years)
work_experience = (age - 18) - np.random.randint(0, 4, num_samples)
work_experience = np.clip(work_experience, 0, 42)

# Canadian work experience is a fraction of total work experience
canada_workex = (work_experience * np.random.uniform(0.3, 0.9, num_samples)).astype(int)

# Education level: weighted choice simulating real-world distribution
level_of_schooling = np.random.choice([6, 8, 10, 12, 14], size=num_samples, p=[0.1, 0.25, 0.3, 0.25, 0.1])

# English proficiency: fluent_english impacts reading/speaking/writing scores
fluent_english = np.random.randint(4, 10, num_samples)
reading_english = np.clip(fluent_english + np.random.randint(-1, 2, num_samples), 1, 10)
speaking_english = np.clip(fluent_english + np.random.randint(-1, 2, num_samples), 1, 10)
writing_english = np.clip(fluent_english + np.random.randint(-1, 2, num_samples), 1, 10)

# Numeracy and computer skills
numeracy = np.random.randint(3, 10, num_samples)
computer = np.random.randint(3, 10, num_samples)

# Binary features generator (0 or 1)
binary_features = lambda: np.random.randint(0, 2, num_samples)

# Base success rate formula influenced by key features
success_rate_base = (
    fluent_english * 2 + 
    level_of_schooling * 2 +
    computer * 2 +
    numeracy * 1.5 +
    work_experience * 1.2 +
    (binary_features() * 10)  # bonus random life factors
)

# Normalize and add Gaussian noise
success_rate = (success_rate_base / success_rate_base.max() * 100) + np.random.normal(0, 5, num_samples)
success_rate = np.clip(success_rate.astype(int), 0, 100)

# Create the dataframe
data = pd.DataFrame({
    "age": age,
    "gender": binary_features(),
    "work_experience": work_experience,
    "canada_workex": canada_workex,
    "dep_num": np.random.randint(0, 5, num_samples),
    "canada_born": binary_features(),
    "citizen_status": binary_features(),
    "level_of_schooling": level_of_schooling,
    "fluent_english": fluent_english,
    "reading_english_scale": reading_english,
    "speaking_english_scale": speaking_english,
    "writing_english_scale": writing_english,
    "numeracy_scale": numeracy,
    "computer_scale": computer,
    "transportation_bool": binary_features(),
    "caregiver_bool": binary_features(),
    "housing": np.random.randint(1, 10, num_samples),
    "income_source": np.random.randint(1, 10, num_samples),
    "felony_bool": binary_features(),
    "attending_school": binary_features(),
    "currently_employed": binary_features(),
    "substance_use": binary_features(),
    "time_unemployed": np.random.randint(0, 8, num_samples),
    "need_mental_health_support_bool": binary_features(),
    "employment_assistance": binary_features(),
    "life_stabilization": binary_features(),
    "retention_services": binary_features(),
    "specialized_services": binary_features(),
    "employment_related_financial_supports": binary_features(),
    "employer_financial_supports": binary_features(),
    "enhanced_referrals": binary_features(),
    "success_rate": success_rate
})

# Save to CSV
# output_path = os.path.join("app", "clients", "service", "data_commontool_synthetic.csv")
output_path = os.path.join(os.path.dirname(__file__), "data_commontool_synthetic.csv")

data.to_csv(output_path, index=False)

print(f"✅ {num_samples} synthetic data rows generated and saved to data_commontool_synthetic.csv")
