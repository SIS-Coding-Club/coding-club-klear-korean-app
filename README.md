# Klear Korean

Klear Korean is a modular Korean language learning application designed to help learners improve specific language skills through interactive exercises and progress tracking.

Rather than following a fixed curriculum, users can practice individual areas of Korean at their own pace, with exercises that gradually increase in difficulty.

## Modules

- **Particles Practice** — Practice choosing the correct Korean particles in sentences.
- **Pronunciation Practice** — Planned
- **Sentence Structure Practice** - Planned
- **Politeness Practice** - Planned

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** SQLite, SQLAlchemy ORM, aiosqlite
- **Authentication:** Cookie-based session authentication

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SIS-Coding-Club/coding-club-klear-korean-app.git
cd coding-club-klear-korean-app
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

The backend will run at `http://127.0.0.1:8000`.

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Current Progress

Klear Korean is currently under development. Currently, the program established a backend authentication system and is working on the Korean particles practice module. Additional learning modules are planned for future development.