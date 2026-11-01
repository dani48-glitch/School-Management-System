"""Central configuration.

Every setting is read from an environment variable first and from Streamlit
secrets (``.streamlit/secrets.toml`` locally, the *Secrets* box on Streamlit
Community Cloud) second, so credentials never need to live in the source code.
"""
from __future__ import annotations

import os
from typing import Any


def get_setting(key: str, default: Any = None) -> Any:
    """Return ``key`` from the environment, then ``st.secrets``, then ``default``."""
    value = os.environ.get(key)
    if value not in (None, ""):
        return value
    try:
        import streamlit as st

        if key in st.secrets:
            return st.secrets[key]
    except Exception:  # no secrets file, or not running under Streamlit
        pass
    return default


def get_bool(key: str, default: bool = False) -> bool:
    """Read a boolean setting ("true", "1", "yes" and "on" are truthy)."""
    value = get_setting(key, None)
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


# --------------------------------------------------------------------------
# Deployment settings (override through environment variables or secrets)
# --------------------------------------------------------------------------
SCHOOL_NAME = str(get_setting("SCHOOL_NAME", "Green Valley School"))
CURRENCY = str(get_setting("CURRENCY", "Rs."))
TIMEZONE = str(get_setting("TIMEZONE", "UTC"))
DATABASE_URL = str(get_setting("DATABASE_URL", "sqlite:///school.db"))

# DEMO_MODE seeds sample data and shows the demo logins on the sign-in page.
# Set DEMO_MODE=false and ADMIN_PASSWORD=... for a real deployment.
DEMO_MODE = get_bool("DEMO_MODE", True)
ADMIN_USERNAME = str(get_setting("ADMIN_USERNAME", "admin"))
ADMIN_PASSWORD = get_setting("ADMIN_PASSWORD", None)
SESSION_TIMEOUT_MINUTES = int(get_setting("SESSION_TIMEOUT_MINUTES", 60))

# --------------------------------------------------------------------------
# Domain constants
# --------------------------------------------------------------------------
ROLES = ("admin", "teacher", "student")

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
PERIODS = {
    1: "08:00-08:40",
    2: "08:40-09:20",
    3: "09:20-10:00",
    4: "10:20-11:00",
    5: "11:00-11:40",
    6: "11:40-12:20",
}

ATTENDANCE_STATUSES = ["Present", "Absent", "Late", "Leave"]
LOW_ATTENDANCE_PERCENT = 75

PAYMENT_METHODS = ["Cash", "Bank Transfer", "Cheque", "Online"]

# (minimum percentage, grade, remark) - checked from the top down.
GRADE_SCALE = [
    (90, "A+", "Outstanding"),
    (80, "A", "Excellent"),
    (70, "B", "Very Good"),
    (60, "C", "Good"),
    (50, "D", "Satisfactory"),
    (40, "E", "Pass"),
    (0, "F", "Fail"),
]
PASS_PERCENT = 40

MAX_FAILED_LOGINS = 5
LOCKOUT_MINUTES = 10
