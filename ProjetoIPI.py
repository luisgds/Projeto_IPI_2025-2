import cv2
from reordenar import *
from reduzirframe import reduzirframe, aumentarframe
from calcularlimiares import calcula_limiares_video
# ---------------------------------------------
# 1. LER O VÍDEO
# ---------------------------------------------

def ler_frames(input_path):
    cap = cv2.VideoCapture(input_path)
    frames = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()

    print(f"Total de frames lidos: {len(frames)}")
    return frames
# 2. APLICAR A DESORDENAÇÃO
# Caso seja necessario 
#REF = 3
#reordered = reorder_frames(frames, REF)

# Reduzir os quadro em 1/16

input_path = "akiyo_cif.y4m"
output_path = "video_16x_menor.y4m"
reduzirframe(input_path, output_path)

#Aumentar os frames do video reduzio 
frame_reduzido = "video_16x_menor.y4m"
output_path = "video_aumentado.y4m"
aumentarframe(frame_reduzido, output_path)

video_original = input_path
video_menor = "video_16x_menor.y4m"
frames_orig = ler_frames(video_original)
frames_aumento = ler_frames(video_menor)
limiares_principal = calcula_limiares_video(frames_orig)
# introduzir erros ao video original
# reduzir ele para comparar com o preview
#limiares_previa = calcula_limiares_preview(frames_preview, frames_reduzidos)

print("Vetor de limiares principal:")
print(limiares_principal)
print("Vetor de limiares previo:")
#print(limiares_previa)
