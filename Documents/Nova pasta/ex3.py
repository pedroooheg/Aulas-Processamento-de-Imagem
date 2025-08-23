import FreeSimpleGUI as sg
from PIL import Image, ExifTags
import io
from PIL.ExifTags import Base
import webbrowser

image_original = None

def resize_image(image_path):
    img =  Image.open(file_path)
    global image_original
    image_original = img
    img = img.resize((800,600), Image.Resampling.LANCZOS)
    return img 

def converter_coordenada(image_path):
          dados = image_path.getexif()
          lat = dados.get_ifd(ExifTags.IFD.GPSInfo)[2]
          horas_lat = lat[0]
          minutos_lat = lat[1]
          segundos_lat = lat[2]
          lon = dados.get_ifd(ExifTags.IFD.GPSInfo)[4]
          horas_lon = lon[0]
          minutos_lon = lon[1]
          segundos_lon = lon[2]
          latitude = (horas_lat + minutos_lat/60 + segundos_lat/3600)
          longitude = (horas_lon + minutos_lon/60 + segundos_lon/3600)* -1
    
          if dados.get_ifd(ExifTags.IFD.GPSInfo)[3] == "W":
              longitude = (horas_lon + minutos_lon/60 + segundos_lon/3600)* -1
          url = "https://www.google.com/maps?q=" + str(float(latitude)) +","+ str(float(longitude))
          return(url)
    




layout  =[ [sg.Menu([["Arquivo",["abrir", "fechar"]]
                     ,["Ajuda",["sobre"]],
                     ["EXIF",["Mostrar dados da Imagem","Mostrar dados de GPS"]]
                     ])],
            [sg.Image(key= '-IMAGE-', size = (800,600))]
        ]


window = sg.Window("Olá mundo", layout, resizable= True)


while True:
    event, values =  window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == 'abrir':
        file_path  = sg.popup_get_file('selecione uma imagem', file_types=(("Imagens", "*.jpg *.png"),))
        if file_path:
          resize_img = resize_image(file_path)
          img_bytes = io.BytesIO()
          resize_img.save(img_bytes, format="PNG")
          window['-IMAGE-'].update(data=img_bytes.getvalue())
    
    elif event == "Mostrar dados da Imagem" and image_original != None:
        nome = image_original.filename
        dimensao = [image_original.width, image_original.height]
        formato = image_original.format
        sg.popup(nome, dimensao, formato )
    elif event == "Mostrar dados de GPS" and image_original != None:
        webbrowser.open(converter_coordenada(image_original))
    elif event == 'sobre':
        sg.popup('Desenvolvido por Pedro Henrique Gomes')
    elif event == 'fechar':
        window['-IMAGE-'].update()

window.close