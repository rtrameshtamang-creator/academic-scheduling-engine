from academic_scheduler.models.timetable import Timetable


class TimetablePrinter:
    """
    Prints a generated timetable.
    """

    def print(
        self,
        timetable: Timetable,
    ) -> None:

        print("\nGenerated Timetable\n")

        print(
            f"{'Session ID':35}"
            f"{'Section':15}"
            f"{'Day':10}"
            f"{'Block':8}"
            f"{'Room':10}"
            f"{'Teachers'}"
        )

        print("-" * 110)

        for entry in timetable.entries:

            teachers = ", ".join(entry.teacher_ids)

            print(
                f"{entry.session_id:35}"
                f"{entry.section_id:15}"
                f"{entry.weekday.value:10}"
                f"{entry.block_id:8}"
                f"{entry.room_id:10}"
                f"{teachers}"
            )