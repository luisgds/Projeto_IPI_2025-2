import cv2
import numpy as np

def mse(block1, block2):
    err = np.mean((block1.astype(np.float32) - block2.astype(np.float32))**2)
    return err

def get_blocks(frame, block_size=16):
    H, W = frame.shape
    blocks = []
    for i in range(0, H, block_size):
        for j in range(0, W, block_size):
            block = frame[i:i+block_size, j:j+block_size]
            blocks.append(block)
    return blocks


def calcula_limiar(frame1, frame2):
    limiar = 0
    blocks1 = get_blocks(frame1)
    blocks2 = get_blocks(frame2)

    for b1, b2 in zip(blocks1, blocks2):
        # Caso tamanhos diferentes → redimensiona 0.25 igual ao livro
        if b1.shape != b2.shape:
            b1 = cv2.resize(b1, (b2.shape[1], b2.shape[0]))
        mse_atual = mse(b1, b2)
        # Guarda o maior MSE (limiar)
        if mse_atual > limiar:
            limiar = mse_atual

    return limiar


def calcula_limiares_video(frames):
    limiares = []

    for i in range(1, len(frames)):
        # Converte frame BGR -> YUV
        yuv1 = cv2.cvtColor(frames[i-1], cv2.COLOR_BGR2YUV)
        yuv2 = cv2.cvtColor(frames[i],   cv2.COLOR_BGR2YUV)

        # Pega apenas o Y (luma) verdadeiro
        f1 = yuv1[:, :, 0]
        f2 = yuv2[:, :, 0]

        limiar = calcula_limiar(f1, f2)
        limiares.append(limiar)

    return limiares
