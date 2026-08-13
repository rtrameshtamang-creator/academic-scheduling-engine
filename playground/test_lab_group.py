from academic_scheduler.models.lab_group import LabGroup


group1 = LabGroup(
    id="oop-lab-g1",
    name="Group 1",
    student_count=20,
    teacher_ids=["hari", "sita"],
)

group2 = LabGroup(
    id="oop-lab-g2",
    name="Group 2",
    student_count=24,
    teacher_ids=["sita"],
)

print(group1)
print(group2)