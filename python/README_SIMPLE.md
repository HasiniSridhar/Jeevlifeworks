# 🏥 Drug Safety Analysis Project
## A 10th Grade Science Fair Project

---

## 📚 What is This Project?

This is a program that analyzes **drug safety data** from the FDA (Food and Drug Administration).

Imagine the FDA gets hundreds of thousands of reports about drugs and their side effects. Doctors report things like:
- "Patient took Aspirin and got a headache"
- "Patient took Tylenol and had stomach pain"

We need to figure out: **Which side effects happen most often with which drugs?**

That's what this project does!

---

## 🎯 The Main Idea: PRR (Proportional Reporting Ratio)

### Simple Analogy

Imagine two stores:

**Store A:**
- 100 customers buy apples
- 50 customers get sick

**Store B:**
- 100 customers buy apples
- 10 customers get sick

Which store has the problem? **Store A is 5 times more likely to have sick customers!**

That ratio (5x) is similar to what we call **PRR**.

### The Real Definition

**PRR = Risk with Drug / Risk without Drug**

In math form:
```
PRR = (a/(a+b)) / (c/(c+d))
```

Where:
- **a** = people who took drug AND got side effect
- **b** = people who took drug but NO side effect
- **c** = people who didn't take drug but got side effect  
- **d** = people who didn't take drug and no side effect

### How to Read PRR Scores

- **PRR = 1.0** → Same risk as normal (the drug doesn't cause the side effect)
- **PRR = 2.0** → 2 times more risky than normal
- **PRR = 5.0** → 5 times more risky than normal
- **PRR = 10.0** → 10 times more risky! (Very dangerous!)

---

## 📊 The Data We Use

We have two CSV files with FDA data:

### drug_file.csv
Contains information about which drugs people took:
```
caseid,primaryid,drugname
12345,001,ASPIRIN
12346,002,TYLENOL
12347,003,IBUPROFEN
```

### reac_file.csv
Contains information about side effects:
```
caseid,primaryid,pt
12345,001,HEADACHE
12346,002,NAUSEA
12347,003,DIZZINESS
```

We match them up by case ID and person ID to connect drugs with side effects.

---

## 🚀 How to Run the Program

### Step 1: Check you have the data files

Make sure you have these two files in the same folder:
- `drug_file.csv`
- `reac_file.csv`

### Step 2: Run the simple version (RECOMMENDED FOR 10TH GRADE)

```bash
python3 simple_prr.py
```

This will:
1. Load the data
2. Count side effects for each drug
3. Calculate PRR scores
4. Show you the riskiest combinations

The output will look like:
```
# DRUG              SIDE EFFECT      RISK SCORE    STATUS
1 ASPIRIN           HEADACHE         4.50          ⚠️  IMPORTANT!
2 TYLENOL           NAUSEA           2.30          ⚠️  IMPORTANT!
3 IBUPROFEN         DIZZINESS        1.80          Normal
```

### Step 3 (Optional): Run the detailed version

```bash
python3 faers_prr_analyzer.py
```

This is more detailed and shows more information.

---

## 📂 Files in This Project

| File | What It Does |
|------|-------------|
| `simple_prr.py` | 🌟 **START HERE!** Simple version for learning |
| `faers_prr_analyzer.py` | More detailed version with extra features |
| `drug_file.csv` | Data about drugs (from FDA) |
| `reac_file.csv` | Data about side effects (from FDA) |
| `test_faers_prr.py` | Tests to make sure code works correctly |

---

## 🎓 What You'll Learn

By doing this project, you'll learn:

✅ **Real-world data analysis** - Doctors and pharmacists use this!  
✅ **Python programming** - Write working code  
✅ **Statistics** - Calculate meaningful numbers from data  
✅ **Data science** - Find patterns in large datasets  
✅ **Drug safety** - How the FDA keeps us safe  

---

## 💡 Example Output

When you run the program, you'll see something like this:

```
============================================================
🏥 FAERS DRUG SAFETY ANALYSIS
FDA Adverse Event Reporting System
============================================================

============================================================
LOADING DRUG SAFETY DATA
============================================================
Loading drugs from: drug_file.csv
  ✓ Loaded 15,000 drug records
Loading side effects from: reac_file.csv
  ✓ Loaded 12,500 side effect records

============================================================
DATA LOADED SUCCESSFULLY!
============================================================
Total reports: 12,500
Different drugs: 250
Different side effects: 180
Loading took: 0.2543 seconds

============================================================
CALCULATING SAFETY SCORES
============================================================
Checking 5 drugs × 5 side effects
Total combinations: 25

✓ Calculated 18 scores in 0.0134 seconds

============================================================
TOP 10 RISKY DRUG-SIDE EFFECT COMBINATIONS
============================================================
# DRUG               SIDE EFFECT          RISK SCORE   STATUS
1 ASPIRIN            HEADACHE             4.50         ⚠️  IMPORTANT!
2 ASPIRIN            NAUSEA               3.20         ⚠️  IMPORTANT!
3 IBUPROFEN          DIZZINESS            2.10         ⚠️  IMPORTANT!
4 TYLENOL            LIVER DAMAGE         1.80         Normal
5 ADVIL              STOMACH PAIN         1.50         Normal

============================================================
STATISTICS
============================================================
Total combinations checked: 18
Important combinations (PRR >= 2.0): 3

PRR Score Statistics:
  Average:  2.45
  Median:   2.10
  Highest:  4.50
  Lowest:   1.05
```

---

## 🔍 Understanding the Results

### What does "⚠️ IMPORTANT!" mean?

If the PRR score is **2.0 or higher**, the combination is marked as important.

This means: **The drug is at least 2 times more likely to cause that side effect than normal.**

This doesn't mean the drug is always bad - just that doctors should watch out for this side effect in patients taking this drug.

### How reliable are these numbers?

The more reports we have (higher 'a' value), the more reliable the PRR score.

If we only have 1 report saying Aspirin caused a headache, that's not very reliable.

If we have 1,000 reports, that's very reliable!

---

## 🤔 Interesting Questions to Think About

After running the program, try to answer these:

1. **Which drug has the most side effects?**
2. **Which side effect is most common?**
3. **Are there any surprising results?**
4. **Why might some drugs have higher PRR scores than others?**

---

## 📖 How the Program Works (Step-by-Step)

### Step 1: Load Drug Data
The program reads `drug_file.csv` and stores each drug report in memory.

### Step 2: Load and Match Side Effect Data
The program reads `reac_file.csv` and matches each side effect to the corresponding drug (using case ID and person ID).

### Step 3: Count Occurrences
The program counts:
- How many times each drug appears
- How many times each side effect appears
- How many times each drug-side effect pair appears

### Step 4: Calculate PRR
For each drug-side effect pair, the program uses the formula:
```
PRR = (a/(a+b)) / (c/(c+d))
```

### Step 5: Display Results
The program sorts the results by PRR (highest first) and displays them in a table.

---

## 🛠️ Troubleshooting

### "ERROR: Could not find file"

**Problem:** The program can't find the CSV files.

**Solution:** 
1. Make sure `drug_file.csv` and `reac_file.csv` are in the same folder as the Python file
2. Check the filenames are spelled correctly (capital letters matter!)

### "No results to show"

**Problem:** The program loaded data but found no matches.

**Solution:**
1. Check that both CSV files have matching case IDs
2. Check that the column names are correct in your CSV files

---

## 📊 Real-World Applications

This same method is used by:

- 🏥 **Hospitals** - To track drug side effects
- 💊 **Pharmaceutical companies** - To find problems early
- 🏛️ **FDA** - To decide if drugs are safe enough
- 🔬 **Pharmacists** - To advise doctors about drug interactions

---

## 🎯 Your Assignment Checklist

- [ ] Download the FDA FAERS data files
- [ ] Save them as `drug_file.csv` and `reac_file.csv`
- [ ] Run `python3 simple_prr.py`
- [ ] Look at the results
- [ ] Answer the interesting questions above
- [ ] Write a summary of what you found
- [ ] Present to your mentor

---

## 📞 Need Help?

If something doesn't work:

1. Check that Python 3 is installed: `python3 --version`
2. Check that the data files are in the right place
3. Copy the error message and look it up on Google
4. Ask your mentor

---

## 🎉 Great Job!

You've completed a real data science project!

This is the kind of work that data scientists and doctors do every day to keep people safe.

**You should be proud! 🌟**

---

*Created: February 2026 | For: 10th Grade Science Fair*
