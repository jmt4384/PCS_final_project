import csv

def select_main_function():
    '''
    základní rozhodování programu - výběr funkce
    
    výstupem bude menu - tj. číslo, kter definuje jaká ze základních funkcí
    programu bude volána
    '''
    while True:
        #zobrazení uživateli hlavního menu a jeho výběr požadované funkce
        print("v hlavní nabídce jsou dostupné tyto možnosti")
        for key, value in nabidka_menu.items():  
            print(f"možnost: {key} funkce: {value}")
        menu=input("Pro výběr funkce zvol číslo: 01234\n")
        try:
            int(menu)
            if int(menu) in nabidka_menu.keys():
                menu=int(menu)
                print(f"zvolil si {menu}, funkci {nabidka_menu[menu]}")
                break
        except:
            print("zvolil si nepovolený znak, povelené jsou pouze čísla 01234")
    return menu

def select_edit_function():
    '''
    sekundární rozhodování programu - výběr editojící funkce funkce
    
    výstupem bude menu - tj. číslo, kter definuje jaká z editujících funkcí
    '''
    for key, value in editace_zaznamu.items():
        print(f"možnost: {key} funkce: {value}")
    while True:
        menu=input("Pro výběr funkce zvol číslo: 12345\n")
        try:
            int(menu)
            if int(menu) in nabidka_menu.keys():
                menu=int(menu)
                print(f"zvolil si {menu}, funkci {nabidka_menu[menu]}")
                break
        except:
            print("zvolil si nepovolený znak, povelené jsou pouze čísla 1234")
    return menu

def main_function_decision():
    '''
    hlavní rozhodovací smyčka, po provedení funkce, program čeká na povel
    k provedení nové funkce popř. exit
    '''
    while True:
        menu=select_main_function()
        if menu==1:                 #načtení vstupního souboru
            data=import_input_file()
            print("data byla importována, nyní může být vytvořen balance sheet")
            import_done=True
        if menu==2 and import_done:        #vytvoření balance sheetu podle lidí
            create_balance_sheet_payer(data)
        if menu==3 and import_done:         #vytvoření balance sheetu podle času
            create_balance_sheet_time(data)
        if menu==4 and import_done:         #editace záznamů
            edit_function_decision()
        if menu==5 and import_done:         #uložení balance sheetu
            save_balance_sheet()
        if menu==0:
            break
        print("----------------------")
        
def edit_function_decision():
    '''
    vedlejší rozhodovací smyčka, po provedení editovací funkce, 
    program čeká na povel k provedení další funkce popř. exit do hlavního menu
    '''
    while True:
        menu=select_edit_function()
        if menu==0:
            break
        if menu==1:
            add_new_member(data)
        if menu==2:
            remove_member(data)
        if menu==3:
            add_pay(data)
        if menu==4:
            edit_pay(data)
        if menu==5:
            remove_pay(data)
        print("----------------------")
        
def import_input_file():
    '''
    načtení vtupního souboru databáze, předpokládám, že existuje soubor
    input_data.csv - jinak vyhodí hlášku "soubor nenalezen"
    funkce provede ověření, setřídění, normalizaci dat
    
    výstupem bude dictionary "data" 
    '''
    data=[]
    try:
        with open("input_data.csv","r") as input_file:
            print("soubor importován")
            reader=csv.DictReader(input_file, delimiter=',',fieldnames=CSV_FIELD_NAME)
            count=1
            for radek in reader:
                count+=1
                #normalizace, osekání řádků a úprava textů, def měna = CZK
                normalised_row=normalise_pay_data(radek)              
                #validace záznamu - musí být vždy alespoň kdo platil a kolik
                #jinak je řádek přeskočen
                if not validate_row(normalised_row):
                    print(f"chybný záznam č. {count} přeskočen")
                    continue
                data.append(radek)
        print(data)
        print("vstupní soubor je řádně upraven")
    except:
        print("vstupní soubor nenalezen")
        return None
    return data

def normalise_pay_data(pay_data):
    '''konverze řádky ve vstupním souboru tak, aby obsahoval pouze 
    požadovaná data
    
    výstup je normalizovaná řádka
    '''
    
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
    '''
    ověření, že má řádka validní parametry kdo platil, částka
    výstup T/F - platný neplatný řádek v datech
    '''
    if row["payer"]=="" or row["amount"]=="":
        return False
    return True

def exchange_eur(eur):
    '''
    převod měny EUR na CZK
    '''
    return EXCHANGE_E_CZK*eur

def exchange_tl(tl):
    '''
    převod měny TL na CZK
    '''
    return EXCHANGE_TL_CZK*tl  
  
def norm_amount(radek):
    
    if radek["currency"]=="CZK":
        norm_amount=radek["currency"]
    elif radek["currency"]=="EUR":
        norm_amount=exchange_eur(radek["currency"])
    elif radek["currency"]=="TL":
        norm_amount=exchange_tl(radek["currency"])
    else:                 #pokud je na znaku měny něco jiného, pak jsou to CZK
        norm_amount=radek["currency"]
   
    return norm_amount

        
def rewrite_input_file():
    '''
    funkce na přepsání vstupního souboru vyčištěnými normalizovanými daty
    '''
def create_balance_sheet_payer(data):
    '''
    vytvoření balance sheetu setříděné podle podle osob
    zobrazení na obrazovku
    možnost: 
        výstup do souboru --- volání funkce 3
        volba pokud nesouhlasíš, volej funkci "editace záznamů"
    '''
    #přidání sloupečku jednotné měny
    for radek in data:
        radek["def_currency"]=norm_amount(radek)
    
    print("tady bude vytvořen balance sheet")
    print(data)
    
    
def create_balance_sheet_time():
    '''
    balancesheet setříděný podle času
    '''
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
    print("tady bude funkce pro odebrání člena party")
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
    0:"exit",
    1:"načtení vtupního souboru databáze",
    2:"vytvoření balance sheetu",
    3:"editace záznamů",
    4:"uložení balance sheetu a přepsání vstupního souboru normalizovanými daty",
    }
editace_zaznamu={
    0:"exit do hlavního menu",
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

main_function_decision()


   
print("program byl řádně ukončen užiatelem")





    


