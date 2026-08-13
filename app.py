import streamlit as st

from academic_scheduler.common.enums import (
    ActivityType,
    DayPart,
    EmploymentType,
    RoomType,
    WeekDay,
)
from academic_scheduler.models.academic_cohort import AcademicCohort
from academic_scheduler.models.assignments.assignment_set import AssignmentSet
from academic_scheduler.models.daily_schedule_template import (
    DailyScheduleTemplate,
)
from academic_scheduler.models.institution_policy import InstitutionPolicy
from academic_scheduler.models.room import Room
from academic_scheduler.models.section_plan import SectionPlan
from academic_scheduler.models.session_requirement_template import (
    SessionRequirementTemplate,
)
from academic_scheduler.models.teacher import Teacher
from academic_scheduler.models.teacher_availability import (
    TeacherAvailability,
)
from academic_scheduler.models.teaching_plan import TeachingPlan
from academic_scheduler.models.time_block_template import (
    TimeBlockTemplate,
)
from academic_scheduler.services.candidate_slot_generator import (
    CandidateSlotGenerator,
)
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
from academic_scheduler.solver.cp_sat_solver import CPSATSolver

from ortools.sat.python import cp_model


st.set_page_config(
    page_title="HCOE Weekly Routine Generator",
    page_icon="📅",
    layout="wide",
)


st.title("📅 HCOE Weekly Routine Generator")

st.caption(
    "Department of Electronics and Computer Engineering"
)

st.markdown(
    """
This prototype generates an optimized weekly routine using
Google OR-Tools CP-SAT.
"""
)


# ============================================================
# TIME STRUCTURE
# ============================================================

def create_schedule():
    t1 = TimeBlockTemplate(
        id="T1",
        code="T1",
        name="Theory 1",
        display_order=1,
        start_time=__import__("datetime").time(7, 10),
        end_time=__import__("datetime").time(8, 45),
        day_part=DayPart.MORNING,
        allowed_activity_types=[ActivityType.THEORY],
    )

    t2 = TimeBlockTemplate(
        id="T2",
        code="T2",
        name="Theory 2",
        display_order=2,
        start_time=__import__("datetime").time(8, 45),
        end_time=__import__("datetime").time(10, 15),
        day_part=DayPart.MORNING,
        allowed_activity_types=[ActivityType.THEORY],
    )

    l1 = TimeBlockTemplate(
        id="L1",
        code="L1",
        name="Morning Lab",
        display_order=3,
        start_time=__import__("datetime").time(7, 10),
        end_time=__import__("datetime").time(9, 40),
        day_part=DayPart.MORNING,
        allowed_activity_types=[ActivityType.LAB],
    )

    t3 = TimeBlockTemplate(
        id="T3",
        code="T3",
        name="Theory 3",
        display_order=4,
        start_time=__import__("datetime").time(11, 0),
        end_time=__import__("datetime").time(12, 30),
        day_part=DayPart.AFTERNOON,
        allowed_activity_types=[ActivityType.THEORY],
    )

    t4 = TimeBlockTemplate(
        id="T4",
        code="T4",
        name="Theory 4",
        display_order=5,
        start_time=__import__("datetime").time(12, 30),
        end_time=__import__("datetime").time(14, 0),
        day_part=DayPart.AFTERNOON,
        allowed_activity_types=[ActivityType.THEORY],
    )

    l2 = TimeBlockTemplate(
        id="L2",
        code="L2",
        name="Afternoon Lab",
        display_order=6,
        start_time=__import__("datetime").time(11, 0),
        end_time=__import__("datetime").time(13, 30),
        day_part=DayPart.AFTERNOON,
        allowed_activity_types=[ActivityType.LAB],
    )

    return DailyScheduleTemplate(
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


# ============================================================
# SAMPLE DEPARTMENT DATA
# ============================================================

def generate_sample_routine():

    policy = InstitutionPolicy(
        max_students_per_section=48,
        max_students_per_lab_group=24,
        auto_split_lab_groups=True,
        auto_create_sections=True,
    )

    # --------------------------------------------------------
    # Academic cohorts
    # --------------------------------------------------------

    bct_cohort = AcademicCohort(
        id="bct-2082-2-1",
        program_id="bct",
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

    bei_cohort = AcademicCohort(
        id="bei-2082-2-1",
        program_id="bei",
        term_id="2-1",
        batch=2082,
        total_students=48,
        section_plans=[
            SectionPlan(
                code="A",
                name="Section A",
                student_count=24,
            ),
            SectionPlan(
                code="B",
                name="Section B",
                student_count=24,
            ),
        ],
    )

    section_generator = SectionGenerator()

    sections = []

    sections.extend(
        section_generator.generate(
            cohort=bct_cohort,
            policy=policy,
        )
    )

    sections.extend(
        section_generator.generate(
            cohort=bei_cohort,
            policy=policy,
        )
    )

    # --------------------------------------------------------
    # Teachers
    # --------------------------------------------------------

    ramesh = Teacher(
        id="ramesh",
        code="RT",
        name="Ramesh Tamang",
        employment_type=EmploymentType.FULL_TIME,
        max_periods_per_week=18,
        max_periods_per_day=4,
    )

    hari = Teacher(
        id="hari",
        code="HK",
        name="Hari Khadka",
        employment_type=EmploymentType.FULL_TIME,
        max_periods_per_week=18,
        max_periods_per_day=4,
    )

    sita = Teacher(
        id="sita",
        code="SP",
        name="Sita Poudel",
        employment_type=EmploymentType.FULL_TIME,
        max_periods_per_week=18,
        max_periods_per_day=4,
    )

    available_blocks = ["T1", "T2", "T3", "T4", "L1", "L2"]

    weekdays = [
        WeekDay.SUNDAY,
        WeekDay.MONDAY,
        WeekDay.TUESDAY,
        WeekDay.WEDNESDAY,
        WeekDay.THURSDAY,
        WeekDay.FRIDAY,
    ]

    for teacher in [ramesh, hari, sita]:

        teacher.availability = [
            TeacherAvailability(
                teacher_id=teacher.id,
                weekday=day,
                block_id=block,
            )
            for day in weekdays
            for block in available_blocks
        ]

    teachers = [ramesh, hari, sita]

    # --------------------------------------------------------
    # Teaching plans
    # --------------------------------------------------------

    teaching_plans = [

        # BCT OOP
        TeachingPlan(
            course_id="bct-oop",
            activity_type=ActivityType.THEORY,
            teacher_ids=["ramesh"],
            weekly_sessions=3,
            duration_minutes=90,
            parallel_groups=1,
            required_room_type=RoomType.CLASSROOM,
        ),

        TeachingPlan(
            course_id="bct-oop",
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
        ),

        # BEI Digital Logic
        TeachingPlan(
            course_id="bei-digital",
            activity_type=ActivityType.THEORY,
            teacher_ids=["ramesh"],
            weekly_sessions=3,
            duration_minutes=90,
            parallel_groups=1,
            required_room_type=RoomType.CLASSROOM,
        ),
    ]

    # --------------------------------------------------------
    # Course offerings
    # --------------------------------------------------------

    from academic_scheduler.models.course_offering import CourseOffering

    offerings = [
        CourseOffering(
            id=f"{bct_cohort.id}-oop",
            course_id="bct-oop",
            cohort_id=bct_cohort.id,
        ),
        CourseOffering(
            id=f"{bei_cohort.id}-digital",
            course_id="bei-digital",
            cohort_id=bei_cohort.id,
        ),
    ]

    # --------------------------------------------------------
    # Teaching assignments
    # --------------------------------------------------------

    assignment_generator = TeachingAssignmentGenerator()

    assignments = []

    assignments.extend(
        assignment_generator.generate(
            offering=offerings[0],
            sections=[
                s for s in sections
                if s.program_id == "bct"
            ],
            teaching_plans=[
                teaching_plans[0],
                teaching_plans[1],
            ],
        )
    )

    assignments.extend(
        assignment_generator.generate(
            offering=offerings[1],
            sections=[
                s for s in sections
                if s.program_id == "bei"
            ],
            teaching_plans=[
                teaching_plans[2],
            ],
        )
    )

    # --------------------------------------------------------
    # Session requirements
    # --------------------------------------------------------

    requirement_generator = SessionRequirementGenerator()

    requirements = requirement_generator.generate(
        teaching_assignments=assignments,
        templates=[
            SessionRequirementTemplate(
                activity_type=ActivityType.THEORY,
                occurrences=3,
                repeat_interval_weeks=1,
            ),
            SessionRequirementTemplate(
                activity_type=ActivityType.LAB,
                occurrences=1,
                repeat_interval_weeks=1,
            ),
        ],
    )

    # --------------------------------------------------------
    # Rooms
    # --------------------------------------------------------

    rooms = [
        Room(
            id="cl101",
            code="CL101",
            name="Classroom 101",
            room_type=RoomType.CLASSROOM,
            capacity=48,
        ),
        Room(
            id="cl102",
            code="CL102",
            name="Classroom 102",
            room_type=RoomType.CLASSROOM,
            capacity=60,
        ),
        Room(
            id="lab1",
            code="LAB1",
            name="Computer Lab 1",
            room_type=RoomType.COMPUTER_LAB,
            capacity=24,
        ),
        Room(
            id="lab2",
            code="LAB2",
            name="Computer Lab 2",
            room_type=RoomType.COMPUTER_LAB,
            capacity=24,
        ),
    ]

    # --------------------------------------------------------
    # Time grid
    # --------------------------------------------------------

    schedule = create_schedule()

    grid = TimeGrid()

    slots = grid.build(
        weekdays=weekdays,
        daily_schedule=schedule,
    )

    # --------------------------------------------------------
    # Sessions
    # --------------------------------------------------------

    session_generator = SessionGenerator()

    sessions = session_generator.generate(
        teaching_assignments=assignments,
        requirements=requirements,
        fixed_sessions=[],
    )

    # --------------------------------------------------------
    # Validate teachers
    # --------------------------------------------------------

    validator = TeacherAvailabilityValidator()

    if not validator.validate(
        teachers=teachers,
        sessions=sessions,
    ):
        raise ValueError(
            "Teacher availability validation failed."
        )

    # --------------------------------------------------------
    # Candidate slots
    # --------------------------------------------------------

    candidate_generator = CandidateSlotGenerator()

    candidates = candidate_generator.generate(
        sessions=sessions,
        slots=slots,
        teachers=teachers,
        rooms=rooms,
    )

    # --------------------------------------------------------
    # Check empty sessions
    # --------------------------------------------------------

    for session in sessions:

        count = sum(
            1
            for candidate in candidates
            if candidate.session_id == session.id
        )

        if count == 0:
            raise ValueError(
                f"No valid candidate slot for {session.id}"
            )

    # --------------------------------------------------------
    # CP-SAT
    # --------------------------------------------------------

    solver = CPSATSolver()

    assignments_set = AssignmentSet()

    variables = solver.build(
        sessions=sessions,
        candidate_slots=candidates,
        teachers=teachers,
        assignments=assignments_set,
    )

    cp_solver, status = solver.solve()

    if status not in (
        cp_model.OPTIMAL,
        cp_model.FEASIBLE,
    ):
        raise ValueError(
            f"No feasible timetable. "
            f"Solver status: {cp_solver.StatusName(status)}"
        )

    # --------------------------------------------------------
    # Build timetable
    # --------------------------------------------------------

    builder = TimetableBuilder()

    timetable = builder.build(
        solver=cp_solver,
        variables=variables,
        sessions=sessions,
        candidate_slots=candidates,
    )

    return timetable


# ============================================================
# UI
# ============================================================

st.sidebar.header("Department")

st.sidebar.info(
    """
Electronics and Computer Engineering

Programs:
• BCT
• BEI
"""
)

st.sidebar.header("Academic Sections")

program = st.sidebar.selectbox(
    "Program",
    ["BCT", "BEI"],
)

academic_part = st.sidebar.selectbox(
    "Year / Part",
    [
        "I/I",
        "I/II",
        "II/I",
        "II/II",
        "III/I",
        "III/II",
        "IV/I",
        "IV/II",
    ],
)

section_code = st.sidebar.selectbox(
    "Section",
    ["A", "B", "C"],
)

student_count = st.sidebar.number_input(
    "Students",
    min_value=1,
    max_value=100,
    value=30,
)

if "sections" not in st.session_state:
    st.session_state.sections = []

if st.sidebar.button(
    "➕ Add Section",
    use_container_width=True,
):

    section = {
        "program": program,
        "part": academic_part,
        "section": section_code,
        "students": student_count,
    }

    st.session_state.sections.append(section)


st.subheader("Academic Sections")

if st.session_state.sections:

    st.dataframe(
        st.session_state.sections,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No academic sections added yet."
    )


generate = st.button(
    "🚀 Generate Optimal Routine",
    type="primary",
    use_container_width=True,
)


if generate:

    with st.spinner("Generating optimized routine..."):

        try:

            timetable = generate_sample_routine()

            st.success(
                "Routine generated successfully."
            )

            st.metric(
                "Timetable Entries",
                len(timetable.entries),
            )

            rows = []

            for entry in timetable.entries:

                rows.append(
                    {
                        "Session": entry.session_id,
                        "Section": entry.section_id,
                        "Day": entry.weekday.value,
                        "Block": entry.block_id,
                        "Room": entry.room_id,
                        "Teachers": ", ".join(
                            entry.teacher_ids
                        ),
                    }
                )

            st.subheader("Generated Weekly Routine")

            st.dataframe(
                rows,
                use_container_width=True,
                hide_index=True,
            )

        except Exception as exc:

            st.error(
                "Routine generation failed."
            )

            st.exception(exc)