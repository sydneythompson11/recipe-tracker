import sqlite3

DB_FILE = "recipes.db"

def get_connection():
    """Returns a connection to the SQLite database file."""
    return sqlite3.connect(DB_FILE)

def initialize_db():
    """Creates the tables if they don't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # One row per recipe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            source TEXT,
            was_good INTEGER,       -- 1 = yes, 0 = no
            bake_again INTEGER,     -- 1 = yes, 0 = no
            easy_to_follow INTEGER  -- 1 = yes, 0 = no
        )
    """)

    # Multiple rows per recipe (one per ingredient)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            amount TEXT,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
    """)

    conn.commit()
    conn.close()

def add_recipe(name, source, was_good, bake_again, easy_to_follow, ingredients):
    """
    Inserts a recipe and its ingredients into the database.
    ingredients: list of dicts with 'name' and 'amount' keys
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO recipes (name, source, was_good, bake_again, easy_to_follow)
        VALUES (?, ?, ?, ?, ?)
    """, (name, source, was_good, bake_again, easy_to_follow))

    recipe_id = cursor.lastrowid  # get the ID of the recipe we just inserted

    for ingredient in ingredients:
        cursor.execute("""
            INSERT INTO ingredients (recipe_id, name, amount)
            VALUES (?, ?, ?)
        """, (recipe_id, ingredient["name"], ingredient["amount"]))

    conn.commit()
    conn.close()

def get_all_recipes():
    """Returns all recipes (without ingredients)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, source, was_good, bake_again, easy_to_follow FROM recipes")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_recipe_with_ingredients(recipe_id):
    """Returns a single recipe and all its ingredients."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()

    cursor.execute("SELECT name, amount FROM ingredients WHERE recipe_id = ?", (recipe_id,))
    ingredients = cursor.fetchall()

    conn.close()
    return recipe, ingredients
