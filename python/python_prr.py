import pandas as pd

# Set your file paths
drug_file = "/Users/hasinisridhar/Documents/faers_prr_project/drug_file.csv"
reac_file = "/Users/hasinisridhar/Documents/faers_prr_project/reac_file.csv"

# Load the CSVs (FAERS uses $ as separator)
drug_df = pd.read_csv(drug_file, sep="$", dtype=str)
reac_df = pd.read_csv(reac_file, sep="$", dtype=str)

# Print columns for sanity check
print("Drug dataframe columns:", drug_df.columns)
print("Reaction dataframe columns:", reac_df.columns)

# Rename columns to consistent names
drug_df.rename(columns={
    'caseid': 'CASEID',
    'primaryid': 'PRIMARYID'
}, inplace=True)

reac_df.rename(columns={
    'caseid': 'CASEID',
    'primaryid': 'PRIMARYID'
}, inplace=True)

# Merge on BOTH CASEID and PRIMARYID
merged = pd.merge(drug_df, reac_df, on=["CASEID", "PRIMARYID"], how="inner")

# Check merged columns
print("Merged dataframe columns:", merged.columns)

# Clean text columns (important for FAERS)
merged["drugname"] = merged["drugname"].str.strip().str.upper()
merged["pt"] = merged["pt"].str.strip().str.upper()

# Example: count occurrences of a specific drug-event combination
drug_name = "ASPIRIN"     # Replace with your drug
event_name = "HEADACHE"  # Replace with your adverse event

# Count how many times the drug-event pair occurs
A = len(merged[
    (merged["drugname"] == drug_name.upper()) &
    (merged["pt"] == event_name.upper())
])

print(f"Occurrences of {drug_name} causing {event_name}: {A}")

# Save merged dataframe for inspection
merged.to_csv("/Users/hasinisridhar/Documents/faers_prr_project/merged_output.csv", index=False)
