import PySimpleGUI as sg
from unit import *

def choose_units_layout():
    layout = [
        [
            sg.Text("Add a unit to battleground!")
        ],
        [
            sg.Text("Side:", size=(3, 1)),
            sg.Combo(["GREEN", "RED"], enable_events=True, readonly=False, key='-SIDE-', default_value="GREEN"),
        ],
        [
            sg.Text("Unit Type:", size=(3, 1)),
            sg.Combo(["Infantry", "Heavy", "Cavalry"], enable_events=True, readonly=False, key='-UNIT_TYPE-', default_value="Infantry"),
        ],
        [
            sg.Text("X coordinate in range 0 - 179"),
            sg.In(enable_events=True, key='-UNIT_X-', size=(3, 1)),
            sg.Text("Y coordinate in range 0 - 99"),
            sg.In(enable_events=True, key='-UNIT_Y-', size=(3, 1))
        ],
        [
            sg.Button("Submit Unit", key='-SUBMIT_UNIT-'),
            sg.Button("Finish Submiting", key='-FINISH_SUBMITING-'),
            sg.Text("Units added: 0", key='-UNITS_ADDED-')
        ]
    ]
    # col2 = [
    #     [
    #         sg.Text("X coordinate in range 0 - 179"),
    #         sg.PopupScrolled("XDXD")
    #     ]
    # ]
    # layout = [sg.Column(col1), sg.Column(col2)]

    window = sg.Window("Units layout", layout)

    layout_units_locations = []
    units_dict = {Side.RED: [], Side.GREEN: []}

    while True:
        event, values = window.read()
            
        if event == '-SUBMIT_UNIT-':
            x = int(values['-UNIT_X-'])
            y = int(values['-UNIT_Y-'])
            side = values['-SIDE-']
            unit_type = values['-UNIT_TYPE-']
            if x not in range(0, 180):
                sg.popup("x coordinate value out of range")
            elif y not in range(0, 100):
                sg.popup("y coordinate value out of range")
            elif (x, y) in layout_units_locations:
                sg.popup("x, y block already contains a unit")
            else:
                if side == "GREEN":
                    side = Side.GREEN
                    color = Color.BLUE
                else:
                    side = Side.RED
                    color = Color.RED
                # units_dict[side].append(create_unit(side, color, unit_type, x, y))
                yield create_unit(side, color, unit_type, x*BLOCK_SIZE, y*BLOCK_SIZE)
                # units_added = len(units_dict[Side.RED]) + len(units_dict[Side.GREEN])
                layout_units_locations.append((x, y))
                units_added = len(layout_units_locations)
                window['-UNITS_ADDED-'].update(f'Units added: {units_added}')
             
        if event == "Exit" or event == sg.WIN_CLOSED or event == '-FINISH_SUBMITING-':
            break

    window.close()

def create_unit(side, color, unit_type, x, y):
    
    if unit_type == "Infantry":
        unit = Infantry(color, x, y, side)
    elif unit_type == "Heavy":
        unit = Heavy(color, x, y, side)
    elif unit_type == "Cavalry":
        unit = Cavalry(color, x, y, side)
    
    return unit
    

