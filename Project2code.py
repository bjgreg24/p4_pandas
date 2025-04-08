# Ethan Carn
# IS 303 - Retail Sales Pandas and Postgres Project
# This script reads retail sales data from Excel, processes it, stores it in Postgres, and summarizes it based on category

import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plot
import getpass

# Define the product-category mapping
dProductCategories = {
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

# Ask user for input
sChoice = input("If you want to import data, enter 1. If you want to see summaries of stored data, enter 2. Enter any other value to exit the program: ")

# This is an extra step i included NOT originally described in the project requirements. When testing, if you created a username or database name 
# Other than postgres, it won't work. in addition, everyone's passwords are different. This is a way to get around that.
sDBUser = input("Enter your Postgres username: ")
sDBPass = getpass.getpass("Enter your Postgres password: ")
sDBName = input("Enter your Postgres database name: ")

# Build the connection string
sConnString = f"postgresql+psycopg2://{sDBUser}:{sDBPass}@localhost:5432/{sDBName}"
oEngine = sqlalchemy.create_engine(sConnString)

# If user selects to import data
if sChoice == "1":

    # Read the Excel file into a DataFrame
    dfSales = pd.read_excel("Retail_Sales_Data.xlsx")

    # Split the name column into first and last names
    dfNameSplit = dfSales["name"].str.split("_", expand=True)

    # Insert first_name and last_name columns at the beginning
    dfSales.insert(1, "first_name", dfNameSplit[0])
    dfSales.insert(2, "last_name", dfNameSplit[1])

    # Delete the original name column
    del dfSales["name"]

    # Fix the category column based on product name
    dfSales["category"] = dfSales["product"].map(dProductCategories)

    # Save to PostgreSQL table named 'sale'
    dfSales.to_sql("sale", oEngine, if_exists='replace', index=False)

    # Confirmation message
    print("You've imported the excel file into your postgres database.")

# If user selects to view summary
elif sChoice == "2":

    # Read data from sale table into DataFrame
    dfSaleData = pd.read_sql_query("SELECT * FROM sale", oEngine)

    # Print available categories
    print("The following are all the categories that have been sold:")

    # Get unique categories
    lCategories = dfSaleData["category"].unique()

    # Create a mapping of number to category name
    dCategoryOptions = {}

    # Display numbered list
    for iIndex, sCategory in enumerate(lCategories, start=1):
        print(f"{iIndex}: {sCategory}")
        dCategoryOptions[str(iIndex)] = sCategory

    # Ask user to choose category by number
    sSelection = input("Please enter the number of the category you want to see summarized: ")

    # Validate and proceed
    if sSelection in dCategoryOptions:

        # Get selected category name
        sCategoryChosen = dCategoryOptions[sSelection]

        # Filter dataframe by category
        dfFiltered = dfSaleData.query("category == @sCategoryChosen")

        # Calculate total sales, average sale, and total units sold
        iTotalSales = dfFiltered["total_price"].sum()
        fAverageSale = dfFiltered["total_price"].mean()
        iTotalUnits = dfFiltered["quantity_sold"].sum()

        # Print results
        print(f"Total sales for {sCategoryChosen}: {iTotalSales:,.2f}")
        print(f"Average sale amount for {sCategoryChosen}: {fAverageSale:,.2f}")
        print(f"Total units sold for {sCategoryChosen}: {iTotalUnits}")

        # Prepare data for chart
        dfChart = dfFiltered.groupby("product")["total_price"].sum().reset_index()

        # Create bar chart
        plot.figure(figsize=(10, 6))
        plot.bar(dfChart["product"], dfChart["total_price"])
        plot.title(f"Total Sales by Product in Category: {sCategoryChosen}")
        plot.xlabel("Product")
        plot.ylabel("Total Sales")
        plot.xticks(rotation=45)
        plot.tight_layout()
        plot.show()

# If user enters anything else
else:
    print("Closing the program.")
