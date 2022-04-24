import PySimpleGUI as sg


sg.theme('DarkBrown7')

class Gobang():
    def __init__(self):
        self.board = [[0 for _ in range(15)] for _ in range(15)]
        self.player = '○'
        self.player_color = '白'
        self.count = 0
    
    def turn_change(self):
        if self.player == '○':
            self.player = '●'
            self.player_color = '黒'
        else:
            self.player = '○'
            self.player_color = '白'
            
    def set_stone(self, y, x):
        if self.board[y][x] == 0:
            self.board[y][x] = self.player
            return True
        else:
            return False
    
    def stone_judgement():
        pass
            
def create_layout():
    layout = [[sg.Push(), sg.Text('白のターン', font=(None, 10), key='-TURN-')]]
    for y in range(15):
        inner = []
        for x in range(15):
            inner.append(sg.Button('', size=(4, 2), font=(None, 10), pad=(0, 0), key=str(y)+','+str(x)))
        layout.append(inner.copy())
    return layout

def main():
    game = Gobang()
    layout = create_layout()
    window = sg.Window('五目並べ', layout)
    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        y, x = map(int, event.split(','))
        setted = game.set_stone(y, x)
        if setted == False:
            continue
        
        window[event].update(game.player)
        game.turn_change()
        window['-TURN-'].update(f'{game.player_color}のターン')

if __name__ == '__main__':
    main()
