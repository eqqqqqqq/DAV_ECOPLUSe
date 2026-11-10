
import pandas as pd

# 1. Load the Excel dataset
file_path = "combined_2000_people_analysis_dataset.xlsx"
df = pd.read_excel(file_path, sheet_name="2000_People_Data")

print("Original shape:", df.shape)

# 2. Clean column names
df.columns = df.columns.str.strip()

# 3. Remove duplicate records
df = df.drop_duplicates()

# 4. Remove extra spaces from text columns
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].apply(
        lambda x: x.strip() if isinstance(x, str) else x
    )

# 5. Convert numeric columns to proper numeric format
numeric_columns = [
    "Age", "Outdoor_Exposure_Hours_Day", "Sleep_Hours",
    "latitude", "longitude", "Avg_Temp_Max_C",
    "Avg_Temp_Min_C", "Avg_Rain_mm", "Avg_Wind_kmh",
    "Dengue_Cases_2019_2024", "Dengue_Deaths_2019_2024",
    "Dengue_Cases_2024", "Hospital_Count",
    "Avg_Hospital_Rating", "Environmental_Dengue_Risk_Index"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 6. Replace invalid values with missing values
if "Age" in df.columns:
    df.loc[~df["Age"].between(0, 120), "Age"] = pd.NA

if "Sleep_Hours" in df.columns:
    df.loc[~df["Sleep_Hours"].between(0, 24),
           "Sleep_Hours"] = pd.NA

# 7. Fill missing numeric values with the median
for col in df.select_dtypes(include="number").columns:
    if df[col].isna().any():
        median_value = df[col].median()
        if pd.notna(median_value):
            df[col] = df[col].fillna(median_value)

# 8. Fill missing text values
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].fillna("Unknown")

# 9. Save the cleaned dataset
output_file = "ECO_PULSE_Cleaned_Data.xlsx"
df.to_excel(output_file, index=False)

# 10. Display cleaning results
print("Cleaning completed successfully!")
print("Final shape:", df.shape)
print("Duplicate rows:", df.duplicated().sum())
print("Missing values:", df.isna().sum().sum())
print("Saved as:", output_file)
