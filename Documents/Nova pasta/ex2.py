import FreeSimpleGUI as sg


layout  =[ [sg.Text("E ai mundo", text_color="yellow")],
          [sg.InputText(key='-INPUT-')],
           [sg.Button("mostrar valor")]
           
           
           ]




window = sg.Window("Olá mundo", layout, size=(800,600))


while True:
    event, values =  window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "mostrar valor":
        entrada = values['-INPUT-']
        sg.popup(f'você digitou:{entrada}')
window.close