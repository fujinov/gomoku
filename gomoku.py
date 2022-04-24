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

def main():
    layout = create_layout()
    window = sg.Window('五目並べ', layout)
    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED:
            break

if __name__ == '__main__':
    main()
