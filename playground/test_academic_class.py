from academic_scheduler.models.academic_class import AcademicClass


academic_class = AcademicClass(
    id="bct-2-2",
    program_id="bct",
    year_part="II/II",
    maximum_students=48,
    enrolled_students=20,
)

print(academic_class)