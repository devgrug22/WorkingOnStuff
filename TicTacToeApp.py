
# type: ignore
from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')
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
import math


class TicTacToe(BoxLayout):

    board = StringProperty([[0 for i in range(3)] for i in range(3)])
    inputs = StringProperty([])
    font_size = 35
    human_player_1 = None
    human_player_2 = None
    computer_player = None
    hard_comp = False
    def __init__(self, **kwargs):
        super(TicTacToe, self).__init__(**kwargs)

        self.cell_size = self.ids.tic_board.size

    def on_kv_post(self, *args):
        for row in range(len(self.board[0])):
            for col in range(len(self.board)):
                box_area = TextInput(size_hint=(0.333, 0.333), font_size = self.font_size, halign=('center'), multiline=False, on_touch_down=self.update_padding, input_filter=self.insert_text)
                box_area.bind(text=self.make_callback(row, col))
                box_area.bind(on_text_validate=self.on_enter_press(row, col))
                self.ids.tic_board.add_widget(box_area)
                self.inputs.append(box_area)

    def update_padding(self, instance, size):

        cell = instance.line_height
        height_of_cell = instance.height

        height_of_cell = int((height_of_cell) - (cell)) / 2
        instance.padding = (0, height_of_cell, 0, 0)

    def insert_text(self, substring, from_undo=False):

        try:
            upper_letter = substring.upper()
            if upper_letter == 'X' or upper_letter == 'O':
                return f'{upper_letter}'
                
        except:
            raise KeyError
    
    def check_if_row_won(self, row_check,  col_check, value):

        row = [self.board[row_check][i] for i in range(3)]

        if all(letter == value for letter in row):
            return True

        return False
    
    def check_if_col_won(self, row_check,  col_check, value):

        
        col = [self.board[i][col_check] for i in range(3)]

        if all(letter == value for letter in col):
            return True

        return False
    
    def check_if_diagonal_won(self, row_check,  col_check, value):

        diagonal1 = [self.board[i][0+i] for i in range(3)]
        if all(letter == value for letter in diagonal1):
            return True
            
        diagonal2 = [self.board[2-i][i] for i in range(3)]
        if all(letter == value for letter in diagonal2):
            return True
        
        return False

    def if_board_full(self):

        squares = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    squares += 1
        
        return squares

    def check_if_won(self, row_check,  col_check, value):

        if (self.check_if_row_won(row_check,  col_check, value) == True) or (self.check_if_col_won(row_check,  col_check,  value) == True) or (self.check_if_diagonal_won(row_check,  col_check, value) == True):
            return True
        
        return False
        
    def empty_cells(self):
        
        empty_cell = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    empty_loc = row, col
                    empty_cell.append(empty_loc)
        
        return empty_cell
    
    def make_callback(self, row, col):

        def callback(instance, value):
            
            index = row *3 +col
            self.board[row][col] = self.inputs[index].text

            upper_value = value.upper()

            if len(value) > 1:
                self.board[row][col] = value[:1]
                self.inputs[index].text = value[:1]

        return callback
    
    def easy_computer_opponent(self, computer):

        empty_locs = self.empty_cells()
        
        random_loc = random.choice(empty_locs)
        if len(empty_locs[0]) == 0:
            return f'No more moves!'
        
        #making ai move
        
        
        return random_loc

    def face_off_choice(self, instance):
        
        if instance.text == 'Ai easy vs player':
            self.human_player_1 = 'X'
            self.computer_player = 'O'
            
        elif instance.text == 'player vs player':
            self.human_player_1 = 'X'
            self.human_player_2 = 'O'
        else:
            self.human_player_1 = 'X'
            self.computer_player = 'O'
            self.hard_comp = True

    def easy_computer_move(self, value):

        move = self.easy_computer_opponent(value)
        
        index = move[0] * 3 + move[1]
        self.board[move[0]][move[1]] = self.computer_player
        self.inputs[index].text = self.computer_player

        return move

    def on_enter_press(self, row, col):

        def on_enter(instance, *Args):
            
            index = row * 3 + col
            opponent_1 = self.human_player_1
            opponent_2 = self.computer_player if self.human_player_2 == None else self.human_player_2

            if opponent_2 == None:
                instance.text = ''
                return print('Please press start game and choose an opponent')
            move = instance.text
            
            print(f'human player move was {move} ')
            if self.check_if_won(row,  col, move) == True:
                print('you have won!')
                return 'Play again?'
            if move:
                if self.hard_comp == True:
                    ai_move_hard = self.best_move()
                    if ai_move_hard == None:
                        return print('its a tie')
                    index = ai_move_hard[0] * 3 + ai_move_hard[1]
                    self.inputs[index].text = opponent_2
                    if self.check_if_won(ai_move_hard[0], ai_move_hard[1], opponent_2):
                        print('Congrats, you have lost')
                        return print('To play again press start game')
                    
                else:
                    ai_move_easy = self.easy_computer_move(opponent_2)
                    index = ai_move_easy[0] * 3 + ai_move_easy[1]
                    self.inputs[index].text = opponent_2
                    
                
            

        return on_enter
    def smart_computer_player(self, move, MaxPlayer):
        print('depth call')
        
        if self.check_if_won(move[0], move[1], 'O'):
            return 1
        
        if self.check_if_won(move[0], move[1], 'X'):
            return -1
        
        if self.if_board_full() == 0:
            return 0
        
        if MaxPlayer:
            best_score = -math.inf

            for move in self.empty_cells():
                
                self.board[move[0]][move[1]] = 'O'
                score = self.smart_computer_player(move, False)
                self.board[move[0]][move[1]] = 0
                
                best_score = max(score, best_score)
                
            return best_score
        
        else:

            best_score = math.inf
            for move in self.empty_cells():
                
                self.board[move[0]][move[1]] = 'X'
                score = self.smart_computer_player(move, True)
                self.board[move[0]][move[1]] = 0
                best_score = min(score, best_score)

            return best_score
        
    def best_move(self):

        best_score = -math.inf
        best_move = None

        for move in self.empty_cells():

            self.board[move[0]][move[1]] = 'O'
            score = self.smart_computer_player(move, False)
            self.board[move[0]][move[1]] = 0
            
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

        
class TicTacToeApp(App):

    def build(self):
        return TicTacToe()
    

if __name__ == '__main__':
    
    TicTacToeApp().run()