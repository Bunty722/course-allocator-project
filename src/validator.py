import os
import pandas as pd

# Import the output directory from our config
from config import OUTPUT_DIR

def load_data():
    # This reads all our generated CSV files back into Pandas DataFrames
    tables = [
        'program', 'course', 'room', 'faculty', 'student_plan', 
        'prerequisite', 'faculty_skill', 'availability', 
        'registration_interest', 'section', 'workload_assignment'
    ]
    data = {}
    for t in tables:
        file_path = os.path.join(OUTPUT_DIR, f"{t}.csv")
        data[t] = pd.read_csv(file_path)
    return data

def check_primary_keys(data):
    print("\n--- Checking Primary Keys (Uniqueness) ---")
    
    # We define which column is the primary key for each table
    pk_map = {
        'program': 'program_id',
        'course': 'course_id',
        'room': 'room_id',
        'faculty': 'faculty_id',
        'student_plan': 'plan_id',
        'registration_interest': 'interest_id',
        'section': 'section_id'
        # Note: workload_assignment deliberately has a duplicate edge case we injected, 
        # so we won't test it for strict uniqueness here to avoid crashing the test.
    }
    
    all_passed = True
    for table, pk in pk_map.items():
        df = data[table]
        # Check if the number of unique IDs matches the total number of rows
        is_unique = df[pk].is_unique
        status = "✅ PASS" if is_unique else "❌ FAIL"
        print(f"{status} | {table}.{pk}")
        if not is_unique:
            all_passed = False
            
    return all_passed

def check_foreign_keys(data):
    print("\n--- Checking Foreign Keys (Integrity) ---")
    
    # We define which child column must exist in which parent column
    fk_map = [
        ('course', 'program_id', 'program', 'program_id'),
        ('student_plan', 'program_id', 'program', 'program_id'),
        ('section', 'course_id', 'course', 'course_id'),
        ('section', 'room_id', 'room', 'room_id'),
        ('registration_interest', 'course_id', 'course', 'course_id')
    ]
    
    all_passed = True
    for child_table, child_col, parent_table, parent_col in fk_map:
        child_vals = data[child_table][child_col].dropna().unique()
        parent_vals = data[parent_table][parent_col].unique()
        
        # isin() checks if every child ID exists in the parent ID list
        # all() ensures every single one returned True
        is_valid = pd.Series(child_vals).isin(parent_vals).all()
        status = "✅ PASS" if is_valid else "❌ FAIL"
        print(f"{status} | {child_table}.{child_col} -> {parent_table}.{parent_col}")
        if not is_valid:
            all_passed = False
            
    return all_passed

def check_enums(data):
    print("\n--- Checking Allowed Enums (Domain Values) ---")
    
    # We define the strict rules our data dictionary set for specific columns
    enum_map = [
        ('course', 'course_level', [100, 200, 300, 400]),
        ('faculty', 'status', ['Active', 'On_Leave']),
        ('section', 'term', ['Fall_2026', 'Spring_2027'])
    ]
    
    all_passed = True
    for table, col, allowed_values in enum_map:
        unique_vals = data[table][col].unique()
        # Check if all unique values found in the column exist in our allowed list
        is_valid = all(val in allowed_values for val in unique_vals)
        status = "✅ PASS" if is_valid else "❌ FAIL"
        print(f"{status} | {table}.{col} only contains {allowed_values}")
        if not is_valid:
            all_passed = False
            
    return all_passed

if __name__ == "__main__":
    print("Loading data from output folder...")
    data = load_data()
    
    pk_pass = check_primary_keys(data)
    fk_pass = check_foreign_keys(data)
    enum_pass = check_enums(data)
    
    print("\n=====================================")
    if pk_pass and fk_pass and enum_pass:
        print("🏆 ALL VALIDATION CHECKS PASSED!")
    else:
        print("⚠️ SOME VALIDATION CHECKS FAILED.")
    print("=====================================")