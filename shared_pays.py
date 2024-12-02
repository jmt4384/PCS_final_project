# Import modulů
import csv
import os

# vyčištění okna


def clear_screen():
    # detekce operačního systému a jeho vyčištění
    if os.name == "nt":         # Windows
        os.system("cls")
    else:                       # Unix / Linux / MacOS
        os.system("clear")

# Výběrové funkce


def select_main_function():
    '''
    Funkce pro bezpečnou volbu funkce v hlavním menu
    Parameters:
        vstup z klávesnice
    Returns:
        int menu
    '''
    while True:
        # zobrazení uživateli hlavního menu
        print(40*"-")
        print("V hlavní nabídce jsou dostupné tyto možnosti :")
        for key, value in MAIN_MENU.items():
            print(f"Možnost: {key} Funkce: {value}")
        # vstup z klávesnice
        print(40*"-")
        menu = input("Pro výběr funkce zvol číslo: 01234\n")
        try:
            # vstupní znak je v povolených
            int(menu)
            if int(menu) in MAIN_MENU.keys():
                menu = int(menu)
                print(f"Zvolil si {menu}, funkci {MAIN_MENU[menu]}")
                break
        # ošetření vyjímky, pro znak, který nelze převést na int
        except:
            print("Zvolil si nepovolený znak"
                  "Pro výběr funkce zvol číslo: 01234")
    return menu


def select_edit_function():
    '''
    Funkce pro bezpečnou volbu funkce v editovacím menu
    Parameters:
        vstup z klávesnice
    Returns:
        int menu
    '''
    # vypsání možností editace
    print(40*"-")
    print("V nabídce jsou dostupné tyto možnosti :")
    for key, value in EDIT_MENU.items():
        print(f"Možnost: {key} Funkce: {value}")
    print(40*"-")
    while True:
        # vstup z klávesnice
        menu = input("Pro výběr funkce zvol číslo: 0123\n")
        try:
            int(menu)
            # vstupní znak je v povolených
            if int(menu) in EDIT_MENU.keys():
                menu = int(menu)
                print(f"Zvolil si {menu}, Funkci {EDIT_MENU[menu]}")
                break
        except:
            print("Zvolil si nepovolený znak"
                  "Pro výběr funkce zvol číslo: 0123")
    return menu


# Funkce provádějící zvolené operace - volání dílčích funkcí

def main_function_decision():
    '''
    hlavní rozhodovací smyčka, po provedení požadované funkce
    Parameters:
        int výstup funkce select_main_function()
    Returns:
        None
    '''
    # při prvním spuštění ještě nebyl proveden import dat
    import_done = False
    # při prvním spuštění ještě nebyl vytvořen Balance Sheet
    balance_sheet_done = False
    # výstup z cyklu lze pouze volbou 0 - řádné ukončení programu
    while True:
        menu = select_main_function()
        if menu == 0:
            break
        # načtení vstupního souboru
        if menu == 1:
            data = import_input_file()
            import_done = True
            pause_to_menu()
        # editace záznamů
        if menu == 2 and import_done:
            data = edit_function_decision(data)
            pause_to_menu()
        # vytvoření balance sheetu a výsl. rozpočtu
        if menu == 3 and import_done:
            [BS_data, final_table] = create_balance_sheet(data)
            balance_sheet_done = True
            pause_to_menu()
        # uložení balance sheetu a výsl. rozpočtu
        if menu == 4 and balance_sheet_done:
            save_balance_sheet(BS_data, final_table)
            pause_to_menu()
        # pokud nebyl proveden import nelze pokračovat
        if not import_done:
            print("Funkci není možno provést, data nebyla importována")
            pause_to_menu()
        #clear_screen()

def edit_function_decision(data):
    '''
    vedlejší rozhodovací smyčka, po provedení požadované funkce
    Parameters:
        int výstup funkce select_edit_function()
    Returns:
        data (list)
    '''
    # výstup z cyklu lze pouze volbou 0 - výstup do hlavního menu
    while True:
        menu = select_edit_function()
        # výstup do hlavního menu
        if menu == 0:
            break
        # provedení funkce odebrání člena
        if menu == 1:
            data = remove_member(data)
            pause_to_menu()
        # provedení funkce doplnění nové platby
        if menu == 2:
            add_pay(data)
            pause_to_menu()
        # provedení funkce odebrání platby
        if menu == 3:
            data = remove_pay(data)
            pause_to_menu()
    return data


# Funkce pozastavení výběru

def pause_to_menu():
    '''
    funkce pauzy
    Parameters:
        vstup z klávesnice
    Returns:
        None
    '''
    print(40*"-")
    input("Pro pokračování běhu programu stiskni libovolnou klávesu\n")
    return


# Funkce importu souboru, setřídění, normalizace, validace, přepočet kurzů

def import_input_file():
    '''
        načtení vstupního souboru input_data_full.csv
        funkce provede ověření, setřídění, normalizaci dat
    Parameters:
        input_data_full.csv
    Returns:
        list data
    '''

    data = []
    fail_data = []
    # ošetření vyjímky kdyby soubor nebylo možné otevřít
    try:
        with open("input_data_full.csv", "r", encoding="utf-8") as input_file:
            # print("soubor importován")
            reader = csv.DictReader(input_file, delimiter=',',
                                    fieldnames=CSV_FIELD_NAME)
            # očíslování záznamů - přidání klíče "num"
            count = 0

            for row in reader:
                count += 1
                # normalizace, osekání řádků a úprava textů, def měna = CZK
                normalised_row = normalise_pay_data(row, count)
                # ověření, že normalizace a validace proběhla v pořádku
                if normalised_row == None or validate_row(normalised_row) == False:
                    print(f"Chybný záznam na řádku č. {count} přeskočen")
                    fail_data.append(row)
                    continue
                else:
                    # normalizovaná, validovaná data jsou připojena do
                    # pracovních dat
                    data.append(normalised_row)
            print(40*"-")
            print("Vstupní soubor upraven, může být vytvořen Balance Sheet")

            # pokud byla vypsána nějaká chybová data, uložit do souboru
            if fail_data != []:
                # soubor fail_input_data režim přepis
                with open("fail_input_data.csv",
                          "w", encoding="utf-8") as fail_input_file:
                    writer = csv.DictWriter(fail_input_file,
                                            fieldnames=CSV_FIELD_NAME)
                    writer.writeheader()
                    for radek in fail_data:
                        writer.writerow(radek)
                print(40*"-")
                print("Ve vstupním souboru byla nalezena nekorektní data"
                      " tyto záznamy byly přeskočeny "
                      "a vypsány v fail_input_data.csv")
            # print(data)
    # Vyjímka nenalezení souboru
    except FileNotFoundError:
        print("Vstupní soubor nenalezen")
        return None
    return data


def normalise_pay_data(pay_data, num):
    '''
    konverze řádky ve vstupním souboru tak, aby obsahoval pouze
    požadovaná data, pokud není možné provést, vrátí None

    Parameters:
        list pay_data, int num
    Returns:
        list normalised_data/ None
    '''
    try:
        # ošetření vyjímky, pokud by nebylo možné záznam převést na float
        # doplnění polí do normalizované délky
        normalised_data = {key: str(value) for key, value in pay_data.items()
                           if key in CSV_FIELD_NAME}

        # načtení do polí korektních dat
        normalised_data = {
            "num": num,
            "date_time": normalised_data["date_time"].strip()
            if normalised_data.get("date_time") else "nevyplněno",
            "payer": normalised_data["payer"].strip().title()
            if normalised_data.get("payer") else "nevyplněno",
            "subject": normalised_data["subject"].strip()
            if normalised_data.get("subject") else "nevyplněno",
            "amount": float(normalised_data["amount"])
            if normalised_data.get("amount") else "nevyplněno",
            "currency": normalised_data["currency"].strip()
            if normalised_data.get("currency") and
            normalised_data["currency"].strip() else "CZK",
                }
        # doplnění pole jednotné měny
        normalised_data["norm_amount"] = norm_amount(normalised_data["amount"],
                                                normalised_data["currency"])
        return normalised_data
    except:
        return None


def validate_row(row):
    '''
    ověření, že má řádka validní parametry kdo platil, částka

    Parameters:
        list row
    Returns:
        True / False
    '''
    # pokud je v řádce alespoň kdo platil a částka, je řádka vylidní
    if (row["payer"] == "nevyplněno") or (row["amount"] == "nevyplněno") or row["payer"] == "":
        return False
    return True


def norm_amount(amount, currency):
    '''
    přepočet částky na normativní měnu pomocí směnných kurzů
    Parameters:
        float amount, str currency
    Returns:
        float result
    '''
    # podmínka pro měnu EUR
    if currency == "EUR":
        result = amount*EXCHANGE_E_CZK
    # podmínka pro měnu Tl
    elif currency == "TL":
        result = amount*EXCHANGE_TL_CZK
    # jinak je předpoklad vstupu v CZK
    else:
        result = amount
    return round(result, 2)


# Funkce pro editaci záznamů - odebrání člena, přidání platby, odebrání platby

def remove_member(data):
    '''
    funkce odebere člena - všechny jeho platby
    Parameters:
        list data
    Returns:
        list out_data
    '''

    dict_of_payers = {}
    out_data = []

    # vytvoření seznamu všech členů
    payers = get_list_payers(data)
    # očíslování všech členů pro jednotnou identifikaci
    for index in range(1, len(payers)+1):
        dict_of_payers[index] = payers[index-1]
        print(f"Zvol {index} pro odebrání {dict_of_payers[index]}")

    # zvolenému číslu náleží jméno ze slovníku
    removed_payer_num = select_payer(dict_of_payers)
    # podmínka návratu do menu, data jsou nezměněna oproti vstupním
    if removed_payer_num == 0:
        return data
    removed_payer = dict_of_payers[removed_payer_num]
    # projdi všechny záznamy a pokud je tam někde řádka s jiným platičem
    # tak ji přiřaˇ%d do výstupních dat
    for row in data:
        if row["payer"] != removed_payer:
            out_data.append(row)
    # výstupní data jsou vyfiltrována o definovaného člena
    return out_data


def select_payer(dict_of_payers):
    '''
    funkce na výběr validního člena ze vstupu klávesnice
    Parameters:
        dict dict_of_payers
    Returns:
        int result
    '''
    # smyčka pro opakování při nevalidním vstupu
    while True:
        try:
            # zadání čísla člena k vymazání
            result = int(input("Zadej číslo člena k vymazání, 0 pro exit\n"))
            # podmínka, že zadané číslo je není mimo validní označení člena
            # a je nenulové ... je int, ale není validní
            if (result not in dict_of_payers.keys()) and result != 0:
                print("zvolil si nepovolený znak")
                continue
            break
        except:
            # ošetření podmínky nepovoleného znaku
            print("Zvolil si nepovolený znak")
    return result


def add_pay(data):
    '''
    funkce na přidání platby do seznamu

    Parameters:
        list of dict
    Returns:
        list of dict
    '''

    # zavolal jsem si funkce pro načtení dat
    date_time = insert_pay("date_time")
    payer = insert_pay("payer")
    subject = insert_pay("subject")
    amount = insert_pay("amount")
    currency = insert_pay("currency")

    # nalezení čísla kterým bude nový záznam označen
    max_num = 0
    # nalezení maximálního označení v balance sheetu
    for row in data:
        if row["num"] > max_num:
            max_num = row["num"]

    # nový záznam bude mít max pořadí +1
    new_num = max_num+1
    #
    new_pay_data = {
        "date_time": date_time,
        "payer": payer,
        "subject": subject,
        "amount": amount,
        "currency": currency,
          }
    # nový záznam bude znormalizován a bude doplněn přepočet
    # do CZK "norm amount
    new_pay_data = normalise_pay_data(new_pay_data, new_num)
    new_pay_data["norm_amount"] = norm_amount(amount, currency)

    # nový záznam doplněný do stávajícího pole
    data.append(new_pay_data)
    return data


def insert_pay(text):
    '''
    funkce na korektní vsup nové platby z klávesnice

    Parameters:
        str text
    Returns:
        str nebo float
    '''
    # vynulování proměnných
    date_time = ""
    payer = ""
    subject = ""
    amount = 0
    currency = ""

    # nekonečná smyčka pokud zadání selže, bude se opakovat
    while True:
        try:
            # pokud bude zadávání v režimu datum čas
            if text == "date_time" and date_time == "":
                date_time = input("zadej datum a čas "
                                  "ve formátu dd.mm.rrrr hh:mm\n")
                # podmínka formátu date_time
                return date_time
            # pokud bude zadávání v režimu kdo platil
            if text == "payer" and payer == "":
                payer = input("zadej kdo platil\n")
                if payer.isalpha():
                    return payer
            # pokud bude zadávání v režimu co se platilo
            if text == "subject" and subject == "":
                subject = input("zadej za co byla platba provedena\n")
                if subject.isalnum():
                    return subject
            # pokud bude zadávání v režimu placené částtky
            if text == "amount" and amount == 0:
                amount = float(input("zadej částku\n"))
                if isinstance(amount, float):
                    return amount
            # pokud bude zadávání v režimu měny placení
            if text == "currency" and currency == "":
                currency = input("zadej měnu ve které byla platba provedena\n")
                return currency
        except:
            # chybová hláška
            print("zadal si nekorektní data, pokračuj")


def remove_pay(data):
    '''
    funkce na smazání konkrétního platebního záznamu
    číslování se bere podle aktuálního balance sheetu na obrazovce
    Parameters:
        list data
    Returns:
        list data
    '''
    # načtení čísla platby z funkce pro ošetření vyjímek
    removed_num = select_num_pay(data)

    # cyklus iteruje přes všechny záznamy a pokud je pro nějaký řádek na
    # pozici označení "num" dané číslo, veme si z něj index tohoto řádku
    for index in range(0, len(data)):
        num = data[index]["num"]
        if num == removed_num:
            break
    # smazání řádku záznamu na nalezeném indexu
    data.pop(index)
    # návrat aktualizovaných dat
    return data


def select_num_pay(data):
    '''
    funkce pro korektní výběr platebního záznamu
    výstupem je číslo bezpečně označující mazaného člena
    Parameters:
        list data
    Returns:
        int num_pay
    '''
    ident_pays = []

    # vytvoření listu čísel záznamů v datech
    for row in data:
        ident_pays.append(row["num"])

    while True:
        # ošetření vyjímky, pro vstup nepoveleného znaku
        try:
            num_pay = int(input("Zadej číslo platby k vymazání z "
                                "aktuálního Balance Sheetu, případně"
                                "0 pro exit"))
            # zvolené číslo není v seznamu záznamů, nebo 0
            if (num_pay not in ident_pays) and num_pay != 0:
                print("Zvolil si nepovolený znak")
                continue
            break
        except:
            print("Zvolil si nepovolený znak")
    return num_pay


# Funkce pro vytvoření Balance Sheetu a výsledného rozpočtu
def create_balance_sheet(data):
    '''
    vytvoření balance sheetu a finálního sumáře rozpočtu setříděné podle podle
    osob - zobrazení na obrazovku
    + výstup v return datech
    Parameters:
        list data
    Returns:
        list [balance_sheet_data, final_table]
    '''
    # print(data)
    # deklarace proměnných
    balance_sheet_data = []
    sumary_data = {}
    total_expense = 0
    final_table = []

    # načtení seznamu platičů v databázi a jejich počet
    payers = get_list_payers(data)
    num_payers = len(payers)

    # cyklus přes všechny platiče v databázi
    for payer in payers:
        # vytištění hlavičky konkrétního platiče
        balance_sheet_data.append(f"\nPro plátce {payer} jsou záznamy:")
        # zaplaceno daným platičem
        payed = 0
        # pro každý záznam v databázi
        for row in data:
            # pokud je záznam pro konkrétního platiče separuj hodnoty
            # a vypiš formatovanou radku
            if row["payer"] == payer:
                num = row["num"]
                date = row["date_time"]
                subject = row["subject"]
                amount = row["amount"]
                currency = row["currency"]
                normativni_cena = row["norm_amount"]
                # odil_ceny = round(normativni_cena/num_payers,2)
                # vypiš řádku
                formated_row = f"|{num:<5}" \
                    f"| {date:<16}" \
                    f"| {subject:<40}"\
                    f"| {amount:>8} "\
                    f"| {currency:<4}"\
                    f"| {normativni_cena:>8}"
                # zapiš řádku do balance sheetu pro uložení do souboru
                balance_sheet_data.append(formated_row)
                # výpočet celkových zaplacených nákladů daným platičem
                payed += normativni_cena
                # výpočet celkových nákladů
                total_expense += normativni_cena
            # definice tabulky výdajů- platič : jeho výdaje
            sumary_data[payer] = round(payed, 2)
    # zaokrouhlení celkových výdajů
    total_expense = round(total_expense, 2)

    # výpis balance sheet tabulky
    for row in balance_sheet_data:
        print(row)
    print("\n")

    # výpis souhrnné tabulky zaplacených nákladů a přepočtu
    print("Souhrn")
    num_payer = 1
    # výpis pro každého platiče v sumáři
    for key, value in sumary_data.items():
        # dopočtení rozdílu kolik měl zaplatit - kolik zapplatil
        rozdil = round(total_expense/num_payers-value, 2)
        # pokud měl zaplatit více musí doplácet
        if rozdil >= 0:
            message = "musí doplatit"
        # pokud zaplatil více, musí mu být doplaceno
        else:
            message = "musí mu být doplaceno"
        # zformátování řádky
        formated_row = f"|{num_payer:<5}"\
            f"| {key:<16}" \
            f"| {message:<40}"\
            f"| {abs(rozdil):>8} "\
            f"| CZK"

        # uložení řádky do výstupních dat
        final_table.append(formated_row)
        # výpis na obrazovku
        print(formated_row)
        # označení dalšího člena
        num_payer += 1

    # doprovodná zpráva
    final_message = f"Celkem se utratilo {total_expense} CZK"
    print(final_message)
    # uložení doprovodné zprávy
    final_table.append(final_message)
    # export 2 tabulek - Balance sheetu a souhrnné tabulky
    return [balance_sheet_data, final_table]


def get_list_payers(data):
    '''
    nalezení seznamu všech platičů
    Parameters:
        list data
    Returns:
        list list_payers
    '''
    list_payers = []
    # výpis všech platičů ve všech záznamech do listu
    for row in data:
        list_payers.append(row["payer"])
    # ošetření duplikátů - set získám jedinečný seznam platičů
    list_payers = list(set(list_payers))
    # výstup setříděný podle abecedy
    return sorted(list_payers)


# Funkce pro uložení Balance Sheetu, a výsledného rozpočtu

def save_balance_sheet(balance_sheet_data, final_table):
    '''
    zápis balance sheetu a finálního rozpočtu do souboru
    tak jak byl naposledy zobrazen na obrazovce / naposledy editován
    Parameters:
        list [balance_sheet_data, final_table]
    Returns:
        file output_data.csv
    '''
    # otevření souboru pro zápis
    with open("output_data.csv", "w", encoding="utf-8", newline="") as output_file:
        writer = csv.writer(output_file)
        # výpis balance sheetu do souboru po řádcích
        for row in balance_sheet_data:
            writer.writerow([row])
        # oddělení
        writer.writerow("")
        # výpis final table do souboru po řádcích
        for row in final_table:
            writer.writerow([row])


# Seznam konstant

CSV_FIELD_NAME = ["date_time", "payer", "subject", "amount", "currency"]
EXCHANGE_E_CZK = 24.7
EXCHANGE_TL_CZK = 0.7

MAIN_MENU = {
    0: "Exit",
    1: "Načtení vtupního souboru input_data.csv",
    2: "Editace záznamů",
    3: "Vytvoření/ zobrazení balance sheetu, výsledného rozpočtu",
    4: "Uložení balance sheetu, výsledného rozpočtu",
    }

EDIT_MENU = {
    0: "Exit do hlavního menu",
    1: "Odebrání stávajícího člena",
    2: "Přidání platby",
    3: "Odebrání platby",
    }


# Hlavní běh programu

print("Vítejte v programu shared Pays")
print("Tento program slouží k přepočtu sdílených nákladů"
      " na společný projekt/ výlet více účastníků a rovnému vyrovnání mezi"
      " nimi")
main_function_decision()
print("Program byl řádně ukončen užiatelem")
