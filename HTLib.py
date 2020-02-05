######################################################################
# Päivämäärä: 13.11.2018
# Tiedosto: HTLib.py
######################################################################

#HARJOITUSTYÖN ALIOHJELMA-MODUULI
import sys
import datetime

##biglistan olioita varten
class Data:
    date = ""
    power = 0

## Tekee annetusta päivämäärästä ja summasta olion (class Data)
def rivitieto(paiva, maara):
    data = Data()
    data.date = paiva
    data.power = maara
    return data

##daysummat ja monthsummat-listojen olioita varten
class dayData:
    date = ""
    power = 0
    total = 0

## Tekee annetusta päivästä/kuukaudesta, tuloksien summasta, ja kumulatiivisesta summasta olion (class dayData)
def daytuotto(paiva, maara, total):
    data = dayData()
    data.date = paiva
    data.power = maara
    data.total = total
    return data

## Lukee halutun tiedoston ja vuoden, muuttaa jokaisen rivin ajan ja tuottosumman data-olioon ja lisää biglistaan
def valinta_1(file_name, file_year):
    biglista = []
    try:
        tiedosto = open("{0}".format(file_name), "r")
    except IOError: #Jos tiedostoa ei löydy
        print("Tiedoston '{0}' lukeminen epäonnistui, ei löydy, lopetetaan.".format(file_name))
        sys.exit()
    else:
        rivi = tiedosto.readline()
        lines_read = 1
        lines_analyzed = 0
        ##Yhdelle tiedoston riville tehtävät asiat:
        while True:
            luvut = tiedosto.readline().replace(";\n", '').split(';')
            if len(luvut[0]) <= 0:                  #kun rivin eka kohta on tyhjä, lopetetaan
                break
            elif str(file_year) not in luvut[0]:    ##Jos luvut-listan eka osa ei ole oikealta vuodelta, skip
                lines_read = lines_read + 1         ##Lasketaan yhä luetuksi riviksi (voi ehkä joutua poistamaan!)
                continue
            for (x, kohta) in enumerate(luvut):     ##Jos kohta on pelkkä "-" niin muutetaan nollaksi
                if kohta == '-':
                    luvut[x] = 0
            lines_read = lines_read + 1
            lines_analyzed = lines_analyzed + 1
        ##day on päivämäärä(datetime) ja power on tuotto. Jos tuotto alle 0 niin muutetaan 0:ksi               
            day = datetime.datetime.strptime(luvut[0], '%Y-%m-%d %H:%M:%S')
            power = float(luvut[1]) + float(luvut[2]) + float(luvut[3]) + float(luvut[4]) + float(luvut[5]) + float(luvut[6]) + float(luvut[7])
            if power < 0:
                power = 0
        ##lisätään biglistalle jokaisesta ajasta ja powerista tehty luokka
            biglista.append(rivitieto(day, power))
        print("Tiedosto '{0}' luettu, {1} riviä, {2} otettu analysoitavaksi.".format(file_name, lines_read, lines_analyzed))
        tiedosto.close()
        try: ##Jos on analysoitu 0 riviä tai ei mitään, ei näytetä analysoitua aikaväliä
            biglista
            biglista[0]
            print("Analysoidaan {0} ja {1} välistä dataa.\n".format(datetime.datetime.strftime(biglista[0].date, '%d.%m.%Y %H:%M'), datetime.datetime.strftime(biglista[-1].date, '%d.%m.%Y %H:%M')))
        except (NameError, IndexError):
            print()
        return biglista

## Analysoi päivätuotanto: (luo daysummat-lista)
def valinta_2(biglista):
    day = 0     #alkuperäinen päivä
    kumulativ = 0
    daysummat = []
    for x in biglista:
        newday = datetime.date.strftime(x.date, '%#d.%#m.%Y')   #katsotaan rivin päivä (#-merkki poistaa 0:n)
        if newday == day:   #Jos sama kuin eilinen, niin lisätään päivän yhteissummaan
            summa = summa + x.power
        else:               #Jos eri päivä kuin eilen
            if day != 0:    #lisätään daysummat-listaan olio, jossa päivä, kertynyt tuotto ja kertynyt kumulatiivinen tuotto
                kumulativ = kumulativ + summa #lasketaan kumulatiivinen summa joka päivän lopussa. JOSTAIN SYYSTÄ JOKA RIVIN LAKSEMINEN YHTEEN EI TUOTA OIKEAA TULOSTA
                daysummat.append(daytuotto(day, summa, kumulativ))
            day = newday    #päivä vaihtuu
            summa = x.power #tuotto "nollataan"
    ##HUOM! Koska listan lopussa päivä ei enää muutu, pitää viimeinen päivä, summa ja kumulatiivisuus lisätä erikseen
    daysummat.append(daytuotto(day, summa, kumulativ + summa))
    print("Päivätuotanto analysoitu.\n")
    return daysummat

## Tallenna päivätuotanto:
def valinta_3(file_year, daysummat):
    while True:
        try:
            savefile = open('tulosPaiva{0}.csv'.format(file_year), 'w')
        except IOError:
            print("Tiedoston tallentaminen epäonnistui, lopetetaan")
            sys.exit()
        break
    ##Kirjoitetaan tiedosto (vuosiluku vielä korjattava)
    savefile.write("Päivittäinen sähköntuotanto:\n;{0}".format(file_year))
    for x in daysummat:
        savefile.write("\n{0};{1}".format(x.date, int(x.power)))
    savefile.write("\n\n\nKumulatiivinen päivittäinen sähköntuotanto:\n;{0}".format(file_year))
    for x in daysummat:
        savefile.write("\n{0};{1}".format(x.date, int(x.total)))
    savefile.write("\n\n\n")
    print("Päivätuotanto tallennettu tiedostoon 'tulosPaiva{0}.csv'.\n".format(file_year))
    savefile.close()

## Analysoi kuukausituotanto: (toimii samalla lailla kuin valinta_2, eli luo monthsummat-listan)
def valinta_4(biglista):
    month = 0   #alkuperäinen kuukausi
    kumulativ = 0
    monthsummat = []
    for x in biglista:
        newmonth = datetime.date.strftime(x.date, '%m/%Y')  #katsotaan rivin kuukausi
        if newmonth == month:
            summa = summa + x.power
        else:
            if month != 0:
                monthsummat.append(daytuotto(month, summa, kumulativ))
            #print(newmonth, "eri päivä", month)
            month = newmonth
            summa = x.power
        kumulativ = kumulativ + x.power
    ##HUOM! Koska listan lopussa kuukausi ei enää muutu, pitää viimeinen kuukausi, summa ja kumulatiivisuus lisätä erikseen
    monthsummat.append(daytuotto(month, summa, kumulativ))
    #print(newmonth, month, summa, kumulativ)
    print("Kuukausituotanto analysoitu.\n")
    return monthsummat

## Tallenna kuukausituotanto:
def valinta_6(file_year, monthsummat):
    while True:
        try:
            savefile = open('tulosKuukausi{0}.csv'.format(file_year), 'w')
        except IOError:
            print("Tiedoston tallentaminen epäonnistui, lopetetaan")
            sys.exit()
        break
    ##Kirjoitetaan tiedosto
    savefile.write("Kuukausittainen sähköntuotanto:\n;{0};%-osuus\n".format(file_year))
    for x in monthsummat:
        osuus = int(x.power / monthsummat[11].total * 100)
        savefile.write(" {0};{1};{2}%\n".format(x.date, int(x.power), osuus))
    savefile.write("Yhteensä;{0}\n\n\n".format(int(monthsummat[11].total)))
    print("Kuukausituotanto tallennettu tiedostoon 'tulosKuukausi{0}.csv'.\n".format(file_year))
    savefile.close()

## Tehdään tyhjä tuntitaulukko, jossa 12 riviä ja 24 saraketta (valinta_5 käyttää tätä)
def hourtuotto():
    tunnit = []
    for x in range(12):
        x = []
        tunnit.append(x)
        for i in range(24):
            i = []
            x.append(0)
    return tunnit

## Analysoi tuntituotanto: (luo hoursummat-taulukko)
def valinta_5(biglista):
    hoursummat = hourtuotto() #Tehdään tyhjä taulukko
    for x in biglista:
        hour = int(datetime.datetime.strftime(x.date, '%#H')) #katsotaan tunti ja muutetaan int
        month = int(datetime.date.strftime(x.date, '%#m')) - 1 #katsotaan kuukausi, muutetaan int ja -1
        hoursummat[month][hour] = hoursummat[month][hour] + x.power #päivitetään summa oikeasta kohtaa kuukausi(12)xtunti(24) taulukosta
    print("Tuntituotanto analysoitu.\n")
    return hoursummat

## Lasketaan tietyn tunnin yhteistuotto, x=haluttu tunti, jolloin jokaisen kuukauden(i) x-kohta lasketaan yhteen
def houryht(x, hoursummat):
    tulos = 0
    for i in hoursummat:
        tulos = tulos + i[x]
    return tulos

## Tallenna tuntituotanto:
def valinta_7(file_year, hoursummat):
    while True:
        try:
            savefile = open('tulosTunti{0}.csv'.format(file_year), 'w')
        except IOError:
            print("Tiedoston tallentaminen epäonnistui, lopetetaan")
            sys.exit()
        break
    ##Kirjoitetaan tiedosto
    savefile.write("Tuntipohjainen sähköntuotanto:\n;0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23\n")
    kuukausi = 0
    for x in hoursummat: #Tuotetaan kuukaudet listan eteen
        kuukausi = kuukausi + 1
        month = datetime.date(file_year, kuukausi, 1).strftime('%m/%Y')
        text = ';'.join(str(int(y)) for y in x)
        savefile.write(" {0};{1}\n".format(month, text))
    tuntien_summa = []
    tuntien_summa_osuus = []
    kumulativ = 0
    for x in range(24): #Lasketaan jokaisen tunnin summa ja kumulatiivinen summa
        tuntien_summa.append(houryht(x,hoursummat))
        kumulativ = kumulativ + houryht(x,hoursummat)
    for x in range(24): #Lasketaan jokaisen tunnin osuus kumulatiivisesta summasta
        tuntien_summa_osuus.append(houryht(x,hoursummat) / kumulativ * 100)
    text = ';'.join(str(int(y)) for y in tuntien_summa)
    savefile.write("Yhteensä;{0}\n\n\n".format(text))
    savefile.write("Yksittäisen tunnin osuus vuosittaisesta sähköntuotannosta:\n;0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23\n")
    text = ';'.join(str(int(y)) + '%' for y in tuntien_summa_osuus)
    savefile.write("%-osuus;{0}\n\n\n".format(text))
    print("Tuntituotanto tallennettu tiedostoon 'tulosTunti{0}.csv'.\n".format(file_year))
    savefile.close()
