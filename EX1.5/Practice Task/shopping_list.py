class ShoppingList(object):
    def __init__(self, list_name):
        self.list_name = str(list_name)
        self.shopping_list = []

    def add_item(self, item):
        if not (str(item).lower() in self.shopping_list):
            self.shopping_list.append(str(item.lower()))

    def remove_item(self, item):
        try:
            self.shopping_list.remove(str(item.lower()))
        except:
            print('Item not found in the list')

    def merge_list(self, obj):
        merged_lists_name = 'Merged List Name - ' + \
            str(self.list_name) + ' + ' + str(obj.list_name)

        merged_lists_obj = ShoppingList(merged_lists_name)

        merged_lists_obj.shopping_list = self.shopping_list.copy()

        for item in obj.shopping_list:
            if not (item in merged_lists_obj.shopping_list):
                merged_lists_obj.shopping_list.append(item)

        return merged_lists_obj

    def view_list(self):
        print('Items in ' + str(self.list_name) + ': ')
        for item in self.shopping_list:
            print(item)


# Create new object
pet_store_list = ShoppingList('Pet Store Shopping List')

# Add items
items = ['dog food', 'frisbee', 'bowl', 'collars', 'flea collars']
for item in items:
    pet_store_list.add_item(item)

# Remove the item 'flea collars'
pet_store_list.remove_item('flea collars')

# Try adding 'frisbee' again
pet_store_list.add_item('frisbee')

pet_store_list.view_list()

grocery_store_list = ShoppingList('Grocery Shopping List')
for item in ['fruits', 'vegetables', 'bowl', 'ice cream']:
    grocery_store_list.add_item(item)

merged_shopping_list = ShoppingList.merge_list(
    pet_store_list, grocery_store_list)

merged_shopping_list.view_list()
