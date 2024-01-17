import json
import requests
import shutil
import dateparser
import datetime
import math
import dateutil.parser
from isoduration import parse_duration
from progress.bar import IncrementalBar
from time import sleep
from ezgraphics import GraphicsImage, GraphicsWindow
from PIL import Image

class Recipe:
    def __init__(self, n, d, iURL, rYield, cookT, prepT, iList):
        self.name = n
        self.description = d
        self.imageURL = iURL
        self.recipeY = rYield
        self.cookTime = cookT
        self.prepTime = prepT
        self.ingredients = iList
        
    def get_name(self):
        return self.name
    
    def get_cook_time(self):
        if not self.cookTime:
            return '00:00'
        time = parse_duration(self.cookTime)
        if time.time.minutes > 9:
            time = str(time.time.hours)+':'+str(time.time.minutes)
        else:
            time = str(time.time.hours)+':0'+str(time.time.minutes)
        
        return time
    
    def get_prep_time(self):
        if not self.prepTime or 'PT' not in self.prepTime:
            return '00:00'
        time = parse_duration(self.prepTime)
        if time.time.minutes > 9:
            time = str(time.time.hours)+':'+str(time.time.minutes)
        else:
            time = str(time.time.hours)+':0'+str(time.time.minutes)
        return time
    
    def set_image(self, url):
        res = requests.get(url, stream = True)
        fill = '█'
        file_name = self.get_image()
        if res.status_code == 200:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
        else:
            print('Fail to load image')
        print(f'Loading {self.name} image:')
        for i in range(20):
            print(f'\r%s%s' % (fill*i, '-'*(19-i)), end = '')
            sleep(0.1)
        print()
        
        scaled_width = 200
        img = Image.open(file_name)
        percent_width = (scaled_width / float(img.size [0]))
        h_size = int((float(img.size [1]) * float(percent_width )))
        img = img.resize (( scaled_width , h_size))
        img.save(file_name) 
        
    def get_image(self):
        return self.name.replace(" ", "_").replace(":", '') + ".gif"
        
class RecipeProcessor:
    recipe_list = []
    def __init__(self):
        recipe_list = []
        
    def load_recipes(self, file_name):
        file = open(file_name, encoding = 'utf-8')
        self.data = json.load(file)
    
    def get_recipes(self):
        for rec in self.data:
            r = Recipe(rec['name'], rec['description'], rec['image'], rec['recipeYield'], rec['cookTime'], rec['prepTime'], rec['ingredients'])
            self.recipe_list.append(r)
        return self.recipe_list
    
    def tabulate_recipes(self):
        print('name description img-url recipeYield cookTime prepTime ingredients')
        for i in self.recipe_list:
            print(i.get_name(), i.get_cook_time(), i.get_prep_time())
            
class RecipeUI:
    def __init__(self):
        self.gap = 60
        self.window = None
        self.canvas = None
        self.size = [1080, 820]
    
    def setup_window(self):
        self.window = GraphicsWindow(self.size[0], self.size[1])
        self.window.setTitle("16 Recipes")
        self.canvas = self.window.canvas()
        
    def layout_ui(self, recipes):
        x = self.gap
        y = 0
        maxY = 0
        pic = GraphicsImage(recipes[0].get_image())
        self.canvas.drawImage(x, y, pic)
        name = recipes[0].get_name()
        if len(name) > 25:
            name = name[0:25]
        self.canvas.drawText(x, y + pic.height(), "Name: " + name)
        self.canvas.drawText(x, y + pic.height() + 20, "Prep time: " + str(recipes[0].get_prep_time()))
        self.canvas.drawText(x, y + pic.height() + 40, "Cook time: " + str(recipes[0].get_cook_time()))
        for r in range(1, 16):
            maxY = max(maxY, pic.height())
            prev = pic
            pic = GraphicsImage(recipes[r].get_image())
            x = x + prev.width() + self.gap
            if x + pic.width() < self.size[0] - 20:
                self.canvas.drawImage(x, y, pic)
                name = recipes[r].get_name()
                if len(name) > 25:
                    name = name[0:25]
                self.canvas.drawText(x, y + pic.height(), "Name: " + name)
                self.canvas.drawText(x, y + pic.height() + 20, "Prep time: " + str(recipes[r].get_prep_time()))
                self.canvas.drawText(x, y + pic.height() + 40, "Cook time: " + str(recipes[r].get_cook_time()))
            else:
                x = self.gap
                y = y + maxY + self.gap
                self.canvas.drawImage(x, y, pic)
                name = recipes[r].get_name()
                if len(name) > 25:
                    name = name[0:25]
                self.canvas.drawText(x, y + pic.height(), "Name: " + name)
                self.canvas.drawText(x, y + pic.height() + 20, "Prep time: " + str(recipes[r].get_prep_time()))
                self.canvas.drawText(x, y + pic.height() + 40, "Cook time: " + str(recipes[r].get_cook_time()))
        self.window.wait()

            
        
    def show_recipe_desc(recipe, x, y):
        print()
        
    
def main():

    proc = RecipeProcessor()
    proc.load_recipes('recipes.json')
    l = proc.get_recipes()
    for r in range(3):
        l[r].set_image(l[r].imageURL)
    ui = RecipeUI()
    ui.setup_window()
    ui.layout_ui(l)
    proc.tabulate_recipes()

main()