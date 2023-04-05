class Recipe:
    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.cooking_time = int(0)
        self.ingredients = []
        self.difficulty = ''

    def get_name(self):
        return self.name

    def set_name(self):
        self.name = input('Enter the name for your recipe: ')

    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self):
        self.cooking_time = int(
            input('Enter the cooking time in minutes (e.g. 5): '))

    def add_ingredients(self, *ingredients):
        self.ingredients = list(ingredients)
        self.update_all_ingredients()

    def get_ingredients(self):
        return self.ingredients

    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = 'Hard'

    def get_difficulty(self):
        if self.difficulty == '':
            self.calculate_difficulty()
        return self.difficulty

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if not (ingredient in Recipe.all_ingredients):
                Recipe.all_ingredients.append(ingredient)

    def __str__(self):
        output = '\nRecipe Name: ' + self.get_name() + '\nCooking Time: ' + str(self.get_cooking_time()) + \
            '\nDifficulty: ' + self.get_difficulty() + '\nIngredients: \n'
        for ingredient in self.ingredients:
            output += ingredient + '\n'
        return output

    def search_ingredient(self, ingredient, ingredients):
        if (ingredient in ingredients):
            return True
        else:
            return False

    def recipe_search(self, data, search_term):
        for recipe in data:
            if self.search_ingredient(search_term, recipe.ingredients):
                print(recipe)


tea = Recipe('tea')
tea.set_name()
tea.add_ingredients('Tea Leaves', 'Sugar', 'Water')
tea.set_cooking_time()
print(tea)

coffee = Recipe('coffee')
coffee.set_name()
coffee.add_ingredients('Coffee Powder', 'Sugar', 'Water')
coffee.set_cooking_time()
print(coffee)

cake = Recipe('cake')
cake.set_name()
cake.add_ingredients('Sugar', 'Butter', 'Eggs',
                     'Vanilla Essence', 'Flour', 'Baking Powder', 'Milk')
cake.set_cooking_time()
print(cake)

banana_smoothie = Recipe('banana smoothie')
banana_smoothie.set_name()
banana_smoothie.add_ingredients(
    'Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes')
banana_smoothie.set_cooking_time()
print(banana_smoothie)

recipes_list = [tea, coffee, cake, banana_smoothie]

search_terms = ['Water', 'Sugar', 'Bananas']
for search_term in search_terms:
    print('Results for recipe search with ' + search_term)
    print('-' * 40)
    tea.recipe_search(recipes_list, search_term)
