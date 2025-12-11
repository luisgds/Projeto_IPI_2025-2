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

"""
Vetor de limiares
"""
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
erros_preview, loc_erros = detectar_erros_preview("reduzido_e_corrompido.y4m",
                             "preview_corrompido.y4m",  
                             limiares_preview)
erros_principal, loc_erros = detectar_erros_principal(
    "video_corrompido.y4m", 
    limiares_principal)
#print(erros_preview)
#print(erros_principal)

"""
Limiar baseado no primeiro quadro
"""
# valores empíricos 
K_preview = 10
K_principal = 100

# Limiar do primeiro quadro do Preview
L_preview_1 = limiares_preview[0]
# Limiar do segundo quadro da vista principal
L_principal_2 = limiares_principal[1]

limiar_global_preview = L_preview_1 * K_preview
limiar_global_principal = L_principal_2 * K_principal

print("Limiar global do Preview:", limiar_global_preview)
print("Limiar global do Principal:", limiar_global_principal)

limiares_preview_global = [limiar_global_preview] * len(limiares_preview)
limiares_principal_global = [limiar_global_principal] * len(limiares_principal)

erros_preview, loc_preview = detectar_erros_preview(
    "reduzido_e_corrompido.y4m",
    "preview_corrompido.y4m",
    limiares_preview_global
)

erros_principal, loc_principal = detectar_erros_principal(
    "video_corrompido.y4m",
    limiares_principal_global
)


print(erros_preview)
print(erros_principal)



