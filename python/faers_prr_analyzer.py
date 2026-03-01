\
"""
FAERS PRR (Proportional Reporting Ratio) Analyzer
====================================================

This is a simple program to analyze drug safety reports from the FDA.

What does this program do?
- Reads data about drugs and their side effects (called "adverse reactions")
- Counts how often each drug causes each side effect
- Calculates a number called "PRR" that tells us how risky a drug-side effect combination is
- Higher PRR number = more likely the drug causes that side effect

Simple Analogy:
Think of it like this - if 100 people take Drug X and 50 get a headache,
but only 10 people take Drug Y and 5 get a headache,
Drug X seems more likely to cause headaches!

PRR does the math to compare these numbers fairly.

Created: February 2026
For: 10th Grade Science Project
"""

import csv
import time
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict
import statistics


@dataclass
class ADRReport:
    """
    A simple class to store one drug safety report.
    
    Think of it like a form that records:
    - caseid: A number that identifies this report
    - primaryid: Another identifying number
    - drugname: What drug the person took
    - reaction_pt: What bad thing happened (the side effect)
    
    Example:
    Report(caseid="12345", primaryid="001", 
           drugname="ASPIRIN", reaction_pt="HEADACHE")
    """
    caseid: str
    primaryid: str
    drugname: str
    reaction_pt: str
    
    def __hash__(self):
        return hash((self.caseid, self.primaryid))
    
    def __eq__(self, other):
        if not isinstance(other, ADRReport):
            return False
        return (self.caseid == other.caseid and 
                self.primaryid == other.primaryid)


@dataclass
class ContingencyTable:
    """
    A simple 2x2 table to organize drug safety data.
    
    It's like organizing people into 4 groups:
    
    a = People who took the drug AND got the side effect
    b = People who took the drug but did NOT get the side effect
    c = People who did NOT take the drug but got the side effect
    d = People who did NOT take the drug and did NOT get the side effect
    
    Example:
    If we're looking at Aspirin and Headaches:
    a = 50 (took aspirin, got headache)
    b = 950 (took aspirin, no headache)
    c = 10 (didn't take aspirin, got headache)
    d = 9990 (didn't take aspirin, no headache)
    """
    a: int
    b: int
    c: int
    d: int
    
    @property
    def total(self) -> int:
        """Total number of reports"""
        return self.a + self.b + self.c + self.d
    
    def __repr__(self) -> str:
        return f"Table(drug+reaction={self.a}, drug only={self.b}, reaction only={self.c}, neither={self.d})"


@dataclass
class PRRResult:
    """
    The final answer from our PRR calculation.
    
    This tells us:
    - drug: What drug we're looking at
    - reaction: What side effect we're checking
    - prr: The PRR score (higher = more risky)
    - significant: Is this number important? (True if PRR >= 2.0)
    
    How to read a PRR result:
    - PRR = 1.0 means the drug is no more likely to cause the side effect than normal
    - PRR = 2.0 means the drug is twice as likely to cause the side effect
    - PRR = 5.0 means the drug is 5 times as likely to cause the side effect
    """
    drug: str
    reaction: str
    contingency: ContingencyTable
    prr: Optional[float]
    confidence_interval: Tuple[float, float] = field(default=(0.0, 0.0))
    significant: bool = field(default=False)
    
    def __repr__(self) -> str:
        ci_str = f" (95% confident it's between {self.confidence_interval[0]:.2f} and {self.confidence_interval[1]:.2f})"
        sig_str = f" - IMPORTANT!" if self.significant else ""
        return (f"PRR = {self.prr:.2f} for {self.drug} causing {self.reaction}{ci_str}{sig_str}")


class FAERSDatabase:
    """
    Non-distributed FAERS database handler.
    
    This class manages loading, merging, and analyzing FDA FAERS data
    for adverse drug reaction reporting using object-oriented design.
    
    Attributes:
        reports: List of merged ADR reports
        drug_reaction_pairs: Counter for drug-reaction occurrences
        drug_counts: Counter for drug occurrences
        reaction_counts: Counter for reaction occurrences
        total_reports: Total number of merged reports
        data_loaded: Flag indicating if data has been loaded
    """
    
    def __init__(self):
        """Initialize an empty FAERS database"""
        self.reports: List[ADRReport] = []
        self.drug_reaction_pairs: Dict[Tuple[str, str], int] = defaultdict(int)
        self.drug_counts: Dict[str, int] = defaultdict(int)
        self.reaction_counts: Dict[str, int] = defaultdict(int)
        self.total_reports: int = 0
        self.data_loaded: bool = False
        self._start_time = None
        self._load_time = None
    
    def load_data(self, drug_file: str, reac_file: str) -> None:
        """
        Load and merge drug and reaction data from CSV files.
        
        The method loads drug data first, then loads reaction data and matches
        on (caseid, primaryid) to create merged reports.
        
        Args:
            drug_file: Path to drug CSV file (with $ delimiter)
            reac_file: Path to reaction CSV file (with $ delimiter)
        
        Raises:
            FileNotFoundError: If either file doesn't exist
            ValueError: If required columns are missing
        """
        self._start_time = time.time()
        print(f"\n{'='*80}")
        print("LOADING FAERS DATA")
        print(f"{'='*80}")
        print(f"Loading drug data from: {drug_file}")
        print(f"Loading reaction data from: {reac_file}")
        
        try:
            # Load drug data into a dictionary keyed by (caseid, primaryid)
            drugs_data = self._load_drug_file(drug_file)
            print(f"✓ Loaded {len(drugs_data)} unique drug records")
            
            # Load and merge reaction data with drugs
            matched_count = self._load_and_merge_reaction_file(reac_file, drugs_data)
            print(f"✓ Loaded and merged {matched_count} reaction records")
            
            self.total_reports = len(self.reports)
            self.data_loaded = True
            
            self._load_time = time.time() - self._start_time
            
            # Display summary statistics
            self._print_data_summary()
            
        except FileNotFoundError as e:
            print(f"✗ Error: {e}")
            raise
        except ValueError as e:
            print(f"✗ Data format error: {e}")
            raise
    
    def _load_drug_file(self, drug_file: str) -> Dict[Tuple[str, str], str]:
        """Load drug data from CSV file"""
        drugs_data = {}
        with open(drug_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='$')
            
            # Validate required columns
            if reader.fieldnames is None or 'caseid' not in reader.fieldnames:
                raise ValueError("Drug file missing required columns")
            
            for row in reader:
                key = (row['caseid'], row['primaryid'])
                drugs_data[key] = row.get('drugname', 'UNKNOWN')
        
        return drugs_data
    
    def _load_and_merge_reaction_file(self, reac_file: str, 
                                      drugs_data: Dict[Tuple[str, str], str]) -> int:
        """Load reaction data and merge with drug data"""
        matched_count = 0
        with open(reac_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='$')
            
            if reader.fieldnames is None or 'caseid' not in reader.fieldnames:
                raise ValueError("Reaction file missing required columns")
            
            for row in reader:
                key = (row['caseid'], row['primaryid'])
                
                # Only include if we have matching drug record
                if key in drugs_data:
                    report = ADRReport(
                        caseid=row['caseid'],
                        primaryid=row['primaryid'],
                        drugname=drugs_data[key],
                        reaction_pt=row.get('pt', 'UNKNOWN')
                    )
                    
                    self.reports.append(report)
                    
                    # Update frequency counters
                    self.drug_reaction_pairs[(report.drugname, report.reaction_pt)] += 1
                    self.drug_counts[report.drugname] += 1
                    self.reaction_counts[report.reaction_pt] += 1
                    matched_count += 1
        
        return matched_count
    
    def _print_data_summary(self) -> None:
        """Print data loading summary statistics"""
        print(f"\n{'='*80}")
        print("DATA SUMMARY")
        print(f"{'='*80}")
        print(f"Total merged reports: {self.total_reports:,}")
        print(f"Unique drugs: {len(self.drug_counts):,}")
        print(f"Unique reactions: {len(self.reaction_counts):,}")
        print(f"Unique drug-reaction pairs: {len(self.drug_reaction_pairs):,}")
        print(f"Data loading time: {self._load_time:.4f} seconds")
    
    def compute_prr(self, drug: str, reaction: str) -> Optional[PRRResult]:
        """
        Compute PRR for a specific drug-reaction pair.
        
        PRR = (a/(a+b)) / (c/(c+d))
        
        Where:
            a = reports with drug AND reaction
            b = reports with drug but NOT reaction
            c = reports with reaction but NOT drug
            d = reports with neither drug nor reaction
        
        Args:
            drug: Drug name
            reaction: Reaction preferred term
        
        Returns:
            PRRResult object or None if insufficient data
        """
        # Count: a - drug AND reaction
        a = self.drug_reaction_pairs.get((drug, reaction), 0)
        
        if a == 0:
            return None
        
        # Count: b - drug but NOT reaction
        drug_total = self.drug_counts.get(drug, 0)
        b = drug_total - a
        
        # Count: c - reaction but NOT drug
        reaction_total = self.reaction_counts.get(reaction, 0)
        c = reaction_total - a
        
        # Count: d - neither
        d = self.total_reports - a - b - c
        
        # Ensure valid contingency table
        if d < 0:
            return None
        
        contingency = ContingencyTable(a=a, b=b, c=c, d=d)
        
        # Compute PRR
        if (a + b) > 0 and (c + d) > 0:
            prr = (a / (a + b)) / (c / (c + d))
        else:
            prr = None
        
        # Create result object
        result = PRRResult(
            drug=drug,
            reaction=reaction,
            contingency=contingency,
            prr=prr,
            significant=(prr >= 2.0 if prr else False)  # PRR >= 2 often considered significant
        )
        
        return result
    
    def compute_all_prrs(self, limit_drugs: Optional[int] = None, 
                        limit_reactions: Optional[int] = None,
                        min_reports: int = 1) -> List[PRRResult]:
        """
        Compute PRR for all or a subset of drug-reaction pairs.
        
        Args:
            limit_drugs: Maximum number of drugs to include (None for all)
            limit_reactions: Maximum number of reactions to include (None for all)
            min_reports: Minimum number of reports for inclusion
        
        Returns:
            List of PRRResult objects sorted by PRR value (descending)
        """
        if not self.data_loaded:
            raise ValueError("Data must be loaded before computing PRR")
        
        print(f"\n{'='*80}")
        print("COMPUTING PRR VALUES")
        print(f"{'='*80}")
        
        compute_start = time.time()
        
        # Get unique drugs and reactions
        unique_drugs = sorted(self.drug_counts.keys())
        unique_reactions = sorted(self.reaction_counts.keys())
        
        # Apply limits
        if limit_drugs:
            unique_drugs = unique_drugs[:limit_drugs]
        if limit_reactions:
            unique_reactions = unique_reactions[:limit_reactions]
        
        print(f"Computing PRR for {len(unique_drugs)} drugs × {len(unique_reactions)} reactions")
        print(f"Minimum reports threshold: {min_reports}")
        
        results = []
        total_pairs = len(unique_drugs) * len(unique_reactions)
        computed = 0
        
        for drug in unique_drugs:
            for reaction in unique_reactions:
                result = self.compute_prr(drug, reaction)
                
                # Only include if meets minimum threshold
                if result and result.contingency.a >= min_reports:
                    results.append(result)
                    computed += 1
        
        compute_time = time.time() - compute_start
        
        # Sort by PRR value (descending)
        results.sort(key=lambda x: x.prr if x.prr else 0, reverse=True)
        
        print(f"✓ Computed {computed} pairs in {compute_time:.4f} seconds")
        print(f"  (Skipped {total_pairs - computed} pairs due to minimum report threshold)")
        
        return results
    
    def print_results(self, results: List[PRRResult], limit: int = 10) -> None:
        """
        Print PRR results in a formatted table.
        
        Args:
            results: List of PRRResult objects
            limit: Maximum number of results to display
        """
        print(f"\n{'='*80}")
        print("TOP PRR RESULTS")
        print(f"{'='*80}")
        
        if not results:
            print("No results to display")
            return
        
        # Print header
        print(f"{'#':<4} {'Drug':<25} {'Reaction':<25} {'PRR':<8} {'a':<6} {'b':<6} {'c':<6} {'d':<6}")
        print("-" * 80)
        
        # Print top results
        for i, result in enumerate(results[:limit], 1):
            sig = "*" if result.significant else " "
            print(f"{i:<4} {result.drug[:24]:<25} {result.reaction[:24]:<25} "
                  f"{result.prr:<8.4f}{sig} {result.contingency.a:<6} "
                  f"{result.contingency.b:<6} {result.contingency.c:<6} "
                  f"{result.contingency.d:<6}")
        
        print(f"\n* = Statistically significant (PRR >= 2.0)")
        print(f"Total results: {len(results)}")
    
    def get_statistics(self, results: List[PRRResult]) -> Dict[str, float]:
        """
        Calculate statistics for PRR results.
        
        Args:
            results: List of PRRResult objects
        
        Returns:
            Dictionary of statistical metrics
        """
        if not results:
            return {}
        
        prr_values = [r.prr for r in results if r.prr is not None]
        
        if not prr_values:
            return {}
        
        stats = {
            'count': len(prr_values),
            'mean': statistics.mean(prr_values),
            'median': statistics.median(prr_values),
            'stdev': statistics.stdev(prr_values) if len(prr_values) > 1 else 0,
            'min': min(prr_values),
            'max': max(prr_values),
            'significant_count': sum(1 for r in results if r.significant)
        }
        
        return stats
    
    def print_statistics(self, results: List[PRRResult]) -> None:
        """Print statistical summary of PRR results"""
        stats = self.get_statistics(results)
        
        if not stats:
            print("No statistics available")
            return
        
        print(f"\n{'='*80}")
        print("STATISTICAL SUMMARY")
        print(f"{'='*80}")
        print(f"Total drug-reaction pairs analyzed: {stats['count']}")
        print(f"Significant pairs (PRR >= 2.0): {stats['significant_count']}")
        print(f"\nPRR Statistics:")
        print(f"  Mean:    {stats['mean']:.4f}")
        print(f"  Median:  {stats['median']:.4f}")
        print(f"  Std Dev: {stats['stdev']:.4f}")
        print(f"  Min:     {stats['min']:.4f}")
        print(f"  Max:     {stats['max']:.4f}")


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("FAERS PRR ANALYZER - Pure Python OOP Implementation")
    print("="*80)
    
    # Initialize database
    db = FAERSDatabase()
    
    # Load data
    try:
        db.load_data("drug_file.csv", "reac_file.csv")
    except (FileNotFoundError, ValueError) as e:
        print(f"Failed to load data: {e}")
        return
    
    # Compute PRR for sample pairs
    print("\n" + "="*80)
    print("ANALYZING DRUG-REACTION ASSOCIATIONS")
    print("="*80)
    
    results = db.compute_all_prrs(limit_drugs=10, limit_reactions=10, min_reports=1)
    
    # Display results
    db.print_results(results, limit=15)
    
    # Print statistics
    db.print_statistics(results)
    
    print(f"\n{'='*80}")
    print("✓ Analysis Complete!")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
