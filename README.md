# Recipe Tracker

A simple command-line app to track recipes you've baked, built with Python and SQLite.

## Features
- Save recipes with name, source, and ingredients
- Rate each recipe: was it good, would you bake again, easy to follow?
- View all recipes or drill into details with full ingredient list

## How to Run

```bash
python app.py
```

No installs needed — uses Python's built-in `sqlite3` module.

## Project Structure

```
recipe-tracker/
├── app.py        # CLI interface
├── database.py   # Database setup and queries
└── recipes.db    # Auto-created SQLite database file
```
