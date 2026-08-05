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
        print("-" * 80)

        for entry in timetable.entries:

            teachers = ", ".join(entry.teacher_ids)

            print(
                f"{entry.course_id:10}"
                f"{entry.weekday.value:10}"
                f"{entry.block_id:6}"
                f"{entry.room_id:10}"
                f"{teachers}"
            )