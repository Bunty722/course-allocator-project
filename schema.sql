-- these sql commands have been written with reference to the Blueprint created as 
-- Data_Dictonary.md
CREATE TABLE Program (
    program_id VARCHAR(10) PRIMARY KEY,
    program_name VARCHAR(100) NOT NULL,
    total_credits_required INT NOT NULL CHECK (total_credits_required > 0)
);

CREATE TABLE Course (
    course_id VARCHAR(10) PRIMARY KEY,
    program_id VARCHAR(10) REFERENCES Program(program_id),
    course_name VARCHAR(100) NOT NULL,
    credits INT NOT NULL CHECK (credits IN (1, 2, 3, 4)),
    course_level INT NOT NULL CHECK (course_level IN (100, 200, 300, 400))
);

CREATE TABLE Prerequisite (
    target_course_id VARCHAR(10) REFERENCES Course(course_id),
    prereq_course_id VARCHAR(10) REFERENCES Course(course_id),
    PRIMARY KEY (target_course_id, prereq_course_id),
    CHECK (target_course_id != prereq_course_id)
);

CREATE TABLE Room (
    room_id VARCHAR(10) PRIMARY KEY,
    capacity INT NOT NULL CHECK (capacity IN (30, 60, 120, 250))
);

CREATE TABLE Faculty (
    faculty_id VARCHAR(10) PRIMARY KEY,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Active', 'On_Leave')),
    max_workload_hours INT NOT NULL CHECK (max_workload_hours > 0)
);

CREATE TABLE FacultySkill (
    faculty_id VARCHAR(10) REFERENCES Faculty(faculty_id),
    course_id VARCHAR(10) REFERENCES Course(course_id),
    PRIMARY KEY (faculty_id, course_id)
);

CREATE TABLE Availability (
    faculty_id VARCHAR(10) REFERENCES Faculty(faculty_id),
    term VARCHAR(20) NOT NULL CHECK (term IN ('Fall_2026', 'Spring_2027')),
    is_available BOOLEAN NOT NULL,
    PRIMARY KEY (faculty_id, term)
);

CREATE TABLE StudentPlan (
    plan_id VARCHAR(10) PRIMARY KEY,
    program_id VARCHAR(10) REFERENCES Program(program_id),
    enrollment_year INT NOT NULL
);

CREATE TABLE RegistrationInterest (
    interest_id VARCHAR(10) PRIMARY KEY,
    plan_id VARCHAR(10) REFERENCES StudentPlan(plan_id),
    course_id VARCHAR(10) REFERENCES Course(course_id),
    term VARCHAR(20) NOT NULL CHECK (term IN ('Fall_2026', 'Spring_2027'))
);

CREATE TABLE Section (
    section_id VARCHAR(15) PRIMARY KEY,
    course_id VARCHAR(10) REFERENCES Course(course_id),
    room_id VARCHAR(10) REFERENCES Room(room_id),
    term VARCHAR(20) NOT NULL CHECK (term IN ('Fall_2026', 'Spring_2027')),
    capacity INT NOT NULL
);

CREATE TABLE WorkloadAssignment (
    assignment_id VARCHAR(15) PRIMARY KEY,
    faculty_id VARCHAR(10) REFERENCES Faculty(faculty_id),
    section_id VARCHAR(15) REFERENCES Section(section_id),
    hours_assigned INT NOT NULL CHECK (hours_assigned > 0)
);