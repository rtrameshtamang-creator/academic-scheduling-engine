from enum import Enum


# ==========================================================
# Academic
# ==========================================================

class WeekDay(str, Enum):
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


class ActivityType(str, Enum):
    THEORY = "Theory"
    LAB = "Lab"
    TUTORIAL = "Tutorial"
    SEMINAR = "Seminar"
    WORKSHOP = "Workshop"
    PROJECT = "Project"
    PRESENTATION = "Presentation"
    VIVA = "Viva"
    EXAM = "Exam"


class DayPart(str, Enum):
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"


# ==========================================================
# People
# ==========================================================

class EmploymentType(str, Enum):
    FULL_TIME = "Full-Time"
    PART_TIME = "Part-Time"
    VISITING = "Visiting"
    ADJUNCT = "Adjunct"


# ==========================================================
# Rooms
# ==========================================================

class RoomType(str, Enum):
    CLASSROOM = "Classroom"
    LABORATORY = "Laboratory"
    SEMINAR_HALL = "Seminar Hall"
    AUDITORIUM = "Auditorium"


# ==========================================================
# Constraints
# ==========================================================

class ConstraintType(str, Enum):
    HARD = "Hard"
    SOFT = "Soft"


class ConstraintPriority(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


# ==========================================================
# Schedule
# ==========================================================

class ScheduleStatus(str, Enum):
    DRAFT = "Draft"
    GENERATED = "Generated"
    VALIDATED = "Validated"
    PUBLISHED = "Published"
    ARCHIVED = "Archived"