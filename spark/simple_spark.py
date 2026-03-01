"""
SIMPLE SPARK VERSION - Drug Safety Analysis
============================================

This is the SPARK version - for handling HUGE amounts of data.

What's different from simple_prr.py?
- simple_prr.py: Works on ONE computer (smaller datasets)
- This file: Works across MANY computers (bigger datasets)

Spark is like having 100 workers instead of 1 worker!

For this assignment, the simple version is easier.
Only run this if you want to learn about distributed computing.

Created: February 2026
For: 10th Grade Science Fair
"""

import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when

# Set up Java (needed for Spark)
os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home"

# Create a Spark session (like starting up a team of workers)
print("Starting Spark... (this takes a few seconds)")
spark = SparkSession.builder \
    .appName("DrugSafetyAnalysis") \
    .master("local[*]") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

print("✓ Spark started!")

# File paths
drug_file = "drug_file.csv"
reac_file = "reac_file.csv"

print("\n" + "="*60)
print("LOADING DATA WITH SPARK")
print("="*60)

# Load drug data
print("Loading drugs...")
drug_df = spark.read.option("header", True).option("sep", "$").csv(drug_file)

# Load reaction data
print("Loading side effects...")
reac_df = spark.read.option("header", True).option("sep", "$").csv(reac_file)

# Join them together (match by caseid and primaryid)
print("Joining data...")
merged = drug_df.join(
    reac_df,
    on=["caseid", "primaryid"],
    how="inner"
)

print(f"✓ Loaded and joined data")
print(f"  Total reports: {merged.count():,}")

print("\n" + "="*60)
print("CALCULATING SAFETY SCORES")
print("="*60)

# Count total reports
total = merged.count()

# Get top 5 drugs
top_drugs = drug_df.groupBy("drugname").count() \
    .orderBy(col("count").desc()) \
    .limit(5) \
    .select("drugname") \
    .collect()

drug_names = [row.drugname for row in top_drugs]

# Get top 5 side effects
top_effects = reac_df.groupBy("pt").count() \
    .orderBy(col("count").desc()) \
    .limit(5) \
    .select("pt") \
    .collect()

effect_names = [row.pt for row in top_effects]

print(f"Checking {len(drug_names)} drugs × {len(effect_names)} side effects")

# Calculate for each combination
results = []

for drug in drug_names:
    for effect in effect_names:
        # Count: a - drug AND side effect
        a = merged.filter(
            (col("drugname") == drug) & (col("pt") == effect)
        ).count()
        
        if a == 0:
            continue
        
        # Count: b - drug but NOT side effect
        drug_total = drug_df.filter(col("drugname") == drug).count()
        b = drug_total - a
        
        # Count: c - side effect but NOT drug
        effect_total = reac_df.filter(col("pt") == effect).count()
        c = effect_total - a
        
        # Count: d - neither
        d = total - a - b - c
        
        # Calculate PRR
        if (a + b) > 0 and (c + d) > 0:
            prr = (a / (a + b)) / (c / (c + d))
            is_important = prr >= 2.0
            
            results.append({
                'drug': drug,
                'effect': effect,
                'prr': prr,
                'count_a': a,
                'important': is_important
            })

# Sort by PRR
results.sort(key=lambda x: x['prr'], reverse=True)

print(f"✓ Calculated {len(results)} combinations")

print("\n" + "="*60)
print("TOP RESULTS")
print("="*60)

print(f"{'#':<3} {'DRUG':<20} {'SIDE EFFECT':<20} {'PRR':<10} {'STATUS'}")
print("-" * 60)

for i, result in enumerate(results[:10], 1):
    status = "⚠️ IMPORTANT" if result['important'] else "Normal"
    print(f"{i:<3} {result['drug'][:19]:<20} {result['effect'][:19]:<20} "
          f"{result['prr']:<10.2f} {status}")

print("\n✅ Analysis complete!")

# Stop Spark
spark.stop()
