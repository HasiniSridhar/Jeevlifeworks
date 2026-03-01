# PRR Algorithm: Distributed Spark vs Non-Distributed OOP Implementation

## Assignment Completion

This project implements the **Proportional Reporting Ratio (PRR)** algorithm using two different approaches:
1. **Distributed PySpark implementation** - for parallel processing on large datasets
2. **Non-distributed OOP implementation** - pure Python for performance comparison

## Files

- **spark_prr.py** - Distributed implementation using Apache Spark
- **oop_prr.py** - Non-distributed OOP implementation using pure Python
- **compare_performance.py** - Performance benchmarking and comparison script
- **drug_file.csv** - FDA FAERS drug data (quarterly dataset)
- **reac_file.csv** - FDA FAERS adverse reaction data (quarterly dataset)

## What is PRR?

The Proportional Reporting Ratio (PRR) is a statistical measure used in pharmacovigilance to detect adverse drug reactions. It calculates:

```
PRR = (a / (a+b)) / (c / (c+d))
```

Where:
- **a** = reports with drug AND reaction
- **b** = reports with drug but NOT reaction
- **c** = reports with reaction but NOT drug
- **d** = reports with neither drug nor reaction

Higher PRR values indicate a stronger association between the drug and the adverse reaction.

## Running the Code

### 1. Run Spark Implementation (Distributed)
```bash
python3 spark_prr.py
```

### 2. Run OOP Implementation (Non-Distributed)
```bash
python3 oop_prr.py
```

### 3. Compare Performance
```bash
python3 compare_performance.py
```

## Key Differences

| Aspect | Spark | OOP |
|--------|-------|-----|
| **Processing** | Distributed, parallel | Single-machine, sequential |
| **Scalability** | Excellent for large datasets | Limited by memory |
| **Startup Time** | Higher (JVM initialization) | Lower |
| **Memory Usage** | Distributed across nodes | Single machine |
| **Implementation** | Declarative DataFrame API | Imperative OOP pattern |

## Implementation Details

### Spark Implementation (spark_prr.py)
- Uses PySpark DataFrame operations for distributed computing
- Loads CSV files with '$' separator (FAERS standard format)
- Computes PRR values for sampled drug-reaction pairs
- Optimal for large-scale datasets across clusters

### OOP Implementation (oop_prr.py)
- Pure Python with class-based design
- Uses Python dictionaries for fast lookups
- Loads and merges data in memory
- Better for understanding the algorithm clearly

## Performance Notes

For small datasets (like the sample quarterly FAERS data), the OOP implementation may be faster due to Spark's initialization overhead. However, Spark's performance advantage increases significantly with larger datasets and parallel processing requirements.

## Expected Output

Both implementations will display:
- Number of loaded reports
- Number of unique drugs and reactions
- Sample PRR results for top drug-reaction pairs
- Execution time for performance comparison

## Requirements

- Python 3.7+
- PySpark 3.x
- Java 21 (for Spark)

## Notes

- The sample dataset contains quarterly FDA FAERS data
- Results show PRR values for the first 5 drugs × 5 reactions (25 pairs maximum)
- Only pairs with at least one report are included in results
