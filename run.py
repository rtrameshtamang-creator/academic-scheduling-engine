from collections import defaultdict
from datetime import time

from ortools.sat.python import cp_model

from academic_scheduler.common.enums import (
    ActivityType,
    DayPart,
    EmploymentType,
    RoomType,
    WeekDay,
)
from academic_scheduler.models.academic_cohort import AcademicCohort
from academic_scheduler.models.assignments.assignment_set import AssignmentSet
from academic_scheduler.models.assignments.fixed_room_assignment import (
    FixedRoomAssignment,
)
from academic_scheduler.models.daily_schedule_template import (
    DailyScheduleTemplate,
)
from academic_scheduler.models.department import Department
from academic_scheduler.models.fixed_session import FixedSession
from academic_scheduler.models.institution import Institution
from academic_scheduler.models.institution_policy import InstitutionPolicy
from academic_scheduler.models.room import Room
from academic_scheduler.models.room_availability import RoomAvailability
from academic_scheduler.models.section_plan import SectionPlan
from academic_scheduler.models.session_requirement_template import (
    SessionRequirementTemplate,
)
from academic_scheduler.models.teacher import Teacher
from academic_scheduler.models.teacher_availability import TeacherAvailability
from academic_scheduler.models.teacher_preference import TeacherPreference
from academic_scheduler.models.teaching_plan import TeachingPlan
from academic_scheduler.models.time_block_template import TimeBlockTemplate
from academic_scheduler.services.candidate_slot_generator import (
    CandidateSlotGenerator,
)
from academic_scheduler.services.penalty_calculator import PenaltyCalculator
from academic_scheduler.services.section_generator import SectionGenerator
from academic_scheduler.services.session_generator import SessionGenerator
from academic_scheduler.services.session_requirement_generator import (
    SessionRequirementGenerator,
)
from academic_scheduler.services.teacher_availability_validator import (
    TeacherAvailabilityValidator,
)
from academic_scheduler.services.teaching_assignment_generator import (
    TeachingAssignmentGenerator,
)
from academic_scheduler.services.time_grid import TimeGrid
from academic_scheduler.services.timetable_builder import TimetableBuilder
from academic_scheduler.services.timetable_printer import TimetablePrinter
from academic_scheduler.solver.cp_sat_solver import CPSATSolver
from academic_scheduler.models.course_offering import CourseOffering


def main():
    # ----------------------------
    # Create Time Blocks
    # ----------------------------

    t1 = TimeBlockTemplate(
        id="T1",
        code="T1",
        name="Theory Block 1",
        display_order=1,
        start_time=time(7, 10),
        end_time=time(8, 45),
        day_part=DayPart.MORNING,
        allowed_activity_types=[ActivityType.THEORY],
    )

    t2 = TimeBlockTemplate(
        id="T2",
        code="T2",
        name="Theory Block 2",
        display_order=2,
        start_time=time(8, 45),
        end_time=time(10, 15),
        day_part=DayPart.MORNING,
        allowed_activity_types=[ActivityType.THEORY],
    )

    l1 = TimeBlockTemplate(
        id="L1",
        code="L1",
        name="Morning Lab",
        display_order=3,
        start_time=time(7, 10),
        end_time=time(9, 40),
        day_part=DayPart.MORNING,
        allowed_activity_types=[ActivityType.LAB],
    )

    t3 = TimeBlockTemplate(
        id="T3",
        code="T3",
        name="Theory Block 3",
        display_order=3,
        start_time=time(11, 0),
        end_time=time(12, 30),
        day_part=DayPart.AFTERNOON,
        allowed_activity_types=[ActivityType.THEORY],
    )

    t4 = TimeBlockTemplate(
        id="T4",
        code="T4",
        name="Theory Block 4",
        display_order=4,
        start_time=time(12, 30),
        end_time=time(14, 0),
        day_part=DayPart.AFTERNOON,
        allowed_activity_types=[ActivityType.THEORY],
    )

    l2 = TimeBlockTemplate(
        id="L2",
        code="L2",
        name="Afternoon Lab",
        display_order=6,
        start_time=time(11, 0),
        end_time=time(13, 30),
        day_part=DayPart.AFTERNOON,
        allowed_activity_types=[ActivityType.LAB],
    )

    # ----------------------------
    # Create Daily Schedule
    # ----------------------------

    regular_day = DailyScheduleTemplate(
        id="REGULAR",
        name="Regular Teaching Day",
        time_blocks=[
            t1,
            t2,
            l1,
            t3,
            t4,
            l2,
        ],
    )

    # ----------------------------
    # Create Institution
    # ----------------------------

    institution = Institution(
        id="ioe",
        name="Institute of Engineering",
        timezone="Asia/Kathmandu",
        daily_schedule_templates=[regular_day],
    )

    # ----------------------------
    # Create Department
    # ----------------------------

    department = Department(
        id="doece",
        code="DOECE",
        name="Department of Electronics and Computer Engineering",
    )

    # ----------------------------
    # Create Program and Term
    # ----------------------------

    from academic_scheduler.models.program import Program
    from academic_scheduler.models.term import Term

    program = Program(
        id="bct",
        code="BCT",
        name="Bachelor in Computer Engineering",
        department_id=department.id,
        total_terms=8,
    )

    term = Term(
        id="bct-1",
        program_id=program.id,
        number=1,
        name="Semester I",
    )

    # ----------------------------
    # Create Institution Policy
    # ----------------------------

    policy = InstitutionPolicy(
        max_students_per_section=48,
        max_students_per_lab_group=24,
        auto_split_lab_groups=True,
        auto_create_sections=True,
    )

    # ----------------------------
    # Create Academic Cohort
    # ----------------------------

    cohort = AcademicCohort(
        id="bct-2082-2-1",
        program_id=program.id,
        term_id="2-1",
        batch=2082,
        total_students=60,
        section_plans=[
            SectionPlan(
                code="A",
                name="Section A",
                student_count=30,
            ),
            SectionPlan(
                code="B",
                name="Section B",
                student_count=30,
            ),
        ],
    )

    course_offering = CourseOffering(
        id=f"{cohort.id}-oop",
        course_id="oop",
        cohort_id=cohort.id,
    )

    # ----------------------------
    # Generate Sections
    # ----------------------------

    section_generator = SectionGenerator()

    generated_sections = section_generator.generate(
        cohort=cohort,
        policy=policy,
    )

    # ----------------------------
    # Create Teachers
    # ----------------------------

    teacher = Teacher(
        id="ramesh",
        code="RT",
        name="Ramesh Tamang",
        employment_type=EmploymentType.FULL_TIME,
        max_periods_per_week=18,
        max_periods_per_day=4,
    )

    teacher2 = Teacher(
        id="hari",
        code="HK",
        name="Hari Khadka",
        employment_type=EmploymentType.FULL_TIME,
        max_periods_per_week=18,
        max_periods_per_day=4,
    )

    teacher3 = Teacher(
        id="sita",
        code="SP",
        name="Sita Poudel",
        employment_type=EmploymentType.FULL_TIME,
        max_periods_per_week=18,
        max_periods_per_day=4,
    )

    teacher.availability = [
        TeacherAvailability(
            teacher_id="ramesh",
            weekday=WeekDay.SUNDAY,
            block_id="T1",
        ),
        TeacherAvailability(
            teacher_id="ramesh",
            weekday=WeekDay.SUNDAY,
            block_id="T2",
        ),
        TeacherAvailability(
            teacher_id="ramesh",
            weekday=WeekDay.MONDAY,
            block_id="T1",
        ),
        TeacherAvailability(
            teacher_id="ramesh",
            weekday=WeekDay.MONDAY,
            block_id="T2",
        ),
        TeacherAvailability(
            teacher_id="ramesh",
            weekday=WeekDay.TUESDAY,
            block_id="T1",
        ),
        TeacherAvailability(
            teacher_id="ramesh",
            weekday=WeekDay.TUESDAY,
            block_id="T2",
        ),
        TeacherAvailability(
            teacher_id="ramesh",
            weekday=WeekDay.WEDNESDAY,
            block_id="T1",
        ),
        TeacherAvailability(
            teacher_id="ramesh",
            weekday=WeekDay.WEDNESDAY,
            block_id="T2",
        ),
        TeacherAvailability(
            teacher_id="ramesh",
            weekday=WeekDay.SUNDAY,
            block_id="L1",
        ),
        TeacherAvailability(
            teacher_id="ramesh",
            weekday=WeekDay.MONDAY,
            block_id="L1",
        ),
    ]

    teacher2.availability = teacher.availability.copy()
    teacher3.availability = teacher.availability.copy()

    teachers = [
        teacher,
        teacher2,
        teacher3,
    ]

    # ----------------------------
    # Create Teaching Plans
    # ----------------------------

    theory_plan = TeachingPlan(
        course_id="oop",
        activity_type=ActivityType.THEORY,
        teacher_ids=["ramesh"],
        weekly_sessions=3,
        duration_minutes=90,
        parallel_groups=1,
        required_room_type=RoomType.CLASSROOM,
    )

    lab_plan = TeachingPlan(
        course_id="oop",
        activity_type=ActivityType.LAB,
        teacher_ids=[],
        parallel_group_teacher_ids=[
            ["hari"],
            ["sita"],
        ],
        weekly_sessions=1,
        duration_minutes=150,
        parallel_groups=2,
        required_room_type=RoomType.COMPUTER_LAB,
    )

    teaching_plans = [
        theory_plan,
        lab_plan,
    ]

    # ----------------------------
    # Generate Teaching Assignments
    # ----------------------------

    assignment_generator = TeachingAssignmentGenerator()

    generated_assignments = assignment_generator.generate(
        offering=course_offering,
        sections=generated_sections,
        teaching_plans=teaching_plans,
    )

    # ----------------------------
    # Create Session Requirement Templates
    # ----------------------------

    theory_template = SessionRequirementTemplate(
        activity_type=ActivityType.THEORY,
        occurrences=3,
        repeat_interval_weeks=1,
    )

    lab_template = SessionRequirementTemplate(
        activity_type=ActivityType.LAB,
        occurrences=1,
        repeat_interval_weeks=1,
    )

    # ----------------------------
    # Generate Session Requirements
    # ----------------------------

    requirement_generator = SessionRequirementGenerator()

    generated_requirements = requirement_generator.generate(
        teaching_assignments=generated_assignments,
        templates=[
            theory_template,
            lab_template,
        ],
    )

    print("\nGenerated Session Requirements")
    print("-" * 80)

    for requirement in generated_requirements:
        print(
            f"{requirement.teaching_assignment_id:30}"
            f"{requirement.activity_type.name:8}"
            f"{requirement.occurrences:2} occurrence(s)"
        )

    print(
        f"\nTotal Session Requirements: "
        f"{len(generated_requirements)}"
    )

    # ----------------------------
    # Display Teaching Assignments
    # ----------------------------

    print("\nGenerated Teaching Assignments")
    print("-" * 80)

    for assignment in generated_assignments:
        print(
            f"{assignment.id:30}"
            f"{assignment.activity_type.name:8}"
            f"G{assignment.group_index:<3}"
            f"{assignment.students_per_session:4} students   "
            f"{assignment.teacher_ids}"
        )

    print("-" * 60)

    for assignment in generated_assignments:
        print(
            f"{assignment.id:20}"
            f"{assignment.activity_type.name:10}"
            f"{assignment.section_id:15}"
            f"{assignment.teacher_ids}"
        )

    print(
        f"Generated Teaching Assignments: "
        f"{len(generated_assignments)}"
    )

    # ----------------------------
    # Display Generated Sections
    # ----------------------------

    print("\nGenerated Section Details")
    print("-" * 60)

    for section in generated_sections:
        print(f"ID      : {section.id}")
        print(f"Code    : {section.code}")
        print(f"Name    : {section.name}")
        print(f"Program : {section.program_id}")
        print(f"Term    : {section.term_id}")
        print(f"Batch   : {section.batch}")
        print(f"Students: {section.student_count}")
        print("-" * 60)

    print("\nGenerated Sections")
    print("-" * 50)

    for section in generated_sections:
        print(
            f"{section.code:8}"
            f"{section.student_count:4} students"
        )

    print(f"Generated Sections: {len(generated_sections)}")

    # ----------------------------
    # Create Teacher Preference
    # ----------------------------

    teacher_preference = TeacherPreference(
        teacher_id="ramesh",
        preferred_weekdays=[
            "Sunday",
            "Monday",
        ],
        preferred_blocks=[
            "T1",
            "T2",
        ],
    )

    # ----------------------------
    # Validate Teacher Availability
    # ----------------------------

    # ----------------------------
    # Create Rooms
    # ----------------------------

    classroom1 = Room(
        id="cl101",
        code="CL101",
        name="Classroom 101",
        room_type=RoomType.CLASSROOM,
        capacity=48,
    )

    classroom2 = Room(
        id="cl102",
        code="CL102",
        name="Classroom 102",
        room_type=RoomType.CLASSROOM,
        capacity=60,
    )

    classroom3 = Room(
        id="cl103",
        code="CL103",
        name="Classroom 103",
        room_type=RoomType.CLASSROOM,
        capacity=72,
    )

    computer_lab1 = Room(
        id="lab1",
        code="LAB1",
        name="Computer Lab 1",
        room_type=RoomType.COMPUTER_LAB,
        capacity=24,
    )

    computer_lab2 = Room(
        id="lab2",
        code="LAB2",
        name="Computer Lab 2",
        room_type=RoomType.COMPUTER_LAB,
        capacity=30,
    )

    rooms = [
        classroom1,
        classroom2,
        classroom3,
        computer_lab1,
        computer_lab2,
    ]

    classroom1.availability = [
        RoomAvailability(
            room_id="cl101",
            weekday=WeekDay.SUNDAY,
            block_id="T1",
            available=False,
        ),
        RoomAvailability(
            room_id="cl101",
            weekday=WeekDay.SUNDAY,
            block_id="T2",
            available=True,
        ),
    ]

    # ----------------------------
    # Build Time Grid
    # ----------------------------

    grid = TimeGrid()

    slots = grid.build(
        weekdays=[
            WeekDay.SUNDAY,
            WeekDay.MONDAY,
            WeekDay.TUESDAY,
            WeekDay.WEDNESDAY,
            WeekDay.THURSDAY,
            WeekDay.FRIDAY,
        ],
        daily_schedule=regular_day,
    )

    # ----------------------------
    # Generate Sessions
    # ----------------------------

    generator = SessionGenerator()

    fixed_sessions = [
        FixedSession(
            session_id="oop-theory-O2-G1",
            time_slot_id="Monday_T2",
        )
    ]

    sessions = generator.generate(
        teaching_assignments=generated_assignments,
        requirements=generated_requirements,
        fixed_sessions=fixed_sessions,
    )

    # ----------------------------
    # Validate Teacher Availability
    # ----------------------------

    validator = TeacherAvailabilityValidator()

    is_valid = validator.validate(
        teachers=teachers,
        sessions=sessions,
    )

    if not is_valid:
        print("\nScheduling stopped because validation failed.")
        return

    print(f"\nGenerated Sessions: {len(sessions)}")

    # ----------------------------
    # Generate Candidate Slots
    # ----------------------------

    candidate_generator = CandidateSlotGenerator()

    candidates = candidate_generator.generate(
        sessions=sessions,
        slots=slots,
        teachers=teachers,
        rooms=rooms,
    )

    # ----------------------------
    # Calculate Candidate Penalties
    # ----------------------------

    penalty_calculator = PenaltyCalculator()

    penalty_calculator.calculate(
        candidates,
        sessions,
        [teacher_preference],
    )

    print(f"\nGenerated Candidates: {len(candidates)}")

    session_times = defaultdict(set)

    for candidate in candidates:
        session_times[candidate.session_id].add(
            candidate.time_slot_id
        )

    print("\nUnique time slots per session")
    print("-" * 60)

    for session_id, times in session_times.items():
        print(
            f"{session_id:40} "
            f"{sorted(times)}"
        )

    has_empty_session = False

    for session in sessions:
        count = sum(
            1
            for candidate in candidates
            if candidate.session_id == session.id
        )

        print(f"{session.id:20} -> {count}")

        if count == 0:
            has_empty_session = True

    if has_empty_session:
        print(
            "\nERROR: One or more sessions have "
            "no valid candidate slots."
        )
        return

    # ----------------------------
    # Build and Solve CP-SAT Model
    # ----------------------------

    solver = CPSATSolver()

    assignments = AssignmentSet()

    assignments.fixed_rooms.append(
        FixedRoomAssignment(
            session_id="oop-lab-O1-G1",
            room_id="lab1",
        )
    )

    variables = solver.build(
        sessions=sessions,
        candidate_slots=candidates,
        teachers=teachers,
        assignments=assignments,
    )

    print(f"Variables: {len(variables)}")

    cp_solver, status = solver.solve()

    print(f"Solver Status: {cp_solver.StatusName(status)}")

    if status == cp_model.OPTIMAL:
        # ----------------------------
        # Build Timetable
        # ----------------------------

        builder = TimetableBuilder()

        timetable = builder.build(
            solver=cp_solver,
            variables=variables,
            sessions=sessions,
            candidate_slots=candidates,
        )

        print(f"\nTimetable Entries: {len(timetable.entries)}")

        printer = TimetablePrinter()

        printer.print(timetable)

    else:
        print("\nNo feasible timetable found.")


if __name__ == "__main__":
    main()