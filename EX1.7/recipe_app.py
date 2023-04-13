from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, String
from sqlalchemy import Column
from sqlalchemy.orm import sessionmaker

# Connect to the database through SQLAlchemy
engine = create_engine("mysql://cf-python:password@localhost/task_database")

# Create session object
Session = sessionmaker(bind=engine)
session = Session()

# Create declarative base class
Base = declarative_base()


class Recipe(Base):
    __tablename__ = 'final_recipes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Getter methods
    def get_name(self):
        return self.name

    def get_ingredients(self):
        return self.ingredients

    def get_cooking_time(self):
        return self.cooking_time

    def get_difficulty(self):
        return self.difficulty

    # Caluculate difficulties based on the number of ingredients and cooking time
    def calculate_difficulty(self):
        ingredients_list = self.return_ingredietns_as_list()
        if self.cooking_time < 10 and len(ingredients_list) < 4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and len(ingredients_list) >= 4:
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(ingredients_list) < 4:
            self.difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(ingredients_list) >= 4:
            self.difficulty = 'Hard'

    # Converts string of ingredients to a list
    def return_ingredietns_as_list(self):
        if self.ingredients == '':
            ingredients_list = []
        else:
            ingredients_list = self.ingredients.split(', ')
        return ingredients_list

    def __repr__(self):
        return '\n<Recipe ID: ' + str(self.id) + ' - Name: ' + self.name + ' - Difficulty: ' + self.difficulty + '>'

    def __str__(self):
        ingredients_list = self.return_ingredietns_as_list()
        output = '\nRecipe Name: ' + self.get_name() + '\nCooking Time: ' + str(self.get_cooking_time()) + \
            '\nDifficulty: ' + self.get_difficulty() + '\nIngredients: \n'
        for ingredient in ingredients_list:
            output += ingredient + '\n'
        return output


# Create talble of the model defined above
Base.metadata.create_all(engine)


def create_recipe():
    # Ask user for recipe name and check if it doesn't extend past 50 chars
    correct_name = False
    while correct_name == False:
        name = str(input('\nEnter the recipe name: '))
        if len(name) > 50:
            print('\nRecipe name must be maximum 50 characters.')
        else:
            correct_name = True

    # Ask user for cooking time and check if the input contains only numbers
    correct_cooking_time = False
    while correct_cooking_time == False:
        cooking_time = input('\nEnter the cooking time in minutes (e.g. 5): ')
        if cooking_time.isnumeric() and int(cooking_time) > 0:
            cooking_time = int(cooking_time)
            correct_cooking_time = True
        else:
            print('\nInvalid input. It must be positive integer.')

    # Define temporary ingredietns list
    ingredients_list = []
    # Ask user for the amount of ingredients to be added and check if the input contains only a number
    correct_input_num = False
    while correct_input_num == False:
        input_num = input('\nHow many ingredients would you like to add?: ')
        if input_num.isnumeric() and int(input_num) > 0:
            input_num = int(input_num)
            correct_input_num = True
        else:
            print('\nEnter only a valid number (positive integer)')

    # Ask user for ingredients
    for i in range(0, input_num):
        ingredient_input = input('\nEnter an ingredient: ')
        if ingredient_input not in ingredients_list:
            ingredients_list.append(ingredient_input)

    # Convert list of ingredients to a string
    ingredients_str = ", ".join(ingredients_list)

    # Create a new recipe object from Recipe model
    recipe_entry = Recipe(
        name=name,
        cooking_time=cooking_time,
        ingredients=ingredients_str,
    )
    # Calculate difficulty and asign the result value to the difficulty attributes
    Recipe.calculate_difficulty(recipe_entry)

    # Add the entry to final_recipes table on databse and commit changes
    session.add(recipe_entry)
    session.commit()

    print('\nRecipe saved into database.')


def view_all_recipes():
    # Retrieve all recipes on the database
    # If no recipes found on the database, return to main menu
    all_recipes_list = session.query(Recipe).all()
    if len(all_recipes_list) == 0:
        print('\nThere is no recipes found on the database.')
        return None
    else:
        print('\nAll recipes found on database:')
        print('=' * 50)
        for recipe in all_recipes_list:
            print(recipe)
            print()


def search_by_ingredients():
    # Retrieve all recipes on the database
    # If no recipes found on the database, return to main menu
    if session.query(Recipe).count() == 0:
        print('\nThere is no recipes found on the database.')
        return None

    # Retrive only the values from ingredients column
    ingredients_result = session.query(Recipe.ingredients).all()

    all_ingredients = []
    # Append all ingredients to all_ingredients list
    for ingredients_tup in ingredients_result:
        for ingredients_str in ingredients_tup:
            ingredients_split = ingredients_str.split(', ')
            all_ingredients.extend(ingredients_split)

    # Remove dupication
    all_ingredients = list(dict.fromkeys(all_ingredients))
    # Create list of ingredients using enumerate()
    all_ingredients_list = list(enumerate(all_ingredients))

    print('\nAvailable Ingredients to search from: ')
    print('-' * 50)
    for ingredients_tup in all_ingredients_list:
        print('\t' + str(ingredients_tup[0] + 1) + '. ' + ingredients_tup[1])

    try:
        # Ask user to select the numbers corresponding to the ingredients
        search_number = input(
            '\nEnter the number corresponding to the ingredient you would like to select. You can enter several numbers separated by comma followed by a space (e.g. 1, 3, 5): ')
        search_number_list = search_number.split(', ')

        # Create a list of ingredients to search for recipes containing selected ingredients
        search_ingredients_list = []
        for number in search_number_list:
            search_index = int(number) - 1
            search_ingredient = all_ingredients_list[search_index][1]
            search_ingredients_list.append(search_ingredient)
        print('\nYou selected the ingredient(s): ')
        for ingredient in search_ingredients_list:
            print(ingredient)

        condition_list = []
        for ingredient in search_ingredients_list:
            like_term = "%"+ingredient+"%"
            condition = Recipe.ingredients.like(like_term)
            condition_list.append(condition)
        recipes_result = session.query(Recipe).filter(*condition_list).all()
    except:
        print('\nAn unexpected error occurred. Make sure to select numbers from the list.')
    else:
        print('\nRecipes found containing the ingredient(s) selected:')
        print('=' * 50)
        for recipe in recipes_result:
            print(recipe)


def edit_recipe():
    # Retrieve all recipes on the database
    # If no recipes found on the database, return to main menu
    if session.query(Recipe).count() == 0:
        print('\nThere is no recipes found on the database.')
        return None

    # Retrieve IDs and names of all the recipes and display them to user
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    print('\nRecipes available for modification:')
    print('=' * 50)
    for result in results:
        print('Recipe ID: ' + str(result[0]) + ' - ' + result[1])

    # Ask user to enter the ID of the recipe to be modified and check if the input is valid
    selected_id = input('Enter the ID of the recipe you would like to edit: ')
    # Make a temporary list of only IDs to check if selected ID exists
    results_ids = []
    for result in results:
        results_ids.append(result[0])

    if not (selected_id.isnumeric()):
        print('\nID must be a number.')
        return None
    elif not (int(selected_id) in results_ids):
        print('\nThe recipe with entered ID doesn\'t exist.')
        return None
    else:
        recipe_to_edit = session.get(Recipe, int(selected_id))
        print('\n1. Recipe Name: ' + recipe_to_edit.name + '\n2. Cooking Time: ' +
              str(recipe_to_edit.cooking_time) + '\n3. Ingredients:\n' + recipe_to_edit.ingredients)

        # Ask user for the field to be modified and check if the input is valid
        correct_edit_option = False
        option_nums = [1, 2, 3]
        while correct_edit_option == False:
            edit_option = input(
                '\nEnter the number of the filed you would like to edit: ')
            if not (edit_option.isnumeric()) or not (int(edit_option) in option_nums):
                print('\nInalid option number. It must be 1, 2 or 3')
            else:
                correct_edit_option = True

        # If user choose option 1 (Edit name)
        if edit_option == '1':
            correct_name = False
            while correct_name == False:
                name = str(input('\nEnter the new recipe name: '))
                if len(name) > 50:
                    print('\nRecipe name must be maximum 50 characters.')
                else:
                    correct_name = True
            # Save and commit changes
            recipe_to_edit.name = name
            session.commit()
            print('\nRecipe name changed to ' + name)

        # If user choose option 2 (Edit cooking time)
        elif edit_option == '2':
            correct_cooking_time = False
            while correct_cooking_time == False:
                cooking_time = input(
                    '\nEnter the cooking time in minutes (e.g. 5): ')
                if cooking_time.isnumeric() and int(cooking_time) > 0:
                    cooking_time = int(cooking_time)
                    correct_cooking_time = True
                else:
                    print('\nInvalid input. It must be positive integer.')
            # Save and commit changes
            recipe_to_edit.cooking_time = cooking_time
            recipe_to_edit.calculate_difficulty()
            session.commit()
            print('\nCooking time changed to ' + str(cooking_time))

        # If user choose option 3 (Edit ingredients)
        elif edit_option == '3':
            # Define temporary ingredietns list
            ingredients_list = []
            print('\nNote that you have to write all the ingredients for the recipe as the data will be overwritten.')
            # Ask user for the amount of ingredients to be added and check if the input contains only a number
            correct_input_num = False
            while correct_input_num == False:
                input_num = input(
                    '\nHow many ingredients would you like to add?: ')
                if input_num.isnumeric():
                    input_num = int(input_num)
                    correct_input_num = True
                else:
                    print('\nEnter only a valid number (positive integer)')

            # Ask user for ingredients
            for i in range(0, input_num):
                ingredient_input = input('\nEnter an ingredient: ')
                if ingredient_input not in ingredients_list:
                    ingredients_list.append(ingredient_input)

            # Convert list of ingredients to a string
            ingredients_str = ", ".join(ingredients_list)

            # Save and commit changes
            recipe_to_edit.ingredients = ingredients_str
            recipe_to_edit.calculate_difficulty()
            session.commit()
            print('\nIngredients changed to ' + ingredients_str)


def delete_recipe():
    # Retrieve all recipes on the database
    # If no recipes found on the database, return to main menu
    if session.query(Recipe).count() == 0:
        print('\nThere is no recipes found on the database.')
        return None

    # Retrieve IDs and names of all the recipes and display them to user
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    print('\nRecipes available:')
    print('=' * 50)
    for result in results:
        print('Recipe ID: ' + str(result[0]) + ' - ' + result[1])

    # Ask user to enter the ID of the recipe to be modified and check if the input is valid
    selected_id = input(
        '\nEnter the ID of the recipe you would like to delete: ')
    # Make a temporary list of only IDs to check if selected ID exists
    results_ids = []
    for result in results:
        results_ids.append(result[0])

    if not (selected_id.isnumeric()):
        print('\nID must be a number.')
        return None
    elif not (int(selected_id) in results_ids):
        print('\nThe recipe with entered ID doesn\'t exist.')
        return None
    else:
        recipe_to_delete = session.get(Recipe, int(selected_id))
        # Confirm user for the deletion
        confirmation = input(
            '\nAre you sure you would like to delete the recipe? (yes/no): ').lower()
        if confirmation == 'yes':
            # Proceed the deletion and commit change
            session.delete(recipe_to_delete)
            session.commit()
            print('\nRecipe ' + recipe_to_delete.name + ' deleted')
        elif confirmation == 'no':
            return None


def main_menu():
    choice = ''
    # Ask user which operation to perform until user enters 'quit'
    while (choice != 'quit'):
        print('\nMain Menu')
        print('=' * 50)
        print('Pick a number from the options below:')
        print('\t1. Create a new recipe')
        print('\t2. View all recipes')
        print('\t3. Search for a recipe by ingredient')
        print('\t4. Update an existing recipe')
        print('\t5. Delete a recipe')
        print('\tType "quit" to exit the program')
        choice = input('Your choice: ')

        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        else:
            if choice == 'quit':
                print('Goodbye')
            else:
                print(
                    '\nEnter the valid option number. or type "quit" to exit the program')
    # Close database connection
    session.close()


# Calls the main menu
main_menu()
