# type: ignore
from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, VariableListProperty, DictProperty, ObjectProperty
from kivy.properties import Clock
from kivy.uix.textinput import TextInput
from kivy.graphics.vertex_instructions import Rectangle
from kivy.metrics import dp
import random
import copy
import json
from kivy.graphics import Color
#from kivy.core.window import Window

# initialize the class for kv
class SudokuGame(BoxLayout):
    # storing time to dispaly to kv
    timer_input = StringProperty('00:00')
    # storing the grid for the game
    grid = StringProperty([["" for row in range(9)] for col in range(9)])
    # storing the inputs for kv to clicks
    inputs = StringProperty([])
    # storing difficulty level
    difficulty_level = NumericProperty()
    # storing sudokus to choose completed board from
    solvable_sudokus = DictProperty({})
    # size of the game board
    Stack_size = ObjectProperty()
    # converting the board to a string
    board_to_str = []
    # size of the font
    size_of_font = 25
    # saving current board for loading the board again for reset
    current_board = []


    def __init__(self, **kwargs):
        super(SudokuGame, self).__init__(**kwargs)
        
        self.time = 0
        self.placements = []
        self.Stack_size = self.ids.main_board.size
        self.cell_size = self.inputs[0].size
        self.app_size = self.ids.whole_app.size
        
        print(self.Stack_size)
        print(f'X: {self.Stack_size[0]}, Y: {self.Stack_size[1]}')
        Clock.schedule_interval(lambda dt: print(f'X: {self.Stack_size[0]}, Y: {self.Stack_size[1]}'), 2)
        Clock.schedule_interval(lambda dt: print(self.cell_size), 2)
        Clock.schedule_interval(lambda dt: print(self.app_size), 2)
        Clock.schedule_interval(lambda dt: self.rectangle_placement(), 1)
        
    def on_kv_post(self, *args):
        for row in range(9):
            for col in range(9):
                # creating 9x9 grid in kv
                ti = TextInput(size_hint=(0.111, 0.111), halign=('center'), multiline=False, on_touch_down=self.update_padding, font_size=(self.size_of_font), background_color=(1, 1, 1, .9), input_filter=self.insert_text)
                # binding so that play clicks populate fields
                
                ti.bind(text=self.make_callback(row,col))
                # adding the widgets and appending the inputs list
                self.ids.main_board.add_widget(ti)
                self.inputs.append(ti)
            

    #Only used for storing 10 sudoku generated boards

    def insert_text(self, substring, from_undo=False):
        
        try:
            only_ints = substring
            if only_ints.isdigit():
                return f"{only_ints}"
        except:
            print('You have not inputed an integer between 1-9')

    def rectangle_placement(self):

        with self.canvas.before:
            for row in range(9):
                for col in range(9):
                    Color(1, 1, 1)
                    self.rectangles = Rectangle(size=(self.cell_size[0], self.cell_size[1]), pos=((self.Stack_size[0]-(self.cell_size[0] * (row + 1)),(self.Stack_size[1]-(self.cell_size[1] * (col + 1))))))
                    
    def copying_sudoku(self):
        #copying complete grid placement
        completed_sudoku = copy.deepcopy(self.grid)
        try:
            with open('completable_sudokus.json') as json_file:
                self.solvable_sudokus = json.load(json_file)
        except:
            print('empty dict')
        finally:
            # if json is not empty with sudoku solutions
            if self.solvable_sudokus == {}:
                
                with open('completable_sudokus.json', 'w') as json_file:
                    
                    self.solvable_sudokus[1] = completed_sudoku
                    json.dump(self.solvable_sudokus,json_file)
                    
                    
            else:
                with open('completable_sudokus.json') as json_file:
                    #if json doesnt have more then 9 boards
                    if len(self.solvable_sudokus.keys()) <= 8:
                        self.solvable_sudokus = json.load(json_file)
                        # iter through the dict keys, retrieving the key, converting it to int, adding +1, converitng back to str and adding a new sudoku board that is solved
                        int_key = map(int, self.solvable_sudokus.keys())
                        new_key = max(int_key, default=-1) +1
                        self.solvable_sudokus[str(new_key)] = completed_sudoku
                    else:
                        return print('List is full')
            
            with open('completable_sudokus.json', 'w') as json_file:
                json_file.seek(0)   
                json.dump(self.solvable_sudokus, json_file)


    # To check if the last location has been entered and if won the game
    def last_location(self):
        
        taken_location = self.taken_locations()
        row, col = taken_location[80]
        digit = self.inputs[80].text

        if len(taken_location) < 81:
            print('You still have empty boxes')

        else:
            if self.check_if_won(row, col, digit) and self.solve():
                print('You have completed the puzzle!')
            else:
                print('somehting went wrong')

    # Checking taken locations
    def taken_locations(self):
            taken_locs= []
            for row in range(len(self.grid)):
                for col in range(len(self.grid[0])):
                    if self.grid[row][col] != "":
                        loc = row, col
                        taken_locs.append(loc)
            return taken_locs

    # assigning to grid and kv 
    def assign_to_grid(self):

        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == "":
                    index = row * 9 + col
                    self.grid[row][col] = self.board_to_str[row][col]
                    self.inputs[index].text = self.board_to_str[row][col]


    # Picking a random board from 10 pre saved boards
    def Picking_random_board_from_json_and_selecting_difficulty(self):

        try:
            with open('completable_sudokus.json') as json_file:
                self.solvable_sudokus = json.load(json_file)
        except:
            print('not able to load the file')

        # choosing the board, converting it to a list
        picking_random_board = random.choice(list(map(lambda x: x, self.solvable_sudokus.keys())))
        board_to_conver_to_str = self.solvable_sudokus[picking_random_board]
        self.board_to_str = [[str(x) for x in row] for row in board_to_conver_to_str]

    # coppying current board for reset if a mistake made
    def copy_currenct_board(self):

        current_game_board = copy.deepcopy(self.current_board)
        print(current_game_board)
        for row in range(len(current_game_board)):
            for col in range(len(current_game_board[0])):
                index = row * 9 +col
                self.grid[row][col] = current_game_board[row][col]
                self.inputs[index].text = current_game_board[row][col]

    # Creating a new board pre loaded board
    def board_creation(self):

        amount_of_digits = 0
        difficulty = self.difficulty_level
        
        while amount_of_digits < difficulty:
            
            locs = self.taken_locations()
            random_x, random_y = random.choice(locs)
            index = random_x * 9 + random_y
            self.grid[random_x][random_y] = ""
            self.inputs[index].text = ""
            amount_of_digits += 1
        
        self.current_board = copy.deepcopy(self.grid)

    # updating grid field location to be center of textinput field
    def update_padding(self, instance, size):
        line_height_of_instance = instance.line_height
        height_of_instance = instance.height
        
        padding_y = int((height_of_instance) - (line_height_of_instance)) / 2
        instance.padding = (0, padding_y, 0, 0)
    # a list to all retrieve empty locations for random location picking
    def empty_locs(self):

        empty_locations = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == "":
                    lock = row, col
                    empty_locations.append(lock)
        return empty_locations
    # simple clock to calc elapsed game time

    def time_update_click(self):
        
        
        Clock.schedule_interval(self.time_calc, 1)
    # calculating the elaped time to secs, mins
    def time_calc(self, dt):
        
        self.minutes, self.seconds = divmod(self.time, 60)
        self.hours, self.minutes = divmod(self.minutes, 60)
        self.time += 1
        self.timer_input = '{:02d}:{:02d}'.format(self.minutes, self.seconds)
        
    # checking if there are any empty location for single lock for backtracking
    def empty_loc(self):
        
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == "":
                    lock = row, col
                    return lock
        
        return None
    # selecting difficulty level by retrieving the field on which the player clicked on
    def difficulty(self, instance):
        
        if instance.text == 'Easy':
            self.difficulty_level = (random.choice(range(35,45)))
            return self.difficulty_level
        elif instance.text  == 'Medium':
            self.difficulty_level = (random.choice(range(44,52)))
            return self.difficulty_level
        else:
            self.difficulty_level = (random.choice(range(52,58)))
            return self.difficulty_level
    # used only for generating random boards to have pre-loaded boards
    def random_location_pick_number_assign(self):

        amount_of_digits = 0
        difficulty = self.difficulty_level
        # while amount of digits is less then selected difficulty digits
        while amount_of_digits < difficulty:
            # picking from a list of empty locs and then choosing a random empty location
            empty_locations = self.empty_locs()
            random_x, random_y = random.choice(empty_locations)
            random_digit = random.choice(range(1, 10))
            index = random_x * 9 + random_y
            # checking if possible to place and incrementing amount of digits by 1 and if possible updating grid/kv file
            if self.check_if_won(random_x, random_y, random_digit):
                self.grid[random_x][random_y] = random_digit
                self.inputs[index].text = str(random_digit)
                amount_of_digits += 1
            # if not able to palce, make the location empty
            else:
                
                self.grid[random_x][random_y] = ""
                self.inputs[index].text = ""

    # reseting the board for a new play
    def reset_board(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] != "":
                    self.grid[row][col] = ""
                    index = row * 9 + col
                    self.inputs[index].text = ""

    # checking if solved 
    def solve(self):
        # checking if the cell is empty
        find_empty = self.empty_loc()
        if not find_empty:
            
            return True
        # if cell not empty retrieve the location
        else:
            row, col = find_empty
        # loop through numbers to find which numbers can be placed
        for num in range(1, 10):
            if self.check_if_won(row, col, str(num)):
                    # selecting the index for kv digit placement, selecting python grid location placement for test
                    index = row * 9 + col
                    self.grid[row][col] = str(num)
                    self.inputs[index].text = str(num)
                    # if number placement is correct
                    if self.solve():
                        
                        return True
                    # if location does not satisfy the check_if_won condition
                    self.grid[row][col] = ""
                    self.inputs[index].text = ""
            
        return False
    # checking if all boxes, rows, cols are correct
    def check_if_won(self, x_loc, y_loc, digit):
        # checking if cols are correct
        if not all(
            
            self.grid[x_loc][col] != str(digit) or col == y_loc
            for col in range(len(self.grid[0]))
            
        ):
            return False
        # checking if rows are correct
        if not all(
            self.grid[row][y_loc] != str(digit) or row == x_loc
            for row in range(len(self.grid))
        ):
            return False
        # picking the box to check
        box_x = y_loc // 3
        box_y = x_loc // 3
        
        if not all(
            
            
            self.grid[row][col] != str(digit) or (row == x_loc and col == y_loc)
            
            for row in range(box_y * 3, box_y * 3 +3)
            for col in range(box_x *3, box_x * 3 + 3)
            
            
            
        ):
            return False
        # if all pass continue with next iteration or game win
        return True

    # populating textinput area, grid area and checking if  3 digits have been entered
    def make_callback(self, row, col):
        
        def callback(instance, value):

            length = 3
            index = row * 9 + col
            self.grid[row][col] = self.inputs[index].text

            if len(value) > length:
                self.inputs[index].text = value[:3]
                
            
        return callback
# initialize the app itself
class SudokuApp(App):

    def build(sef):
        return SudokuGame()

if __name__ == '__main__':
    
    SudokuApp().run()