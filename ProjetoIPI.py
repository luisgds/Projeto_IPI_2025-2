import cv2
from reordenar import *
from reduzirframe import reduzirframe, aumentarframe
# ---------------------------------------------
# 1. LER O VÍDEO
# ---------------------------------------------

input_path = "akiyo_cif.y4m"
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

# 2. APLICAR A DESORDENAÇÃO
# Caso seja necessario 
#REF = 3
#reordered = reorder_frames(frames, REF)

# Reduzir os quadro em 1/16

output_path = "video_16x_menor.y4m"
reduzirframe(input_path, output_path)

#Aumentar os frames do video reduzio 
frame_reduzido = "video_16x_menor.y4m"
output_path = "video_aumentado.y4m"
aumentarframe(frame_reduzido, output_path)

