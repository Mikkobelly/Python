import pickle


def calc_difficulty(recipe):
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        difficulty = 'Easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        difficulty = 'Medium'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        difficulty = 'Intermediate'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        difficulty = 'Hard'
    return difficulty


def take_recipe():
    name = input('Please enter the recipe name: ')
    cooking_time = int(
        input('Please enter the cooking time in minutes(e.g. 10): '))
    ingredients = input(
        'Please enter the ingredients for your recipe separated with comma (e.g. pasta, olive oil): ').lower().split(', ')
    recipe_obj = dict({
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    })
    recipe_obj['difficulty'] = calc_difficulty(recipe_obj)
    return recipe_obj


# Main code begins here
recipes_list = []
all_ingredients = []

file_name = input(
    'Please enter the file name where you\'ve stored your recipes: ')

try:
    file = open(file_name, 'rb')
    data = pickle.load(file)
except FileNotFoundError:
    print('File not found. Creating a new file.')
    data = {
        'recipes_list': recipes_list,
        'all_ingredients': all_ingredients
    }
except:
    print('Something went wrong. Creating a new file.')
    data = {
        'recipes_list': recipes_list,
        'all_ingredients': all_ingredients
    }
else:
    file.close()
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']


num = int(input('How many recipes would you like to add? '))

for i in range(0, num):
    recipe = take_recipe()
    recipes_list.append(recipe)
    for ele in recipe['ingredients']:
        if not (ele in all_ingredients):
            all_ingredients.append(ele)
    data = {
        'recipes_list': recipes_list,
        'all_ingredients': all_ingredients
    }

new_file_name = input('Enter a name for your new file: ')
with open(new_file_name, 'wb') as file:
    pickle.dump(data, file)
