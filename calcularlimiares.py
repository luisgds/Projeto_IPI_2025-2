import cv2
import numpy as np
import random

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
        f1 = yuv1[:, :, 0]
        f2 = yuv2[:, :, 0]
        limiar = calcula_limiar(f1, f2)
        limiares.append(limiar)

    return limiares

def calcula_limiares_com_corrompido(frames_orig, frames_corr):
    """
    Calcula limiares frame-a-frame comparando:
       frames_orig[i]  <->  frames_corr[i]
    usando exatamente os mesmos métodos da função principal.
    """
    limiares = []
    # Garante que tem o mesmo tamanho
    n = min(len(frames_orig), len(frames_corr))
    for i in range(n):
        # Converte ambos para YUV e pega apenas o Y
        yuv1 = cv2.cvtColor(frames_orig[i], cv2.COLOR_BGR2YUV)
        yuv2 = cv2.cvtColor(frames_corr[i], cv2.COLOR_BGR2YUV)
        f1 = yuv1[:, :, 0]
        f2 = yuv2[:, :, 0]
        limiar = calcula_limiar(f1, f2)
        limiares.append(limiar)

    return limiares


def corromper_frames(frames, bits_por_frame=50):
    #Seleciona 3 frames aleatórios e troca bits aleatórios em cada um.
    novos_frames = [bytearray(f) for f in frames]
    indices = random.sample(range(len(frames)), 3)
    for idx in indices:
        frame = novos_frames[idx]
        for _ in range(bits_por_frame):
            pos = random.randint(0, len(frame) - 1)
            bit = 1 << random.randint(0, 7)
            frame[pos] ^= bit   # XOR troca o bit

    return novos_frames
