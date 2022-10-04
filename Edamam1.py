import requests
from pprint import pprint

YOUR_APP_ID ="6f5f98e8"
YOUR_APP_KEY = "426af851f161e02fe4793df73858e7fc"
INGREDIENT = input("What Ingredient do you want to search for? ")
url = 'https://api.edamam.com/search?q={}&app_id={}&app_key={}'.format(INGREDIENT,YOUR_APP_ID,YOUR_APP_KEY)

response = requests.get(url)
print(response)
ingredients = response.json()


#pprint(ingredients["hits"])
list=[]

dict = {}
recipe = {'name', 'ingredients', 'link'}
n=0
for a in range(len(ingredients["hits"])):
    recipies_names = ingredients["hits"][a]["recipe"]["label"]
    recipies_link = ingredients["hits"][a]["recipe"]["shareAs"]
    recipies_items = ingredients["hits"][a]["recipe"]["ingredientLines"]
    n+=1
    dict[n] = {'name': recipies_names, 'ingredients': recipies_items, 'link': recipies_link}


#print(dict)
print("These are the recipes which contain {} ingredient \n".format(INGREDIENT))

print(n)

for i in range(n):
    print(i+1, dict[i+1]['name'])

valid = 0
while valid == 0:
    user_choice = input("Type the recipe number:")
    choice = int(user_choice)
    if choice <= n and choice > 0:
        valid = 1
    else: print('Invalid option')


print("\n ================================== \nYou chose:", dict[choice]['name'] )
print("More info:",dict[choice]['link'])
print("Ingredients:")
for ing in range (len(dict[choice]['ingredients'])):
     print(dict[choice]['ingredients'][ing])

valid_print = 0
while valid_print == 0:
    user_print = input("Would you like to export all of your results? (y/n)")
    if user_print in ('y', 'n'):
        valid_print = 1
    else:
        print('Invalid option')

if user_print == 'y':

#export dictionary in a text file
    title= "These are the recipes which contain {} ingredient \n".format(INGREDIENT)
    with open("recipes.txt", 'w') as recipe_file:
        recipe_file.write(title)
        for key in dict.keys():
            recipe_file.write('%s:%s\n' % (key, dict[key]['name']))
            recipe_file.write('Link: %s\n' % (dict[key]['link']))
            recipe_file.write('Ingredients:\n')
            for ing in range(len(dict[key]['ingredients'])):
                recipe_file.write('     - %s\n' % (dict[key]['ingredients'][ing]))
            recipe_file.write('-------------------------------------\n')
print("Thanks, nice cooking!")
