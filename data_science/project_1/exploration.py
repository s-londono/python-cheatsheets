import pandas as pd

# (1259, 27)
df_mental_h = pd.read_csv("data_science/project_1/datasets/mental-health-in-tech/survey.csv")
print(f"Mental Health in Tech: {df_mental_h.shape}")

# (7043, 21)
df_telco_chrn = pd.read_csv("data_science/project_1/datasets/telco-customer-churn/WA_Fn-UseC_-Telco-Customer-Churn.csv")
print(f"Telco Customer Churn: {df_telco_chrn.shape}")

# (32560, 15)
df_cs_income = pd.read_csv("data_science/project_1/datasets/us-census-income/adult.data")
print(f"US Census Adult Income: {df_cs_income.shape}")

# (4812, 29)
df_hospital = pd.read_csv("data_science/project_1/datasets/hospital-general-information/HospInfo.csv")
print(f"Hospital General Information: {df_hospital.shape}")

# (85800, 29)
df_heart_dp = pd.read_csv("data_science/project_1/datasets/heart-disease-prevention/dataset.csv")
print(f"Heart Disease and Stroke Prevention: {df_heart_dp.shape}")

# (179096, 67) **
df_nys_patient_dp = pd.read_csv("data_science/project_1/datasets/nys-patient-characteristics/patient-characteristics-survey-pcs-2015.csv")
print(f"NYS Patient Characteristics: {df_nys_patient_dp.shape}")

# (886102, 22) ***
df_sf_comp_dp = pd.read_csv("data_science/project_1/datasets/sf-employee-compensation/employee-compensation.csv")
print(f"SF Employee Compensation: {df_sf_comp_dp.shape}")
