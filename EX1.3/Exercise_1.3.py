# Defining a funtion that takes users input and returns a recipe in a dictionary format
def take_recipe():
    name = input('Enter the name of the recipe: ')
    cooking_time = int(input('Enter the cooking time in minutes (e.g. 10): '))
    ingredients = input(
        'Enter the ingredients separating with conma (e.g. pasta, olive oil, eggs): ')
    recipe = dict({
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients.split(', ')
    })
    return recipe


# Initializing lists
recipes_list = []
ingredients_list = []

n = int(input('How many recipes would you like to enter? '))


# Add each ingredient to the ingredients list which is a global variable
for i in range(0, n):
    recipe = take_recipe()

    for ele in recipe['ingredients']:
        if not (ele in ingredients_list):
            ingredients_list.append(ele)

    recipes_list.append(recipe)


# Define the difficulty of each recipe and print them out
for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        difficulty = 'Easy'

    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        difficulty = 'Medium'

    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        difficulty = 'Intermediate'

    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        difficulty = 'Hard'

    print('Recipe: ' + recipe['name'])
    print('Cooking Time (min): ' + str(recipe['cooking_time']))
    print('Ingredients: ')
    for ele in recipe['ingredients']:
        print(ele)
    print('Difficulty level: ' + difficulty)


# Print out all the ingredients stored in the ingredients list
print('Ingredietns Available Across All Recipes')
print('-----------------------------------------------')
for ele in ingredients_list:
    print(ele)
