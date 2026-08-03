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


class SessionFrequency(str, Enum):
    """
    How often a session repeats.
    """

    WEEKLY = "Weekly"
    BIWEEKLY = "Biweekly"
    CUSTOM = "Custom"


# ==========================================================
# People
# ==========================================================

class EmploymentType(str, Enum):
    FULL_TIME = "Full-Time"
    PART_TIME = "Part-Time"
    VISITING = "Visiting"
    ADJUNCT = "Adjunct"


class PreferenceLevel(str, Enum):
    """
    Used for teacher preferences, room preferences,
    preferred time slots, etc.
    """

    REQUIRED = "Required"
    PREFERRED = "Preferred"
    NEUTRAL = "Neutral"
    AVOID = "Avoid"
    FORBIDDEN = "Forbidden"


# ==========================================================
# Rooms
# ==========================================================

class RoomType(str, Enum):
    CLASSROOM = "Classroom"

    COMPUTER_LAB = "Computer Lab"

    ELECTRONICS_LAB = "Electronics Lab"

    ELECTRICAL_LAB = "Electrical Lab"

    MECHANICAL_LAB = "Mechanical Lab"

    CIVIL_LAB = "Civil Lab"

    CHEMISTRY_LAB = "Chemistry Lab"

    PHYSICS_LAB = "Physics Lab"

    SEMINAR_HALL = "Seminar Hall"

    SMART_CLASSROOM = "Smart Classroom"

    AUDITORIUM = "Auditorium"


# ==========================================================
# Grouping
# ==========================================================

class GroupStrategy(str, Enum):
    """
    How student groups are formed.
    """

    NONE = "None"

    USER_DEFINED = "User Defined"

    AUTO = "Auto"


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