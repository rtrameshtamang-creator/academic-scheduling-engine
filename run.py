from datetime import time

from academic_scheduler.common.enums import (
    ActivityType,
    DayPart,
)
from academic_scheduler.models.time_block_template import TimeBlockTemplate
from academic_scheduler.models.daily_schedule_template import DailyScheduleTemplate
from academic_scheduler.models.institution import Institution
from academic_scheduler.common.enums import ActivityType, RoomType
from academic_scheduler.models.department import Department
from academic_scheduler.models.teacher import Teacher
from academic_scheduler.common.enums import EmploymentType
from academic_scheduler.models.course import Course
from academic_scheduler.models.teaching_assignment import TeachingAssignment
from academic_scheduler.models.session_requirement import SessionRequirement
from academic_scheduler.models.room import Room
from academic_scheduler.common.enums import RoomType
from academic_scheduler.services.time_grid import TimeGrid
from academic_scheduler.common.enums import WeekDay
from academic_scheduler.services.session_generator import SessionGenerator
from academic_scheduler.services.candidate_slot_generator import (
    CandidateSlotGenerator,
)
from academic_scheduler.solver.cp_sat_solver import CPSATSolver
from ortools.sat.python import cp_model

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

    # ----------------------------
    # Create Daily Schedule
    # ----------------------------

    regular_day = DailyScheduleTemplate(
        id="REGULAR",
        name="Regular Teaching Day",
        time_blocks=[t1, t2, t3, t4]
    )

    # ----------------------------
    # Create Institution
    # ----------------------------

    inst = Institution(
        id="ioe",
        name="Institute of Engineering",
        timezone="Asia/Kathmandu",
        daily_schedule_templates=[regular_day]
    )

    #print(inst)


    department = Department(
        id="doece",
        code="DOECE",
        name="Department of Electronics and Computer Engineering"
    )

    #print(department)

    from academic_scheduler.models.program import Program

    program = Program(
        id="bct",
        code="BCT",
        name="Bachelor in Computer Engineering",
        department_id="doece",
        total_terms=8,
    )

    #print(program)

    from academic_scheduler.models.term import Term

    term = Term(
        id="bct-1",
        program_id="bct",
        number=1,
        name="Semester I"
    )

    #print(term)

    from academic_scheduler.models.section import Section

    section = Section(
        id="bct-2082-1-a",
        code="A",
        name="Section A",
        program_id="bct",
        term_id="bct-term-1",
        batch=2082,
        student_count=48,
    )

    #print(section)


    teacher = Teacher(
    id="ramesh",
    code="RT",
    name="Ramesh Tamang",
    employment_type=EmploymentType.FULL_TIME,
    max_periods_per_week=18,
    max_periods_per_day=4,
    )

    #print(teacher)

    from academic_scheduler.models.teacher_availability import (
        TeacherAvailability,
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

    ]

    # ----------------------------
    # Create Course
    # ----------------------------

    course = Course(
        id="oop",
        code="CT651",
        title="Object Oriented Programming",
        credit=3.0,
        department_id="doece",
        program_id="bct",
    )

    #print(course)

    assignment = TeachingAssignment(
    id="oop-bct2a",
    course_id="oop",
    section_id="bct-2082-2-a",
    teacher_ids=["ramesh"],
    )

    #print(assignment)

    lab_requirement = SessionRequirement(
    id="oop-lab",
    teaching_assignment_id="oop-bct2a",
    activity_type=ActivityType.LAB,
    occurrences=1,
    repeat_interval_weeks=2,
    duration_minutes=150,
    students_per_session=24,
    parallel_groups=2,
    required_room_type=RoomType.COMPUTER_LAB,
    )

    #print(lab_requirement)

    classroom = Room(
    id="cl101",
    code="CL101",
    name="Classroom 101",
    room_type=RoomType.CLASSROOM,
    capacity=48,
    )

    #print(classroom)

    computer_lab = Room(
    id="comp1",
    code="LAB1",
    name="Computer Lab 1",
    room_type=RoomType.COMPUTER_LAB,
    capacity=24,
    )

    #print(computer_lab)

    #print(activity)
    
    #print("\n============================")
    #print("TIME GRID")
    #print("============================")

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

    #print(f"Total Slots: {len(slots)}\n")

    #for slot in slots:
        #print(slot)


    theory_requirement = SessionRequirement(
        id="oop-theory",
        teaching_assignment_id="oop-bct2a",
        activity_type=ActivityType.THEORY,
        occurrences=3,
        repeat_interval_weeks=1,
        duration_minutes=90,
        students_per_session=48,
        parallel_groups=1,
        required_room_type=RoomType.CLASSROOM,
    )

    lab_requirement = SessionRequirement(
        id="oop-lab",
        teaching_assignment_id="oop-bct2a",
        activity_type=ActivityType.LAB,
        occurrences=1,
        repeat_interval_weeks=1,
        duration_minutes=150,
        students_per_session=24,
        parallel_groups=2,
        required_room_type=RoomType.COMPUTER_LAB,
    )

    generator = SessionGenerator()

    sessions = generator.generate(
        teaching_assignments=[
            assignment,
        ],
        requirements=[
            theory_requirement,
            lab_requirement,
        ],
    )

    from academic_scheduler.services.room_compatibility import (
        RoomCompatibilityService,
    )

    compatibility = RoomCompatibilityService()

    print("\nRoom Compatibility Test\n")

    for session in sessions:

        print(f"\n{session.id}")

        for room in [classroom, computer_lab]:

            print(
                f"{room.code}:",
                compatibility.is_compatible(
                    session,
                    room,
                ),
            )

    print("\nGenerated Sessions\n")

    for session in sessions:
        print(session)
    
    candidate_generator = CandidateSlotGenerator()

    candidates = candidate_generator.generate(
        sessions=sessions,
        slots=slots,
        teachers=[
            teacher,
        ],
        rooms=[
            classroom,
            computer_lab,
        ],
    )

    print(f"\nGenerated Candidates: {len(candidates)}")

    #for candidate in candidates[:10]:
        #print(candidate)

    solver = CPSATSolver()

    variables = solver.build(
        sessions=sessions,
        candidate_slots=candidates,
    )

    #print(f"Variables: {len(variables)}")

    cp_solver, status = solver.solve()

    #print(status == cp_model.OPTIMAL)

    if status == cp_model.OPTIMAL:
        solver.print_solution(cp_solver, variables)


if __name__ == "__main__":
    main()