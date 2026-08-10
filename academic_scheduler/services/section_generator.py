from academic_scheduler.models.course_offering import (
    CourseOffering,
)
from academic_scheduler.models.institution_policy import (
    InstitutionPolicy,
)
from academic_scheduler.models.section import (
    Section,
)


class SectionGenerator:
    """
    Generates academic sections from course offerings
    and institution policy.
    """

    def generate(
        self,
        offering: CourseOffering,
        policy: InstitutionPolicy,
    ) -> list[Section]:

        sections = []

        for plan in offering.section_plans:

            section = Section(
                id=f"{offering.program_id}-{offering.batch}-{plan.code}",
                code=plan.code,
                name=plan.name,
                program_id=offering.program_id,
                term_id=offering.term_id,
                batch=offering.batch,
                student_count=plan.student_count,
            )

            sections.append(section)

        return sections