import sys

from klasy_pomocnicze import *

#jesli chcemy zmienic nazwe w polu na taka ze spacja to nalezy uzyc np. 1,1,"nowa nazwa" (pierwszy wiersz pierwsza kolumna)
if sys.argv[1]:
  plik_bazowy = PlikBazowy(sys.argv) #plik bazowy użyty dla funkcji is'owych do if'ów

  #obsluga wejscia csv
  if plik_bazowy.isCsv():
    plik_csv = PlikCsv(sys.argv)
    #odczyt pliku
    plik_csv.odczyt()
    #edycja pliku
    plik_csv.edytujXY()
    #zapis pliku
    plik_csv.zapisz()

  #obsluga wejscia pkl
  elif plik_bazowy.isPkl():
    plik_pkl = PlikPkl(sys.argv)
    #odczyt pliku
    plik_pkl.odczyt()
    #edycja pliku
    plik_pkl.edytujXY()
    #zapis pliku
    plik_pkl.zapisz()

  #obsluga wejscia json
  elif plik_bazowy.isJSON():
    plik_json = PlikJson(sys.argv)
    #odczyt pliku
    plik_json.odczyt()
    #edycja pliku
    plik_json.edytujXY()
    #zapis pliku
    plik_json.zapisz()

  else:
    print('Podano błędną nazwę pliku wejściowego')