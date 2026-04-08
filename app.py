from database import initialize_db, migrate_db, add_recipe, get_all_recipes, get_recipe_with_ingredients, update_recipe_instructions

def yes_no_input(prompt):
    """Helper to get a yes/no answer and convert to 1/0."""
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer in ("y", "n"):
            return 1 if answer == "y" else 0
        print("Please enter y or n.")

def add_recipe_flow():
    """Walks the user through adding a new recipe."""
    print("\n--- Add a New Recipe ---")
    name = input("Recipe name: ").strip()
    source = input("Where did you find it? (URL, cookbook, etc.): ").strip()
    was_good = yes_no_input("Was it good?")
    bake_again = yes_no_input("Would you bake it again?")
    easy_to_follow = yes_no_input("Was it easy to follow?")

    ingredients = []
    print("Enter ingredients one at a time. Type 'done' when finished.")
    while True:
        ing_name = input("  Ingredient name (or 'done'): ").strip()
        if ing_name.lower() == "done":
            break
        amount = input(f"  Amount/measurement for {ing_name}: ").strip()
        ingredients.append({"name": ing_name, "amount": amount})

    print("Enter the recipe instructions (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    instructions = "\n".join(lines)

    add_recipe(name, source, was_good, bake_again, easy_to_follow, ingredients, instructions)
    print(f"\nRecipe '{name}' saved!")

def view_all_recipes():
    """Prints a summary list of all recipes."""
    recipes = get_all_recipes()
    if not recipes:
        print("\nNo recipes saved yet.")
        return

    print("\n--- Your Recipes ---")
    for r in recipes:
        id, name, source, was_good, bake_again, easy_to_follow = r
        print(f"[{id}] {name} | Source: {source} | Good: {'Yes' if was_good else 'No'} | "
              f"Bake Again: {'Yes' if bake_again else 'No'} | Easy: {'Yes' if easy_to_follow else 'No'}")

def view_recipe_detail():
    """Shows full detail including ingredients for one recipe."""
    view_all_recipes()
    try:
        recipe_id = int(input("\nEnter recipe ID to view details: "))
    except ValueError:
        print("Invalid ID.")
        return

    recipe, ingredients = get_recipe_with_ingredients(recipe_id)
    if not recipe:
        print("Recipe not found.")
        return

    id, name, source, was_good, bake_again, easy_to_follow, instructions = recipe
    print(f"\n--- {name} ---")
    print(f"Source: {source}")
    print(f"Was it good? {'Yes' if was_good else 'No'}")
    print(f"Bake again? {'Yes' if bake_again else 'No'}")
    print(f"Easy to follow? {'Yes' if easy_to_follow else 'No'}")
    print("Ingredients:")
    for ing_name, amount in ingredients:
        print(f"  - {amount} {ing_name}")
    if instructions:
        print(f"\nInstructions:\n{instructions}")

def edit_recipe_instructions():
    """Lets the user add or update instructions on an existing recipe."""
    view_all_recipes()
    try:
        recipe_id = int(input("\nEnter recipe ID to edit instructions: "))
    except ValueError:
        print("Invalid ID.")
        return

    print("Enter the updated instructions (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    instructions = "\n".join(lines)

    update_recipe_instructions(recipe_id, instructions)
    print("Instructions updated!")

def main():
    initialize_db()
    migrate_db()  # safely adds new columns without losing existing data
    while True:
        print("\n=== Recipe Tracker ===")
        print("1. Add a recipe")
        print("2. View all recipes")
        print("3. View recipe details")
        print("4. Edit recipe instructions")
        print("5. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_recipe_flow()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            view_recipe_detail()
        elif choice == "4":
            edit_recipe_instructions()
        elif choice == "5":
            print("Bye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
