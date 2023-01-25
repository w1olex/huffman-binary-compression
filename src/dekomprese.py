import os
import binascii
import json

def decompress(input_file, output_file, folder):
    """
     Dekomprese binárního souboru do txt formátu a následné uložení do složky

    :param input_file: Binární soubor, který chceme dekompresovat
    :type str
    :param output_file: Výstupní soubor ve formátu
    :type str
    :param folder: Složka do které chceme výstupní soubor uložit
    :type str
    :return: Dekompresovaná data
    :rtype str

    """

    file_name = input_file

    # Otevře vstupní soubor v režimu pro čtení binárních dat a následně se obsah souboru načte do objektu typu bytes.
    # Poté se každý bajt v objektu bytes převede na binární řetězec.
    with open(os.path.join('../outputs', input_file), 'rb') as file:

        input_file = file.read()

    bin_to_str = bin(int(binascii.hexlify(input_file), 16))[2:]


    final_input_file = file_name.replace(".bin", "") + ".txt"

    # Otevře soubor s kódovací tabulkou, který se použil při kompresi.
    # Pokud soubor s kódovací tabulkou není k dispozici, vyvolá se výjimka FileNotFoundError.

    try:
        with open(os.path.join('../tables', final_input_file), "r") as f:
            binarni_dict_str = f.read()

        binarni_dict = json.loads(binarni_dict_str)
    except:
        FileNotFoundError("Nebyla nalezena kodovaci tabulka k souboru"+ final_input_file)


    decompressed_data = ''
    # Start from the left of the compressed data
    i = 0

    # Začne iterovat přes binární řetězec a hledat nejdelší kód z tabulky, který odpovídá kompresovaným datům.
    # Pokud je nalezen takový kód, přidá se k dekomprimovaným datům příslušný znak a proces se opakuje,
    # dokud není projita celá kompresovaná data.

    while i < len(bin_to_str):
        for j in range(i, len(bin_to_str)):
            if bin_to_str[i:j + 1] in binarni_dict.values():
                decompressed_data += next(key for key, value in binarni_dict.items() if value == bin_to_str[i:j + 1])
                i = j + 1
                break


    # Zjistí cestu do rodičovského adresáře
    current_file_path = os.path.abspath(__file__)
    parent_dir = os.path.dirname(current_file_path)
    grandparent_dir = os.path.dirname(parent_dir)
    new_dir_path = os.path.join(grandparent_dir, folder)

    #Pokud složka neexistuje vytvoří se nová, pokud složka existuje zapíše se soubor do existující
    os.makedirs(new_dir_path, exist_ok=True)


    # Výstupní soubor se zapíše složky.
    with open(os.path.join(new_dir_path, output_file), "w") as f:
        f.write(decompressed_data)

    return decompressed_data
