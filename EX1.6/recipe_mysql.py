import mysql.connector

# Initialize connection object
conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password')

# Initialize cursor object in order to perform operations on the database
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)
)''')

# cursor.execute("DESCRIBE Recipes")
# result = cursor.fetchall()
# for row in result:
#     print(row[0])


def main_menu(conn, cursor):
    choice = ''
    while (choice != 'quit'):
        print('Main Menu')
        print('=========================================')
        print('Pick a choice: ')
        print('    1. Create a new recipe')
        print('    2. Search for a recipe by ingredient')
        print('    3. Update an existing recipe')
        print('    4. Delete a recipe')
        print('    5. View all recipes')
        print('    Type "quit" to exit the program')
        choice = input('Your choice: ')

        if choice == '1':
            create_recipe(conn, cursor)

        elif choice == '2':
            search_recipe(conn, cursor)

        elif choice == '3':
            update_recipe(conn, cursor)

        elif choice == '4':
            delete_recipe(conn, cursor)

        elif choice == '5':
            view_all_recipes(conn, cursor)
    conn.close()


def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = 'Easy'
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = 'Medium'
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = 'Intermediate'
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = 'Hard'
    return difficulty


def create_recipe(conn, cursor):
    # Take Recipe details from user (name, cooking time, ingredients) and calculate difficulty
    name = str(input('Enter the recipe name: '))
    ingredients = str(input(
        'Enter the ingredients separated with commas (e.g. pasta, eggs, oil): '))
    ingredients_list = ingredients.split(', ')
    cooking_time = int(
        input('Enter the cooking time in minutes (e.g. 5): '))
    difficulty = calculate_difficulty(cooking_time, ingredients_list)

    sql = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, ingredients, cooking_time, difficulty)
    cursor.execute(sql, val)
    conn.commit()
    print('Recipe ' + name + 'saved into the database')


def search_recipe(conn, cursor):
    all_ingredients = []
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    for row in results:
        for ingredients_tup in row:
            ingredients_list = ingredients_tup.split(', ')
            all_ingredients.extend(ingredients_list)

    # Remove dupication
    all_ingredients = list(dict.fromkeys(all_ingredients))
    # Create enumerate list of ingredients
    all_ingredients_list = list(enumerate(all_ingredients))

    print('Available Ingredients to search from: ')
    print('--------------------------------------------')
    for ingredients_tup in all_ingredients_list:
        print(str(ingredients_tup[0] + 1) + '. ' + ingredients_tup[1])

    try:
        search_number = int(
            input('Enter the number corresponding to the ingredient you want to select: '))
        search_ingredient = all_ingredients_list[search_number - 1][1]
    except:
        print('An unexpected error occurred. Make sure to select a number from the list')
    else:
        cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s",
                       ('%' + search_ingredient + '%',))
        result_recipes = cursor.fetchall()
        print('Recipe found with ' + search_ingredient + ': ')
        print('--------------------------------------------')
        for row in result_recipes:
            print('ID: ', row[0])
            print('Recipe Name: ', row[1])
            print('Ingredients: ', row[2])
            print('Cooking time: ', str(row[3]), ' minutes')
            print('Difficulty: ', row[4])
            print()


def update_recipe(conn, cursor):
    # Display all the recipes
    view_all_recipes(conn, cursor)

    # Ask user to enter the ID of the recipe to be updated
    selected_id = int(input(
        'Enter the ID number of the recipe you would like to update: '))

    # Ask user to select the column to be updated
    print('Select the field you would like to update: ')
    print('    1. name')
    print('    2. cooking time')
    print('    3. ingredients')
    selected_field_num = input('Your choice: ')

    if selected_field_num == '1':
        name = str(input('Enter the new recipe name: '))
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s",
                       (name, selected_id))
        print('Recipe name updated')

    elif selected_field_num == '2':
        # Update cooking time
        cooking_time = int(
            input('Enter the cooking time in minutes (e.g. 5): '))
        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s",
                       (cooking_time, selected_id))

        # Get ingredients of the recipe and recalculate difficulty
        cursor.execute(
            "SELECT ingredients FROM Recipes WHERE id = %s", (selected_id,))
        ingredients = cursor.fetchall()
        ingredients_list = ingredients[0][0].split(', ')
        difficulty = calculate_difficulty(cooking_time, ingredients_list)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s",
                       (difficulty, selected_id))

    elif selected_field_num == '3':
        # Update ingredients
        ingredients = str(input(
            'Enter the ingredients separated with commas (e.g. pasta, eggs, oil): '))
        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s",
                       (ingredients, selected_id))

        # Get cooking time of the recipe and recalculate difficulty
        ingredients_list = ingredients.split(', ')
        cursor.execute(
            "SELECT cooking_time FROM Recipes WHERE id = %s", (selected_id,))
        cooking_time = cursor.fetchall()
        difficulty = calculate_difficulty(
            int(cooking_time[0][0]), ingredients_list)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s",
                       (difficulty, selected_id))

    conn.commit()


def delete_recipe(conn, cursor):
    view_all_recipes(conn, cursor)
    selected_id = int(input(
        'Enter the ID number of the recipe you would like to delete: '))
    cursor.execute("DELETE FROM Recipes WHERE id = %s", (selected_id,))
    conn.commit()
    print('Recipe ID: ' + str(selected_id) + 'deleted from the database')


def view_all_recipes(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    result_all_recipes = cursor.fetchall()
    print('All recipes: ')
    print('--------------------------------------------')
    for row in result_all_recipes:
        print('ID: ', row[0])
        print('Recipe Name: ', row[1])
        print('Ingredients: ', row[2])
        print('Cooking time: ', str(row[3]) + ' minutes')
        print('Difficulty: ', row[4])
        print()


main_menu(conn, cursor)
