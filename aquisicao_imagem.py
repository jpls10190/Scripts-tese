import os
from vimba import *
import numpy as np
import cv2
import datetime
import functions as fc
import time

count = 1

with Vimba.get_instance() as vimba:

    # Lista de câmeras disponíveis
    camera_ids = vimba.get_all_cameras()
    print(f"Found {len(camera_ids)} camera(s)")
    
    if len(camera_ids) == 0:
        print('Câmara não reconhecida')
        exit()

    # Imprimir lista de câmeras
    print('Câmaras disponíveis:')
    for camera_id in camera_ids:
        print(camera_id)
     
    # Abrir a câmera
    camera_id = camera_ids[0]  
    
    with camera_id as camera:
        ficheiro_settings = 'settings.xml'
        camera.load_settings(ficheiro_settings, PersistType.All)
        
        print("Settings da câmara importadas! (" + ficheiro_settings + ")\n")
        print("----------------------------------------------------------\n")
        print("pressionar :\n")
        print("g -> guardar imagem\n")
        print("e -> editar parâmetros\n")       
        print("q -> sair\n")

        while 1:
            #camera.set_pixel_format(PixelFormat.Mono8)
            frame = camera.get_frame()
            image_data = frame.as_numpy_ndarray()
            image_data = image_data.astype(np.uint8)

            # Redimensionar a imagem para um tamanho menor 
            scale_percent = 16  # Definir a percentagem em relação à imagem original
            width = int(image_data.shape[1] * scale_percent / 100)
            height = int(image_data.shape[0] * scale_percent / 100)
            dim = (width, height)
            image = cv2.resize(image_data, dim, interpolation=cv2.INTER_AREA)
            cv2.imshow('Frame',image)

            if cv2.waitKey(1) & 0xFF ==ord('g'):
                valor_guardar = input('Guardar? (y/n): ') 
                if valor_guardar == 'y':
                    time=datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
                    arquivo = os.path.join('aquisicao_imagens', 'tentativa_{}.jpg'.format(time))
                    cv2.imwrite(arquivo, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                    print('Imagem {} guardada!'.format(count))
                    count=count+1
                    
                    print("----------------------------------------------------------\n")
                    print("pressionar :\n")
                    print("g -> guardar imagem\n")
                    print("e -> editar parâmetros\n")       
                    print("q -> sair\n")
                else:
                    print("----------------------------------------------------------\n")
                    print("pressionar :\n")
                    print("g -> guardar imagem\n")
                    print("e -> editar parâmetros\n")       
                    print("q -> sair\n")

            elif cv2.waitKey(1) & 0xFF ==ord('e'):
                print("Editar (pressionar enter sem nenhum valor para manter o atual) :\n")
                valor_exposicao = input('Exposição ({}): '.format(camera.ExposureTime.get())) 
                if valor_exposicao == '':
                    tempo_exposicao=camera.ExposureTime
                    valor_exposicao = tempo_exposicao.get()
                print(valor_exposicao)
                valor_ganho = input('Ganho ({}): '.format(camera.Gain.get())) 
                if valor_ganho == '':
                    valor_ganho = camera.Gain.get()
                print(valor_ganho)

                # Atualizar ficheiro 
                fc.novos_parametros(ficheiro_settings, valor_exposicao, valor_ganho)

                print("----------------------------------------------------------\n")
                print("pressionar :\n")
                print("g -> guardar imagem\n")
                print("e -> editar parâmetros\n")       
                print("q -> sair\n")

            elif cv2.waitKey(1) & 0xFF ==ord('q'):
                break

    cv2.destroyAllWindows()