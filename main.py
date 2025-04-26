import numpy as np
from PIL import Image

def embed_data(cover_img, secret_bits):
    # Ubah ke grayscale sehingga mudah dilakukan operasi tidak nilai {R, G, B}
    img = np.array(cover_img.convert('L'))
    # Merubah gambar 2 dimensi menjadi 1 dimensi linear
    flat = img.flatten()
    # Menyimpan di variabel lain
    stego_img = flat.copy()
    key_table = []
    # Variabel untuk tracking index image
    idx = 0
    # Variabel untuk tracking index secret bits
    bit_idx = 0

    while idx < len(flat) - 1 and bit_idx < len(secret_bits):
        p1 = int(flat[idx])
        p2 = int(flat[idx + 1])
        d = p1 - p2
        s = int(secret_bits[bit_idx])

        if 0 <= d <= 3:
            new_pixel = p1 + d + s
            if new_pixel > 255:
                stego_img[idx] = p1
                key_table.append(0)
            else:
                stego_img[idx] = new_pixel
                key_table.append(1)
                bit_idx += 1
        elif 4 <= d <= 5:
            d_prime = int(np.floor(d/2))
            new_pixel = p1 + d_prime + s
            if new_pixel > 255:
                stego_img[idx] = p1
                key_table.append(0)
            else:
                stego_img[idx] = new_pixel
                key_table.append(2)
                bit_idx += 1
        else:
            stego_img[idx] = p1
            key_table.append(0)

        stego_img[idx + 1] = p2  # biarkan piksel kedua tidak berubah
        idx += 2 # index image maju 2

    stego_img = np.reshape(stego_img, img.shape) # Mengembalikan dari 1 dimensi linear ke 2 dimensi semula
    return Image.fromarray(np.uint8(stego_img)), key_table

def extract_data(stego_img, key_table):
    # Ubah ke grayscale sehingga mudah dilakukan operasi tidak nilai {R, G, B}, ubah juga ke 1 dimensi linear
    img = np.array(stego_img.convert('L')).flatten()
    # Buat simpen shape
    dummy = np.array(stego_img.convert('L'))
    # Variabel untuk tracking index image
    idx = 0
    # Penyimpanan pesan rahasia
    bits = []
    # Penyimpanan gambar asli
    new_img = img.copy()

    for key in key_table:
        p1 = int(img[idx])
        p2 = int(img[idx + 1])
        d = p1 - p2

        if key == 1:
            new_img[idx] = p1 - int(np.floor(d/2))
            s = d % 2
            bits.append(str(s))
        elif key == 2:
            new_img[idx] = p1 - int(np.floor(d/2)) + 1
            s = d % 2
            bits.append(str(s))
        # key == 0 → skip

        new_img[idx + 1] = p2
        idx += 2

    new_img = np.reshape(new_img, dummy.shape)
    return Image.fromarray(np.uint8(new_img)), ''.join(bits)

# Contoh penggunaan:
if __name__ == "__main__":
    # Buka citra grayscale
    img = Image.open("test.png")  # ganti dengan path citramu
    secret = "1101010101011100"     # data rahasia
    
    stego, key = embed_data(img, secret)
    stego.save("stego.png")

    # Ekstraksi kembali
    stego_loaded = Image.open("stego.png")
    new_image, extracted = extract_data(stego_loaded, key)
    new_image.save("after_extract.png")
    print("Data yang diekstrak:", extracted)