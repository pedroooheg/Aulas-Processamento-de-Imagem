import FreeSimpleGUI as sg
from PIL import Image 
import io


def resize_image(image_path):
    img =  Image.open(image_path)
    img = img.resize((100,600), Image.Resampling.LANCZOS)
    return img

layout  =[ [sg.Menu([["Arquivo",["abrir", "fechar"]]
                     ,["Ajuda",["sobre"]]
                     ])],
            [sg.Image(key= '-IMAGE-', size = (800,600))]
        ]




window = sg.Window("Olá mundo", layout, resizable= True)


while True:
    event, values =  window.read()S

    if event == sg.WIN_CLOSED:
        break
    elif event == 'abrir':
        file_path  = sg.popup_get_file('selecione uma imagem', file_types=(("Imagens", "*.jpg *.png"),))
        if file_path:
          resize_img = resize_image(file_path)
          img_bytes = io.BytesIO()
          resize_img.save(img_bytes, format="PNG")
          window['-IMAGE-'].update(data=img_bytes.getvalue())
    elif event == 'sobre':
        sg.popup('Desenvolvido por Pedro Henrique Gomes')
    elif event == 'fechar':
        window['-IMAGE-'].update()

window.close