"""
Non-distributed OOP implementation of PRR (Proportional Reporting Ratio)
This version uses pure Python without Spark for performance comparison
"""

import time
import csv
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class ADRReport:
    """Represents a single adverse drug reaction report"""
    caseid: str
    primaryid: str
    drugname: str
    reaction_pt: str


class FAERSDatabase:
    """Non-distributed FAERS database handler using OOP"""
    
    def __init__(self):
        self.reports = []
        self.drug_reaction_pairs = defaultdict(int)
        self.drug_counts = defaultdict(int)
        self.reaction_counts = defaultdict(int)
        self.total_reports = 0
    
    def load_data(self, drug_file, reac_file):
        """Load drug and reaction files and merge them"""
        print(f"Loading data from {drug_file} and {reac_file}...")
        
        # Load drug data
        drugs_data = {}
        with open(drug_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='$')
            for row in reader:
                key = (row['caseid'], row['primaryid'])
                drugs_data[key] = row['drugname']
        
        # Load reaction data and merge with drugs
        with open(reac_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='$')
            for row in reader:
                key = (row['caseid'], row['primaryid'])
                if key in drugs_data:
                    report = ADRReport(
                        caseid=row['caseid'],
                        primaryid=row['primaryid'],
                        drugname=drugs_data[key],
                        reaction_pt=row['pt']
                    )
                    self.reports.append(report)
                    
                    # Update counts
                    self.drug_reaction_pairs[(report.drugname, report.reaction_pt)] += 1
                    self.drug_counts[report.drugname] += 1
                    self.reaction_counts[report.reaction_pt] += 1
        
        self.total_reports = len(self.reports)
        print(f"✓ Loaded {self.total_reports} merged reports")
        print(f"  Unique drugs: {len(self.drug_counts)}")
        print(f"  Unique reactions: {len(self.reaction_counts)}")
    
    def compute_prr(self, drug, reaction):
        """
        Compute PRR for a specific drug-reaction pair
        PRR = (a/(a+b)) / (c/(c+d))
        where:
            a = reports with drug AND reaction
            b = reports with drug but NOT reaction
            c = reports with reaction but NOT drug
            d = reports with neither drug nor reaction
        """
        a = self.drug_reaction_pairs.get((drug, reaction), 0)
        
        if a == 0:
            return None, None
        
        # Count reports with this drug (regardless of reaction)
        drug_total = self.drug_counts[drug]
        b = drug_total - a
        
        # Count reports with this reaction (regardless of drug)
        reaction_total = self.reaction_counts[reaction]
        c = reaction_total - a
        
        # Reports with neither
        d = self.total_reports - a - b - c
        
        # Compute PRR
        if (a + b) > 0 and (c + d) > 0:
            prr = (a / (a + b)) / (c / (c + d))
        else:
            prr = None
        
        return prr, {'a': a, 'b': b, 'c': c, 'd': d}
    
    def compute_all_prrs(self, limit_drugs=5, limit_reactions=5):
        """Compute PRR for multiple drug-reaction pairs"""
        results = []
        
        # Get unique drugs and reactions
        unique_drugs = list(self.drug_counts.keys())[:limit_drugs]
        unique_reactions = list(self.reaction_counts.keys())[:limit_reactions]
        
        for drug in unique_drugs:
            for reaction in unique_reactions:
                prr, counts = self.compute_prr(drug, reaction)
                if prr is not None:
                    results.append({
                        'drug': drug,
                        'reaction': reaction,
                        'a': counts['a'],
                        'b': counts['b'],
                        'c': counts['c'],
                        'd': counts['d'],
                        'prr': round(prr, 4)
                    })
        
        return results


def main():
    """Main execution"""
    print("\n" + "="*80)
    print("NON-DISTRIBUTED OOP PRR IMPLEMENTATION")
    print("="*80)
    
    start_time = time.time()
    
    # Initialize database
    db = FAERSDatabase()
    
    # Load data
    db.load_data("drug_file.csv", "reac_file.csv")
    
    # Compute PRR for sample pairs
    print("\nComputing PRR values...")
    results = db.compute_all_prrs(limit_drugs=5, limit_reactions=5)
    
    # Display results
    print(f"\nSample PRR Results (first 10):")
    for i, result in enumerate(results[:10]):
        print(f"{i+1}. Drug: {result['drug']}, Reaction: {result['reaction']}, PRR: {result['prr']}")
    
    end_time = time.time()
    oop_time = end_time - start_time
    
    print(f"\n✓ OOP PRR computation completed in {oop_time:.4f} seconds")
    print("="*80)
    
    return oop_time


if __name__ == "__main__":
    main()
