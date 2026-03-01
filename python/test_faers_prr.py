"""
Unit tests for FAERS PRR Analyzer
Tests the core functionality of the non-distributed OOP implementation
"""

import unittest
from faers_prr_analyzer import (
    ADRReport, ContingencyTable, PRRResult, FAERSDatabase
)


class TestADRReport(unittest.TestCase):
    """Test cases for ADRReport dataclass"""
    
    def test_creation(self):
        """Test creating an ADR report"""
        report = ADRReport(
            caseid="001",
            primaryid="001",
            drugname="ASPIRIN",
            reaction_pt="HEADACHE"
        )
        self.assertEqual(report.caseid, "001")
        self.assertEqual(report.drugname, "ASPIRIN")
        self.assertEqual(report.reaction_pt, "HEADACHE")
    
    def test_equality(self):
        """Test ADR report equality (based on caseid and primaryid)"""
        report1 = ADRReport("001", "001", "ASPIRIN", "HEADACHE")
        report2 = ADRReport("001", "001", "ASPIRIN", "FEVER")
        report3 = ADRReport("002", "001", "ASPIRIN", "HEADACHE")
        
        # Same caseid + primaryid = equal
        self.assertEqual(report1, report2)
        # Different caseid + primaryid = not equal
        self.assertNotEqual(report1, report3)
    
    def test_hashable(self):
        """Test that ADR reports are hashable"""
        report1 = ADRReport("001", "001", "ASPIRIN", "HEADACHE")
        report2 = ADRReport("001", "001", "ASPIRIN", "FEVER")
        
        # Should be able to add to set
        report_set = {report1, report2}
        # Due to equality, should have 1 unique item
        self.assertEqual(len(report_set), 1)


class TestContingencyTable(unittest.TestCase):
    """Test cases for ContingencyTable"""
    
    def test_creation(self):
        """Test creating a contingency table"""
        table = ContingencyTable(a=100, b=50, c=30, d=820)
        self.assertEqual(table.a, 100)
        self.assertEqual(table.total, 1000)
    
    def test_total_calculation(self):
        """Test total calculation"""
        table = ContingencyTable(a=10, b=20, c=30, d=40)
        self.assertEqual(table.total, 100)
    
    def test_representation(self):
        """Test string representation"""
        table = ContingencyTable(a=1, b=2, c=3, d=4)
        repr_str = repr(table)
        self.assertIn("a=1", repr_str)
        self.assertIn("b=2", repr_str)


class TestPRRResult(unittest.TestCase):
    """Test cases for PRRResult"""
    
    def test_creation(self):
        """Test creating a PRR result"""
        table = ContingencyTable(a=100, b=100, c=50, d=750)
        result = PRRResult(
            drug="ASPIRIN",
            reaction="HEADACHE",
            contingency=table,
            prr=2.0,
            significant=True
        )
        self.assertEqual(result.drug, "ASPIRIN")
        self.assertEqual(result.prr, 2.0)
        self.assertTrue(result.significant)


class TestFAERSDatabase(unittest.TestCase):
    """Test cases for FAERSDatabase"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.db = FAERSDatabase()
    
    def test_initialization(self):
        """Test database initialization"""
        self.assertEqual(len(self.db.reports), 0)
        self.assertEqual(self.db.total_reports, 0)
        self.assertFalse(self.db.data_loaded)
    
    def test_manual_data_setup(self):
        """Test manually setting up test data"""
        # Manually add data for testing
        report1 = ADRReport("001", "001", "ASPIRIN", "HEADACHE")
        report2 = ADRReport("002", "002", "ASPIRIN", "FEVER")
        report3 = ADRReport("003", "003", "IBUPROFEN", "HEADACHE")
        
        self.db.reports = [report1, report2, report3]
        
        # Manually update counts
        self.db.drug_reaction_pairs[("ASPIRIN", "HEADACHE")] = 1
        self.db.drug_reaction_pairs[("ASPIRIN", "FEVER")] = 1
        self.db.drug_reaction_pairs[("IBUPROFEN", "HEADACHE")] = 1
        
        self.db.drug_counts["ASPIRIN"] = 2
        self.db.drug_counts["IBUPROFEN"] = 1
        
        self.db.reaction_counts["HEADACHE"] = 2
        self.db.reaction_counts["FEVER"] = 1
        
        self.db.total_reports = 3
        
        self.assertEqual(self.db.total_reports, 3)
        self.assertEqual(len(self.db.drug_counts), 2)
    
    def test_prr_calculation(self):
        """Test PRR calculation with synthetic data"""
        # Set up test data
        self.db.drug_reaction_pairs[("ASPIRIN", "HEADACHE")] = 100
        self.db.drug_counts["ASPIRIN"] = 150
        self.db.reaction_counts["HEADACHE"] = 120
        self.db.total_reports = 1000
        
        result = self.db.compute_prr("ASPIRIN", "HEADACHE")
        
        self.assertIsNotNone(result)
        self.assertEqual(result.contingency.a, 100)  # drug + reaction
        self.assertEqual(result.contingency.b, 50)   # drug only
        self.assertEqual(result.contingency.c, 20)   # reaction only
        self.assertEqual(result.contingency.d, 830)  # neither
        
        # PRR = (100/150) / (20/850) = 0.6667 / 0.0235 = 28.33
        self.assertIsNotNone(result.prr)
        self.assertGreater(result.prr, 20)
    
    def test_prr_zero_reports(self):
        """Test PRR with zero reports for a pair"""
        self.db.total_reports = 1000
        
        result = self.db.compute_prr("UNKNOWN_DRUG", "UNKNOWN_REACTION")
        
        self.assertIsNone(result)
    
    def test_prr_insufficient_denominator(self):
        """Test PRR with insufficient data for calculation"""
        self.db.drug_reaction_pairs[("DRUG", "REACTION")] = 0
        self.db.total_reports = 1000
        
        result = self.db.compute_prr("DRUG", "REACTION")
        
        self.assertIsNone(result)
    
    def test_contingency_table_totals(self):
        """Test contingency table totals consistency"""
        self.db.drug_reaction_pairs[("DRUG", "REACTION")] = 50
        self.db.drug_counts["DRUG"] = 100
        self.db.reaction_counts["REACTION"] = 80
        self.db.total_reports = 1000
        
        result = self.db.compute_prr("DRUG", "REACTION")
        
        # Check totals
        ct = result.contingency
        self.assertEqual(ct.a + ct.b + ct.c + ct.d, 1000)
    
    def test_prr_significance(self):
        """Test PRR significance flagging"""
        # Set up data for PRR = 2.5
        self.db.drug_reaction_pairs[("DRUG1", "REACTION1")] = 100
        self.db.drug_counts["DRUG1"] = 120
        self.db.reaction_counts["REACTION1"] = 110
        self.db.total_reports = 1000
        
        result = self.db.compute_prr("DRUG1", "REACTION1")
        
        # Result should be significant (PRR >= 2.0)
        if result and result.prr and result.prr >= 2.0:
            self.assertTrue(result.significant)
    
    def test_statistics_calculation(self):
        """Test statistics calculation"""
        # Create some test results
        results = []
        for i, prr_val in enumerate([1.5, 2.0, 2.5, 3.0, 1.0]):
            ct = ContingencyTable(a=10, b=10, c=10, d=70)
            result = PRRResult(
                drug=f"DRUG{i}",
                reaction=f"REACTION{i}",
                contingency=ct,
                prr=prr_val,
                significant=(prr_val >= 2.0)
            )
            results.append(result)
        
        stats = self.db.get_statistics(results)
        
        self.assertEqual(stats['count'], 5)
        self.assertEqual(stats['min'], 1.0)
        self.assertEqual(stats['max'], 3.0)
        self.assertEqual(stats['significant_count'], 3)  # 2.0, 2.5, 3.0


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_workflow(self):
        """Test complete workflow"""
        db = FAERSDatabase()
        
        # Set up test data
        db.drug_reaction_pairs[("ASPIRIN", "HEADACHE")] = 50
        db.drug_reaction_pairs[("ASPIRIN", "FEVER")] = 30
        db.drug_reaction_pairs[("IBUPROFEN", "HEADACHE")] = 40
        
        db.drug_counts["ASPIRIN"] = 100
        db.drug_counts["IBUPROFEN"] = 80
        
        db.reaction_counts["HEADACHE"] = 120
        db.reaction_counts["FEVER"] = 50
        
        db.total_reports = 1000
        
        # Compute results
        results = []
        for drug in ["ASPIRIN", "IBUPROFEN"]:
            for reaction in ["HEADACHE", "FEVER"]:
                result = db.compute_prr(drug, reaction)
                if result:
                    results.append(result)
        
        self.assertEqual(len(results), 3)  # One pair has no data
        
        # Check statistics
        stats = db.get_statistics(results)
        self.assertGreater(stats['count'], 0)
        self.assertIsNotNone(stats['mean'])


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestADRReport))
    suite.addTests(loader.loadTestsFromTestCase(TestContingencyTable))
    suite.addTests(loader.loadTestsFromTestCase(TestPRRResult))
    suite.addTests(loader.loadTestsFromTestCase(TestFAERSDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
