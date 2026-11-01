"""School Management System - Streamlit entrypoint.

Run with:  streamlit run app.py

Handles database bootstrap, sign-in and role-based navigation. Each page lives
in ``pages/`` and is registered explicitly with ``st.navigation`` so that every
role only sees (and can only open) its own pages.
"""
from __future__ import annotations

import streamlit as st

from utils.config import DEMO_MODE, SCHOOL_NAME

st.set_page_config(
    page_title=SCHOOL_NAME,
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

from database.seed import DEMO_ACCOUNTS, DEMO_ADMIN_PASSWORD  # noqa: E402
from database.session import init_db  # noqa: E402
from services import auth  # noqa: E402
from utils import session  # noqa: E402
from utils.config import ADMIN_USERNAME  # noqa: E402
from utils.ui import show_flash  # noqa: E402
from utils.validators import ValidationError  # noqa: E402

# (file, title, icon, url_path) for each page.
_PAGES = {
    "dashboard": ("pages/dashboard.py", "Dashboard", "📊"),
    "announcements": ("pages/announcements.py", "Announcements", "📢"),
    "students": ("pages/students.py", "Students", "🎓"),
    "teachers": ("pages/teachers.py", "Teachers", "👩‍🏫"),
    "academics": ("pages/classes_subjects.py", "Classes & Subjects", "🏫"),
    "attendance": ("pages/attendance.py", "Attendance", "🗓️"),
    "exams": ("pages/exams_results.py", "Exams & Results", "📝"),
    "fees": ("pages/fees.py", "Fees", "💰"),
    "timetable": ("pages/timetable.py", "Timetable", "⏰"),
    "users": ("pages/users.py", "User Accounts", "🔐"),
    "account": ("pages/account.py", "My Account", "⚙️"),
}

_NAV_BY_ROLE = {
    "admin": ["dashboard", "announcements", "students", "teachers", "academics", "attendance",
              "exams", "fees", "timetable", "users", "account"],
    "teacher": ["dashboard", "announcements", "students", "attendance", "exams", "timetable",
                "account"],
    "student": ["dashboard", "announcements", "attendance", "exams", "fees", "timetable",
                "account"],
}


@st.cache_resource(show_spinner="Preparing the database...")
def _bootstrap() -> bool:
    """Create tables and seed data once per server process."""
    init_db()
    return True


def _login_screen() -> None:
    _, middle, _ = st.columns([1, 1.4, 1])
    with middle:
        st.markdown(f"## 🏫 {SCHOOL_NAME}")
        st.caption("School Management System")
        show_flash()
        with st.form("login_form"):
            username = st.text_input("Username", autocomplete="username")
            password = st.text_input("Password", type="password", autocomplete="current-password")
            submitted = st.form_submit_button("Sign in", type="primary")
        if submitted:
            try:
                session.login(auth.authenticate(username, password))
                st.rerun()
            except ValidationError as exc:
                st.error(str(exc))
        if DEMO_MODE:
            with st.expander("Demo logins", expanded=True):
                st.markdown(
                    f"| Role | Username | Password |\n|---|---|---|\n"
                    f"| Admin | `{ADMIN_USERNAME}` | `{DEMO_ADMIN_PASSWORD}` |\n"
                    + "".join(
                        f"| {label} | `{user}` | `{password}` |\n"
                        for label, user, password in DEMO_ACCOUNTS
                    )
                )
                st.caption("Demo mode is on. Set DEMO_MODE=false before real use.")


def main() -> None:
    try:
        _bootstrap()
    except RuntimeError as exc:  # e.g. ADMIN_PASSWORD missing in production mode
        st.error(f"Setup problem: {exc}")
        st.stop()

    user = session.current_user()
    if user is None:
        _login_screen()
        return

    pages = {
        key: st.Page(path, title=title, icon=icon, url_path=key, default=(key == "dashboard"))
        for key, (path, title, icon) in _PAGES.items()
    }
    navigation = st.navigation([pages[key] for key in _NAV_BY_ROLE[user["role"]]])

    with st.sidebar:
        st.markdown(f"**{user['full_name']}**")
        st.caption(f"{user['role'].title()} · {SCHOOL_NAME}")
        st.button("Sign out", on_click=session.logout, key="sign_out")

    show_flash()
    navigation.run()


main()
