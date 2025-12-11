import cv2
# Ver o video
cap = cv2.VideoCapture("akiyo_cif.y4m")
#cap = cv2.VideoCapture("video_16x_menor.y4m")
#cap = cv2.VideoCapture("video_aumentado.y4m")
#cap = cv2.VideoCapture("video_corrompido.y4m")
#cap = cv2.VideoCapture("reduzido_e_corrompido.y4m")
#cap = cv2.VideoCapture("preview_corrompido.y4m")

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