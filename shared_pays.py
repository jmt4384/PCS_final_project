import csv

def select_main_function():
    '''
    základní rozhodování programu - výběr funkce
    výstupem bude menu - tj. číslo, kter definuje jaká funkce programu bude volána
    '''
    while True:
        menu=input("Pro výběr funkce zvol číslo: 1234\n")
        try:
            int(menu)
            if int(menu) in nabidka_menu.keys():
                menu=int(menu)
                break
        except:
            print("zvolil si nepovolený znak, povelené jsou pouze čísla 1234")
    return menu

def select_edit_function():
    for key, value in editace_zaznamu.items():
        print(f"zvol možnost {key} pro provedení funkce {value}")
    while True:
        menu=input("Pro výběr funkce zvol číslo: 12345\n")
        try:
            int(menu)
            if int(menu) in nabidka_menu.keys():
                menu=int(menu)
                break
        except:
            print("zvolil si nepovolený znak, povelené jsou pouze čísla 1234")
    return menu

        
def import_input_file():
    '''
    načtení vtupního souboru databáze
    vstupní parametr cesta k souboru
        funkce musí provést ověření, setřídění, normalizaci
    výstupem budou data v paměti "živý obraz databáze"
    vstupní soubor bude přepsán normalizovanými daty
    '''
    data=[]
    try:
        with open("input_data.csv","r") as input_file:
            print("soubor importován")
            reader=csv.DictReader(input_file, delimiter=',',fieldnames=CSV_FIELD_NAME)
            count=1
            for radek in reader:
                count+=1
                normalised_row=normalise_pay_data(radek)
                #normalizace, osekání řádků a úprava textů, def měna = CZK
                
                #validace záznamu - musí být vždy alespoň kdo platil a kolik
                #jinak je řádek přeskočen
                if not validate_row(normalised_row):
                    print(f"chybný záznam č. {count} přeskočen")
                    continue
                if normalised_row["currency"]=="CZK":
                    norm_amount=normalised_row["currency"]
                if normalised_row["currency"]=="EUR":
                    norm_amount=exchange_eur(normalised_row["currency"])
                if normalised_row["currency"]=="TL":
                    norm_amount=exchange_tl(normalised_row["currency"])                        
                radek.append(norm_amount)
                data.append(radek)
        print(data)
        print("vstupní soubor je řádně upraven, připraveno k přepsání vstupu")
        #rewrite_input_file()
    except:
        print("vstupní soubor nenalezen")
        return None

def normalise_pay_data(pay_data):
    '''osekání polí, která nepotřebuji'''
    pay_data_str={key:str(value) for key,value in pay_data.items() if key in CSV_FIELD_NAME}
    ''''doplnění polí do plné délky'''
    normalised_data={
        "date_time":pay_data_str["date_time"].strip() if pay_data_str.get("date_time") else "nevyplněno",
        "payer":pay_data_str["payer"].strip().capitalize() if pay_data_str.get("payer") else "nevyplněno",
        "subject":pay_data_str["subject"].strip() if pay_data_str.get("subject") else "nevyplněno",
        "amount":pay_data_str["amount"].strip() if pay_data_str.get("amount") else "nevyplněno",
        "currency":pay_data_str["currency"].strip() if pay_data_str.get("currency") else "CZK",
        }
    return normalised_data
def validate_row(row):
    if row["payer"]=="" or row["amount"]=="":
        return False
    return True
def exchange_eur(eur):
    return EXCHANGE_E_CZK*eur
def exchange_tl(tl):
    return EXCHANGE_TL_CZK*tl    
def rewrite_input_file():
    '''
    funkce na přepsání vstupního souboru vyčištěnými normalizovanými daty
    '''
def create_balance_sheet():
    '''
    vytvoření balance sheetu
    možnosti zobrazení: setříděné podle času zadání/ podle osob
    zobrazení na obrazovku
    možnost: 
        výstup do souboru --- volání funkce 3
        volba pokud nesouhlasíš, volej funkci "editace záznamů"
    '''
    print("tady bude vytvořen balance sheet")
def add_new_member():
    '''
    funkce přidá nového člena do živé databáze plus jeho platby
    možnost --- aktualizuj balance sheet
    '''
def remove_member():
    '''
    funkce odebere člena a všechny jeho platby
    možnost --- aktualizuj balance sheet
    '''
def add_pay():
    '''
    funkce přidá záznam do živých načtených dat
    možnost --- aktualizuj balance sheet
    '''
def remove_pay():
    '''
    funkce odebere záznam z živých načtených dat
    možnost --- aktualizuj balance sheet
    '''
def edit_pay():
    '''
    funkce umožní editaci 1 řádku živých dat
    možnost --- aktualizuj balance sheet
    '''
def save_balance_sheet():
    '''
    po výstupu na obrazovce ... uložení balance sheetu do souboru č.2
    '''
'''konstanty'''
CSV_FIELD_NAME=["date_time", "payer","subject", "amount", "currency"]
CURRENCY="CZK"
EXCHANGE_E_CZK=24.7
EXCHANGE_TL_CZK=0.7

'''
hlavní menu projektu
'''
#tohle jsou dostupné funkce
'''možnost doplnit - vytvoření vstupního souboru, '''

nabidka_menu={
    1:"načtení vtupního souboru databáze",
    2:"vytvoření balance sheetu",
    3:"editace záznamů",
    4:"uložení balance sheetu a přepsání vstupního souboru normalizovanými daty",
    }
editace_zaznamu={
    1:"přidání nového člena",
    2:"odebrání stávajícího člena",
    3:"přidání platby",
    4:"editace jedné platby",
    5:"odebrání platby",
    }

#uvítání
print('''Vítejte v programu "shared Pays"\n''')

print("Tento program slouží k přepočtu sdílených nákladů" 
"na společný projekt/ výlet více účastníků a rovnému vyrovnání mezi nimi\n")

#zobrazení uživateli hlavního menu a jeho výběr požadované funkce
print("v hlavní nabídce jsou dostupné tyto možnosti")

for key, value in nabidka_menu.items():  
    print(f"zvol možnost {key} pro provedení funkce {value}")

#print(nabidka_menu.keys())
#print(1 in nabidka_menu.keys())
menu=select_main_function()
print(f"zvolil sis funkci {menu}, tj funkci {nabidka_menu[menu]}")

if menu==1:                 #načtení vstupního souboru
    import_input_file()
    print("data byla importována, nyní bude vytvořen balance sheet")
    menu=2

if menu==2:                 #vytvoření balance sheetu
    create_balance_sheet()

if menu==3:                 #editace záznamů
    menu=select_edit_function()
    if menu==1:
        add_new_member()
    if menu==2:
        remove_member()
    if menu==3:
        add_pay()
    if menu==4:
        edit_pay()
    if menu==5:
        remove_pay()

if menu==4:                 #uložení balance sheetu
    save_balance_sheet()





    


