import PySimpleGUI as sg


sg.theme('DarkBrown7')

class Gobang():
    def __init__(self):
        self._board = [[0 for _ in range(15)] for _ in range(15)]
        self._count = 1
        self.player = '○'
        self.player_color = '白'
    
    def turn_change(self):
        if self.player == '○':
            self.player = '●'
            self.player_color = '黒'
        else:
            self.player = '○'
            self.player_color = '白'
            
    def set_stone(self, y, x):
        if self._board[y][x] == 0:
            self._board[y][x] = self.player
            return True
        else:
            return False

    def _count_color_stone(self, yi, xi, before_stone):
        stone = self._board[yi][xi]
        if stone == 0:
            self._count = 1
        elif stone == before_stone:
            self._count += 1
        else:
            self._count = 1

    def stone_judgement(self, y, x):
        # 横方向の判定
        for xi in range(15):
            if xi == 0:
                before_stone = 0
            else:
                before_stone = self._board[y][xi-1]
            
            self._count_color_stone(y, xi, before_stone)

            if self._count == 5:
                stones_coordinates = [(y, xj) for xj in range(xi, xi-5, -1)]
                return stones_coordinates

        # 縦方向の判定
        self._count = 1
        for yi in range(15):
            if yi == 0:
                before_stone = 0
            else:
                before_stone = self._board[yi-1][x]

            self._count_color_stone(yi, x, before_stone)
            
            if self._count == 5:
                stone_coordinates = [(yj, x) for yj in range(yi, yi-5, -1)]
                return stone_coordinates

        # 斜め（\方向）の判定
        if y > x:
            start_y = y - x
            start_x = 0
            end_y = 15
            end_x = x + 15 - y
        elif x > y:
            start_y = 0
            start_x = x - y
            end_y = y + 15 - x
            end_x = 15
        else:
            start_y, start_x = 0, 0
            end_y, end_x = 15, 15

        self._count = 1
        for yi, xi in zip(range(start_y, end_y), range(start_x, end_x)):
            if yi == 0 or xi == 0:
                before_stone = 0
            else:
                before_stone = self._board[yi-1][xi-1]

            self._count_color_stone(yi, xi, before_stone)

            if self._count == 5:
                stone_coordinates = [(yj, xj) for yj, xj in zip(range(yi, yi-5, -1), range(xi, xi-5, -1))]
                return stone_coordinates

        # 斜め（/方向）の判定
        if y + x <= 14:
            start_y = 0
            start_x = y + x
            end_y = y + x + 1
            end_x = -1
        else:
            start_y = y + x -14
            start_x = 14
            end_y =  15
            end_x = start_y - 1

        self._count =1
        for yi, xi in zip(range(start_y, end_y), range(start_x, end_x, -1)):
            if yi == start_y and xi == start_x:
                before_stone = 0
            else:
                before_stone = self._board[yi-1][xi+1]

            self._count_color_stone(yi, xi, before_stone)
            
            if self._count == 5:
                stone_coordinates = [(yj, xj) for yj, xj in zip(range(yi, yi-5, -1), range(xi, xi+5))]
                return stone_coordinates
        return []


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
        winner = game.player_color
        game.turn_change()
        window['-TURN-'].update(f'{game.player_color}のターン')

        stones_coordinates = game.stone_judgement(y, x)
        if stones_coordinates:
            for key_y, key_x in stones_coordinates:
                key = str(key_y) + ',' + str(key_x)
                window[key].update(button_color='red')
            sg.popup(f'{winner}の勝利！', no_titlebar=True, grab_anywhere=True)
            break

if __name__ == '__main__':
    main()
