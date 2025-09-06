import FreeSimpleGUI as sg
from PIL import Image, ExifTags, ImageFilter, ImageDraw
import io
import os
import webbrowser
import requests

image_atual = None
image_path = None
imagem_anterior= None


def show_histogram_rgb():
    global image_atual
    try:
        if not image_atual:
            sg.popup("Nenhuma imagem aberta.")
            return

        #Garante que a imagem em RGB
        img_rgb = image_atual.convert('RGB')
        hist = img_rgb.histogram()

        r = hist[0:256]
        g = hist[256:512]
        b = hist[512:768]

        #Normaliza para caber na altura do gráfico
        width, height = 256, 200
        margin = 10
        max_count = max(max(r), max(g), max(b), 1)

        hist_img = Image.new('RGB', (width, height), 'black')
        draw = ImageDraw.Draw(hist_img)

        for x in range(256):
            rh = int((r[x] / max_count) * (height - margin))
            gh = int((g[x] / max_count) * (height - margin))
            bh = int((b[x] / max_count) * (height - margin))

            #Desenha linhas verticais sobrepostas para cada canal
            draw.line([(x, height - 1), (x, height - 1 - rh)], fill=(255, 0, 0))
            draw.line([(x, height - 1), (x, height - 1 - gh)], fill=(0, 255, 0))
            draw.line([(x, height - 1), (x, height - 1 - bh)], fill=(0, 0, 255))

        #Amplia para melhor visualização mantendo aspecto
        scale_x, scale_y = 3, 2
        hist_big = hist_img.resize((width * scale_x, height * scale_y), Image.LANCZOS)

        img_bytes = io.BytesIO()
        hist_big.save(img_bytes, format='PNG')

        layout = [
            [sg.Image(data=img_bytes.getvalue(), key='-HIST-')],
            [sg.Button('Fechar')]
        ]
        win_hist = sg.Window('Histograma RGB', layout, modal=True, finalize=True)
        while True:
            e, _ = win_hist.read()
            if e in (sg.WINDOW_CLOSED, 'Fechar'):
                break
        win_hist.close()
    except Exception as e:
        sg.popup(f"Erro ao gerar histograma: {str(e)}")


def desfazer():
    global image_atual
    if imagem_anterior is not None:
        image_atual = imagem_anterior.copy()
    show_image()


def apply_blur_filter():
    global image_atual
    global imagem_anterior
    
    radius = sg.popup_get_text("Digite a quantidade de blur (0 a 20)", default_text='2')
    try:
        radius = int(radius)
        radius = max(0, min(20, radius))
    except ValueError:
        sg.popup('Por favor, insira um valor numérico valido')
        return
    try:
        if  image_atual:
            imagem_anterior = image_atual.copy()
            image_atual = image_atual.filter(ImageFilter.GaussianBlur(radius))
            show_image()
    except Exception as e:
        sg.popup(f'Erro ao aplicar o filtro:{str(e)}')


def four_bits():
    global image_atual
    global imagem_anterior
    try:
        if image_atual:
            imagem_anterior = image_atual.copy()
            image_atual = image_atual.convert('P', palette=Image.ADAPTIVE, colors=4)
            show_image()
        else:
            sg.popup('Nenhuma imagem aberta')
    except Exception as e:
        sg.popup(f'Erro ao aplicar o filtro:{str(e)}')


def espelhar():
    global image_atual
    global imagem_anterior
    imagem_anterior = image_atual.copy()
    largura, altura = image_atual.size
    nova_imagem = Image.new(image_atual.mode, (largura, altura))
    pixels_original = image_atual.load()
    pixels_novo = nova_imagem.load()
    for h in range(altura):
        for w in range(largura):
            pixels_novo[w, h] = pixels_original[largura - 1 - w, h]
    image_atual = nova_imagem
    show_image()

def pb():
    global image_atual
    global imagem_anterior
    imagem_anterior = image_atual.copy()
    imagem = image_atual.load()
    largura, altura = image_atual.size
    formato = image_atual.format.upper()
    print(formato)
    if formato == "JPG" or formato == "JPEG":
        for h in range(altura):
            for w in range(largura):
                color = image_atual.getpixel((w, h))
                r = int((float(color[0]) * 0.3))
                g = int((float(color[1]) * 0.59))
                b = int((float(color[2]) * 0.11))

                imagem[w, h] =(int(r) + int(g) + int(b),
                               int(r) + int(g) + int(b),
                               int(r) + int(g) + int(b))
        show_image()            
    if formato == "PNG":
        for h in range(altura):
            for w in range(largura):
                color = image_atual.getpixel((w, h))
                r = int((float(color[0]) * 0.3))
                g = int((float(color[1]) * 0.59))
                b = int((float(color[2]) * 0.11))
                imagem[w, h] = (int(r) + int(g) + int(b),
                                int(r) + int(g) + int(b),
                                int(r) + int(g) + int(b))
        show_image()

def sepia():
    global image_atual
    global imagem_anterior
    imagem_anterior = image_atual.copy()
    imagem = image_atual.load()
    largura, altura = image_atual.size
    formato = image_atual.format.upper()
    print(formato)
    if formato == "JPG" or formato == "JPEG":
        for h in range(altura):
            for w in range(largura):
                color = image_atual.getpixel((w, h))
                r = (color[0] + 150 if color[0] + 150 < 255 else 255)
                g = (color[1] + 100 if color[1] + 100 < 255 else 255)
                b = (color[2] + 50 if color[2] + 50 < 255 else 255)
                imagem[w, h] = (r, g, b)
            
        show_image()            
    if formato == "PNG":
        for h in range(altura):
            for w in range(largura):
                color = image_atual.getpixel((w, h))
                r = (color[0] + 150 if color[0] + 150 < 255 else 255)
                g = (color[1] + 100 if color[1] + 100 < 255 else 255)
                b = (color[2] + 50 if color[2] + 50 < 255 else 255)
                imagem[w, h] = (r, g, b)
            
        show_image()
    


def negativo():
    global image_atual
    global imagem_anterior
    imagem_anterior = image_atual.copy()
    imagem = image_atual.load()
    largura, altura = image_atual.size
    formato = image_atual.format.upper()
    print(formato)
    if formato == "JPG" or formato == "JPEG":
        for h in range(altura):
            for w in range(largura):
                color = image_atual.getpixel((w, h))
                imagem[w, h] = (255 - color[0], 255 - color[1], 255 - color[2])
        show_image()            
    if formato == "PNG":
        for h in range(altura):
            for w in range(largura):
                color = image_atual.getpixel((w, h))
                imagem[w, h] = (255 - color[0], 255 - color[1], 255 - color[2])
        show_image()

def url_download(url):
    global image_atual
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            image_atual = Image.open(io.BytesIO(r.content))
            show_image()
        else:
            sg.popup("Falha ao baixar a imagem. Verifique a URL e tente novamente.")
    except Exception as e:
        sg.popup(f"Erro ao baixar a imagem: {str(e)}")

def show_image():
    global image_atual
    try:
        resized_img = resize_image(image_atual)
        img_bytes = io.BytesIO()
        resized_img.save(img_bytes, format='PNG')
        window['-IMAGE-'].update(data=img_bytes.getvalue())
    except Exception as e:
        sg.popup(f"Erro ao exibir a imagem: {str(e)}")

def resize_image(img):
    try:
        img = img.resize((800, 600), Image.Resampling.LANCZOS) 
        return img
    except Exception as e:
        sg.popup(f"Erro ao redimensionar a imagem: {str(e)}")

def open_image(filename):
    global image_atual
    global image_path
    try:
        image_path = filename
        image_atual = Image.open(filename)    
        show_image()
    except Exception as e:
        sg.popup(f"Erro ao abrir a imagem: {str(e)}")

def save_image(filename):
    global image_atual
    try:
        if image_atual:
            with open(filename, 'wb') as file:
                image_atual.save(file)
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao salvar a imagem: {str(e)}")

def info_image():
    global image_atual
    global image_path
    try:
        if image_atual:
            largura, altura = image_atual.size
            formato = image_atual.format
            tamanho_bytes = os.path.getsize(image_path)
            tamanho_mb = tamanho_bytes / (1024 * 1024)
            sg.popup(f"Tamanho: {largura} x {altura}\nFormato: {formato}\nTamanho em MB: {tamanho_mb:.2f}")
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao exibir informações da imagem: {str(e)}")

def exif_data():
    global image_atual
    try:
        if image_atual:
            exif = image_atual._getexif() 
            if exif:
                exif_data = ""
                for tag, value in exif.items():
                    if tag in ExifTags.TAGS:
                        if tag == 37500 or tag == 34853: #Remove os dados customizados (37500) e de GPS (34853)
                            continue
                        tag_name = ExifTags.TAGS[tag]
                        exif_data += f"{tag_name}: {value}\n"
                sg.popup("Dados EXIF:", exif_data)
            else:
                sg.popup("A imagem não possui dados EXIF.")
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao ler dados EXIF: {str(e)}")

def gps_data():
    global image_atual
    try:
        if image_atual:
            exif = image_atual._getexif()
            if exif:
                gps_info = exif.get(34853)  #Tag para informações de GPS
                print (gps_info[1], gps_info[3])
                if gps_info:
                    latitude = int(gps_info[2][0]) + int(gps_info[2][1]) / 60 + int(gps_info[2][2]) / 3600
                    if gps_info[1] == 'S':  #Verifica se a direção é 'S' (sul)
                        latitude = -latitude
                    longitude = int(gps_info[4][0]) + int(gps_info[4][1]) / 60 + int(gps_info[4][2]) / 3600
                    if gps_info[3] == 'W':  #Verifica se a direção é 'W' (oeste)
                        longitude = -longitude
                    sg.popup(f"Latitude: {latitude:.6f}\nLongitude: {longitude:.6f}")
                    open_in_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
                    if sg.popup_yes_no("Deseja abrir no Google Maps?") == "Yes":
                        webbrowser.open(open_in_maps_url)
                else:
                    sg.popup("A imagem não possui informações de GPS.")
            else:
                sg.popup("A imagem não possui dados EXIF.")
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao ler dados de GPS: {str(e)}")

layout = [
    [sg.Menu([
            ['Arquivo', ['Abrir', 'Abrir URL', 'Salvar', 'Fechar']],
            ['Editar', ['Desfazer']],
            ['Imagem',[
                'Girar',['Girar 90 graus à direita', 'Girar 90 graus á esquerda', 'Espelhar'],
                'Filtro',['Preto e Branco', 'Sépia', 'Negativo', '4 bits', 
                          'Blur', 'Contorno', 'Detalhe', 'Realce de borda',
                          'Relevo', 'Detector borda', 'Nitidez', 'Suavizar',
                          'Filtro minimo', 'Filtro máximo'],
                'Histograma RGB'    
            ]],
            ['EXIF', ['Mostrar dados da imagem', 'Mostrar dados de GPS']], 
            ['Sobre a image', ['Informacoes']], 
            ['Sobre', ['Desenvolvedor']],

        ])],
    [sg.Image(key='-IMAGE-', size=(800, 600))],
]

window = sg.Window('Photo Shoping', layout, finalize=True)

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Fechar'):
        break
    elif event == 'Abrir':
        arquivo = sg.popup_get_file('Selecionar image', file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
        if arquivo:
            open_image(arquivo)
    elif event == 'Abrir URL':
        url = sg.popup_get_text("Digite a url")
        if url:
            url_download(url)
    elif event == 'Salvar':
        if image_atual:
            arquivo = sg.popup_get_file('Salvar image como', save_as=True, file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
            if arquivo:
                save_image(arquivo)
    elif event == 'Informacoes':
        info_image()
    elif event == 'Mostrar dados da imagem':
        exif_data()
    elif event == 'Mostrar dados de GPS':
        gps_data()
    elif event == 'Desenvolvedor':
        sg.popup('Desenvolvido por [Seu Nome] - BCC 6º Semestre')
    elif event == 'Negativo' and image_atual != None:
        negativo() 
    elif event == 'Sépia' and image_atual != None:
        sepia()
    elif event == 'Preto e Branco' and image_atual != None:
        pb()
    elif event == 'Espelhar' and image_atual != None:
        espelhar()
    elif event == '4 bits' and image_atual != None:
        four_bits()
    elif event == 'Blur' and image_atual != None:
        apply_blur_filter()
    elif event == 'Desfazer' and image_atual != None:
        desfazer()
    elif event == 'Histograma RGB' and image_atual != None:
        show_histogram_rgb()
window.close()