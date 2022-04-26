import PySimpleGUI as sg


sg.theme('DarkBrown7')

def create_layout():
    layout = [[sg.Push(), sg.Text('白のターン', font=(None, 10), key='-TURN-')]]
    for y in range(15):
        inner = []
        for x in range(15):
            inner.append(sg.Button('', size=(4, 2), font=(None, 10), pad=(0, 0), key=str(y)+','+str(x)))
        layout.append(inner.copy())
    return layout

def waiting_list():
    while True:
        yield '○'
        yield '●'

def stone_judgement(goban, y, x):

    def compare_stone_colors(yi, xi, count):
        stone = goban[yi][xi]
        if stone == 0:
            count = 1
        elif stone == before_stone:
            count += 1
        else:
            count = 1
        return count

    # 横方向の判定
    count = 0
    for xi in range(15):
        if xi == 0:
            before_stone = 0
        else:
            before_stone = goban[y][xi-1]
        
        count = compare_stone_colors(y, xi, count)

        if count == 5:
            stone_coordinates = [(y, xj) for xj in range(xi, xi-5, -1)]
            return stone_coordinates

    # 縦方向の判定
    count = 0
    for yi in range(15):
        if yi == 0:
            before_stone = 0
        else:
            before_stone = goban[yi-1][x]

        count = compare_stone_colors(yi, x, count)
        
        if count == 5:
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

    count = 0
    for yi, xi in zip(range(start_y, end_y), range(start_x, end_x)):
        if yi == 0 or xi == 0:
            before_stone = 0
        else:
            before_stone = goban[yi-1][xi-1]

        count = compare_stone_colors(yi, xi, count)

        if count == 5:
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

    count = 0
    for yi, xi in zip(range(start_y, end_y), range(start_x, end_x, -1)):
        if yi == start_y and xi == start_x:
            before_stone = 0
        else:
            before_stone = goban[yi-1][xi+1]

        count = compare_stone_colors(yi, xi, count)
        
        if count == 5:
            stone_coordinates = [(yj, xj) for yj, xj in zip(range(yi, yi-5, -1), range(xi, xi+5))]
            return stone_coordinates
    return []


def main():
    players = waiting_list()
    goban = [[0 for _ in range(15)] for _ in range(15)]
    layout = create_layout()
    window = sg.Window('五目並べ', layout)

    while True:
        restart = 'No'
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        y, x = map(int, event.split(','))
        if goban[y][x] == 0:
            player = next(players)
            goban[y][x] = player
            window[event].update(player)
            if player == '○':
                next_player = '黒'
                winner = '白'
            else:
                next_player = '白'
                winner = '黒'
            window['-TURN-'].update(f'{next_player}のターン')

            stone_coordinates = stone_judgement(goban, y, x)

            if stone_coordinates:
                for key_y, key_x in stone_coordinates:
                    key = str(key_y) + ',' + str(key_x)
                    window[key].update(button_color='red')
                restart = sg.popup_yes_no(f'{winner}の勝利！\nリスタートしますか？', no_titlebar=True, grab_anywhere=True)
                break

    window.close()
    if restart == 'Yes':
        main()

if __name__ == '__main__':
    main()
