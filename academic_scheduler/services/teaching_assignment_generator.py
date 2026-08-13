from academic_scheduler.models.section import Section
from academic_scheduler.models.teaching_assignment import TeachingAssignment
from academic_scheduler.models.teaching_plan import TeachingPlan
from academic_scheduler.common.enums import ActivityType
from academic_scheduler.models.course_offering import CourseOffering

class TeachingAssignmentGenerator:
    """
    Generates teaching assignments from
    teaching plans and generated sections.
    """

    def generate(
        self,
        offering: CourseOffering,
        sections: list[Section],
        teaching_plans: list[TeachingPlan],
    ) -> list[TeachingAssignment]:

        for section in sections:

            if section.cohort_id != offering.cohort_id:
                raise ValueError(
                    f"Section '{section.id}' does not belong to "
                    f"course offering cohort '{offering.cohort_id}'."
                )

            for plan in teaching_plans:

                if plan.course_id != offering.course_id:
                    raise ValueError(
                        f"Teaching plan for course '{plan.course_id}' "
                        f"does not match course offering '{offering.course_id}'."
                    )

                # existing assignment-generation logic continues here

        assignments = []

        for section in sections:

            for plan in teaching_plans:

                group_count = (
                    plan.parallel_groups
                    if plan.activity_type == ActivityType.LAB
                    else 1
                )

                if plan.activity_type == ActivityType.LAB:

                    students_per_group = (
                        section.student_count
                        // plan.parallel_groups
                    )

                else:

                    students_per_group = section.student_count

                for group_index in range(1, group_count + 1):

                    assignment = TeachingAssignment(

                        id=(
                            f"{plan.course_id}-"
                            f"{section.code}-"
                            f"{plan.activity_type.name.lower()}-"
                            f"G{group_index}"
                        ),

                        course_id=plan.course_id,

                        section_id=section.id,

                        teacher_ids=(
                            plan.parallel_group_teacher_ids[group_index - 1]
                            if (
                                plan.activity_type == ActivityType.LAB
                                and plan.parallel_group_teacher_ids is not None
                            )
                            else plan.teacher_ids
                        ),

                        activity_type=plan.activity_type,

                        group_index=group_index,

                        weekly_sessions=plan.weekly_sessions,

                        duration_minutes=plan.duration_minutes,

                        students_per_session=students_per_group,

                        required_room_type=plan.required_room_type,

                    )

                    assignments.append(assignment)

        return assignments