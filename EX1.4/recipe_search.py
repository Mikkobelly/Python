import pickle


def display_recipe(recipe):
    print('---------------------------------------------------')
    print('Recipe Name: ' + recipe['name'])
    print('Cooking Time: ' + str(recipe['cooking_time']) + ' ' + 'minutes')
    print('Ingredients: ')
    print(', '.join(recipe['ingredients']))
    print('Difficulty: ' + recipe['difficulty'])
    print('---------------------------------------------------')


def search_ingredient(data):
    # Display all the available ingredients
    print('---------------------------------------------------')
    print('Available ingredients: ')
    for position, value in enumerate(data['all_ingredients'], 1):
        print(str(position) + ': ' + value)
    print('---------------------------------------------------')

    try:
        index_searched = int(
            input('Enter the corresponding number of your chosen ingredient: '))
        ingredient_searched = data['all_ingredients'][index_searched - 1]
    except IndexError:
        print('The number you entered is invalid.')
    except:
        print('Unexpected error occured.')
    else:
        for recipe in data['recipes_list']:
            for ingredient in recipe['ingredients']:
                if ingredient == ingredient_searched:
                    print('Recipe found that contains ' + ingredient + ': ')
                    display_recipe(recipe)


file_name = input('Enter the file name that contains recipes data: ')

try:
    file = open(file_name, 'rb')
    data = pickle.load(file)
except FileNotFoundError:
    print('The file doesn\'t exist. Check whether the file name is correct.')
except:
    print('Unexpected error occured. Please try again.')
else:
    search_ingredient(data)
