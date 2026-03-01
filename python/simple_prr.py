"""
FAERS Drug Safety Analysis - Simple Version
=============================================

This program helps analyze drug safety reports from the FDA.

What does it do?
1. Reads reports about drugs and their side effects
2. Counts how often side effects happen with each drug
3. Calculates a "safety score" called PRR
4. Shows which drug-side effect combinations are risky

Think of it this way:
- If Drug A causes headaches in 50% of people
- But Drug B only causes headaches in 10% of people
- Then Drug A is 5 times more risky for headaches!
- The PRR score would be 5.0

Created: February 2026
For: 10th Grade Science Fair
"""

import csv
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


@dataclass
class DrugReport:
    """
    Stores ONE drug side effect report.
    
    Like a form that records:
    - case_id: A unique number for this report
    - person_id: Another ID for the person
    - drug_name: What drug they took
    - side_effect: What bad thing happened
    
    Example:
    DrugReport("12345", "001", "ASPIRIN", "HEADACHE")
    """
    case_id: str
    person_id: str
    drug_name: str
    side_effect: str


@dataclass
class SafetyTable:
    """
    A simple table to count people in 4 groups.
    
    Imagine we're checking if Aspirin causes headaches:
    
    group_a = People who took aspirin AND got headaches
    group_b = People who took aspirin but NO headaches
    group_c = People who didn't take aspirin but got headaches
    group_d = People who didn't take aspirin and no headaches
    
    We use these 4 numbers to calculate PRR.
    """
    group_a: int  # drug + side effect
    group_b: int  # drug + no side effect
    group_c: int  # no drug + side effect
    group_d: int  # no drug + no side effect


@dataclass
class SafetyScore:
    """
    The ANSWER from our safety calculation.
    
    Shows us how risky a drug-side effect combination is.
    
    How to read it:
    - prr = 1.0 means normal risk
    - prr = 2.0 means twice as risky
    - prr = 5.0 means 5 times as risky
    """
    drug_name: str
    side_effect: str
    table: SafetyTable
    prr: Optional[float]  # The safety score
    is_important: bool    # True if PRR >= 2.0


class DrugSafetyDatabase:
    """
    A simple database to analyze drug safety reports.
    
    This class:
    1. Loads drug and side effect data from CSV files
    2. Counts how often each combo appears
    3. Calculates PRR scores
    """
    
    def __init__(self):
        """Create an empty database"""
        self.reports: List[DrugReport] = []
        self.drug_side_effect_count: Dict[Tuple[str, str], int] = defaultdict(int)
        self.drug_total_count: Dict[str, int] = defaultdict(int)
        self.side_effect_total_count: Dict[str, int] = defaultdict(int)
        self.total_reports: int = 0
        self.data_loaded: bool = False
        self.load_time: float = 0
    
    def load_data(self, drug_file: str, side_effect_file: str) -> None:
        """
        Load data from two CSV files and combine them.
        
        Args:
            drug_file: Path to drug data file (uses $ as separator)
            side_effect_file: Path to side effect data file (uses $ as separator)
        """
        print("\n" + "="*60)
        print("LOADING DRUG SAFETY DATA")
        print("="*60)
        
        start_time = time.time()
        
        try:
            # Step 1: Load drug data into a dictionary
            print(f"Loading drugs from: {drug_file}")
            drug_data = {}
            with open(drug_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='$')
                for row in reader:
                    key = (row['caseid'], row['primaryid'])
                    drug_data[key] = row.get('drugname', 'UNKNOWN')
            
            print(f"  ✓ Loaded {len(drug_data)} drug records")
            
            # Step 2: Load side effect data and match with drugs
            print(f"Loading side effects from: {side_effect_file}")
            matched_count = 0
            with open(side_effect_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='$')
                for row in reader:
                    key = (row['caseid'], row['primaryid'])
                    
                    # Only use if we have matching drug record
                    if key in drug_data:
                        report = DrugReport(
                            case_id=row['caseid'],
                            person_id=row['primaryid'],
                            drug_name=drug_data[key],
                            side_effect=row.get('pt', 'UNKNOWN')
                        )
                        
                        self.reports.append(report)
                        
                        # Count occurrences
                        pair = (report.drug_name, report.side_effect)
                        self.drug_side_effect_count[pair] += 1
                        self.drug_total_count[report.drug_name] += 1
                        self.side_effect_total_count[report.side_effect] += 1
                        
                        matched_count += 1
            
            print(f"  ✓ Loaded {matched_count} side effect records")
            
            # Save results
            self.total_reports = len(self.reports)
            self.data_loaded = True
            self.load_time = time.time() - start_time
            
            # Print summary
            print("\n" + "="*60)
            print("DATA LOADED SUCCESSFULLY!")
            print("="*60)
            print(f"Total reports: {self.total_reports:,}")
            print(f"Different drugs: {len(self.drug_total_count):,}")
            print(f"Different side effects: {len(self.side_effect_total_count):,}")
            print(f"Loading took: {self.load_time:.4f} seconds")
            
        except FileNotFoundError as e:
            print(f"ERROR: Could not find file: {e}")
            raise
    
    def calculate_prr(self, drug_name: str, side_effect: str) -> Optional[SafetyScore]:
        """
        Calculate PRR for one drug-side effect pair.
        
        Formula:
        PRR = (a/(a+b)) / (c/(c+d))
        
        Where:
        a = people who took drug AND got side effect
        b = people who took drug but NO side effect
        c = people who didn't take drug but got side effect
        d = people who didn't take drug and no side effect
        
        Args:
            drug_name: Name of the drug
            side_effect: Name of the side effect
        
        Returns:
            SafetyScore object with the PRR value
        """
        # Count: a - people with both drug and side effect
        a = self.drug_side_effect_count.get((drug_name, side_effect), 0)
        
        if a == 0:
            return None  # No data for this combination
        
        # Count: b - people with drug but no side effect
        total_drug_users = self.drug_total_count.get(drug_name, 0)
        b = total_drug_users - a
        
        # Count: c - people with side effect but no drug
        total_side_effect_cases = self.side_effect_total_count.get(side_effect, 0)
        c = total_side_effect_cases - a
        
        # Count: d - people with neither
        d = self.total_reports - a - b - c
        
        if d < 0:
            return None
        
        # Calculate PRR
        if (a + b) > 0 and (c + d) > 0:
            prr = (a / (a + b)) / (c / (c + d))
        else:
            prr = None
        
        # Create the safety score
        table = SafetyTable(group_a=a, group_b=b, group_c=c, group_d=d)
        score = SafetyScore(
            drug_name=drug_name,
            side_effect=side_effect,
            table=table,
            prr=prr,
            is_important=(prr >= 2.0 if prr else False)  # Flag if 2x or more risky
        )
        
        return score
    
    def analyze_top_drugs(self, num_drugs: int = 5, num_side_effects: int = 5) -> List[SafetyScore]:
        """
        Calculate PRR for the most common drug-side effect pairs.
        
        Args:
            num_drugs: How many drugs to check
            num_side_effects: How many side effects to check
        
        Returns:
            List of SafetyScore objects sorted by PRR (highest first)
        """
        if not self.data_loaded:
            raise ValueError("You must load data first!")
        
        print("\n" + "="*60)
        print("CALCULATING SAFETY SCORES")
        print("="*60)
        
        start_time = time.time()
        
        # Get top drugs and side effects
        top_drugs = sorted(self.drug_total_count.items(), 
                          key=lambda x: x[1], reverse=True)
        top_drugs = [d[0] for d in top_drugs[:num_drugs]]
        
        top_side_effects = sorted(self.side_effect_total_count.items(),
                                 key=lambda x: x[1], reverse=True)
        top_side_effects = [s[0] for s in top_side_effects[:num_side_effects]]
        
        print(f"Checking {len(top_drugs)} drugs × {len(top_side_effects)} side effects")
        print(f"Total combinations: {len(top_drugs) * len(top_side_effects)}")
        
        results = []
        
        # Calculate PRR for each combination
        for drug in top_drugs:
            for side_effect in top_side_effects:
                score = self.calculate_prr(drug, side_effect)
                if score:
                    results.append(score)
        
        # Sort by PRR (highest first)
        results.sort(key=lambda x: x.prr if x.prr else 0, reverse=True)
        
        calc_time = time.time() - start_time
        print(f"✓ Calculated {len(results)} scores in {calc_time:.4f} seconds")
        
        return results
    
    def print_results(self, results: List[SafetyScore], num_to_show: int = 10) -> None:
        """
        Print the safety scores in a nice table.
        
        Args:
            results: List of SafetyScore objects
            num_to_show: How many to display
        """
        print("\n" + "="*60)
        print("TOP 10 RISKY DRUG-SIDE EFFECT COMBINATIONS")
        print("="*60)
        
        if not results:
            print("No results to show")
            return
        
        # Print header
        print(f"{'#':<3} {'DRUG':<20} {'SIDE EFFECT':<20} {'RISK SCORE':<12} {'STATUS'}")
        print("-" * 60)
        
        # Print results
        for i, score in enumerate(results[:num_to_show], 1):
            status = "⚠️  IMPORTANT!" if score.is_important else "Normal"
            print(f"{i:<3} {score.drug_name[:19]:<20} {score.side_effect[:19]:<20} "
                  f"{score.prr:<12.2f} {status}")
        
        print(f"\nPRR Meaning:")
        print(f"  1.0 = Normal risk")
        print(f"  2.0 = 2 times more risky")
        print(f"  5.0 = 5 times more risky")
    
    def print_statistics(self, results: List[SafetyScore]) -> None:
        """
        Print summary statistics about the results.
        
        Args:
            results: List of SafetyScore objects
        """
        if not results:
            print("No results available")
            return
        
        prr_values = [r.prr for r in results if r.prr is not None]
        
        if not prr_values:
            return
        
        # Calculate statistics
        average = sum(prr_values) / len(prr_values)
        prr_values_sorted = sorted(prr_values)
        middle = len(prr_values_sorted) // 2
        median = prr_values_sorted[middle]
        
        print("\n" + "="*60)
        print("STATISTICS")
        print("="*60)
        print(f"Total combinations checked: {len(results)}")
        print(f"Important combinations (PRR >= 2.0): {sum(1 for r in results if r.is_important)}")
        print(f"\nPRR Score Statistics:")
        print(f"  Average:  {average:.2f}")
        print(f"  Median:   {median:.2f}")
        print(f"  Highest:  {max(prr_values):.2f}")
        print(f"  Lowest:   {min(prr_values):.2f}")


# Main program
def main():
    """Run the drug safety analysis"""
    
    print("\n" + "="*60)
    print("🏥 FAERS DRUG SAFETY ANALYSIS")
    print("FDA Adverse Event Reporting System")
    print("="*60)
    
    # Set up the database
    db = DrugSafetyDatabase()
    
    # Load the data
    try:
        db.load_data(
            "drug_file.csv",
            "reac_file.csv"
        )
    except FileNotFoundError:
        print("\nERROR: Make sure drug_file.csv and reac_file.csv are in the same folder!")
        print("You can download them from the FDA FAERS website.")
        return
    
    # Analyze the top drugs and side effects
    results = db.analyze_top_drugs(num_drugs=5, num_side_effects=5)
    
    # Show the results
    db.print_results(results, num_to_show=10)
    db.print_statistics(results)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    main()
