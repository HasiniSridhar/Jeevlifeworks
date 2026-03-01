"""
Quick Start Guide - FAERS PRR Analyzer
Get started with the non-distributed OOP implementation in 5 minutes
"""

import os
import sys


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(title)
    print("="*80)


def main():
    """Interactive quick start guide"""
    
    print_section("FAERS PRR ANALYZER - Quick Start Guide")
    
    print("""
This guide will help you get started with the FAERS PRR Analyzer,
a pure Python object-oriented implementation for computing Proportional
Reporting Ratios from FDA adverse event data.

FILES INCLUDED:
  ✓ faers_prr_analyzer.py   - Main module with core classes
  ✓ faers_examples.py        - Comprehensive usage examples  
  ✓ test_faers_prr.py        - Unit tests and validation
  ✓ drug_file.csv            - Sample FAERS drug data
  ✓ reac_file.csv            - Sample FAERS reaction data
  ✓ PYTHON_OOP_README.md     - Complete documentation
""")
    
    print_section("Step 1: Verify Files")
    
    required_files = [
        "faers_prr_analyzer.py",
        "drug_file.csv",
        "reac_file.csv"
    ]
    
    print("\nChecking for required files:")
    all_present = True
    for filename in required_files:
        exists = os.path.exists(filename)
        status = "✓" if exists else "✗"
        print(f"  {status} {filename}")
        all_present = all_present and exists
    
    if not all_present:
        print("\n⚠ Some required files are missing!")
        print("  Please ensure all data files are in the same directory.")
        return
    
    print("\n✓ All required files present!")
    
    print_section("Step 2: Basic Usage")
    
    print("""
Here's the simplest way to use the analyzer:

    from faers_prr_analyzer import FAERSDatabase
    
    # Create and load database
    db = FAERSDatabase()
    db.load_data("drug_file.csv", "reac_file.csv")
    
    # Compute PRR for multiple pairs
    results = db.compute_all_prrs(
        limit_drugs=10,
        limit_reactions=10,
        min_reports=1
    )
    
    # Display results
    db.print_results(results, limit=15)
    db.print_statistics(results)
""")
    
    print_section("Step 3: Run Examples")
    
    print("""
The easiest way to see the analyzer in action:

    python3 faers_prr_analyzer.py

This will:
  1. Load your FAERS data
  2. Compute PRR for 10 drugs × 10 reactions
  3. Display results in a formatted table
  4. Show statistical summary

For more comprehensive examples:

    python3 faers_examples.py

This runs 5 different examples demonstrating:
  - Basic usage
  - Computing specific drug-reaction pairs
  - Filtering and analyzing results
  - Batch analysis with different parameters
  - Performance timing measurements
""")
    
    print_section("Step 4: Run Unit Tests")
    
    print("""
Verify the implementation with unit tests:

    python3 test_faers_prr.py

This runs tests for:
  - ADRReport dataclass
  - ContingencyTable calculations
  - PRRResult structure
  - FAERSDatabase operations
  - PRR computation accuracy
  - Statistical calculations
  - Integration workflows
""")
    
    print_section("Step 5: Understanding Output")
    
    print("""
The results are displayed in a table format:

  # Drug                   Reaction               PRR      a    b    c    d
  1 ASPIRIN               HEADACHE               2.5043*  45   85   20   1050
  2 IBUPROFEN             PAIN                   2.1230*  38   92   25   1045

Legend:
  * = Significant (PRR >= 2.0)
  a = Drug AND Reaction
  b = Drug only
  c = Reaction only  
  d = Neither

Statistical Summary shows:
  - Total pairs analyzed
  - Number of significant pairs
  - PRR statistics (mean, median, stdev, min, max)
""")
    
    print_section("Step 6: Key Concepts")
    
    print("""
PROPORTIONAL REPORTING RATIO (PRR):

  PRR = (a/(a+b)) / (c/(c+d))

Interpretation:
  - PRR = 1.0: No association (observed as expected)
  - PRR > 1.0: Positive association (more reports than expected)
  - PRR >= 2.0: Generally considered statistically significant
  - PRR < 1.0: Negative association (fewer reports than expected)

CONTINGENCY TABLE:
  
                    With Reaction    Without Reaction
  With Drug              a                  b
  Without Drug           c                  d
  
  Total = a + b + c + d
""")
    
    print_section("Step 7: Common Tasks")
    
    print("""
1. COMPUTE PRR FOR SPECIFIC PAIR:
   
   result = db.compute_prr("ASPIRIN", "HEADACHE")
   if result:
       print(f"PRR: {result.prr:.4f}")

2. GET ALL SIGNIFICANT ASSOCIATIONS:
   
   significant = [r for r in results if r.significant]
   
3. FIND STRONGEST ASSOCIATIONS:
   
   results.sort(key=lambda x: x.prr, reverse=True)
   for result in results[:10]:
       print(f"{result.drug}: {result.reaction} (PRR={result.prr:.2f})")

4. FILTER BY MINIMUM REPORTS:
   
   filtered = [r for r in results if r.contingency.a >= 10]

5. GET DETAILED STATISTICS:
   
   stats = db.get_statistics(results)
   print(f"Mean PRR: {stats['mean']:.4f}")
   print(f"Max PRR: {stats['max']:.4f}")
""")
    
    print_section("Step 8: Customization")
    
    print("""
MODIFY PARAMETERS:

Change the number of drugs and reactions analyzed:
  
  results = db.compute_all_prrs(
      limit_drugs=20,        # Analyze up to 20 drugs
      limit_reactions=20,    # Analyze up to 20 reactions
      min_reports=5          # Only include if >= 5 reports
  )

FILTER RESULTS:

By statistical significance:
  significant = [r for r in results if r.prr >= 2.0]

By specific drug or reaction:
  aspirin_results = [r for r in results if r.drug == "ASPIRIN"]

By report count:
  high_freq = [r for r in results if r.contingency.a >= 100]
""")
    
    print_section("Step 9: Performance Expectations")
    
    print("""
Typical performance on quarterly FAERS data:

  Loading data:                    < 1 second
  Computing 50 drug-reaction pairs:   < 0.5 seconds
  Computing 100+ pairs:                < 2 seconds
  Generating statistics:             < 0.1 seconds
  
Total analysis time for 100 pairs:  ~2 seconds

Memory usage (100k+ reports):      ~100-200 MB

This is MUCH faster than Spark for small datasets,
but Spark scales better for very large datasets (>10GB).
""")
    
    print_section("Step 10: Next Steps")
    
    print("""
1. Read the full documentation:
   → Open PYTHON_OOP_README.md
   
2. Review the code structure:
   → faers_prr_analyzer.py (main module)
   
3. Study working examples:
   → faers_examples.py (5 comprehensive examples)
   
4. Understand the implementation:
   → test_faers_prr.py (unit tests with usage patterns)
   
5. Customize for your needs:
   → Modify faers_prr_analyzer.py for custom analysis
   → Extend classes for additional functionality
   
6. Compare with Spark version:
   → Run spark_prr.py for distributed comparison
   → Use compare_performance.py for benchmarking
""")
    
    print_section("Command Cheat Sheet")
    
    print("""
# Run basic analysis
python3 faers_prr_analyzer.py

# Run comprehensive examples
python3 faers_examples.py

# Run unit tests
python3 test_faers_prr.py

# Run Spark version (distributed)
python3 spark_prr.py

# Compare performance
python3 compare_performance.py

# Read documentation
cat PYTHON_OOP_README.md
""")
    
    print_section("Troubleshooting")
    
    print("""
ISSUE: "FileNotFoundError: drug_file.csv"
SOLUTION: Ensure CSV files are in the same directory as the script

ISSUE: "No results returned"
SOLUTION: Check that min_reports threshold isn't too high
          or limit_drugs/limit_reactions parameters

ISSUE: "Computation is slow"
SOLUTION: This is normal for large datasets on single machine
          Consider using Spark version for massive datasets

ISSUE: "Out of memory error"
SOLUTION: Reduce limit_drugs/limit_reactions
          or filter results before analysis
          
For help, read: PYTHON_OOP_README.md
""")
    
    print_section("✓ Quick Start Complete!")
    
    print("""
You're now ready to use the FAERS PRR Analyzer!

Recommended next step:
  python3 faers_prr_analyzer.py

This will load your data and compute the first set of results.
""")


if __name__ == "__main__":
    main()
