import PySimpleGUI as sg

from dependence.utils.hwnd_util import list_all_hwnd
from dependence.utils.screenshot_util import take_screenshot_of_program_using_win32api


def show_all_hwnd_select_gui():
    hwnd_list = list_all_hwnd()
    listbox_element = sg.Listbox(values=hwnd_list, size=(50, 10))
    select = None
    layout = [[sg.Text('Please select the hWnd of Fishing Planet')],
              [sg.Text('请选择钓鱼星球应用的句柄')],
              [listbox_element],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    window = sg.Window('hWnd Selector', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == "Ok":
            select = values[0]
            if not select:
                continue
            else:
                break

    window.close()
    if select:
        return select[0][0]
    else:
        return None


def show_child_hwnd_select_gui(hwnd_list):
    listbox_element = sg.Listbox(values=hwnd_list, size=(50, 10))
    select = None
    layout = [[sg.Text('Please select the hWnd of Fishing Planet')],
              [sg.Text('请选择钓鱼星球的句柄')],
              [listbox_element],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    window = sg.Window('hWnd Selector', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == "Ok":
            select = values[0]
            if not select:
                continue
            else:
                break

    window.close()
    if select:
        return select[0][0]
    else:
        return None
