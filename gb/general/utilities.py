from events.models import Category

def app_db_initialization():
    product_categories = ['Assortments', 'Bottle Rockets', 'Cakes - 200g', 'Cakes - 500g', 'Cakes - NOAB',
                          'Firecrackers', 'Fountains', 'Novelties', 'Reloadable Shells', 'Roman Candles',
                          'Single Shot Tubes', 'Skyrockets']
    for category in product_categories:
        new_category = Category(name=category)
        new_category.save() #todo remove

