# P4 Pandas and PostgreSQL
# Brinley Gregory, Ethan Carn, Luke Miller
# Madi Diefenbach, Seth Mortensen, Sydney Trojahn Hedges
# IS 303 Section 004
# PROJECT DESCRIPTION: **PUT STUFF HERE

# needed libraries
import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plot

# get user input
user_input = int(input("If you want to import data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program: "))

while user_input == 1 or user_input == 2:
    if user_input == 1:
        # read excel file
        df = pd.read_excel("Retail_Sales_Data.xlsx") 
        # Separate the "name” column into a “first_name” and “last_name” column
        df[['first_name', 'last_name']] = df['name'].str.split('_', expand=True)
        
        # delete the original “name” column
        df.drop(columns=['name'], inplace=True)

        # fix the “category” column so that the categories match the product that was sold
        # use this dictionary
        productCategoriesDict = {
        'Camera': 'Technology',
        'Laptop': 'Technology',
        'Gloves': 'Apparel',
        'Smartphone': 'Technology',
        'Watch': 'Accessories',
        'Backpack': 'Accessories',
        'Water Bottle': 'Household Items',
        'T-shirt': 'Apparel',
        'Notebook': 'Stationery',
        'Sneakers': 'Apparel',
        'Dress': 'Apparel',
        'Scarf': 'Apparel',
        'Pen': 'Stationery',
        'Jeans': 'Apparel',
        'Desk Lamp': 'Household Items',
        'Umbrella': 'Accessories',
        'Sunglasses': 'Accessories',
        'Hat': 'Apparel',
        'Headphones': 'Technology',
        'Charger': 'Technology'
        }

        df['category'] = df['product'].map(productCategoriesDict)

        # Save the results as a table called ‘sale’ in your is303 postgres database
        # need to do this still!!!!!

        print("You've imported the excel file into your postgres database.")

    else:
        # put stuff here for  when = 2 and delete pass
        pass
    

    # ask again to avoid infinite loop
    user_input = input("Enter 1 to import data, 2 to see summaries, or anything else to exit: ")


# print when they enter something besides 1 or 2
print("Closing the program.")