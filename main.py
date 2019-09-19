import json
from jsonencoder import convert_to_dict
from jsonencoder import dict_to_obj

class Food:
    name = "Unnamed Food"
    calories = 0
    carbs = 0
    protein = 0
    fat = 0

    def __init__(self, name, calories, carbs, protein, fat):
        self.name = name
        self.calories = calories
        self.carbs = carbs
        self.protein = protein
        self.fat = fat

    def set_name(self, name):
        self.name = name

    def set_calories(self, calories):
        self.calories = calories

    def set_carbs(self, carbs):
        self.carbs = carbs

    def set_protein(self, protein):
        self.protein = protein

    def set_fat(self, fat):
        self.fat = fat

class FoodDatabase:
    food_dict = dict()

    def create_food(self):
        new_food = Food()
        new_food.name = input('Food name: ')
        new_food.calories = int(input('Calories: '))
        new_food.carbs = int(input('Carbs: '))
        new_food.protein = int(input('Protein: '))
        new_food.fat = int(input('Fat: '))
        self.food_dict[new_food.name] = new_food

    def delete_food(self, food_name):
        del self.food_dict[food_name]

    def get_food(self, food_name):
        return self.food_dict[food_name]

    def retrieve_food_dict(self):
        return self.food_dict

    def list_foods(self):
        for food in self.food_dict.values():
            print(food.name)
            print('Calories: ' + str(food.calories))
            print('Carbs: ' + str(food.carbs))
            print('Protein: ' + str(food.protein))
            print('Fat: ' + str(food.fat) + '\n')

    def replace_food_dict(self, new_food_dict):
        self.food_dict = new_food_dict


class User:
    calories = 0
    carbs = 0
    protein = 0
    fat = 0
    food_list = []

    def set_calories(self, calories):
        self.calories = calories

    def set_carbs(self, carbs):
        self.carbs = carbs

    def set_protein(self, protein):
        self.protein = protein

    def set_fat(self, fat):
        self.fat = fat

    def display_nutrition(self):
        print('Calories: ' + str(self.calories))
        print('Carbs: ' + str(self.carbs))
        print('Protein: ' + str(self.protein))
        print('Fat: ' + str(self.fat) + '\n')

    def insert_food(self, food_database, food_name):
        food_to_insert = food_database.get_food(food_name)
        self.food_list.append(food_to_insert)

        new_calories = self.calories + food_to_insert.calories
        new_carbs = self.carbs + food_to_insert.carbs
        new_protein = self.protein + food_to_insert.protein
        new_fat = self.fat + food_to_insert.fat

        self.set_calories(new_calories)
        self.set_carbs(new_carbs)
        self.set_protein(new_protein)
        self.set_fat(new_fat)

    def list_foods(self):
        for food in self.food_list:
            print(food.name)
            print('Calories: ' + str(food.calories))
            print('Carbs: ' + str(food.carbs))
            print('Protein: ' + str(food.protein))
            print('Fat: ' + str(food.fat) + '\n')

def database_menu(user, food_database):
    running = True

    while running == True:
        print('b: Back to main menu')
        print('c: Create food for database')
        print('d: Delete food from database')
        print('l: List foods in database')
        print('s: Save food database')
        print('i: Import food database')
        decision = input()
        if decision == 'b':
            running = False
        if decision == 'c':
            food_database.create_food()
        if decision == 'd':
            food_to_delete = input("Name of food to delete: ")
            if food_to_delete not in food_database.retrieve_food_dict().keys():
                print('Invalid name of food.')
            else:
                food_database.delete_food(food_to_delete)
        if decision == 'l':
            food_database.list_foods()
        if decision == 's':
            export_database(food_database)
        if decision == 'i':
            imported_database = convert_json_to_database()
            food_database.replace_food_dict(imported_database)



def food_log_menu(user, food_database):
    running = True

    while running == True:
        print('b: Back to main menu')
        print('a: Add food to log')
        print('l: List foods in log')
        print('n: Display nutrition statistics')

        decision = input()
        if decision == 'b':
            running = False
        if decision == 'a':
            food_name = input('Food name: ')
            if food_name not in food_database.retrieve_food_dict().keys():
                print('Invalid name of food.')
            else:
                user.insert_food(food_database, food_name)
        if decision == 'l':
            user.list_foods()
        if decision == 'n':
            user.display_nutrition()

def main_menu(user, food_database):
    running = True

    while running == True:
        print('f: Modify food log')
        print('d: Modify database')
        print('q: Quit')

        decision = input()
        if decision == 'f':
            food_log_menu(user, food_database)
        if decision == 'd':
            database_menu(user, food_database)
        if decision == 'q':
            running = False

def export_database(food_database):
    new_database = dict()
    for k,v in food_database.food_dict.items():
        new_database[k] = convert_to_dict(v)
    with open('food_database.json', 'w') as outfile:
        json.dump(new_database, outfile)

def convert_json_to_database():
    database = dict()
    with open('food_database.json') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            database[k] = json.loads(json.dumps(v), object_hook=dict_to_obj)
    return database

def begin():
    user = User()
    user.calories = 0
    food_database = FoodDatabase()
    print('Welcome to FoodTracker.')
    main_menu(user, food_database)

if __name__ == "__main__":
    begin()