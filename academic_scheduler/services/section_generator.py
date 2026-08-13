from academic_scheduler.models.academic_cohort import AcademicCohort
from academic_scheduler.models.institution_policy import (
    InstitutionPolicy,
)
from academic_scheduler.models.section import (
    Section,
)



class SectionGenerator:
    """
    Generates academic sections from course cohorts
    and institution policy.
    """

    def generate(
        self,
        cohort: AcademicCohort,
        policy: InstitutionPolicy,
    ) -> list[Section]:

        sections = []

        for plan in cohort.section_plans:

            section = Section(
                id=f"{cohort.program_id}-{cohort.batch}-{plan.code}",
                code=plan.code,
                name=plan.name,
                program_id=cohort.program_id,
                term_id=cohort.term_id,
                batch=cohort.batch,
                student_count=plan.student_count,
            )

            sections.append(section)

        return sections