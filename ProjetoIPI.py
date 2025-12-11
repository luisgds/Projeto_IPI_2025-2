import cv2
from reordenar import *
from reduzirframe import *
from calcularlimiares import *
import numpy as np

# 2. APLICAR A DESORDENAÇÃO
# Caso seja necessario 
#REF = 3
#reordered = reorder_frames(frames, REF)

# Reduzir os quadro em 1/16

input_path = "akiyo_cif.y4m"
output_path = "video_16x_menor.y4m"
reduzirframe(input_path, output_path) # Salvar arquivo reduzido

#Aumentar os frames do video reduzido 
frame_reduzido = "video_16x_menor.y4m"
output_path = "video_aumentado.y4m"
aumentarframe(frame_reduzido, output_path) # sempre salva o arquivo

video_original = input_path
video_menor = "video_16x_menor.y4m"
limiares_principal = calcula_limiares_vetor(video_original)
# Normalmente as bibliotecas que fazem isso acaba introduzindo
# erros fazendo com que haja muito pequenos erros, porém aqui será tudo zero
limiares_preview = calcula_limiares_vetor(video_menor, "video_16x_menor.y4m", False)
#print("Vetor de limiares principal:")
#print(limiares_principal)
#print("Vetor de limiares previo (capaz de ser ajustado se quiser):")
#print(limiares_preview)

# introduzir erros ao video original
corromper_y4m(video_original, "video_corrompido.y4m")
# introduzir erros pequenos ao video preview
corromper_y4m(video_menor, "preview_corrompido.y4m")

reduzirframe("video_corrompido.y4m", "reduzido_e_corrompido.y4m")
erros = detectar_erros_video("reduzido_e_corrompido.y4m",
                             "preview_corrompido.y4m",  
                             limiares_preview)
print(erros)
#limiares = np.array(limiares_principal, dtype=np.float32)
#limiares_preview = np.array(limiares_previa, dtype=np.float32)

#erro = (limiares_preview > limiares).astype(int)
#print(erro)



