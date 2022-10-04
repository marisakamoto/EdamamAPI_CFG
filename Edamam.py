import requests
import webbrowser
from pprint import pprint

YOUR_APP_ID = "6f5f98e8"
YOUR_APP_KEY = "426af851f161e02fe4793df73858e7fc"

# search options for meal and diet restriction types
health = ['vegan', 'vegetarian', 'gluten-free', 'dairy-free', 'low-sugar', 'none']
meal = ['breakfast', 'lunch', 'dinner', 'snack', 'any']

# Search for the results:
    # Keeps asking for the user to input a valid ingredient if search returns zero results

results_found = 0 # begins with 0 if returns results than changes to 1
while results_found == 0:
    INGREDIENT = input("What Ingredient do you want to search for? ")

    # print diet restrictions options:
    for i in range(len(health)):
        print(i, health[i])

    health_input = int(input("\nChoose a diet restriction: "))
    print("You chose:{}\n".format(health[health_input]))

    # print meal type options
    for i in range(len(meal)):
        print(i, meal[i])

    meal_input = int(input("\nChoose a meal type: "))
    print("You chose:{}".format(meal[meal_input]))

    # Search the url based on user preferences:
    if health_input == 5: # if no diet restriction
        if meal_input == 4: #if no diet restriction and no meal type
            url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}&random=TRUE'.format(
                INGREDIENT,
                YOUR_APP_ID,
                YOUR_APP_KEY)
        else: #if no diet restriction but a given meal type
            url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}&mealType={}&random=TRUE'.format(
                INGREDIENT,
                YOUR_APP_ID,
                YOUR_APP_KEY,
                meal[meal_input])
    else: # if user have a diet restriction
        if meal_input == 4:  #if the user have a diet restriction and no meal type
            url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}&health={}&random=TRUE'.format(
                INGREDIENT,
                YOUR_APP_ID,
                YOUR_APP_KEY,
                health[health_input],
                )
        else:  #if the user have a diet restriction and also a meal type
            url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}&health={}&mealType={}&random=TRUE'.format(
                INGREDIENT,
                YOUR_APP_ID,
                YOUR_APP_KEY,
                health[health_input],
                meal[meal_input])

    response = requests.get(url)
    ingredients = response.json()

    if len(ingredients["hits"]) > 0:
        results_found = 1
    else:
        print("Sorry, I didn't find any recipe with {}. Try again\n".format(INGREDIENT))


#Loops inside the results
# n is a variable that helps to store the information in the dictionary dict
n = 0
dict = {}

for a in range(len(ingredients["hits"])):
    recipes_names = ingredients["hits"][a]["recipe"]["label"]
    recipes_link = ingredients["hits"][a]["recipe"]["shareAs"]
    recipes_items = ingredients["hits"][a]["recipe"]["ingredientLines"]
    recipes_mealType = ingredients["hits"][a]["recipe"]["mealType"]
    recipes_cuisineType = ingredients["hits"][a]["recipe"]["cuisineType"]
    recipes_dishType = ingredients["hits"][a]["recipe"]["dishType"]
    recipes_health = ingredients["hits"][a]["recipe"]["healthLabels"]

    n += 1

    #Adding the results to the dictionary
    dict[n] = {'name': recipes_names,
               'ingredients': recipes_items,
               'link': recipes_link,
               'dish': recipes_dishType,
               'meal':recipes_mealType,
               'health': recipes_health,
               'cuisine': recipes_cuisineType
               }

print("\nThese are the recipes which contain {} ingredient: ".format(INGREDIENT))

#This way it shows the name of the recipe and id in each line in a organized way
for i in range(n):
    print(i + 1, dict[i + 1]['name'])

#This validates if the user input for the recipe is among the possibilities
valid = 0
while valid == 0:
    user_choice = input("\nWhat recipe do you want to choose:(number) ")
    choice = int(user_choice)

    #checks if the user chose a number that is bigger than zero and within the range of the search results
    if choice <= n and choice > 0:
        valid = 1
    else: print("The value doesn't exist. Try again")

# Print on the Console the chosen recipe information
print("\n ================================== \n")
print("The recipe in position {} is: ".format(choice), dict[choice]['name'])  # print recipe name from dict
#print("More info:",dict[choice]['link'])

print("Cuisine: {}".format(dict[choice]['cuisine'][0]))
print("Dish Type: {}".format(dict[choice]['dish'][0]))
print("Great for: {}".format(dict[choice]['meal'][0]))
print("Diet restrictions: {}".format(dict[choice]['health']))

print("Ingredients:")
for ing in range (len(dict[choice]['ingredients'])):
     print("    -",dict[choice]['ingredients'][ing])

# Asks if the user wants to go to the browser
valid_browser = 0
while valid_browser == 0:
    user_browser = input("\nWould you like to visit the webpage? (y/n)")
    if user_browser in ('y', 'n'):
        valid_browser = 1
    else:
        print('Invalid option')
# Opens the browser if yes
if user_browser == 'y':
    webbrowser.open_new(dict[choice]['link'])


def export_file():

    # Asks if the user wants to export the results
    valid_print = 0
    while valid_print == 0:
        user_print = input("\nWould you like to export all of your results to a txt file? (y/n)")
        if user_print in ('y', 'n'):
            valid_print = 1
        else:
            print('Invalid option')

    if user_print == 'y':

        #export dictionary in a text file organizing each recipe in each line
        title= "These are the recipes which contain {} ingredient \n".format(INGREDIENT)
        with open("recipes.txt", 'w') as recipe_file:
            recipe_file.write(title)

            #print each recipe in dict
            for key in dict.keys():
                recipe_file.write('%s:%s\n' % (key, dict[key]['name']))
                recipe_file.write('Link: %s\n' % (dict[key]['link']))
                recipe_file.write('Ingredients:\n')

                # print every ingredient in each recipe
                for ing in range(len(dict[key]['ingredients'])):
                    recipe_file.write('     - %s\n' % (dict[key]['ingredients'][ing]))
                recipe_file.write('-------------------------------------\n')

    print("\nThanks, nice cooking!")

export_file()
