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
    
    # Se não encontra 
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
        # Perguntar qual o ficheiro com os parâmetros da câmara
        ficheiro_settings = input('Ficheiro: ')
        if ficheiro_settings == '':
            ficheiro_settings = 'settings.xml'
        elif ficheiro_settings == 'sair'  or ficheiro_settings == 'exit':
            print('Sair')
            exit()
        print(ficheiro_settings)

        while 1:
            tempo_inicio = time.time()
            camera.load_settings(ficheiro_settings, PersistType.All)

            #print(camera.get_pixel_formats())
            #print(camera.get_pixel_format())
            #camera.set_pixel_format(PixelFormat.Mono8)
            frame = camera.get_frame()
            image_data = frame.as_numpy_ndarray()
            image_data = image_data.astype(np.uint8)
            # Perguntar qual o novo valor da exposição da câmara
                        # Mostre a imagem na tela
            # Redimensiona a imagem para um tamanho menor 
            scale_percent = 16  # Defina a porcentagem em relação à original
            width = int(image_data.shape[1] * scale_percent / 100)
            height = int(image_data.shape[0] * scale_percent / 100)
            dim = (width, height)
            image = cv2.resize(image_data, dim, interpolation=cv2.INTER_AREA)
            cv2.imshow('Frame',image)
            FPS = 1/(time.time() - tempo_inicio)
            print('FPS: {:.2f}'.format(FPS))
            if cv2.waitKey(1) & 0xFF ==ord('e'):
                valor_guardar = input('Guardar?: ') 
                if valor_guardar == 'y' or valor_guardar == 's':
                    time=datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
                    arquivo = os.path.join('D:\\imagens_teste', 'tentativa_{}.jpg'.format(time))
                    cv2.imwrite(arquivo, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                    print('Imagem {} guardada!'.format(count))
                    count=count+1
                elif valor_guardar == 'sair' or valor_guardar == 'exit':
                    print('Sair')
                    exit()
                else:
                    valor_exposicao = input('Exposição ({}): '.format(camera.ExposureTime.get())) 
                    if valor_exposicao == '':
                        tempo_exposicao=camera.ExposureTime
                        valor_exposicao = tempo_exposicao.get()
                    elif valor_exposicao == 'sair' or valor_exposicao == 'exit':
                        print('Sair')
                        exit()
                    print(valor_exposicao)
                    valor_ganho = input('Ganho ({}): '.format(camera.Gain.get())) 
                    if valor_ganho == '':
                        valor_ganho = camera.Gain.get()
                    elif valor_ganho == 'sair' or valor_ganho == 'exit':
                        print('Sair')
                        exit()
                    print(valor_ganho)

                    # Atualizar ficheiro 
                    fc.novos_parametros(ficheiro_settings, valor_exposicao, valor_ganho)

            elif cv2.waitKey(1) & 0xFF ==ord('q'):
                break

    cv2.destroyAllWindows()
