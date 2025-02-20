# ORG-TREE

Org Tree is a tree chart showing relationships between employees.

## SETUP

- 1. Clone the repo

```
git clone https://github.com/solobarine/org-tree
cd org-tree
```

- 2. Create virtual environment

```
python -m venv .venv
```

- 3. Activate virtual environment

```
source .venv/bin/activate
```

### BACKEND

- 1. Navigate to backend directory

```
cd backend
```

- 2. Install Backend Dependencies

```
pip install -r requirements.txt
```

- 3. Start FastAPI Server

```
fastapi dev main.py
```

- 4. Seed Database
     Navigate to http://localhost:8000/seed-database to seed db with employees

### CLIENT

- 1. Navigate to client directory

```
cd client
```

- 2. Install dependencies

```
npm install
```

- 3. Start dev server

```
npm run dev
```

- 4. View client on http://localhost:5173

## DESIGN CHOICES

The database used was SQLite because of simplicity and ease of setup.

## TIME LOG

2hrs 34 mins (Outside planning).

## TODOS

- Implement the drag and drop functionality.
- Connect the client with the backend to make the request to update manager.
- Polish the Tree UI, making it look more like a tree.
- Implement UI feedback on successfully or failed API requests and creation of loading indicator when API request is pending.
