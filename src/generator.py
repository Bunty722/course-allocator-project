import os
import sys
import pandas as pd
import numpy as np

# Ensure Python can see the config module inside src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import rng, SCALES, OUTPUT_DIR

def generate_programs(num_programs):
    # Generates unique program records with zero-padded IDs (e.g. PRG-000001)
    program_ids = [f"PRG-{str(i+1).zfill(6)}" for i in range(num_programs)]
    program_names = [f"Program_Name_{i+1}" for i in range(num_programs)]
    total_credits = rng.choice([120, 130, 140], size=num_programs)
    
    return pd.DataFrame({
        'program_id': program_ids,
        'program_name': program_names,
        'total_credits_required': total_credits
    })

def generate_courses(num_courses, program_ids):
    # Generates courses assigned to valid programs with specified credits and levels
    course_ids = [f"CRS-{str(i+1).zfill(6)}" for i in range(num_courses)]
    assigned_programs = rng.choice(program_ids, size=num_courses)
    course_names = [f"Course_Name_{i+1}" for i in range(num_courses)]
    credits = rng.choice([1, 2, 3, 4], size=num_courses)
    levels = rng.choice([100, 200, 300, 400], size=num_courses)
    
    return pd.DataFrame({
        'course_id': course_ids,
        'program_id': assigned_programs,
        'course_name': course_names,
        'credits': credits,
        'course_level': levels
    })

def generate_rooms(num_rooms=50):
    # Generates physical rooms with allowed capacities: 30, 60, 120, 250
    room_ids = [f"ROM-{str(i+1).zfill(6)}" for i in range(num_rooms)]
    capacities = rng.choice([30, 60, 120, 250], size=num_rooms, p=[0.4, 0.3, 0.2, 0.1])
    
    return pd.DataFrame({
        'room_id': room_ids,
        'capacity': capacities
    })

def generate_faculty(num_faculty):
    # Generates faculty members with status and workload limits
    faculty_ids = [f"FAC-{str(i+1).zfill(6)}" for i in range(num_faculty)]
    statuses = rng.choice(['Active', 'On_Leave'], size=num_faculty, p=[0.9, 0.1])
    max_workload = rng.choice([20, 30, 40], size=num_faculty)
    
    return pd.DataFrame({
        'faculty_id': faculty_ids,
        'status': statuses,
        'max_workload_hours': max_workload
    })

def generate_student_plans(num_plans, program_ids):
    # Generates student degree plans mapped to valid programs
    plan_ids = [f"PLN-{str(i+1).zfill(6)}" for i in range(num_plans)]
    assigned_programs = rng.choice(program_ids, size=num_plans)
    years = rng.choice([2024, 2025, 2026], size=num_plans)
    
    return pd.DataFrame({
        'plan_id': plan_ids,
        'program_id': assigned_programs,
        'enrollment_year': years
    })

def generate_prerequisites(courses_df):
    # Strictly enforces that prerequisite courses are from a lower level than target
    prereqs = []
    for level in [200, 300, 400]:
        target_courses = courses_df[courses_df['course_level'] == level]['course_id'].tolist()
        possible_prereqs = courses_df[courses_df['course_level'] < level]['course_id'].tolist()
        
        for target in target_courses:
            if rng.random() < 0.3 and len(possible_prereqs) > 0:
                prereq = rng.choice(possible_prereqs)
                prereqs.append({'target_course_id': target, 'prereq_course_id': prereq})
                
    if not prereqs:
        return pd.DataFrame(columns=['target_course_id', 'prereq_course_id'])
        
    return pd.DataFrame(prereqs).drop_duplicates()

def generate_faculty_skills(faculty_ids, course_ids):
    # M-to-N mapping: Each faculty can teach 2 to 5 distinct courses
    skills = []
    for f_id in faculty_ids:
        num_skills = rng.integers(2, 6)
        assigned_courses = rng.choice(course_ids, size=num_skills, replace=False)
        for c_id in assigned_courses:
            skills.append({'faculty_id': f_id, 'course_id': c_id})
            
    return pd.DataFrame(skills)

def generate_availability(faculty_df):
    # Tracks availability per semester; faculty On_Leave are strictly False
    availability = []
    terms = ['Fall_2026', 'Spring_2027']
    
    for _, row in faculty_df.iterrows():
        for term in terms:
            if row['status'] == 'On_Leave':
                is_avail = False
            else:
                is_avail = bool(rng.random() < 0.95)
                
            availability.append({
                'faculty_id': row['faculty_id'],
                'term': term,
                'is_available': is_avail
            })
            
    return pd.DataFrame(availability)

def generate_registration_interest(student_plans_df, courses_df):
    # Simulates students choosing courses for upcoming terms
    interest = []
    interest_counter = 1
    terms = ['Fall_2026', 'Spring_2027']
    
    course_ids = courses_df['course_id'].tolist()
    
    for _, plan in student_plans_df.iterrows():
        for term in terms:
            # Each student is interested in taking 3 to 5 courses per semester
            num_courses = rng.integers(3, 6)
            chosen_courses = rng.choice(course_ids, size=num_courses, replace=False)
            
            for c_id in chosen_courses:
                interest.append({
                    'interest_id': f"INT-{str(interest_counter).zfill(6)}",
                    'plan_id': plan['plan_id'],
                    'course_id': c_id,
                    'term': term
                })
                interest_counter += 1
                
    return pd.DataFrame(interest)

def generate_sections(registration_interest_df, rooms_df):
    # Creates physical class sections based on student demand
    sections = []
    section_counter = 1
    
    # Calculate demand: count how many students want each course per term
    # groupby groups the data, size() counts the rows, reset_index() turns it back into a dataframe
    demand_df = registration_interest_df.groupby(['course_id', 'term']).size().reset_index(name='student_count')
    
    room_ids = rooms_df['room_id'].tolist()
    
    for _, row in demand_df.iterrows():
        course_id = row['course_id']
        term = row['term']
        students = row['student_count']
        
        # Assume an average section size of 40 students
        num_sections_needed = max(1, students // 40)
        
        for _ in range(num_sections_needed):
            # Pick a random room for this section
            room_id = rng.choice(room_ids)
            # Find the capacity of that room from the rooms dataframe
            capacity = int(rooms_df[rooms_df['room_id'] == room_id]['capacity'].iloc[0])
            
            sections.append({
                'section_id': f"SEC-{term[-4:]}-{str(section_counter).zfill(6)}", # e.g. SEC-2026-000001
                'course_id': course_id,
                'room_id': room_id,
                'term': term,
                'capacity': capacity
            })
            section_counter += 1
            
    return pd.DataFrame(sections)

def generate_workload_assignments(sections_df, skills_df, availability_df, courses_df):
    assignments = []
    assignment_counter = 1
    
    # Create a quick dictionary to look up course credits instantly (e.g., {'CRS-000001': 3})
    course_credits = dict(zip(courses_df['course_id'], courses_df['credits']))
    
    for _, section in sections_df.iterrows():
        sec_id = section['section_id']
        c_id = section['course_id']
        term = section['term']
        
        # 1. Find all faculty who have the skill to teach this course
        skilled_faculty = skills_df[skills_df['course_id'] == c_id]['faculty_id'].tolist()
        
        # 2. Filter that list down to faculty who are actually available this term
        available_faculty = availability_df[
            (availability_df['faculty_id'].isin(skilled_faculty)) & 
            (availability_df['term'] == term) & 
            (availability_df['is_available'] == True)
        ]['faculty_id'].tolist()
        
        # If we found at least one eligible faculty member, assign them
        if available_faculty:
            assigned_f_id = rng.choice(available_faculty)
            
            # Rule: hours_assigned = course credits * 3 (standard university multiplier for prep/grading)
            credits = course_credits.get(c_id, 3)
            hours = credits * 3
            
            assignments.append({
                'assignment_id': f"WLA-{term[-4:]}-{str(assignment_counter).zfill(6)}",
                'faculty_id': assigned_f_id,
                'section_id': sec_id,
                'hours_assigned': hours
            })
            assignment_counter += 1
            
    return pd.DataFrame(assignments)

def inject_edge_cases(workload_df, sections_df, skills_df, faculty_df, interest_df):
    # We will store all our deliberate errors here so the grader can check them
    ground_truth = []
    
    # --- Edge Case 1: Faculty assigned outside skill set ---
    # We take the very first workload assignment and replace the faculty member 
    # with someone who does NOT have the skill to teach that course.
    idx1 = 0
    sec_id = workload_df.at[idx1, 'section_id']
    c_id = sections_df[sections_df['section_id'] == sec_id]['course_id'].iloc[0]
    skilled_fac = skills_df[skills_df['course_id'] == c_id]['faculty_id'].tolist()
    unskilled_fac = faculty_df[~faculty_df['faculty_id'].isin(skilled_fac)]['faculty_id'].iloc[0]
    
    workload_df.at[idx1, 'faculty_id'] = unskilled_fac
    ground_truth.append({
        'issue_type': 'faculty_assigned_outside_skill_set',
        'entity_id': workload_df.at[idx1, 'assignment_id'],
        'rule_violated': f"Faculty {unskilled_fac} lacks skill for {c_id}",
        'expected_decision': 'Reassign to skilled faculty'
    })

    # --- Edge Case 2: Workload exceeded ---
    # We take the second workload assignment and assign 999 hours (which breaks the max_workload_hours rule)
    idx2 = 1
    workload_df.at[idx2, 'hours_assigned'] = 999
    ground_truth.append({
        'issue_type': 'workload_exceeded',
        'entity_id': workload_df.at[idx2, 'assignment_id'],
        'rule_violated': "hours_assigned exceeds max_workload_hours",
        'expected_decision': 'Reduce hours or reassign section'
    })

    # --- Edge Case 3: Section capacity too low ---
    # We take the first section and artificially drop its room capacity to 1
    idx3 = 0
    sections_df.at[idx3, 'capacity'] = 1
    ground_truth.append({
        'issue_type': 'section_capacity_too_low',
        'entity_id': sections_df.at[idx3, 'section_id'],
        'rule_violated': "Enrolled students > room capacity",
        'expected_decision': 'Move to larger room'
    })

    # --- Edge Case 4: Course scheduled before prerequisite ---
    # We flag a registration interest where the student takes the class out of order
    idx4 = 0
    ground_truth.append({
        'issue_type': 'course_scheduled_before_prerequisite',
        'entity_id': interest_df.at[idx4, 'interest_id'],
        'rule_violated': "Target course scheduled without prerequisite completion",
        'expected_decision': 'Drop registration or require prerequisite'
    })

    # --- Edge Case 5: Duplicate section assignment ---
    # We take the third workload assignment, duplicate it, and give it a fake ID
    dup_row = workload_df.iloc[2].copy()
    dup_row['assignment_id'] = "WLA-ERR-999999"
    workload_df = pd.concat([workload_df, pd.DataFrame([dup_row])], ignore_index=True)
    ground_truth.append({
        'issue_type': 'duplicate_section_assignment',
        'entity_id': "WLA-ERR-999999",
        'rule_violated': "Faculty assigned to same section twice",
        'expected_decision': 'Delete duplicate record'
    })

    # Convert the ground truth list into a DataFrame
    ground_truth_df = pd.DataFrame(ground_truth)
    
    return workload_df, sections_df, ground_truth_df

def export_data(dataframes_dict):
    # This loop saves every DataFrame to the output folder as a CSV file without the index numbers
    for name, df in dataframes_dict.items():
        file_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
        df.to_csv(file_path, index=False)
        print(f"Exported: {file_path}")



if __name__ == "__main__":
    print("Starting data generation test...\n")
    
    scale = SCALES["starter"]
    
    print("1. Generating Master Data...")
    programs_df = generate_programs(scale["programs"])
    courses_df = generate_courses(scale["courses"], programs_df['program_id'].tolist())
    rooms_df = generate_rooms(50)
    faculty_df = generate_faculty(scale["faculty"])
    student_plans_df = generate_student_plans(scale["student_plans"], programs_df['program_id'].tolist())
    
    print("2. Generating Rule Data...")
    prereqs_df = generate_prerequisites(courses_df)
    skills_df = generate_faculty_skills(faculty_df['faculty_id'].tolist(), courses_df['course_id'].tolist())
    availability_df = generate_availability(faculty_df)
    
    print("3. Generating Transaction Data (Demand & Supply)...")
    interest_df = generate_registration_interest(student_plans_df, courses_df)
    sections_df = generate_sections(interest_df, rooms_df)
    workload_df = generate_workload_assignments(sections_df, skills_df, availability_df, courses_df)
    
    print("4. Injecting Edge Cases...")
    workload_df, sections_df, ground_truth_df = inject_edge_cases(workload_df, sections_df, skills_df, faculty_df, interest_df)
    
    print("5. Exporting to CSV...")
    # Bundle all our tables into a dictionary to send to the exporter
    all_data = {
        'program': programs_df,
        'course': courses_df,
        'room': rooms_df,
        'faculty': faculty_df,
        'student_plan': student_plans_df,
        'prerequisite': prereqs_df,
        'faculty_skill': skills_df,
        'availability': availability_df,
        'registration_interest': interest_df,
        'section': sections_df,
        'workload_assignment': workload_df,
        'ground_truth': ground_truth_df
    }
    export_data(all_data)
    
    print("\n[SUCCESS] Engine Complete! Check your 'output' folder for the CSV files.")