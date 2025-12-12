import cv2
import numpy as np
import random

def ler_frames(input_path):
    cap1 = cv2.VideoCapture(input_path)
    frames = []
    while True:
        ret, frame = cap1.read()
        if not ret:
            break
        frames.append(frame)
    cap1.release()
    return frames

def pegar_frames(input_path):
    frames = []
    with open(input_path, "rb") as f:
        data = f.read()
    partes = data.split(b"FRAME\n")
    header = partes[0]
    header_text = header.decode("ascii", errors="ignore")
    W = int(header_text.split(" W")[1].split(" ")[0])
    H = int(header_text.split(" H")[1].split(" ")[0])
    frame_size = W * H + (W // 2) * (H // 2) * 2
    for p in partes[1:]:
        if len(p) < frame_size:
            continue
        frames.append(bytearray(p[:frame_size]))
    return frames, header, W, H

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


def calcula_limiar(frame1, frame2, blocos = 16):
    limiar = 0
    blocks1 = get_blocks(frame1, blocos)
    blocks2 = get_blocks(frame2, blocos)
    for b1, b2 in zip(blocks1, blocks2):
        # Caso tamanhos diferentes → redimensiona 0.25 igual ao livro
        if b1.shape != b2.shape:
            b1 = cv2.resize(b1, (b2.shape[1], b2.shape[0]))
        mse_atual = mse(b1, b2)
        # Guarda o maior MSE (limiar)
        if mse_atual > limiar:
            limiar = mse_atual

    return limiar


def calcula_limiares_vetor(orig_path, redu_path = None, mode = True):
    if mode: 
        frames = ler_frames(orig_path)
        limiares = [0]
        for i in range(1, len(frames)):
            yuv1 = frames[i-1]
            yuv2 = frames[i]
            f1 = yuv1[:, :, 0]
            f2 = yuv2[:, :, 0]  
            limiar = calcula_limiar(f1, f2)
            limiares.append(limiar)

        return limiares     
    else:
        frames_orig = ler_frames(orig_path)
        frames_corr = ler_frames(redu_path)
        limiares = []
        n = min(len(frames_orig), len(frames_corr))
        for i in range(n):
            yuv1 = frames_orig[i]
            yuv2 = frames_orig[i]
            f1 = yuv1[:, :, 0] 
            f2 = yuv2[:, :, 0]
            limiar = calcula_limiar(f1, f2, 4)
            limiares.append(limiar)
        return limiares
    
def detectar_erros_frame(frame_preview, frame_recon, limiar, block_size=16):
    p = frame_preview[:, :, 0]
    r = frame_recon[:, :, 0]

    blocks_p = get_blocks(p, block_size)
    blocks_r = get_blocks(r, block_size)

    # Redimensiona blocos reconstruídos para bater com os do preview
    erros = 0
    loc_erros = []
    for bp, br in zip(blocks_p, blocks_r):
        if bp.shape != br.shape:
            br = cv2.resize(br, (bp.shape[1], bp.shape[0]))

        mse_atual = mse(bp, br)

        if mse_atual > limiar:
            erros += 1
            loc_erros.append(1)
        else:
            loc_erros.append(0)

    return erros > 0 , loc_erros

def detectar_erros_preview(path_preview, path_recon, limiares):
    frames_prev = ler_frames(path_preview)
    frames_recon = ler_frames(path_recon)
    erros_frames = []
    loc_erros_frames = []


    for i in range(len(frames_prev)):
        erro, loc_erros = detectar_erros_frame(frames_prev[i], frames_recon[i], limiares[i])
        erros_frames.append(erro)
        loc_erros_frames.append(loc_erros)

    return erros_frames, loc_erros_frames

def detectar_erros_principal(path_preview, limiares):
    frames_prev = ler_frames(path_preview)
    erros_frames = []
    loc_erros_frames = []
    for i in range(len(frames_prev)):
        erro, loc_erros = detectar_erros_frame(frames_prev[i], frames_prev[i-1], limiares[i])
        erros_frames.append(erro)
        loc_erros_frames.append(loc_erros)


    return erros_frames, loc_erros_frames
import random

def corromper_y4m(
    input_path,
    output_path,
    bits_por_frame=1000,
    usar_blocos= False,
    tamanho_bloco=16,
    num_blocos_por_frame=3,
    perder_frames=False,
    prob_perder_frame=0.5
):
    with open(input_path, "rb") as f:
        data = f.read()

    partes = data.split(b"FRAME\n")
    header = partes[0]
    frames = partes[1:]  
    print(f"Total de frames encontrados: {len(frames)}")

    frames = [bytearray(f) for f in frames]
    indices = random.sample(range(len(frames)), 60)
    for idx in indices:
        frame = frames[idx]
        if perder_frames and random.random() < prob_perder_frame:
            for i in range(len(frame)):
                frame[i] = 0
            continue 
        for _ in range(bits_por_frame):
            pos = random.randint(0, len(frame) - 1)
            bit = 1 << random.randint(0, 7)
            frame[pos] ^= bit  # XOR flip bit
        if usar_blocos:
            frame_len = len(frame)
            for _ in range(num_blocos_por_frame):
                inicio = random.randint(0, max(0, frame_len - tamanho_bloco))
                for i in range(tamanho_bloco):
                    frame[inicio + i] ^= 0xFF  # invertendo todos os bits
    with open(output_path, "wb") as out:
        out.write(header)
        for frame in frames:
            out.write(b"FRAME\n")
            out.write(frame)

    print("Arquivo salvo como:", output_path)

