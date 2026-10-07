# CodeLens — AI Code Reviewer

> A full-stack developer tool for analyzing source code for security, quality, and maintainability issues using both deterministic static analysis and AI-powered review.

**Live Demo:** [CodeLens — Live Demo](https://codelens-ai-code-reviewer-1.onrender.com/?utm_source=chatgpt.com)
**Backend API:** [CodeLens API](https://codelens-ai-code-reviewer-8qxr.onrender.com/?utm_source=chatgpt.com)
**Repository:** [GitHub Repository](https://github.com/Sandip-Px/codelens-ai-code-reviewer.git?utm_source=chatgpt.com)

---

## Overview

CodeLens is a full-stack AI-assisted code review application designed to demonstrate how a modern developer tool can combine traditional static analysis with large language models.

Users can paste source code into a browser-based Monaco editor, select a programming language, choose an analysis mode, and receive a structured code review containing:

* Overall code quality score
* Security issues
* Maintainability problems
* Code quality issues
* Severity levels
* Source-code line references
* Explanations
* Suggested improvements
* Review history

The application supports two analysis approaches:

### Local Analysis

A deterministic analyzer checks the submitted code using predefined rules.

This provides fast, predictable feedback without requiring an AI API call.

### AI Analysis

The application sends the code to an AI model and requests a structured review.

The AI response is converted into the same review format used by the local analyzer, allowing both approaches to be displayed through the same frontend.

---

## Why I Built This

CodeLens was built as a portfolio project to demonstrate practical full-stack development rather than simply building another CRUD application.

The project combines:

* **React frontend development**
* **FastAPI backend development**
* **REST API design**
* **PostgreSQL database integration**
* **SQLAlchemy ORM**
* **Monaco Editor integration**
* **Static code analysis**
* **OpenAI API integration**
* **Environment-based configuration**
* **Cloud database deployment**
* **Backend deployment**
* **Frontend deployment**
* **Git/GitHub workflow**

The goal was to build a small but complete developer product that can be used from a public URL.

---

# Features

## Code Editor

CodeLens uses the Monaco Editor to provide a browser-based coding environment.

Users can:

* Write or paste code
* Select the programming language
* View line numbers
* Navigate through source code
* Jump directly to lines associated with detected issues

Supported languages currently include:

* Python
* JavaScript
* Java

---

## Two Review Modes

### Local Analysis

The local analyzer uses predefined rules to identify common problems.

Advantages:

* Fast
* Deterministic
* No AI API request required
* Useful for predictable security and quality checks

Example issues can include unsafe operations and suspicious coding patterns.

---

### AI Analysis

AI Analysis sends the submitted source code to the configured AI model and requests a structured code review.

The resulting review contains:

```text
Score
Summary
Issues
Severity
Category
Line
Message
Suggestion
```

The AI result is normalized into the same format used by the frontend.

This means the UI does not need separate result rendering logic for local and AI reviews.

---

# Review Results

Each review produces an overall score from **0–10**.

The interface also summarizes detected issues by severity:

| Severity | Meaning                                                   |
| -------- | --------------------------------------------------------- |
| HIGH     | Significant security, correctness, or reliability concern |
| MEDIUM   | Important quality or maintainability concern              |
| LOW      | Minor issue or improvement opportunity                    |

Individual issues can contain:

* Severity
* Category
* Line number
* Explanation
* Suggested fix

Clicking a line reference moves the Monaco editor directly to the relevant line.

---

# Review History

Every completed review is stored in PostgreSQL.

The application displays recent reviews including:

* Review ID
* Programming language
* Creation date
* Number of detected issues
* Quality score

Selecting a previous review restores its source code and review results.

This allows CodeLens to function as more than a one-time code checker.

---

# Architecture

```text
                         ┌──────────────────────┐
                         │      User Browser    │
                         │                      │
                         │  React + Vite        │
                         │  Monaco Editor       │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP / JSON
                                    ▼
                         ┌──────────────────────┐
                         │     FastAPI API      │
                         │                      │
                         │  Review Endpoints    │
                         │  CORS                │
                         │  Validation          │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌──────────────────┐             ┌──────────────────┐
          │ Local Analyzer   │             │   AI Analyzer    │
          │                  │             │                  │
          │ Rule-based       │             │ OpenAI API       │
          │ analysis         │             │ structured       │
          └────────┬─────────┘             │ review           │
                   │                       └────────┬─────────┘
                   │                                │
                   └──────────────┬─────────────────┘
                                  │
                                  ▼
                         ┌──────────────────────┐
                         │    PostgreSQL /      │
                         │        Neon          │
                         │                      │
                         │  code_reviews        │
                         │  review_issues       │
                         └──────────────────────┘
```

---

# Tech Stack

## Frontend

* React
* Vite
* JavaScript
* Monaco Editor
* CSS

The frontend provides the interactive workspace and communicates with the FastAPI backend through REST endpoints.

---

## Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

FastAPI handles:

* HTTP requests
* Request validation
* Review execution
* Database persistence
* Review history
* Health checks
* CORS configuration

---

## Database

* PostgreSQL
* Neon
* SQLAlchemy ORM

The production database is hosted on Neon.

The database stores both review-level information and individual issues.

---

## AI

* OpenAI API

AI reviews are requested as structured JSON and converted into the application's review schema.

This allows AI-generated results to be presented consistently with deterministic local analysis.

---

## Deployment

### Frontend

The React/Vite application is deployed as a Render static site.

### Backend

The FastAPI application is deployed as a Render web service.

### Database

PostgreSQL is hosted using Neon.

```text
Browser
   │
   ▼
Render Static Site
   │
   │ REST API
   ▼
Render FastAPI Service
   │
   ▼
Neon PostgreSQL
```

---

# Project Structure

```text
ai-code-reviewer/
│
├── app/
│   ├── api/
│   │   └── reviews.py
│   │
│   ├── database/
│   │   └── init_db.py
│   │
│   ├── models/
│   │   └── ...
│   │
│   ├── schemas/
│   │   └── ...
│   │
│   ├── services/
│   │   ├── analyzer.py
│   │   └── ai_analyzer.py
│   │
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── tests/
│   └── ...
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# API

The backend exposes a small REST API for interacting with reviews.

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

This endpoint is also used by the frontend to determine whether the API is available.

---

## List Recent Reviews

```http
GET /api/reviews/
```

Returns recent code reviews.

The frontend uses this endpoint to populate the **Recent Reviews** section.

---

## Create Review

```http
POST /api/reviews/
```

Example request:

```json
{
  "code": "def calculate_total(items):\n    return sum(items)",
  "language": "python",
  "mode": "local"
}
```

The `mode` field determines which analyzer is used.

```text
local → deterministic local analyzer

ai → AI-powered analyzer
```

---

## Get Review

```http
GET /api/reviews/{review_id}
```

Returns a previously stored review and its associated issues.

---

# Example Review

Given code such as:

```python
def calculate_total(items):
    total = 0

    for item in items:
        total += eval(item)

    print(total)
    return total
```

CodeLens can identify the use of `eval()` as a security concern.

A review can contain information such as:

```json
{
  "score": 2,
  "summary": "The code contains a significant security risk.",
  "issues": [
    {
      "severity": "HIGH",
      "category": "Security",
      "line": 5,
      "message": "Use of eval() can execute arbitrary code.",
      "suggestion": "Avoid eval() and parse or validate the input explicitly."
    }
  ]
}
```

The frontend then presents this information through the review dashboard and allows the user to jump directly to the problematic line.

---

# Database Design

The application separates reviews from individual issues.

## `code_reviews`

Stores information about the overall review.

Conceptually:

```text
code_reviews
├── id
├── code
├── language
├── score
├── summary
└── created_at
```

## `review_issues`

Stores individual problems associated with a review.

```text
review_issues
├── id
├── review_id
├── severity
├── category
├── line
├── message
└── suggestion
```

Relationship:

```text
code_reviews
      │
      │ 1
      │
      │
      │ N
      ▼
review_issues
```

A single review can therefore contain multiple detected issues.

---

# Local Development

## Prerequisites

Install:

* Python 3.13+
* Node.js
* npm
* PostgreSQL

An OpenAI API key is only required when using AI Analysis.

---

## Clone the Repository

```bash
git clone https://github.com/Sandip-Px/codelens-ai-code-reviewer.git

cd codelens-ai-code-reviewer
```

---

# Backend Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=your_database_url

OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=your_model

ANALYZER_MODE=local

FRONTEND_URL=http://localhost:5173
```

### Important

Never commit the real `.env` file or API keys to GitHub.

The repository should only contain placeholder configuration such as:

```env
DATABASE_URL=
OPENAI_API_KEY=
OPENAI_MODEL=
ANALYZER_MODE=local
FRONTEND_URL=http://localhost:5173
```

---

# Initialize the Database

Run:

```bash
python -m app.database.init_db
```

This creates the required PostgreSQL tables.

---

# Start the Backend

Run:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

FastAPI also provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

Move into the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create:

```text
frontend/.env
```

with:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Start Vite:

```bash
npm run dev
```

The development application will normally be available at:

```text
http://localhost:5173
```

---

# Production Frontend Configuration

The deployed frontend uses:

```env
VITE_API_URL=https://codelens-ai-code-reviewer-8qxr.onrender.com
```

The frontend uses this value to communicate with the deployed FastAPI service.

This avoids hardcoding the production API URL throughout the React application.

---

# CORS

The backend configures CORS using the frontend URL supplied through the environment.

Local development:

```env
FRONTEND_URL=http://localhost:5173
```

Production:

```env
FRONTEND_URL=https://your-frontend.onrender.com
```

This allows the deployed React application to communicate with the FastAPI API while avoiding an unrestricted CORS configuration.

---

# Deployment

CodeLens is deployed using three services:

```text
                     ┌─────────────────┐
                     │     Render      │
                     │   React/Vite    │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │     Render      │
                     │    FastAPI      │
                     └────────┬────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
             ┌─────────────┐     ┌─────────────┐
             │    Neon     │     │  OpenAI API │
             │ PostgreSQL  │     │             │
             └─────────────┘     └─────────────┘
```

### Frontend

The frontend is built with:

```bash
npm run build
```

The generated `dist` directory is served by Render.

### Backend

Render runs the FastAPI application using Uvicorn.

### Database

The production PostgreSQL database is hosted on Neon.

---

# Configuration Flow

The application intentionally keeps environment-specific configuration outside the source code.

```text
.env
 │
 ├── DATABASE_URL
 ├── OPENAI_API_KEY
 ├── OPENAI_MODEL
 ├── ANALYZER_MODE
 └── FRONTEND_URL
```

The frontend has its own Vite environment configuration:

```text
frontend/.env
        │
        └── VITE_API_URL
```

This allows the same codebase to run locally and in production without changing API URLs inside React components.

---

# Security Considerations

CodeLens is designed as a demonstration and portfolio application, but several security considerations were intentionally included.

### Environment-based secrets

API keys and database credentials are stored in environment variables instead of source code.

### CORS configuration

The backend restricts browser requests to the configured frontend origin.

### Structured AI output

AI responses are expected to follow a structured schema rather than being rendered as arbitrary generated UI.

### Issue categorization

Security issues are surfaced separately from general maintainability and quality issues.

---

# What I Learned

This project provided hands-on experience with several areas of modern application development.

### Full-stack integration

Connecting React, FastAPI, PostgreSQL, and external APIs required designing a consistent data flow across the entire application.

### REST API design

The frontend communicates with the backend through dedicated endpoints for creating and retrieving reviews.

### Database modeling

Reviews and issues are represented as related database entities instead of storing everything as a single unstructured object.

### AI integration

AI-generated analysis needs to be treated as structured application data rather than simply displaying a block of generated text.

### Production deployment

The application was developed locally and then deployed across separate frontend, backend, and database services.

### Environment configuration

Local and production environments require different API endpoints and credentials, which are handled through environment variables.

### Error handling

The frontend tracks API connectivity and displays different states for connecting, connected, and offline conditions.

---

# Current Limitations

CodeLens is intentionally a relatively small application.

Current limitations include:

* Limited language support
* Rule-based local analysis is not a full compiler/static-analysis engine
* AI analysis depends on external API availability
* No authentication system
* Review history is not user-specific
* No team/project management
* No pull-request integration
* No CI/CD code scanning integration
* No persistent user accounts

These are potential directions for future development.

---

# Future Improvements

Possible next steps include:

### More Languages

Add support for:

* C++
* C#
* TypeScript
* Go
* Rust
* PHP

### Better Static Analysis

Integrate language-specific tools such as:

* AST analysis
* Linters
* Type checking
* Security scanners
* Complexity analysis

### User Accounts

Introduce authentication and user-specific review history.

### GitHub Integration

Allow users to:

* Connect a GitHub repository
* Select a pull request
* Analyze changed files
* Post review comments
* Track review results

### CI/CD Integration

CodeLens could eventually run automatically during pull requests:

```text
Pull Request
     │
     ▼
CodeLens
     │
     ├── Security analysis
     ├── Quality analysis
     └── AI review
     │
     ▼
Review Report
```

### Improved AI Reviews

Future versions could provide:

* More precise issue categorization
* Confidence scores
* Fix generation
* Code explanations
* Refactoring suggestions
* Multi-file analysis

---

# Screenshots

Add screenshots of the deployed application here.

Recommended screenshots:

### Main Workspace

```text
docs/screenshots/editor.png
```

Show:

* Code editor
* Language selector
* Analysis mode selector
* Review button

### Review Results

```text
docs/screenshots/review-results.png
```

Show:

* Quality score
* Severity summary
* Detected issues
* Suggestions

### Review History

```text
docs/screenshots/history.png
```

Show:

* Recent reviews
* Scores
* Languages
* Timestamps

Example Markdown once screenshots are added:

```md
![CodeLens workspace](docs/screenshots/editor.png)

![Code review results](docs/screenshots/review-results.png)

![Review history](docs/screenshots/history.png)
```

---

# Project Goals

The primary goals of CodeLens were:

* Build a complete full-stack application
* Integrate an AI-powered feature into a practical developer workflow
* Provide a deterministic non-AI fallback
* Persist application data using PostgreSQL
* Build an interactive developer-focused UI
* Deploy the application publicly
* Practice production environment configuration
* Create a project suitable for a software development portfolio

---

# Demo Workflow

The typical CodeLens workflow is:

```text
1. Open CodeLens
       │
       ▼
2. Paste source code
       │
       ▼
3. Select language
       │
       ▼
4. Select analysis mode
       │
       ├───────────────┐
       ▼               ▼
   Local Analysis   AI Analysis
       │               │
       └───────┬───────┘
               ▼
        Analyze source
               │
               ▼
        Calculate score
               │
               ▼
        Detect issues
               │
               ▼
        Store review
               │
               ▼
        Display results
               │
               ▼
        Save to history
```

---

# License

This project is available under the license included in this repository.

See [`LICENSE`](LICENSE) for details.

---

# Author

**Sandip**

GitHub: [Sandip-Px](https://github.com/Sandip-Px?utm_source=chatgpt.com)

---

## Live Application

Try CodeLens here:

The application is deployed as a production-style full-stack system using React, FastAPI, PostgreSQL/Neon, Render, and AI-powered code analysis.
