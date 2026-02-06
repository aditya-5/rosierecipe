"""
Generate recipes.json from PDF files
"""
import json
import re

# List of all your PDF files
pdf_files = [
    "001_Banoffee_Cupcakes.pdf",
    "003_Coffee_and_Walnut_Cinnamon_Rolls.pdf",
    "003_Red_Velvet_Mocha_Cake.pdf",
    "004_Pistachio_Lava_Cakes.pdf",
    "005_Mocha_Hazelnut_Cupcakes.pdf",
    "006_Almond_Croissant_Doughnuts.pdf",
    "007_Malva_Pudding.pdf",
    "008_Earl_Grey_Cinnamon_Rolls.pdf",
    "009_Millionaires_Cupcakes.pdf",
    "010_Chocolate_Praline_Mousse_Cake.pdf",
    "011_Berry_Red_Velvet_Cake.pdf",
    "012_Gingerbread_Latte_Cake.pdf",
    "013_Sticky_Gingerbread_Pudding.pdf",
    "014_Toffee_Nut_Latte_Cinnamon_Rolls.pdf",
    "015_Gingerbread_Latte_Cupcakes.pdf",
    "016_Sticky_Toffee_Nut_Latte_Pudding.pdf",
    "017_Self_Saucing_Red_Velvet_Puddings.pdf",
    "018_Gingerbread_Latte_Cinnamon_Rolls.pdf",
    "019_Butter_Pecan_Tres_Leches_Cake.pdf",
    "020_Sticky_Black_Forest_Pudding.pdf",
    "021_Sticky_Toffee_Pudding_Cinnamon_Rolls.pdf",
    "022_Maple_Hazelnut_Doughnuts.pdf",
    "023_Mexican_Chocolate_Milk_Cake.pdf",
    "024_Hot_Chocolate_Cinnamon_Rolls.pdf",
    "025_Sticky_Sweet_Potato_Sponge_Pudding.pdf",
    "026_Chocolate_Caramel_Witches_Hat_Cupcakes.pdf",
    "027_Devils_Food_Cake.pdf",
    "028_Pumpkin_Spice_Latte_Doughnuts.pdf",
    "029_Cinnamon_Roll_Layer_Cake.pdf",
    "030_Salted_Caramel_Pretzel_Cinnamon_Rolls.pdf",
    "031_Salted_Maple_Pumpkin_Cake.pdf",
    "032_Apple_Fritter_Cinnamon_Rolls.pdf",
    "033_Self_Saucing_Molten_Sticky_Toffee_Pudding.pdf",
    "034_Dirty_Chai_Latte_Cinnamon_Rolls.pdf",
    "035_Brown_Butter_Pumpkin_Brownie_Skillet.pdf",
    "036_Sticky_Toffee_Mocha_Pudding.pdf",
    "037_Biscoffee_Cake.pdf",
    "038_Brown_Butter_Espresso_Cinnamon_Rolls.pdf",
    "039_Butter_Pecan_Sticky_Toffee_Pudding.pdf",
    "040_Masala_Chai_Tres_Leches_Cake.pdf",
    "041_Pumpkin_Spice_Mocha_Cake.pdf",
    "042_Tiramisu_Cinnamon_Rolls.pdf",
    "043_Butter_Pecan_Doughnuts_with_Espresso_Glaze.pdf",
    "044_Pumpkin_Spice_Latte_Tres_Leches_Cake.pdf",
    "045_Brown_Sugar_Latte_Cake.pdf",
    "046_Eggless_Apple_Fritter_Cake.pdf",
    "047_Pumpkin_Spice_Latte_Cinnamon_Rolls.pdf",
    "048_Almond_Croissant_Cake.pdf",
    "049_Banana_Pudding_Cupcakes.pdf",
    "050_Cherry_Mocha_Cake.pdf",
    "051_Tres_Leches_Cinnamon_Rolls.pdf",
    "052_Affogato_Lava_Cakes.pdf",
    "053_Neapolitan_Mousse_Cake.pdf",
    "054_Birthday_Cake_Funfetti_Layer_Cake.pdf",
    "055_Mocha_Tres_Leches.pdf",
    "056_Blueberry_and_Lavender_Rolls.pdf",
    "057_Chocolate_Courgette_Pudding.pdf",
    "058_Caramel_Latte_Cupcakes.pdf",
    "059_Honey_and_Blackberry_Cake.pdf",
    "060_Chocolate_Cherry_Cupcakes.pdf",
    "061_Banana_Milk_Latte_Tres_Leches.pdf",
    "062_Sticky_Peach_Cobbler_Pudding.pdf",
    "063_Hummingbird_Cake.pdf",
    "064_Red_Velvet_Tres_Leches_Cake.pdf",
    "065_Brown_Butter_Salted_Caramel_Cake.pdf",
    "067_Brown_Butter_Smores_Cupcakes.pdf",
    "068_Hummingbird_Tres_Leches_Cake.pdf",
    "069_Earl_Grey__Orange_Victoria_Sponge_Cake.pdf",
    "070_Blueberry_Coconut_Cake.pdf",
    "071_Brown_Butter_Espresso_Mousse_Cake.pdf",
    "072_Peanut_Butter_and_Jelly_Cake.pdf",
    "073_Walnut_and_Coffee_Torte.pdf",
    "074_London_Fog_Tres_Leches_Cake.pdf",
    "075_Lemon_Lava_Cakes.pdf",
    "076_Hot_Honey_Chocolate_Cake.pdf",
    "077_Lemon_Dubai_Cake_lemon_pistachio_and_white_chocolate.pdf",
    "078_Peanut_Butter_and_Jelly_Rolls.pdf",
    "079_Strawberry_Shortcake_Tres_Leches.pdf",
    "080_Caramelised_Banana_Date_and_Olive_Oil_Pudding.pdf",
    "081_Salted_Vanilla_and_Pistachio_Cake.pdf",
    "082_Pistachio_Butter_Cake.pdf",
    "083_Honey_Caramel_Lemon_Cake.pdf",
    "084_Dubai_Style_Pistachio_Chocolate_Rolls.pdf",
    "085_Banana_Pudding_Layer_Cake.pdf",
    "086_Triple_Chocolate_Cake.pdf",
    "087_Pistachio_Hot_Cross_Buns.pdf",
    "088_Sticky_Toffee_Pudding_Layer_Cake.pdf",
    "089_Eggless_Gooey_Lemon_and_Lavender_Butter_Cake.pdf",
    "090_Sticky_Pistachio_Sponge_Pudding.pdf",
    "091_Lemon_and_Lavender_Cake.pdf",
    "092_Carrot_and_Caramel_Self_Saucing_Pudding.pdf",
    "093_Almond_Croissant_Crepe_Cake.pdf",
    "094_Lemon_Meringue_Pie_Tres_Leches_Cake.pdf",
    "095_Bounty_Bar_Tres_Leches.pdf",
    "096_Brioche_Pistachio_Croissants.pdf",
    "097_Jaffa_Cake_Cinnamon_Rolls.pdf",
    "098_One_Bowl_Cherry_Almond_Upside_Down_Cake.pdf",
    "099_Jammie_Dodger_Cake.pdf",
    "100_Espresso_Monkey_Bread.pdf",
    "101_Biscoff_Banana_Self_Saucing_Pudding.pdf",
    "102_Spanish_Latte_Tres_Leches.pdf",
    "103_Caramel_Tiramisu_Cupcakes.pdf",
    "104_Apple_Fritter_Cinnamon_Rolls.pdf",
    "105_Pistachio_Latte_Cake.pdf",
    "106_Tahini_and_Pistachio_Sticky_Toffee_Pudding.pdf",
    "107_Coffee_and_Walnut_Sticky_Toffee_Pudding.pdf",
    "108_Sticky_Toffee_Coffee_Pudding_Bundt_Cake.pdf",
    "109_Ferrero_Rocher_Cinnamon_Rolls.pdf",
    "110_Red_Velvet_Tres_Leches_Cake.pdf",
    "111_Chocolate_Orange_Sticky_Toffee_Pudding.pdf",
    "112_Chocolate_Pistachio_Cinnamon_Rolls.pdf",
    "113_Spiced_Orange_Mocha_Molten_Puddings.pdf",
    "114_Gingerbread_Banoffee_Cake.pdf",
    "115_Mince_Pie_Cinnamon_Rolls.pdf",
    "116_Peppermint_Mocha_Cake.pdf",
    "117_Gingerbread_Latte_Tres_Leches_Cake.pdf",
    "118_Giant_Pecan_Sticky_Bun.pdf",
    "119_Smores_Tres_Leches_Cake.pdf",
    "120_Cinna-muffins_Cinnamon_Roll_Muffins.pdf"
]

# URL mapping from the provided list
url_mapping = {
    "banoffee-cupcakes": "https://www.recipebyrosie.com/post/banoffee-cupcakes",
    "coffee-and-walnut-cinnamon-rolls": "https://www.recipebyrosie.com/post/coffee-and-walnut-cinnamon-rolls",
    "red-velvet-mocha-cake": "https://www.recipebyrosie.com/post/red-velvet-mocha-cake",
    "pistachio-lava-cakes": "https://www.recipebyrosie.com/post/pistachio-lava-cakes",
    "mocha-hazelnut-cupcakes": "https://www.recipebyrosie.com/post/mocha-hazelnut-cupcakes",
    "almond-croissant-doughnuts": "https://www.recipebyrosie.com/post/almond-croissant-doughnuts",
    "malva-pudding": "https://www.recipebyrosie.com/post/malva-pudding",
    "earl-grey-cinnamon-rolls": "https://www.recipebyrosie.com/post/earl-grey-cinnamon-rolls",
    "millionaires-cupcakes": "https://www.recipebyrosie.com/post/millionaires-cupcakes",
    "chocolate-praline-mousse-cake": "https://www.recipebyrosie.com/post/chocolate-praline-mousse-cake",
    "berry-red-velvet-cake": "https://www.recipebyrosie.com/post/berry-red-velvet-cake",
    "gingerbread-latte-cake": "https://www.recipebyrosie.com/post/gingerbread-latte-cake",
    "sticky-gingerbread-pudding": "https://www.recipebyrosie.com/post/sticky-gingerbread-pudding-1",
    "toffee-nut-latte-cinnamon-rolls": "https://www.recipebyrosie.com/post/toffee-nut-latte-cinnamon-rolls",
    "gingerbread-latte-cupcakes": "https://www.recipebyrosie.com/post/gingerbread-latte-cupcakes",
    "sticky-toffee-nut-latte-pudding": "https://www.recipebyrosie.com/post/sticky-toffee-nut-latte-pudding",
    "self-saucing-red-velvet-puddings": "https://www.recipebyrosie.com/post/self-saucing-red-velvet-puddings",
    "gingerbread-latte-cinnamon-rolls": "https://www.recipebyrosie.com/post/gingerbread-latte-cinnamon-rolls",
    "butter-pecan-tres-leches-cake": "https://www.recipebyrosie.com/post/butter-pecan-tres-leches-cake",
    "sticky-black-forest-pudding": "https://www.recipebyrosie.com/post/sticky-black-forest-pudding",
    "sticky-toffee-pudding-cinnamon-rolls": "https://www.recipebyrosie.com/post/sticky-toffee-pudding-cinnamon-rolls",
    "maple-hazelnut-doughnuts": "https://www.recipebyrosie.com/post/maple-hazelnut-doughnuts",
    "mexican-chocolate-milk-cake": "https://www.recipebyrosie.com/post/mexican-chocolate-milk-cake",
    "hot-chocolate-cinnamon-rolls": "https://www.recipebyrosie.com/post/hot-chocolate-cinnamon-rolls",
    "sticky-sweet-potato-sponge-pudding": "https://www.recipebyrosie.com/post/sticky-sweet-potato-sponge-pudding",
    "chocolate-caramel-witches-hat-cupcakes": "https://www.recipebyrosie.com/post/chocolate-caramel-witches-hat-cupcakes",
    "devils-food-cake": "https://www.recipebyrosie.com/post/devil-s-food-cake",
    "pumpkin-spice-latte-doughnuts": "https://www.recipebyrosie.com/post/pumpkin-spice-latte-doughnuts",
    "cinnamon-roll-layer-cake": "https://www.recipebyrosie.com/post/cinnamon-roll-layer-cake",
    "salted-caramel-pretzel-cinnamon-rolls": "https://www.recipebyrosie.com/post/salted-caramel-pretzel-cinnamon-rolls",
    "salted-maple-pumpkin-cake": "https://www.recipebyrosie.com/post/salted-maple-pumpkin-cake",
    "apple-fritter-cinnamon-rolls": "https://www.recipebyrosie.com/post/apple-fritter-cinnamon-rolls-1",
    "self-saucing-molten-sticky-toffee-pudding": "https://www.recipebyrosie.com/post/self-saucing-molten-sticky-toffee-pudding",
    "dirty-chai-latte-cinnamon-rolls": "https://www.recipebyrosie.com/post/dirty-chai-latte-cinnamon-rolls",
    "brown-butter-pumpkin-brownie-skillet": "https://www.recipebyrosie.com/post/brown-butter-pumpkin-brownie-skillet",
    "sticky-toffee-mocha-pudding": "https://www.recipebyrosie.com/post/sticky-toffee-mocha-pudding",
    "biscoffee-cake": "https://www.recipebyrosie.com/post/biscoffee-cake",
    "brown-butter-espresso-cinnamon-rolls": "https://www.recipebyrosie.com/post/brown-butter-espresso-cinnamon-rolls",
    "butter-pecan-sticky-toffee-pudding": "https://www.recipebyrosie.com/post/butter-pecan-sticky-toffee-pudding",
    "masala-chai-tres-leches-cake": "https://www.recipebyrosie.com/post/masala-chai-tres-leches-cake",
    "pumpkin-spice-mocha-cake": "https://www.recipebyrosie.com/post/pumpkin-spice-mocha-cake",
    "tiramisu-cinnamon-rolls": "https://www.recipebyrosie.com/post/tiramisu-cinnamon-rolls",
    "butter-pecan-doughnuts-with-espresso-glaze": "https://www.recipebyrosie.com/post/butter-pecan-doughnuts-with-espresso-glaze",
    "pumpkin-spice-latte-tres-leches-cake": "https://www.recipebyrosie.com/post/pumpkin-spice-latte-tres-leches-cake",
    "brown-sugar-latte-cake": "https://www.recipebyrosie.com/post/brown-sugar-latte-cake",
    "eggless-apple-fritter-cake": "https://www.recipebyrosie.com/post/eggless-apple-fritter-cake",
    "pumpkin-spice-latte-cinnamon-rolls": "https://www.recipebyrosie.com/post/pumpkin-spice-latte-cinnamon-rolls",
    "almond-croissant-cake": "https://www.recipebyrosie.com/post/almond-croissant-cake",
    "banana-pudding-cupcakes": "https://www.recipebyrosie.com/post/banana-pudding-cupcakes",
    "cherry-mocha-cake": "https://www.recipebyrosie.com/post/cherry-mocha-cake",
    "tres-leches-cinnamon-rolls": "https://www.recipebyrosie.com/post/tres-leches-cinnamon-rolls",
    "affogato-lava-cakes": "https://www.recipebyrosie.com/post/affogato-lava-cakes",
    "neapolitan-mousse-cake": "https://www.recipebyrosie.com/post/neapolitan-mousse-cake",
    "birthday-cake-funfetti-layer-cake": "https://www.recipebyrosie.com/post/birthday-cake-funfetti-layer-cake",
    "mocha-tres-leches": "https://www.recipebyrosie.com/post/mocha-tres-leches",
    "blueberry-and-lavender-rolls": "https://www.recipebyrosie.com/post/blueberry-and-lavender-rolls",
    "chocolate-courgette-pudding": "https://www.recipebyrosie.com/post/chocolate-courgette-pudding",
    "caramel-latte-cupcakes": "https://www.recipebyrosie.com/post/caramel-latte-cupcakes",
    "honey-and-blackberry-cake": "https://www.recipebyrosie.com/post/honey-and-blackberry-cake",
    "chocolate-cherry-cupcakes": "https://www.recipebyrosie.com/post/chocolate-cherry-cupcakes",
    "banana-milk-latte-tres-leches": "https://www.recipebyrosie.com/post/banana-milk-latte-tres-leches",
    "sticky-peach-cobbler-pudding": "https://www.recipebyrosie.com/post/sticky-peach-cobbler-pudding",
    "hummingbird-cake": "https://www.recipebyrosie.com/post/hummingbird-cake",
    "red-velvet-tres-leches-cake": "https://www.recipebyrosie.com/post/red-velvet-tres-leches-cake-1",
    "brown-butter-salted-caramel-cake": "https://www.recipebyrosie.com/post/brown-butter-salted-caramel-cake",
    "brown-butter-smores-cupcakes": "https://www.recipebyrosie.com/post/brown-butter-smores-cupcakes",
    "hummingbird-tres-leches-cake": "https://www.recipebyrosie.com/post/hummingbird-tres-leches-cake",
    "earl-grey-orange-victoria-sponge-cake": "https://www.recipebyrosie.com/post/earl-grey-orange-victoria-sponge-cake",
    "blueberry-coconut-cake": "https://www.recipebyrosie.com/post/blueberry-coconut-cake",
    "brown-butter-espresso-mousse-cake": "https://www.recipebyrosie.com/post/brown-butter-espresso-mousse-cake",
    "peanut-butter-and-jelly-cake": "https://www.recipebyrosie.com/post/peanut-butter-and-jelly-layer-cake",
    "walnut-and-coffee-torte": "https://www.recipebyrosie.com/post/walnut-and-coffee-torte",
    "london-fog-tres-leches-cake": "https://www.recipebyrosie.com/post/london-fog-tres-leches-cake",
    "lemon-lava-cakes": "https://www.recipebyrosie.com/post/lemon-lava-cakes",
    "hot-honey-chocolate-cake": "https://www.recipebyrosie.com/post/hot-honey-chocolate-cake",
    "lemon-dubai-cake-lemon-pistachio-and-white-chocolate": "https://www.recipebyrosie.com/post/lemon-dubai-cake-lemon-pistachio-and-white-chocolate",
    "peanut-butter-and-jelly-rolls": "https://www.recipebyrosie.com/post/peanut-butter-and-jelly-rolls",
    "strawberry-shortcake-tres-leches": "https://www.recipebyrosie.com/post/strawberry-shortcake-tres-leches",
    "caramelised-banana-date-and-olive-oil-pudding": "https://www.recipebyrosie.com/post/caramelised-banana-date-and-olive-oil-pudding",
    "salted-vanilla-and-pistachio-cake": "https://www.recipebyrosie.com/post/salted-vanilla-and-pistachio-cake",
    "pistachio-butter-cake": "https://www.recipebyrosie.com/post/pistachio-butter-cake",
    "honey-caramel-lemon-cake": "https://www.recipebyrosie.com/post/honey-caramel-lemon-cake",
    "dubai-style-pistachio-chocolate-rolls": "https://www.recipebyrosie.com/post/dubai-style-pistachio-chocolate-rolls",
    "banana-pudding-layer-cake": "https://www.recipebyrosie.com/post/banana-pudding-layer-cake",
    "triple-chocolate-cake": "https://www.recipebyrosie.com/post/triple-chocolate-cake",
    "pistachio-hot-cross-buns": "https://www.recipebyrosie.com/post/pistachio-hot-cross-buns",
    "sticky-toffee-pudding-layer-cake": "https://www.recipebyrosie.com/post/sticky-toffee-pudding-layer-cake",
    "eggless-gooey-lemon-and-lavender-butter-cake": "https://www.recipebyrosie.com/post/eggless-gooey-lemon-and-lavender-butter-cake",
    "sticky-pistachio-sponge-pudding": "https://www.recipebyrosie.com/post/sticky-pistachio-sponge-pudding",
    "lemon-and-lavender-cake": "https://www.recipebyrosie.com/post/lemon-and-lavender-cake",
    "carrot-and-caramel-self-saucing-pudding": "https://www.recipebyrosie.com/post/carrot-and-caramel-self-saucing-pudding",
    "almond-croissant-crepe-cake": "https://www.recipebyrosie.com/post/almond-croissant-crepe-cake",
    "lemon-meringue-pie-tres-leches-cake": "https://www.recipebyrosie.com/post/bounty-bar-tres-leches-1",
    "bounty-bar-tres-leches": "https://www.recipebyrosie.com/post/bounty-bar-tres-leches",
    "brioche-pistachio-croissants": "https://www.recipebyrosie.com/post/brioche-pistachio-croissants",
    "jaffa-cake-cinnamon-rolls": "https://www.recipebyrosie.com/post/jaffa-cake-cinnamon-rolls",
    "one-bowl-cherry-almond-upside-down-cake": "https://www.recipebyrosie.com/post/one-bowl-cherry-almond-upside-down-cake",
    "jammie-dodger-cake": "https://www.recipebyrosie.com/post/jammie-dodger-cake",
    "espresso-monkey-bread": "https://www.recipebyrosie.com/post/espresso-monkey-bread",
    "biscoff-banana-self-saucing-pudding": "https://www.recipebyrosie.com/post/biscoff-banana-self-saucing-pudding",
    "spanish-latte-tres-leches": "https://www.recipebyrosie.com/post/spanish-latte-tres-leches",
    "caramel-tiramisu-cupcakes": "https://www.recipebyrosie.com/post/caramel-tiramisu-cupcakes",
    "pistachio-latte-cake": "https://www.recipebyrosie.com/post/pistachio-latte-cake",
    "tahini-and-pistachio-sticky-toffee-pudding": "https://www.recipebyrosie.com/post/coffee-and-walnut-sticky-toffee-pudding-1",
    "coffee-and-walnut-sticky-toffee-pudding": "https://www.recipebyrosie.com/post/coffee-and-walnut-sticky-toffee-pudding",
    "sticky-toffee-coffee-pudding-bundt-cake": "https://www.recipebyrosie.com/post/sticky-toffee-coffee-pudding-bundt-cake",
    "ferrero-rocher-cinnamon-rolls": "https://www.recipebyrosie.com/post/ferrero-rocher-cinnamon-rolls",
    "chocolate-orange-sticky-toffee-pudding": "https://www.recipebyrosie.com/post/chocolate-orange-sticky-toffee-pudding",
    "chocolate-pistachio-cinnamon-rolls": "https://www.recipebyrosie.com/post/chocolate-pistachio-cinnamon-rolls",
    "spiced-orange-mocha-molten-puddings": "https://www.recipebyrosie.com/post/spiced-orange-mocha-molten-puddings",
    "gingerbread-banoffee-cake": "https://www.recipebyrosie.com/post/gingerbread-banoffee-cake",
    "mince-pie-cinnamon-rolls": "https://www.recipebyrosie.com/post/mince-pie-cinnamon-rolls",
    "peppermint-mocha-cake": "https://www.recipebyrosie.com/post/peppermint-mocha-cake",
    "gingerbread-latte-tres-leches-cake": "https://www.recipebyrosie.com/post/gingerbread-latte-tres-leches-cake",
    "giant-pecan-sticky-bun": "https://www.recipebyrosie.com/post/giant-sticky-pecan-bun",
    "smores-tres-leches-cake": "https://www.recipebyrosie.com/post/smores-tres-leches-cake",
    "cinna-muffins-cinnamon-roll-muffins": "https://www.recipebyrosie.com/post/cinna-muffins-cinnamon-roll-muffins"
}

def extract_recipe_info(filename):
    """Extract recipe number and title from filename"""
    match = re.match(r'(\d+)_(.+)\.pdf', filename)
    if not match:
        return None
    
    number = int(match.group(1))
    title = match.group(2).replace('_', ' ')
    
    return {
        'number': number,
        'title': title,
        'filename': filename
    }

def title_to_slug(title):
    """Convert title to URL slug"""
    slug = title.lower()
    slug = slug.replace(' ', '-')
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug

def main():
    recipes = []
    
    for filename in pdf_files:
        info = extract_recipe_info(filename)
        if info:
            slug = title_to_slug(info['title'])
            url = url_mapping.get(slug, f"https://www.recipebyrosie.com/post/{slug}")
            
            recipe = {
                'number': info['number'],
                'title': info['title'],
                'pdf': f'recipes/{filename}',  # Changed from 'public/recipes/'
                'url': url
            }
            recipes.append(recipe)
    
    # Sort by number
    recipes.sort(key=lambda x: x['number'])
    
    # Save to JSON
    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Generated recipes.json with {len(recipes)} recipes")

if __name__ == '__main__':
    main()