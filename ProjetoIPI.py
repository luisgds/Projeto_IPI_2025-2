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
#corromper_y4m(video_original, "video_corrompido.y4m")
corromper_y4m_2(video_original, "video_corrompido_2.y4m")
# introduzir erros pequenos ao video preview
corromper_y4m(video_menor, "preview_corrompido.y4m")

reduzirframe("video_corrompido_2.y4m", "reduzido_e_corrompido.y4m")
erros_preview, loc_erros_preview = detectar_erros_preview("reduzido_e_corrompido.y4m",
                             "preview_corrompido.y4m",  
                             limiares_preview)
erros_principal, loc_erros_principal = detectar_erros_principal(
    "video_corrompido_2.y4m", 
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

erros_preview_global, loc_preview_global = detectar_erros_preview(
    "reduzido_e_corrompido.y4m",
    "preview_corrompido.y4m",
    limiares_preview_global
)

erros_principal_global, loc_principal_global = detectar_erros_principal(
    "video_corrompido_2.y4m",
    limiares_principal_global
)

#print(erros_preview_global)
#print(erros_principal_global)

"""
 Ocultaçao de erros
"""
def split_yuv420(frame, W, H):
    Y_size = W * H
    U_size = (W // 2) * (H // 2)
    Y = np.frombuffer(frame[0:Y_size], dtype=np.uint8).reshape((H, W))
    U = np.frombuffer(frame[Y_size:Y_size + U_size], dtype=np.uint8).reshape((H // 2, W // 2))
    V = np.frombuffer(frame[Y_size + U_size:Y_size + 2 * U_size], dtype=np.uint8).reshape((H // 2, W // 2))
    return Y, U, V

def correcao(frame_atual, frame_anterior, preview_atual, W, H):
    Y_atual, U_atual, V_atual = split_yuv420(frame_atual, W, H)
    Y_ant, _, _               = split_yuv420(frame_anterior, W, H)
    Y_prev, _, _              = split_yuv420(preview_atual, W//4, H//4)
    low = cv2.resize(Y_ant, (W // 4, H // 4), interpolation=cv2.INTER_LINEAR)
    low_up = cv2.resize(low, (W, H), interpolation=cv2.INTER_LINEAR)
    HF = Y_ant - low_up
    prev_up = cv2.resize(Y_prev, (W, H), interpolation=cv2.INTER_LINEAR)
    Y_corr = prev_up + HF
    Y_corr = np.clip(Y_corr, 0, 255).astype(np.uint8)
    frame_corr = bytearray()
    frame_corr.extend(Y_corr.tobytes())
    frame_corr.extend(U_atual.tobytes())
    frame_corr.extend(V_atual.tobytes())
    return frame_corr


f_corr, header, W, H  = pegar_frames("video_corrompido_2.y4m")
f_p_coor, _, _, _ = pegar_frames("preview_corrompido.y4m")
frames_corrigido = []
tamanho = min(len(f_corr), len(f_p_coor))
for i in range(tamanho):
    if i == 0:
        frames_corrigido.append(f_corr[i])
        continue
    elif (erros_preview[i] or erros_preview_global[i]) or (erros_principal_global[i] or erros_principal[i]):
        f_corrigido = correcao(f_corr[i], f_corr[i-1], f_p_coor[i], W, H)
        frames_corrigido.append(f_corrigido)
    elif (erros_principal_global[i] or erros_principal[i]):
        f_corrigido = correcao(f_corr[i], f_corr[i-1], f_p_coor[i], W, H)
        frames_corrigido.append(f_corrigido)
    else:
        frames_corrigido.append(f_corr[i])

with open("video_corrigido.y4m", "wb") as out:
    out.write(header)
    for frame in frames_corrigido:
        out.write(b"FRAME\n")
        out.write(frame)
print("Arquivo salvo em: video_corrigido.y4m")

