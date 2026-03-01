"""
Performance Comparison: Distributed Spark vs Non-distributed OOP
Measures execution time and displays performance metrics
"""

import subprocess
import time
import sys


def run_spark_prr():
    """Run the Spark PRR implementation"""
    print("\n" + "="*80)
    print("RUNNING SPARK PRR IMPLEMENTATION")
    print("="*80)
    
    start = time.time()
    result = subprocess.run([sys.executable, "spark_prr.py"], capture_output=True, text=True)
    spark_time = time.time() - start
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return spark_time


def run_oop_prr():
    """Run the OOP PRR implementation"""
    print("\n" + "="*80)
    print("RUNNING OOP PRR IMPLEMENTATION")
    print("="*80)
    
    start = time.time()
    result = subprocess.run([sys.executable, "oop_prr.py"], capture_output=True, text=True)
    oop_time = time.time() - start
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return oop_time


def main():
    """Run both implementations and compare performance"""
    print("\n" + "="*80)
    print("PERFORMANCE COMPARISON: SPARK vs OOP PRR")
    print("="*80)
    
    # Run implementations
    spark_time = run_spark_prr()
    oop_time = run_oop_prr()
    
    # Display comparison
    print("\n" + "="*80)
    print("PERFORMANCE RESULTS")
    print("="*80)
    print(f"\nSpark (Distributed) execution time: {spark_time:.4f} seconds")
    print(f"OOP (Non-distributed) execution time: {oop_time:.4f} seconds")
    
    if oop_time > 0:
        speedup = oop_time / spark_time
        print(f"\nSpeedup factor: {speedup:.2f}x")
        
        if spark_time < oop_time:
            print(f"✓ Spark is {speedup:.2f}x FASTER than OOP")
        else:
            print(f"✓ OOP is {1/speedup:.2f}x FASTER than Spark")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total execution time: {spark_time + oop_time:.4f} seconds")
    print("\nNote: For this small dataset, OOP may be faster due to Spark's")
    print("startup overhead. Spark's advantage becomes apparent with larger datasets.")
    print("="*80)


if __name__ == "__main__":
    main()
