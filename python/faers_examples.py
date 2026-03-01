"""
Example usage and testing of the FAERS PRR Analyzer
Demonstrates all features of the non-distributed OOP implementation
"""

from faers_prr_analyzer import FAERSDatabase, PRRResult
import time


def example_basic_usage():
    """Basic usage example"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)
    
    # Initialize and load data
    db = FAERSDatabase()
    db.load_data("drug_file.csv", "reac_file.csv")
    
    # Compute PRR for all available pairs
    results = db.compute_all_prrs(limit_drugs=5, limit_reactions=5)
    
    # Display results
    db.print_results(results, limit=10)
    db.print_statistics(results)


def example_specific_pair():
    """Example of computing PRR for a specific drug-reaction pair"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Compute PRR for Specific Drug-Reaction Pair")
    print("="*80)
    
    db = FAERSDatabase()
    db.load_data("drug_file.csv", "reac_file.csv")
    
    # Get first drug and reaction from loaded data
    if db.drug_counts and db.reaction_counts:
        drug = list(db.drug_counts.keys())[0]
        reaction = list(db.reaction_counts.keys())[0]
        
        print(f"\nComputing PRR for: {drug} - {reaction}")
        
        result = db.compute_prr(drug, reaction)
        
        if result:
            print(f"\nResult:")
            print(f"  Drug: {result.drug}")
            print(f"  Reaction: {result.reaction}")
            print(f"  PRR: {result.prr:.4f}")
            print(f"  Contingency Table:")
            print(f"    a (drug + reaction): {result.contingency.a}")
            print(f"    b (drug only): {result.contingency.b}")
            print(f"    c (reaction only): {result.contingency.c}")
            print(f"    d (neither): {result.contingency.d}")
            print(f"  Significant (PRR >= 2.0): {'Yes' if result.significant else 'No'}")
        else:
            print("  No data available for this pair")


def example_filtering():
    """Example of filtering results"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Filtering and Analyzing Results")
    print("="*80)
    
    db = FAERSDatabase()
    db.load_data("drug_file.csv", "reac_file.csv")
    
    # Compute PRR with minimum reports threshold
    results = db.compute_all_prrs(limit_drugs=8, limit_reactions=8, min_reports=2)
    
    print(f"\nTotal results: {len(results)}")
    
    # Filter for significant results
    significant = [r for r in results if r.significant]
    print(f"Significant results (PRR >= 2.0): {len(significant)}")
    
    if significant:
        print("\nTop significant associations:")
        print(f"{'#':<4} {'Drug':<25} {'Reaction':<25} {'PRR':<8}")
        print("-" * 80)
        for i, result in enumerate(significant[:5], 1):
            print(f"{i:<4} {result.drug[:24]:<25} {result.reaction[:24]:<25} {result.prr:<8.4f}")


def example_batch_analysis():
    """Example of batch analysis with multiple parameter sets"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Batch Analysis with Different Parameters")
    print("="*80)
    
    db = FAERSDatabase()
    db.load_data("drug_file.csv", "reac_file.csv")
    
    # Test different parameters
    params = [
        {"limit_drugs": 3, "limit_reactions": 3, "min_reports": 1},
        {"limit_drugs": 5, "limit_reactions": 5, "min_reports": 2},
        {"limit_drugs": 10, "limit_reactions": 10, "min_reports": 3},
    ]
    
    for i, param in enumerate(params, 1):
        print(f"\n--- Parameter Set {i}: drugs={param['limit_drugs']}, "
              f"reactions={param['limit_reactions']}, min_reports={param['min_reports']} ---")
        
        results = db.compute_all_prrs(**param)
        stats = db.get_statistics(results)
        
        if stats:
            print(f"Results: {stats['count']} pairs, "
                  f"Significant: {stats['significant_count']}, "
                  f"Max PRR: {stats['max']:.4f}")


def example_performance_timing():
    """Example measuring performance of different operations"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Performance Timing Analysis")
    print("="*80)
    
    db = FAERSDatabase()
    
    # Time data loading
    print("\nTiming data loading...")
    load_start = time.time()
    db.load_data("drug_file.csv", "reac_file.csv")
    load_time = time.time() - load_start
    
    # Time PRR computation
    print("Timing PRR computation (10 drugs × 10 reactions)...")
    compute_start = time.time()
    results = db.compute_all_prrs(limit_drugs=10, limit_reactions=10)
    compute_time = time.time() - compute_start
    
    # Time result analysis
    print("Timing result analysis...")
    analysis_start = time.time()
    stats = db.get_statistics(results)
    analysis_time = time.time() - analysis_start
    
    # Print timing results
    print(f"\n{'='*80}")
    print("TIMING RESULTS")
    print(f"{'='*80}")
    print(f"Data loading time:      {load_time:.4f} seconds")
    print(f"PRR computation time:   {compute_time:.4f} seconds")
    print(f"Result analysis time:   {analysis_time:.4f} seconds")
    print(f"Total time:             {load_time + compute_time + analysis_time:.4f} seconds")
    print(f"\nData points:")
    print(f"  Total reports: {db.total_reports:,}")
    print(f"  Unique drugs: {len(db.drug_counts):,}")
    print(f"  Unique reactions: {len(db.reaction_counts):,}")


def main():
    """Run all examples"""
    print("\n" + "="*80)
    print("FAERS PRR ANALYZER - Usage Examples")
    print("="*80)
    
    try:
        example_basic_usage()
        example_specific_pair()
        example_filtering()
        example_batch_analysis()
        example_performance_timing()
        
        print("\n" + "="*80)
        print("✓ All examples completed successfully!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
