from academic_scheduler.models.teacher import Teacher
from academic_scheduler.models.session_instance import SessionInstance


class TeacherAvailabilityValidator:
    """
    Checks whether teachers have enough available
    time slots for their assigned sessions.
    """

    def validate(
        self,
        teachers: list[Teacher],
        sessions: list[SessionInstance],
    ) -> None:

        from collections import defaultdict

        from academic_scheduler.common.enums import ActivityType


        required_theory = defaultdict(int)
        required_lab = defaultdict(int)

        available_theory = defaultdict(int)
        available_lab = defaultdict(int)

        # -------------------------
        # Count required sessions
        # -------------------------

        for session in sessions:

            for teacher_id in session.teacher_ids:

                if session.activity_type == ActivityType.THEORY:
                    required_theory[teacher_id] += 1

                elif session.activity_type == ActivityType.LAB:
                    required_lab[teacher_id] += 1


        # -------------------------
        # Count available slots
        # -------------------------

        for teacher in teachers:

            for availability in teacher.availability:

                if availability.block_id.startswith("T"):
                    available_theory[teacher.id] += 1

                elif availability.block_id.startswith("L"):
                    available_lab[teacher.id] += 1


        # -------------------------
        # Print report
        # -------------------------

        print("\nTeacher Availability Validation")
        print("-" * 60)

        for teacher in teachers:

            theory_required = required_theory[teacher.id]
            theory_available = available_theory[teacher.id]

            lab_required = required_lab[teacher.id]
            lab_available = available_lab[teacher.id]

            print(f"\nTeacher : {teacher.name}")

            print(
                f"Theory : "
                f"{theory_required} required / "
                f"{theory_available} available"
            )

            if theory_required > theory_available:
                print("❌ Insufficient theory availability")
            else:
                print("✅ Theory availability OK")

            print(
                f"Lab    : "
                f"{lab_required} required / "
                f"{lab_available} available"
            )

            if lab_required > lab_available:
                print("❌ Insufficient lab availability")
            else:
                print("✅ Lab availability OK")
        valid = True

        for teacher in teachers:

            theory_required = required_theory[teacher.id]
            theory_available = available_theory[teacher.id]

            lab_required = required_lab[teacher.id]
            lab_available = available_lab[teacher.id]

            # ... existing print statements ...

            if theory_required > theory_available:
                valid = False

            if lab_required > lab_available:
                valid = False

        return valid