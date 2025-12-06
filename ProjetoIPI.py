import cv2
# Ver o video
cap = cv2.VideoCapture("akiyo_cif.y4m")

fps = 30
delay = int(1000 / fps)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Y4M Video", frame)
    if cv2.waitKey(delay) & 0xFF == 27:  # ESC para sair
        break

cap.release()
cv2.destroyAllWindows()

# Talvez não seja necessario desordenar e reordenar
# pois esse processo é apenas para a transmissão
# Reordenar os quadros igual na 
def reorder_frames(frames, REF):
    F = len(frames)
    output = [None] * F

    # Primeiro quadro permanece igual
    output[0] = frames[0]

    j = REF  # REF+1 na notação 1-based, mas aqui usamos 0-based

    for i in range(1, F):  # começa no segundo quadro (índice 1)
        output[i] = frames[j]

        j = j + REF

        if j >= F:
            j = j - F + 1

    return output


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

#REF = 3
#reordered = reorder_frames(frames, REF)

# 3. SALVAR O VÍDEO RESULTANTE
"""
output_path = "video_desordenado.mp4"
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

for frame in reordered:
    writer.write(frame)

writer.release()

print("Vídeo salvo como:", output_path)
"""

# Reduzir os quadro em 1/16

output_path = "video_16x_menor.mp4"
cap = cv2.VideoCapture(input_path)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
new_width = width // 4
new_height = height // 4
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
    writer.write(resized)

cap.release()
writer.release()
