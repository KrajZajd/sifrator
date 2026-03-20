import random
import hashlib
from tqdm import tqdm
import getpass
import tkinter as tk
from tkinter import filedialog
sha = hashlib.sha3_512()
def vyber_souboru():
    root = tk.Tk()
    root.withdraw()
    cesta_k_souboru = filedialog.askopenfilename(
        title="Vyberte soubor k začiforování/dešifrování",
    )

    # Zavře skryté okno
    root.destroy()
    return cesta_k_souboru
def bits_to_bytes(bits):
    bytes_list = []
    for i in tqdm (range(0, len(bits), 8), desc="Ukládám"):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte = (byte << 1) | bits[i + j]
        bytes_list.append(byte)
    return bytes(bytes_list)
def nxor(a, b):
    return (a and b) or (not a and not b)
def generuj_klic(heslo:str, delka):
    sha.update(heslo.encode("utf-8"))
    random.seed(int(sha.hexdigest(), 16))
    return [random.randint(0,1) for _ in tqdm (range(delka), desc="Generuji klíč")]

def main(cesta_k_souboru, heslo):
    if ".zss" in cesta_k_souboru:
        desifruj(cesta_k_souboru, heslo)
    else:    
        zasifruj(cesta_k_souboru, heslo)
def zasifruj(cesta_k_souboru, heslo):
    with open(cesta_k_souboru,"rb") as file:
        data = file.read() 
        seznam_s_bity = bytes_to_bits(data)
    klic = generuj_klic(heslo, len(seznam_s_bity))
    seznam_se_zasifrovanymi_bity = list()
    for i in tqdm(range(len(seznam_s_bity)), desc="Šifruji"):
        if(nxor(seznam_s_bity[i], klic[i])):
            seznam_se_zasifrovanymi_bity.append(1)
        else:
            seznam_se_zasifrovanymi_bity.append(0)
    zasifrovane_byty = bits_to_bytes(seznam_se_zasifrovanymi_bity)
    with open(f'{cesta_k_souboru}.zss', 'wb') as file:
        file.write(zasifrovane_byty)
    

def bytes_to_bits(data):
    bits = []
    for byte in tqdm (data, desc= "Otevírám"):
        for i in range(7, -1, -1):
            bit = (byte >> i) & 1
            bits.append(bit)
    return bits


def desifruj(cesta_k_souboru, heslo):
    with open(cesta_k_souboru,"rb") as file:
        data = file.read() 
        seznam_s_bity = bytes_to_bits(data)
    klic = generuj_klic(heslo, len(seznam_s_bity))
    seznam_se_desifrovanymi_bity = list()
    for i in tqdm(range(len(seznam_s_bity)), desc="Dešifruji"):
        if(nxor(seznam_s_bity[i], klic[i])):
            seznam_se_desifrovanymi_bity.append(1)
        else:
            seznam_se_desifrovanymi_bity.append(0)
    zasifrovane_byty = bits_to_bytes(seznam_se_desifrovanymi_bity)
    cesta_k_souboru = cesta_k_souboru.replace(".zss","")
    with open(f'{cesta_k_souboru}', 'wb') as file:
        file.write(zasifrovane_byty)
if __name__ == "__main__":
    cesta_k_souboru = vyber_souboru()
    heslo = getpass.getpass("Zadejte heslo: ")
    main(cesta_k_souboru, heslo)