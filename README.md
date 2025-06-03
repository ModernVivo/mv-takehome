# Paper Explorer Take-Home Assignment

## Overview

Welcome! This take-home assignment assesses your full-stack engineering skills, with a focus on frontend development using Next.js, React, and TypeScript.  
You will build a “Paper Explorer” interface for browsing and annotating scientific papers, integrating with a provided Django REST backend.

---

## Assignment

**Frontend task:**  
Build a Next.js (TypeScript) frontend that interacts with the provided Django backend API to:

- Display a list of papers (with search/filter by title or author).
- Show details for a selected paper, including abstract and condition sets.
- Allow marking/unmarking a paper as “important” (persisted to backend).
- The design of the UI should follow our established design language. You should mock the UI in Figma before you begin.
- You can view our UI designs [here](https://www.figma.com/design/hnGEJdn9SV5g6nqqd46vE5/ModernVivo-UI-UX?node-id=0-1&t=i8x9JlCitC0uFqxH-1).

**Backend task:**

The current `/api/papers/?search=...` endpoint only matches papers where the search string appears in the title or authors. Improve the current basic search functionality (/api/papers/?search=) by making it more semantically aware (considering abstracts).

- You may use external Python packages (e.g., rapidfuzz, scikit-learn, spaCy, etc.), or full search libraries (e.g., Elasticsearch, Meilisearch, Pinecone, etc.).
- You are encouraged, but not strictly required, to leverage semantic embeddings or external LLM-based APIs (OpenAI, Hugging Face, Cohere, etc.).
- Briefly document your approach and reasoning in your submission.
---

## Tech Stack

**You must use the following frameworks and libraries for the frontend:**

- **Framework:** Next.js (with TypeScript)
- **UI:** React, with components built using Tailwind CSS  
  (If you’re comfortable, consider using [Radix UI](https://www.radix-ui.com/primitives) primitives for accessibility and unstyled base components, then style them with Tailwind.)
- **State Management:**  
  - [Zustand](https://zustand-demo.pmnd.rs/) for client-side state  
  - [TanStack React Query](https://tanstack.com/query/latest) for server state/data fetching
- **API Client:** [Axios](https://axios-http.com/)
- **Styling:** Tailwind CSS

---

## Getting Started

### 1. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata papers
python manage.py runserver
```

- The API will be available at `http://localhost:8000/api/papers/`

### 2. Frontend Setup

- The `frontend/` directory is empty.  
  Please initialize it as a Next.js (TypeScript) project and set up the required libraries above.

---

## API Reference

- `GET /api/papers/`  
  List all papers. Supports `?search=` query parameter.

- `GET /api/papers/<id>/`  
  Retrieve details for a specific paper.

- `POST /api/papers/<id>/important/`  
  Toggle the “important” status for a paper.

---

## Deliverables

- All code in this repository (both backend and frontend).
- Clear instructions in a `frontend/README.md` if any special setup is required.

**Frontend Documentation (README.md):**
- Brief instructions for setup and running your frontend app.
- Short notes (~1–3 short paragraphs or bullet points) about key design choices, assumptions, and any noteworthy technical decisions.

**Backend Documentation (included in README.md or separate markdown):**
- Brief explanation detailing:
  - Your chosen search improvement approach.
  - Any libraries, APIs, or services used, and your rationale for choosing them.
  - Briefly discuss trade-offs and considerations (e.g., simplicity vs. performance, external API costs, ease of setup).
---

## Evaluation Criteria

- Code clarity, structure, and maintainability.
- UI/UX quality and polish.
- Correctness of API integration.
- Use of TypeScript, Next.js, and React best practices.
- Proper use of the required libraries.

---

## Notes

- The backend is pre-populated with sample data.
- No need to deploy the backend or frontend; local setup is sufficient.
- If you have questions, feel free to reach out.
