import cv2
import numpy as np
def reduzirframe(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    new_width = width // 4
    new_height = height // 4
    frames_reduzidos = []
    with open(output_path, "wb") as out:
        new_header = f"YUV4MPEG2 W{new_width} H{new_height} F30000:1001 Ip A0:0\n"
        out.write(new_header.encode("ascii"))
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
            frames_reduzidos.append(resized.copy())
            yuv = cv2.cvtColor(resized, cv2.COLOR_BGR2YUV_I420)
            out.write(b"FRAME\n")
            out.write(yuv.tobytes())
    cap.release()
    print("Arquivo salvo como:", output_path)
    return frames_reduzidos


def aumentarframe(input_path, output_path):
    with open(input_path, "rb") as f:
        header = f.readline().decode("ascii").strip()

    tokens = header.split()
    width_small = int([t[1:] for t in tokens if t.startswith("W")][0])
    height_small = int([t[1:] for t in tokens if t.startswith("H")][0])
    width_original = width_small * 4
    height_original = height_small * 4

    print("Tamanho original pretendido:", width_original, "x", height_original)
    cap = cv2.VideoCapture(input_path)
    with open(output_path, "wb") as out:
        new_header = f"YUV4MPEG2 W{width_original} H{height_original} F30000:1001 Ip A0:0\n"
        out.write(new_header.encode("ascii"))
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            upscaled = cv2.resize(frame, (width_original, height_original), interpolation=cv2.INTER_CUBIC)
            yuv = cv2.cvtColor(upscaled, cv2.COLOR_BGR2YUV_I420)
            out.write(b"FRAME\n")
            out.write(yuv.tobytes())

    cap.release()
    print("Arquivo salvo como:", output_path)
