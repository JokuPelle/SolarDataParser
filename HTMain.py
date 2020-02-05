######################################################################
# Päivämäärä: 13.11.2018
# Tiedosto: HTMain.py
######################################################################

##-------------------------------------HARJOITUSTYÖ----------------------------
import HTLib #oma moduuliohjelma
import sys
import datetime
##--------------------------------------PÄÄOHJELMA-----------------------------
while True:
    print("Anna haluamasi toiminnon numero seuraavasta valikosta:\n1) Lue sähköntuotantotiedot\n2) Analysoi päivätuotanto\n3) Tallenna päivätuotanto\n4) Analysoi kuukausituotanto\n5) Analysoi tuntituotanto\n6) Tallenna kuukausituotanto\n7) Tallenna tuntituotanto\n0) Lopeta")
    try:
        valinta = int(input("Valintasi: ")) ##Pyydetään valinta, jos ei ole numero, ValueError ja kysytään uudestaan
    except ValueError:
        print("Syöte ei kelpaa.\n")
        continue
    if valinta == 0: #LOPETA: Ohjelma sammuu
        print("Kiitos ohjelman käytöstä.")
        break
    
    elif valinta == 1: #LUE TIEDOSTO
        try:                                                    ##Tarkistetaan annettu vuosiluku
            file_name = input("Anna luettavan tiedoston nimi: ")
            file_year = int(input("Anna analysoitava vuosi: "))
        except ValueError:                                      ##Jos vuosi ei ole numero
            print("Vuosiluku ei kelpaa, lopetetaan.")
            sys.exit()
        else:
            biglista = HTLib.valinta_1(file_name, file_year)    ##Luodaan tiedostosta lista olioita (biglista)
            
    elif valinta == 2: #ANALYSOI PÄIVÄT
        try:                                                    ##Tarkistetaan biglistan olemassaolo
            biglista
            biglista[0]
        except (NameError, IndexError):
            print("Lue ensin tiedosto.\n")
            continue
        daysummat = HTLib.valinta_2(biglista)                   ##Luodaan "daysummat" lista biglistasta
        
    elif valinta == 3: #TALLENNA PÄIVÄT
        try:                                                    ##Tarkista daysummat-lista
            daysummat
        except (NameError):
            print("Analysoi ensin päivätuotanto.\n")
            continue
        HTLib.valinta_3(file_year, daysummat)
        
    elif valinta == 4: #ANALYSOI KUUKAUDET
        try:                                                    ##Tarkistetaan biglistan olemassaolo
            biglista
            biglista[0]
        except (NameError, IndexError):
            print("Lue ensin tiedosto.\n")
            continue
        monthsummat = HTLib.valinta_4(biglista)                 ##Luodaan "monthsummat" lista biglistasta
        
    elif valinta == 5: #ANALYSOI TUNNIT
        try:                                                    ##Tarkistetaan biglistan olemassaolo
            biglista
            biglista[0]
        except (NameError, IndexError):
            print("Lue ensin tiedosto.\n")
            continue
        hoursummat = HTLib.valinta_5(biglista)                  ##Luodaan "hoursummat" lista biglistasta
        
    elif valinta == 6: #TALLENNA KUUKAUDET
        try:                                                    ##Tarkista monthsummat-lista
            monthsummat
        except (NameError):
            print("Analysoi ensin kuukausituotanto.\n")
            continue
        HTLib.valinta_6(file_year, monthsummat)
        
    elif valinta == 7: #TALLENNA TUNTI
        try:                                                    ##Tarkista hoursummat-lista
            hoursummat
        except (NameError):
            print("Analysoi ensin tuntituotanto.\n")
            continue
        HTLib.valinta_7(file_year, hoursummat)
    else: #Jos valinta joku muu numero
        print("Syöte ei kelpaa.\n")
