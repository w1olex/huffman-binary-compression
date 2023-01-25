from kodovani import *
from log import log_to_xml, parse_xml
from komprese import compress
from dekomprese import decompress


def main():
    """
    USER INTERFACE:
    1. Zeptá se uživatele na zda chce a) kompresovat b) dekompresovat c) zobrazit logy

        1a) Pokud si uživatel zvolil kompresi, program se zeptá jaký soubor chce kompresovat,
            vybraný soubor však musí být uložen ve složce /txt/, zvolený soubor může být pouze formátu .txt.
            Dále si uživatel zvolí jméno výstupního souboru, jméno nesmí obsahovat jiné znaky než
            malá a velká písmena anglické abecedy a číslice 0-9. Výstupní soubor se uloží do složky /outputs/.

        1b) Pokud si uživatel zvolil dekompresi, program se zeptá jaký soubor chce dekompresovat.
            Pravidlo pro dekompresi je že tento soubor musel být prvně komprimován algorytmem právě tohoto programu,
            soubor musí mít také ve složce /tables/ uloženou vlastní kodovací tabulku. Následně je uživatel tázán
            na jméno výstupního souboru, jméno také nesmí obsahovat jiné znaky než malá a velká písmena
            anglické abecedy a číslice 0-9. Uživatel si může zvolit i složku do které chce soubor nahrát,
            pokud složka neexistuje, vytvoří se nová. Pokud již existuje, soubor se vytvoří do existující.
            Název složky stejně jako název souboru musí obsahovat pouze alá a velká písmena
            anglické abecedy a číslice 0-9.

        1c) Pokud si uživatel zvolil zobrazení logů, vypíší se mu přehledně řádkově oddělené logy z 'log.xml' souboru
            uloženém ve složce /logs/. Pokud se v souboru žádné logy nevyskytují (nebyla zatím provedena komprese)
            či dekomprese) vypíše se uživateli ať kompresuje alespoň 1 soubor.
            Následně se program táže, zda si uživatel také přeje filtrovat dané logy:

            a) Pokud uživatel zvolí ano, program mu nabídne zda chce filtrovat config či výsledek,
                nebo zda chce seřadit dané logy dle datumu, pokud se uživatel rozhodne pro config, může dále napsat
                podle kterých hodnot chce filtrovat (u configu to je komprese či dekomprese), pokud zvolí výsledek
                může si např. nechat zobrazit pouze logy, které byli úspěšné. Seřazení logu dle datumu, je zde pouze navíc
                jelikož logy se sami o sobě zapisují popořadě.

            b) Pokud si uživatel nepřeje filtrovat logy, vrací se zpět do hlavní nabídky

    2. Následně se program ptá zda si uživatel přeje pokračovat či zda chce program ukončit.
        Uživatel může spustit program kolikrát chce.

    """

    #Úvod
    print("Alfa 2 - Jakub Machacek C4b\n")
    print("Navod k pouziti se nachází v README.txt souboru ve slozce /doc/ \n")
    print("_______________________________________________________________________\n")
    while(True):

        # Vytvoření potřebých složek (pokud neexistujou)
        vytvoreni_slozek('data')
        vytvoreni_slozek('outputs')
        vytvoreni_slozek('logs')
        vytvoreni_slozek('tables')
        vytvoreni_slozek('txt')

        print()

        # Hlavní menu
        volba = input("Zvolte zda chcete kompresi nebo dekompresi souboru, ci zobrazeni logu\n(k = komprese, d = dekomprese, l = zobrazit logy) | (k/d/l): ")

        # Komprese
        if(volba == 'k'):

            # Volba souborů
            input_file = input("\nZadejte jmeno souboru ktery chcete kompresovat, soubor musi byt ve slozce /txt/ (bez .txt pripony): ")
            output_file = input("Zadejte jmeno vystupniho souboru (bez .bin pripony): ")

            # Ověření platnosti názvu výstupního souboru
            if(string_checker(output_file)):
                pass
            else:
                raise UnicodeError("Jmeno souboru muze obsahovat pouze male a velka pismena anglicke abecedy a cisla 0-9")

            # Přidání koncovek pro deklarování typu souboru
            input_file_txt = input_file + ".txt"
            output_file_bin = output_file + ".bin"
            print("_______________________________________________________________________\n")

            try:
                compress(input_file_txt, output_file_bin)
            except:
                # Zapíše se log
                log_to_xml("compress", input_file_txt, output_file_bin, "failed")
                raise Exception("Komprese souboru se nezdarila")

            print("Komprese se zdarila! Soubor "+output_file_bin +" byl ulozen do slozky /outputs/\n")

            # Zapíše se log
            log_to_xml("compress", input_file_txt, output_file_bin, "success")

        # Dekomprese
        elif(volba == 'd'):

            # Volba souborů
            input_file_d = input("\nZadejte jmeno souboru ktery chcete dekompresovat (bez .bin pripony): ")
            output_file_d = input("Zadejte jmeno 'output' souboru: ")
            folder_d = input("Zadejte jmeno slozky do ktere chcete soubor ulozit: ")

            # Ověření platnosti názvu výstupního souboru
            if(string_checker(input_file_d) and string_checker(output_file_d)):
                pass
            else:
                raise UnicodeError("Jmeno souboru muze obsahovat pouze male a velka pismena anglicke abecedy a cisla 0-9")

            # Přidání koncovek pro deklarování typu souboru
            final_input_file_d = input_file_d + ".bin"
            final_output_file_d = output_file_d + ".txt"
            print("_______________________________________________________________________\n")

            # Ověření platnosti názvu výstupního souboru
            if(string_checker(folder_d) and string_checker(output_file_d)):
                pass
            else:
                raise UnicodeError("Jmeno slozky a souboru muze obsahovat pouze male a velka pismena anglicke abecedy a cisla 0-9")

            try:
                decompress(final_input_file_d, final_output_file_d, folder_d)
            except:
                # Zapíše se log
                log_to_xml("decompress", final_input_file_d, final_output_file_d, "failed")
                raise Exception("Dekomprese souboru se nezdarila")

            print("Dekomprese se zdarila! Soubor " + final_output_file_d + " byl ulozen do slozky '" + folder_d + "'\n")
            # Zapíše se log
            log_to_xml("decompress", final_input_file_d, final_output_file_d, "success")

        # Zobrazeni logů
        elif(volba == 'l'):

            print("\nLogs (logs/log.xml):")

            try:
                logs = parse_xml("../logs/log.xml")
            except:
                print("Soubor log.xml zatim nebyl zatim vytvoren pro jeho vytvoreni kompresujte alespon 1 soubor\n")
                continue

            # Vypsání logů
            for log in logs:
                print(log)

            volba_log = input("\nPrejete si logy filtrovat podle danych parametru? (Ano = a, Ne = n) | (a/n): ")
            if (volba_log == 'n'):
                print("\n")


            elif (volba_log == 'a'):
                volba_log_param = input("\nPrejete si filtrovat logy dle configu (komprese/dekomprese), "
                                        "vysledku (result) nebo seradit dle datumu (date_time)?\n"
                                        "(config = c, datum = d, vysledek = v) | (c/d/v): ")
                print()

                #config
                if (volba_log_param == 'c'):

                    volba_config = input("Chcete vypsat pouze logy s kompresi (compress) nebo dekompressi (decompress)?\n"
                                         "(komprese = k, dekomprese = d) | (k/d): ")

                    # config - komprese
                    if(volba_config == 'k'):
                        logs_congif_compress = logs
                        logs_congif_compress = [log for log in logs_congif_compress if log['config'] != 'decompress']

                        # vypsání filtrovaných logů
                        for log in logs_congif_compress:
                            print(log)

                    # config - dekomprese
                    elif(volba_config == 'd'):
                        logs_congif_decompress = logs
                        logs_congif_decompress = [log for log in logs_congif_decompress if log['config'] != 'compress']

                        # vypsání filtrovaných logů
                        for log in logs_congif_decompress:
                            print(log)

                    else:
                        raise TypeError("Muzete zadat pouze 'k' nebo 'd'")

                #datum (date_time)
                elif (volba_log_param == 'd'):
                    logs_sorted_dt = sorted(logs, key=lambda x: x['date_time'])
                    for log in logs_sorted_dt:
                        print(log)

                #Vysledek (result)
                elif (volba_log_param == 'v'):

                    volba_result = input("Chcete vypsat pouze logy ktere byly uspesne (success) nebo se pokazily (failed)?\n"
                                        "(uspesne = s, pokazily se = f) | (s/f): ")

                    # result - success
                    if(volba_result == 's'):
                        logs_result_success = logs
                        logs_result_success = [log for log in logs_result_success if log['result'] != 'failed']

                        # vypsání filtrovaných logů
                        for log in logs_result_success:
                            print(log)

                    # result - failed
                    elif(volba_result == 'f'):
                        logs_result_success = logs
                        logs_result_success = [log for log in logs_result_success if log['result'] != 'success']

                        # vypsání filtrovaných logů
                        for log in logs_result_success:
                            print(log)

                    else:
                        raise TypeError("Muzete zadat pouze 's' nebo 'f'")

                else:
                    raise TypeError("Muzete zadat pouze 'c' nebo 'd'")

            else:
                raise TypeError("Muzete zadat pouze 'a' nebo 'n'")

        else:
            raise TypeError("Muzete zadat pouze 'k', 'd', 'l'")


        # Pokracovani, ci ukonceni programu
        volba2 = input("\nPokracovat nebo Ukoncit program?\n(Pokracovat = 1, Ukoncit program = 0) | (1/0): ")
        if(volba2 == '1'):
            print("\n")
            continue
        elif(volba2 == '0'):
            break
        else:
            raise TypeError("Muzete zadat pouze '1' nebo '0'")


if __name__ == "__main__":
    main()