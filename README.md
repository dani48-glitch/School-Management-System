# School-Management-System
# School Management System

A role-based school management web app built with **Python, Streamlit, SQLAlchemy and Plotly**.
It runs locally in one command and deploys to **Streamlit Community Cloud** straight from GitHub.

> 📸 *Screenshots: add images to `docs/` and link them here, for example `![Dashboard](docs/dashboard.png)`.*

## Features

| Module | What it does |
|---|---|
| **Login & roles** | Admin, Teacher and Student/Parent accounts. bcrypt-hashed passwords, `st.session_state` sessions, idle timeout, lock-out after repeated failed logins. Each role only sees its own pages. |
| **Students** | Add, search, edit in place (`st.data_editor`) and delete: name, roll no., class, section, DOB, guardian, phone, address. |
| **Teachers** | Profiles, subjects and classes taught. |
| **Classes & subjects** | Create classes/sections and subjects, assign a teacher to each subject of each class. |
| **Attendance** | Daily marking per class, monthly report, day-by-day grid, attendance % per student. |
| **Exams & results** | Per-subject marks entry, automatic total / percentage / grade / rank, report card as a downloadable PDF. |
| **Fees** | Fee structure per class, record payments, pending dues, printable PDF receipts. |
| **Timetable** | Weekly timetable per class and per teacher, with teacher double-booking detection. |
| **Announcements** | Admin posts notices that every role can read. |
| **Dashboard** | Students, teachers, today's attendance, fees collected vs pending, with Plotly charts. |
| **Exports** | Every table has CSV and Excel download buttons. |

### Who can do what

| Page | Admin | Teacher | Student / Parent |
|---|:-:|:-:|:-:|
| Dashboard | school-wide | own classes | own overview |
| Students | full edit | view own classes | - |
| Teachers, Classes & Subjects, User Accounts | ✅ | - | - |
| Attendance | mark + reports | mark + reports (own classes) | own record |
| Exams & Results | full | enter marks for own subjects | own results + report card |
| Fees | full | - | own fees + receipts |
| Timetable | edit | view (own schedule or any class) | own class |
| Announcements | post + delete | read | read |

## Project structure

```
school-management-system/
├── app.py                  # entry point: sign-in + role-based navigation
├── init_db.py              # create tables / seed / reset from the command line
├── requirements.txt
├── pages/                  # one script per page (dashboard, students, fees, ...)
├── services/               # business logic (no Streamlit code), returns DataFrames/dicts
├── database/               # SQLAlchemy models, engine/session, seed data
├── utils/                  # config, security (bcrypt), validators, table + UI helpers
├── .streamlit/
│   ├── config.toml         # theme
│   └── secrets.toml.example
└── .github/workflows/lint.yml
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The first start creates `school.db` (SQLite) and, because `DEMO_MODE` defaults to `true`, fills it with a sample school.

### Demo logins (demo mode only)

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `Admin@123` |
| Teacher | `teacher` | `Teacher@123` |
| Student / Parent | `student` | `Student@123` |

These are published sample credentials. **Turn demo mode off before real use** (see below).

## Configuration

Every setting is read from an environment variable first, then from Streamlit secrets
(`.streamlit/secrets.toml` locally, the **Secrets** box on Streamlit Cloud). Copy
`.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` to start.

| Key | Default | Purpose |
|---|---|---|
| `DEMO_MODE` | `true` | Load sample data and show demo logins. Set `false` for real use. |
| `ADMIN_USERNAME` | `admin` | First administrator. |
| `ADMIN_PASSWORD` | *(none)* | **Required when `DEMO_MODE=false`.** Min 8 chars, letter + digit. |
| `DATABASE_URL` | `sqlite:///school.db` | Any SQLAlchemy URL, e.g. PostgreSQL. |
| `SCHOOL_NAME` | `Green Valley School` | Shown in the UI and on PDFs. |
| `CURRENCY` | `Rs.` | Prefix for fee amounts. |
| `TIMEZONE` | `UTC` | IANA name (e.g. `Asia/Karachi`); decides what "today" means. |
| `SESSION_TIMEOUT_MINUTES` | `60` | Idle sign-out. |

The admin account is created only when the database has no users yet, so changing
`ADMIN_PASSWORD` later does not change an existing admin. Use **User Accounts → Reset password**.

## Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: School Management System"
git branch -M main
git remote add origin https://github.com/<your-username>/school-management-system.git
git push -u origin main
```

Check that `.streamlit/secrets.toml` and `*.db` do **not** appear in `git status` (they are in `.gitignore`).

## Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **Create app → Deploy a public app from GitHub**.
3. Pick your repository, branch `main`, and main file path `app.py`.
4. Open **Advanced settings**: choose **Python 3.12** and paste your secrets, for example:
   ```toml
   DEMO_MODE = false
   ADMIN_PASSWORD = "a-strong-password-1"
   SCHOOL_NAME = "My School"
   TIMEZONE = "Asia/Karachi"
   DATABASE_URL = "postgresql+psycopg2://user:password@host:5432/dbname"
   ```
5. Click **Deploy**.

### ⚠️ Keep your data safe: use PostgreSQL in production

Streamlit Community Cloud has a **temporary file system**: a SQLite file is wiped whenever the
app restarts or is redeployed. SQLite is fine for trying the app out. For real school data:

1. Create a free PostgreSQL database (for example on [Supabase](https://supabase.com) or [Neon](https://neon.tech)).
2. Uncomment `psycopg2-binary` in `requirements.txt`.
3. Set `DATABASE_URL` to the connection string, as above. Nothing else changes.

## Notes

- **Attendance %** = (Present + Late) / days marked × 100. Below 75% is flagged.
- **Grades:** A+ ≥ 90, A ≥ 80, B ≥ 70, C ≥ 60, D ≥ 50, E ≥ 40, F below 40. A student fails if any subject is below 40%. Change `GRADE_SCALE` and `PASS_PERCENT` in `utils/config.py`.
- **PDFs** use built-in Latin-1 fonts. For Urdu or other scripts, register a Unicode TTF in `services/pdf.py`.
- Deleting a student also deletes their attendance, results, payments and login (enforced by database foreign keys).
- Linting: `pip install flake8 && flake8 .` (also runs on every push through GitHub Actions).

## License

MIT, see [LICENSE](LICENSE).
