import os

from kodovani import kodovaci_metoda


def compress(input_file, output_file):
    """
    Komprimuje zadaný vstupní soubor a uloží výsledek do výstupního souboru.

    :param input_file: The name of the input file to compress.
    :type str
    :param output_file: The name of the output file to save the compressed data to.
    :type str
    """

    # Otevře vstupní soubor a přečte jeho obsah
    file_path = os.path.abspath(os.path.join('../txt', input_file))

    try:
        with open(file_path, "r") as f:
                data = f.read()
    except:
        # Pokud se v souboru vyskytují neplatné znaky vyhodí se vyjímka
        raise Exception("Soubor obsahuje neplatne znaky - nelze ho kompresovat")


    # Použije kodovací metodu ke komprimaci dat
    encoded_data = kodovaci_metoda(data, output_file)

    # Otevře výstupní soubor v binárním režimu a zapíše do něj komprimovaná data
    with open(os.path.join('../outputs', output_file), "wb") as f:
        # Konvertuje zakodovaná data (string jedniček a nul) na integer a následně na byteový objekt
        encoded_data_bytes = int(encoded_data, 2).to_bytes((int(encoded_data, 2).bit_length() + 7) // 8, "big")
        f.write(encoded_data_bytes)