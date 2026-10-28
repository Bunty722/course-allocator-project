# Data Dictionary: Course Demand & Faculty Allocation

## 1. Program (Master)
| Field | Type | Rules & Validation |
|---|---|---|
| program_id | VARCHAR(10) | PK, Format: `PRG-000001`, Unique |
| program_name | VARCHAR(100) | Required (e.g., "B.S. Computer Science") |
| total_credits_required| INT | Required, > 0 |

## 2. Course (Master)
| Field | Type | Rules & Validation |
|---|---|---|
| course_id | VARCHAR(10) | PK, Format: `CRS-000001`, Unique |
| program_id | VARCHAR(10) | FK -> Program.program_id |
| course_name | VARCHAR(100) | Required |
| credits | INT | Required, Allowed: 1, 2, 3, 4 |
| course_level | INT | Required, Allowed: 100, 200, 300, 400 |

## 3. Prerequisite (Rule)
| Field | Type | Rules & Validation |
|---|---|---|
| target_course_id | VARCHAR(10) | PK/FK -> Course.course_id |
| prereq_course_id | VARCHAR(10) | PK/FK -> Course.course_id. Target level MUST be > Prereq level. |

## 4. Room (Master)
| Field | Type | Rules & Validation |
|---|---|---|
| room_id | VARCHAR(10) | PK, Format: `ROM-000001` |
| capacity | INT | Required, Allowed: 30, 60, 120, 250 |

## 5. Faculty (Master)
| Field | Type | Rules & Validation |
|---|---|---|
| faculty_id | VARCHAR(10) | PK, Format: `FAC-000001` |
| status | VARCHAR(20) | Enum: Active, On_Leave |
| max_workload_hours | INT | Required (e.g., 40) |

## 6. FacultySkill (Rule)
| Field | Type | Rules & Validation |
|---|---|---|
| faculty_id | VARCHAR(10) | PK/FK -> Faculty.faculty_id |
| course_id | VARCHAR(10) | PK/FK -> Course.course_id (What they can teach) |

## 7. Availability (Rule)
| Field | Type | Rules & Validation |
|---|---|---|
| faculty_id | VARCHAR(10) | PK/FK -> Faculty.faculty_id |
| term | VARCHAR(20) | PK, Enum: Fall_2026, Spring_2027 |
| is_available | BOOLEAN | Required |

## 8. StudentPlan (Master - Learner)
| Field | Type | Rules & Validation |
|---|---|---|
| plan_id | VARCHAR(10) | PK, Format: `PLN-000001` |
| program_id | VARCHAR(10) | FK -> Program.program_id |
| enrollment_year | INT | Required (e.g., 2024, 2025, 2026) |

## 9. RegistrationInterest (Transaction - Demand)
| Field | Type | Rules & Validation |
|---|---|---|
| interest_id | VARCHAR(10) | PK, Format: `INT-000001` |
| plan_id | VARCHAR(10) | FK -> StudentPlan.plan_id |
| course_id | VARCHAR(10) | FK -> Course.course_id |
| term | VARCHAR(20) | Enum: Fall_2026, Spring_2027 |

## 10. Section (Transaction - Supply)
| Field | Type | Rules & Validation |
|---|---|---|
| section_id | VARCHAR(15) | PK, Format: `SEC-2026-000001` |
| course_id | VARCHAR(10) | FK -> Course.course_id |
| room_id | VARCHAR(10) | FK -> Room.room_id |
| term | VARCHAR(20) | Enum: Fall_2026, Spring_2027 |
| capacity | INT | Derived from Room.capacity |

## 11. WorkloadAssignment (Transaction - Execution)
| Field | Type | Rules & Validation |
|---|---|---|
| assignment_id | VARCHAR(15) | PK, Format: `WLA-2026-000001` |
| faculty_id | VARCHAR(10) | FK -> Faculty.faculty_id |
| section_id | VARCHAR(15) | FK -> Section.section_id |
| hours_assigned | INT | Derived from Course.credits * multiplier |