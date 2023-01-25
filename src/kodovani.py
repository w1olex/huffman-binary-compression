import heapq
import os
import datetime
import binascii
import json
import xml.etree.ElementTree as ET
import re


class Node:
    def __init__(self, char, pocet):
        """
        Třída Node představuje objekt se zadaným charakterem a frekvencí.

        :param char: Charakter obsazený ve vstupních datech
        :type str
        :param pocet: Počet characteru ve vstupních datech
        :type int:
        """

        self.char = char
        self.pocet = pocet
        self.left = None
        self.right = None


    def __lt__(self, other):
        """
        Porovná frekvence dvou objektů Node.

        :param: other: Druhý objekt Node, se kterým se porovnává.
        :type object
        :return: True, pokud je frekvence jednoho Node menší než u druhého Node, pokud je větší, vrací False
        :rtype: bool
        """

        if not other:
            return -1

        if not isinstance(other, Node):
            return -1

        return self.pocet < other.pocet



def kodovaci_metoda(data, output_file):
    """
    Metoda kóduje zadaná data pomocí Huffmanovy kodovací metody:
    Huffmanovo kódování je metoda komprese dat, která využívá principu,
    že často se vyskytující znaky by měly mít kratší kódy než méně často se vyskytující znaky.
    Algoritmus pro vytvoření Huffmanova kódu je následující

    1. Nejprve vytvoří frekvenční tabulku, což je slovník, kde pro každý znak vstupních dat je uvedena jeho četnost výskytu.

    2. Poté vytvoří tzv heap list s Nodes, kde každá Node reprezentuje jeden znak a jeho četnost výskytu.

    3. Heap je tříděn podle četnosti výskytu, takže nejčastěji se vyskytující znaky jsou umístěny na vrcholu heapu.

    4. Poté jsou Nodes z heapu slučovány do stromu tak, že nejčastěji se vyskytující znaky jsou umístěny na nejnižší úrovni stromu.

    5. Procházením stromu odspodu se pro každý znak vygeneruje jeho kód, který představuje cestu od kořenové Node k Node,
    která reprezentuje daný znak.
    Kód se skládá ze série nul a jedniček, kde nula znamená pokračovat po levé větvi stromu a jednička pokračovat po pravé větvi.


    :param: data: Data k zakódování.
    :type: str

    :return: Zakódovaná data.
    :rtype: str

    :raises: ValueError: Pokud vstupní data nejsou string.
    """

    if not isinstance(data, str):
        raise ValueError("Vstupní data musí být string.")


    # Vytvoření frekvenční tabulky
    pocet = {}
    for char in data:
            # Pokud se jedna o již zaznamenaný charakter, pouze se přičte 1
            if char in pocet:
                pocet[char] += 1

            # Pokud se jedna o nezaznamenaný charakter, přidá se do dict. pocet s počtem 1
            else:
                pocet[char] = 1


    # Vytvoření heapů s Nodes
    heap = []
    frekTabulka = {}

    for char, pocet in pocet.items():
        node = Node(char, pocet)
        frekTabulka.update({node.char : node.pocet})
        heapq.heappush(heap, node)


    # Zapsani frekvenčního stolu do souboru pro uzivatele
    with open(os.path.join('../data', "frekvencni_tabulka.txt"), "w") as f:
        for key, value in sorted(frekTabulka.items(), key= lambda x: x[1], reverse= True):
            if (key == " "):
               key = "SPACE"
            if (key == "\n"):
               key = "ENTER"
            f.write("CHARAKTER: " + str(key) + " | FREKVENCE: "+ str(value) + "\n")


    # Sloučení uzlů, dokud zůstane pouze kořenový uzel
    cislovaniNodes = 1


    while len(heap) > 1:
        left = heapq.heappop(heap) # Odstraní nejmenší prvek z heapu a uloží jej do proměnné „left“.
        right = heapq.heappop(heap) # Odstraní další nejmenší prvek z heapu a uloží ho do proměnné „right“.
        node = Node(None, left.pocet + right.pocet) # Vytvoří nový objekt Node bez hodnoty a s frekvencí rovnou součtu frekvencí levé a pravé Node.
        node.left = left
        node.right = right
        heapq.heappush(heap, node) # Tento řádek přidá novou Node do heapu.
        cislovaniNodes += 1


    # Vytvoření Huffmanova kódu procházením stromu
    root = heapq.heappop(heap) #Odstraní nejmenší prvek z heapu a uloží ho do proměnné 'root'
    codes = {} #kodovaci stůl


    #Procházení stromu a generování kodu pro každý charakter
    def generace_kodu(node, code):
        if node.char: #Platí pokud má daná Node daný charakter (Občas může mít None)
            codes[node.char] = code
        else:
            generace_kodu(node.left, code + "0")
            generace_kodu(node.right, code + "1")

    generace_kodu(root, "") #Procházení stromu od kořene


    #Přidání zakodovaných dat do stringu jedniček a nul, který je připraven ke konvertování do bináru
    encoded_data = ""
    for char in data:
        encoded_data += codes[char]


    #Uložení kodovací tabulky do složky tables
    json_string = json.dumps(codes)

    #Uložení v txt dá uživateli možnost k prohlédnutí kodovací tabulky
    final_output_file = output_file.replace(".bin","") + ".txt"

    # Uložení kodovací tabulky do složky tables
    with open(os.path.join('../tables', final_output_file), "w") as f:
        f.write(json_string)


    # Zapsaní kodovací tabulky do složky data pro uživatele (Navíc)
    with open(os.path.join('../data', "binarni_tabulka_readable.txt"), "w") as f:
        for key, value in sorted(codes.items(), key=lambda x: len(x[1])):
            if (key == " "):
                key = "SPACE"
            if (key == "\n"):
                key = "ENTER"

            f.write("CHARAKTER: "+ key +" | BINARY: "+value + "\n")


    # Uložení Zakodovaných dat do souboru (jenom pro zajímavost)
    """
    with open(os.path.join('../data', "encoded_data.txt"), "w") as f:
        f.write(encoded_data)
    """

    return encoded_data



def string_checker(s):
    # Zkontroluje, zda string obsahuje pouze písmena anglické abecedy a čísla od 0 - 9
    return bool(re.match(r'^[a-zA-Z0-9]+$', s))


def vytvoreni_slozek(nazev_slozky):
    # Zjistí cestu do rodičovského adresáře

    # získá absolutní cestu k aktuálnímu souboru
    current_file_path = os.path.abspath(__file__)

    # získá nadřazený adresář aktuálního souboru
    parent_dir = os.path.dirname(current_file_path)
    # získá nadřazený adresář rodiče
    grandparent_dir = os.path.dirname(parent_dir)

    # vytvoří cestu k novému adresáři
    new_dir_path = os.path.join(grandparent_dir, nazev_slozky)


    # Vytvoří složky které neexistují
    if not os.path.exists(new_dir_path):
        try:
            os.makedirs(new_dir_path, exist_ok=True)
        except OSError:
            # Pokud ke složce nemá uživatel práva
            print("Slozku " + nazev_slozky + " se nepodarilo vytvorit (Pravděpodobně nemáte dostatečná práva")
        else:
            # Pokud vytvoření chybějících složek proběhne úspěšně
            print("Slozka " + nazev_slozky + " byla uspesne vytvorena")


    return new_dir_path #Slouží především pro ověření funkčnosti u unittestingu


if __name__ == "__main__":
    pass