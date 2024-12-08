from django.db import models


class StatusZamowienia(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'

class Plec(models.TextChoices):
    K = 'K', 'Kobieta'
    M = 'M', 'Mężczyzna'

class Uzytkownik(models.Model):
    login = models.CharField(max_length=30)
    haslo = models.CharField(max_length=50)
    data_zalozenia = models.DateField()

class Sklep(models.Model):
    nazwa = models.CharField(max_length=30)
    adres_email = models.EmailField(max_length=30)
    numer_telefonu = models.CharField(max_length=15)
    nip = models.CharField(max_length=10)

class Adres(models.Model):
    kraj = models.CharField(max_length=30)
    miasto = models.CharField(max_length=30)
    ulica = models.CharField(max_length=30)
    numer_budynku = models.CharField(max_length=5)
    numer_lokalu = models.CharField(max_length=4, blank=True, null=True)
    kod_pocztowy = models.CharField(max_length=6)
    sklep = models.ForeignKey(Sklep, on_delete=models.CASCADE)
    klient = models.ForeignKey('Klient', on_delete=models.CASCADE)
    pracownik = models.ForeignKey('Pracownik', on_delete=models.CASCADE)

class Klient(models.Model):
    adres_email = models.EmailField(max_length=30)
    numer_telefonu = models.CharField(max_length=15)
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=50)
    plec = models.CharField(max_length=1, choices=Plec.choices)
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    sklep = models.ForeignKey(Sklep, on_delete=models.CASCADE)

class Pracownik(models.Model):
    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=50)
    data_urodzenia = models.DateField()
    pesel = models.CharField(max_length=11)
    data_zatrudnienia = models.DateField()
    adres_email = models.EmailField(max_length=30)
    numer_telefonu = models.CharField(max_length=15)
    numer_konta = models.CharField(max_length=26, blank=True, null=True)
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    sklep = models.ForeignKey(Sklep, on_delete=models.CASCADE)

class Administrator(models.Model):
    pracownik = models.OneToOneField(Pracownik, on_delete=models.CASCADE)

class Operator(models.Model):
    pracownik = models.OneToOneField(Pracownik, on_delete=models.CASCADE)

class Produkt(models.Model):
    nazwa = models.CharField(max_length=100)
    opis = models.TextField()
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    sklad = models.IntegerField()
    sklep = models.ForeignKey(Sklep, on_delete=models.CASCADE)
    waga = models.FloatField()

class Kategoria(models.Model):
    nazwa = models.CharField(max_length=50)
    opis = models.TextField()
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)

class Producent(models.Model):
    nazwa = models.CharField(max_length=30)
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)

class Magazyn(models.Model):
    pojemnosc = models.IntegerField()
    sklep = models.ForeignKey(Sklep, on_delete=models.CASCADE)
    adres = models.ForeignKey(Adres, on_delete=models.CASCADE)

class MiejsceWMagazynie(models.Model):
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    magazyn = models.ForeignKey(Magazyn, on_delete=models.CASCADE)

class Zamowienie(models.Model):
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=StatusZamowienia.choices)
    data_zamowienia = models.DateField()
    data_wysylki = models.DateField()
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    historia = models.TextField(blank=True, null=True)

class SzczegolyZamowienia(models.Model):
    zamowienie = models.ForeignKey(Zamowienie, on_delete=models.CASCADE)
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)

