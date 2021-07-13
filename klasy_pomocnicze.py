import pandas
import json
import os
import sys
class Operacja: #y=0 to headery
  def __init__(self, operacje):
    self.arr = operacje.split(',')
    self.wiersz = int(self.arr[0]) # tu nie trzeba -1 bo naglowki maja id 0
    self.kolumna = int(self.arr[1])-1 #latwiejsze uzywanie kolumn
    self.nowe_dane = self.arr[2].replace('"', '') #usuniecie "" z nazwy w przypadku uzycia spacji

  def debug(self):
    print('Wiersz: {} Kolumna: {} Dane: {}'.format(self.wiersz, self.kolumna, self.nowe_dane))

class PlikBazowy:
  def __init__(self, argv):
    self.nazwa_pliku = argv[1]
    self.nazwa_nowego_pliku = argv[2]
    self.nazwy_kolumn = []
    self.operacje = []
    for op in argv[3:]: #załadowanie operacji z argv
      self.operacje.append(Operacja(op))
    self.plik_dataframe = None

  def edytujXY(self): #y=wiersz x=kolumna
    iter = 1
    if not self.plik_dataframe.empty: #data_frame nie może być pusty
      for operacja in self.operacje:
        #operacja.debug()
        try:
          if operacja.wiersz == 0:
              print('Podano błędny numer wiersza w operacji {} dane w tych komórkach nie uległy zmianie'.format(iter))
          self.plik_dataframe.at[operacja.wiersz, self.nazwy_kolumn[operacja.kolumna]] = operacja.nowe_dane
        except ValueError:
          print('Podano błędny typ danych w operacji: {} dane w tych komórkach nie uległy zmianie'.format(iter))
        iter+=1
    else:
      print('Nie można edytować nie załadowanego pliku')
      sys.exit(1)

  def zapisz(self):
    if not self.plik_dataframe.empty: #data_frame nie może być pusty
      #ustalenie typu pliku wyjsciowego aby funkcja zapisz była wspólna dla wszystkich typów co ułatwi konwersje
      #CSV
      if self.nazwa_nowego_pliku.endswith('.csv'):
        self.plik_dataframe.to_csv(self.nazwa_nowego_pliku, index=False)
      #PICKLE
      elif self.nazwa_nowego_pliku.endswith('.pkl'):
        self.plik_dataframe.to_pickle(self.nazwa_nowego_pliku)
      #JSON
      elif self.nazwa_nowego_pliku.endswith('.json'):
        with open(self.nazwa_nowego_pliku, 'w', encoding='utf-8') as f:
          do_zapisu = json.loads(self.plik_dataframe.to_json(orient="index"))
          json.dump(do_zapisu, f, ensure_ascii=False, indent=4)
      else:
        print('Podano błędną nazwę pliku wyjsciowego')
    else:
      print('Nie można zapisać nie załadowanego pliku')
      sys.exit(1)

  def isCsv(self):
    return self.nazwa_pliku.endswith('.csv')

  def isPickle(self):
    return self.nazwa_pliku.endswith('.pkl')
  
  def isJson(self):
    return self.nazwa_pliku.endswith('.json')

class PlikCsv(PlikBazowy):
  def odczyt(self):
    try:
      data_frame = pandas.read_csv(self.nazwa_pliku) #utworzenie data frame z pliku csv
      data_frame.index += 1 #ladniejsze wyswietlanie z indexowaniem od 1
      for col in data_frame.columns:
        self.nazwy_kolumn.append(col) #przepisanie nazw naglowkow do nowej tablicy
      print(data_frame) #wypisanie pliku przed modyfikacja
      self.plik_dataframe = data_frame
    except FileNotFoundError:
      print('Nie znaleziono pliku, czy chodziło ci o:')
      directory = os.path.dirname(os.path.realpath(__file__))
      for filename in os.listdir(directory):
        if filename.endswith('.csv'): 
            print(filename)
      sys.exit(1)

class PlikPkl(PlikBazowy):
  def odczyt(self):
    try:
      data_frame = pandas.read_pickle(self.nazwa_pliku) #utworzenie data frame z pliku csv
      for col in data_frame.columns:
        self.nazwy_kolumn.append(col) #przepisanie nazw naglowkow do nowej tablicy
      print(data_frame) #wypisanie pliku przed modyfikacja
      self.plik_dataframe = data_frame
    except FileNotFoundError:
      print('Nie znaleziono pliku, czy chodziło ci o:')
      directory = os.path.dirname(os.path.realpath(__file__))
      for filename in os.listdir(directory):
        if filename.endswith('.pkl'): 
            print(filename)
      sys.exit(1)

class PlikJson(PlikBazowy):
  def odczyt(self):
    try:
      data_frame = pandas.read_json(self.nazwa_pliku, orient="index") #utworzenie data frame z pliku csv
      for col in data_frame.columns:
        self.nazwy_kolumn.append(col) #przepisanie nazw naglowkow do nowej tablicy
      print(data_frame) #wypisanie pliku przed modyfikacja
      self.plik_dataframe = data_frame
    except FileNotFoundError:
      print('Nie znaleziono pliku, czy chodziło ci o:')
      directory = os.path.dirname(os.path.realpath(__file__))
      for filename in os.listdir(directory):
        if filename.endswith('.json'): 
            print(filename)
      sys.exit(1)