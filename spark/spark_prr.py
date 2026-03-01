import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, count, when

# ------------------------------
# Ensure PySpark uses Java 21
# ------------------------------
os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home"

# ------------------------------
# Start Spark in local mode
# ------------------------------
spark = SparkSession.builder \
    .appName("FAERS_PRR_Spark") \
    .master("local[*]") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

# ------------------------------
# File paths (update if needed)
# ------------------------------
drug_file = "drug_file.csv"
reac_file = "reac_file.csv"
output_path = "../outputs/spark_merged"

# ------------------------------
# Load CSVs (FAERS uses $ separator)
# ------------------------------
drug_df = spark.read.option("header", True).option("sep", "$").csv(drug_file)
reac_df = spark.read.option("header", True).option("sep", "$").csv(reac_file)

# ------------------------------
# Rename columns for merge
# ------------------------------
drug_df = drug_df.withColumnRenamed("caseid", "CASEID") \
                 .withColumnRenamed("primaryid", "PRIMARYID")

reac_df = reac_df.withColumnRenamed("caseid", "CASEID") \
                 .withColumnRenamed("primaryid", "PRIMARYID")

# Merge on CASEID + PRIMARYID
merged = drug_df.join(reac_df, on=["CASEID", "PRIMARYID"], how="inner")

# Display merged data info
print(f"\nMerged dataset: {merged.count()} rows")
print(f"\nFirst 5 merged rows:")
merged.show(5, truncate=True)

# Write output to CSV
print(f"\nWriting output to {output_path}...")
merged.coalesce(1).write.mode("overwrite").option("header", True).option("sep", "$").csv(output_path)
print("✓ Output written successfully!")


# ======================================================================
# COMPUTE PRR (Proportional Reporting Ratio)
# ======================================================================
print("\n" + "="*80)
print("COMPUTING PRR (Proportional Reporting Ratio)")
print("="*80)

spark_start_time = time.time()

# Get list of unique drugs and reactions
drugs = drug_df.select("drugname").distinct().collect()
reactions = reac_df.select("pt").distinct().collect()

print(f"Unique drugs: {len(drugs)}")
print(f"Unique reactions: {len(reactions)}")

# For each drug-reaction pair, compute:
# a = reports with drug AND reaction
# b = reports with drug but NOT reaction
# c = reports with reaction but NOT drug
# d = reports with neither
# PRR = (a / (a+b)) / (c / (c+d))

prr_results = []

for drug_row in drugs[:5]:  # Sample first 5 drugs for demonstration
    drug_name = drug_row["drugname"]
    
    for reac_row in reactions[:5]:  # Sample first 5 reactions
        reaction_pt = reac_row["pt"]
        
        # Count: a - drug AND reaction
        a = merged.filter(
            (col("drugname") == drug_name) & (col("pt") == reaction_pt)
        ).count()
        
        # Count: b - drug but NOT reaction
        b = drug_df.filter(col("drugname") == drug_name).count() - a
        
        # Count: c - reaction but NOT drug
        c = reac_df.filter(col("pt") == reaction_pt).count() - a
        
        # Count: d - neither (total - a - b - c)
        total = merged.count()
        d = total - a - b - c
        
        # Compute PRR
        if (a + b) > 0 and (c + d) > 0:
            prr = (a / (a + b)) / (c / (c + d))
        else:
            prr = 0
        
        if a > 0:  # Only store if there's at least one report
            prr_results.append({
                "drug": drug_name,
                "reaction": reaction_pt,
                "a": a,
                "b": b,
                "c": c,
                "d": d,
                "prr": round(prr, 4)
            })

spark_end_time = time.time()
spark_time = spark_end_time - spark_start_time

print(f"\nSample PRR Results (first 10):")
for i, result in enumerate(prr_results[:10]):
    print(f"{i+1}. Drug: {result['drug']}, Reaction: {result['reaction']}, PRR: {result['prr']}")

print(f"\n✓ Spark PRR computation completed in {spark_time:.4f} seconds")
print("="*80)

# Stop Spark
spark.stop()