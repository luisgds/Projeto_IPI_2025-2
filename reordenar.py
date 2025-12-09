# Talvez não seja necessario desordenar e reordenar
# pois esse processo é apenas para a transmissão 
# Reordenar os quadros igual no tcc
def reorder_frames(frames, REF):
    F = len(frames)
    output = [None] * F
    # Primeiro quadro permanece igual
    output[0] = frames[0]
    j = REF
    for i in range(1, F):  # começa no segundo quadro
        output[i] = frames[j]
        j = j + REF 
        if j >= F:  
            j = j - F + 1
    return output 
