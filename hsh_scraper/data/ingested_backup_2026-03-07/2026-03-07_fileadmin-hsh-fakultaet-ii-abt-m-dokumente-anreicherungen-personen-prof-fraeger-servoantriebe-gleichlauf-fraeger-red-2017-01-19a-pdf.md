---
source_url: "https://www.hs-hannover.de/fileadmin/HsH/Fakultaet_II/Abt_M/Dokumente/Anreicherungen_Personen/Prof._Fraeger/Servoantriebe-Gleichlauf-Fraeger-red-2017-01-19a.pdf"
title: "Servoantriebe-Gleichlauf-Fraeger-red-2017-01-19a"
crawl_date: "2026-03-07"
content_type: "pdf"
---

## **Einfluss von Spannungsoberschwingungen und** **Rastmomenten auf den Gleichlauf von Servoantrieben** **mit Permanentmagnet-Synchronmotoren**

### **_Influence of voltage harmonics and cogging torque on speed_** **_deviations of servo drives with permanent magnet_** **_synchronous motors._**

**Prof. Dr.-Ing. Carsten Fräger**
**Hochschule Hannover**
**Mechatronik – Elektrische Antriebe**


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 1


# **Inhalt**


  - Anwendung von Servoantrieben,
Bedeutung des Gleichlaufs für die
Anwendung von Servoantrieben


  - Aufbau Servoantriebe, Ursachen des
Rastmoments und der Oberschwingungen,
Regelung der Antriebe


  - Auswirkungen der Rastmomente und
Oberschwingungen an einem konkreten
Beispiel


Rastmomentverlauf



Farbsäume bei
Mehrfarbendruck



**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 2


# **Servoantriebe**

**Elektronisch geregelte Antriebe (Motor + Elektronik)**
Stromregelung
Drehzahlregelung (bzw. Geschwindigkeitsregelung)
Winkelregelung (bzw. Lageregelung)
Sollwertgenerierung
**Hohe Qualität der Bewegung**
Hohe Dynamik
Weite Stellbereiche Drehzahl und Drehmoment
Hohe Genauigkeit von Drehzahl und Winkel
**Anwendung in automatischen Produktionsmaschinen**
Roboter
Werkzeugmaschinen
Handhabungsmaschinen
Druckmaschinen


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 3


# **Gleichlauf von Servoantrieben**

 Servoantriebe dienen für präzise
Bewegungen

 Drehmomentschwankungen führen zu
Drehzahl- und Winkelfehlern der
Motorbewegung

 Qualitätsmängel im Produkt, z.B.

 **Farbsäume** beim Mehrfarbendruck bei
Druckmaschinen

 **Bahnabweichungen** bei Brenn- u.
Laserschneidmaschinen

 **Formabweichungen** bei
Werkzeugmaschinen


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 4


# **Schematischer Aufbau PM-Servomotor**

**Rotor**


 Stator mit 3-strängiger **Wicklung in Nuten** (verteilte Wicklung
oder Zahnspulenwicklung, hier verteilte Wicklung)
 Rotor mit **Oberflächenmagneten**
 Magnete führen mit den Statornuten zu **Rastmomenten** :
winkelabhängige Drehmomentschwankungen, unabhängig vom
Statorstrom
 Oberfelder der Magnete induzieren in der Statorwicklung
Spannungen, die mit dem Statorstrom zu
**Drehmomentschwankungen** führen


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 7


# **Drehzahlregelung, Winkelregelung Antriebe**

Aktueller Strom und aktuelle Drehzahl werden am Motor gemessen
 Regelung wirkt Abweichungen/Drehmomentschwankungen entgegen



_n_
soll



Drehzahl- Strom- FU PWM Motor,























**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 8


# **Analyse Gleichlaufverhalten - Antriebsdaten**

Simulation des Antriebs aus

           - **Leistungselektronik**

           - **Permanentmagnet Servomotor**

           - **Strom- und Drehzahlregelung**



Beispielmotor:
SynchronServomotor mit
Oberflächenmagneten



_P_
N = 1,1 kW
_n_
N = 3800 min [-1]

_I_ _I_
N = 2,3 A, max = 10,0 A
_f_
N = 190 Hz
_U_
N = 330 V
_p_ = 3, 2 _p_ = 6
_M_ _M_
N = 2,8 Nm, max = 11,6 Nm
_k_ = 241 mm, _a_ = 103 mm
_m_ = 5,3 kg, _J_ = 0,00012 kgm [2]



**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 9


# **Stromreglereinstellung für beste Sprungantwort**

Motor ohne
Rastmoment
und
Oberschwingungen


Stromregler:
bestes
Verhalten bei
_K_
pi = 30 V/A
_T_
ni = 2 ms


Totzeit:
_T_
deli = 0,25 ms


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 10


# **Drehzahlreglereinstellung für beste** **Sprungantwort (1)**

Motor ohne
Rastmoment und
Oberschwingungen


Drehzahlregler:
bestes Verhalten
bei
_K_
_T_
nn = 40 ms
(rote Kurve)


Totzeiten:
_T_
deln = 0,25 ms
_T_
dels = 0,25 ms


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 11


# **Drehzahlreglereinstellung für beste** **Sprungantwort (2)**

Drehzahlregler:
bestes Verhalten
bei
_K_
pn = 0,019 Amin
_T_
nn = 40 ms


Verhalten
weitgehend
unabhängig von
der Drehzahl.


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 12


# **Einfluss** **Rastmoment** **auf die** **Drehzahl-** **Abweichung** **(1)**



Sollwertsprung von 0 auf 100 min-1 [-1], 2%

**Sollwertsprung von 0 auf** 25 **00 min** [-1] **, 2%**

Rastmoment, 100ms, Drehzahl hat
_r_ = 18

**Rastmoment, 1** 50 **0ms, Drehzahl hat**

bleibende Schwankungen



Sollwertsprung von 0 auf 100 min-1 [-1], 2%

**Sollwertsprung von 0 auf** 25 **00 min** [-1] **, 2%**

Rastmoment, 100ms, Drehzahl hat

**Rastmoment, 1** 50 **0ms, Drehzahl hat**

bleibende Schwankungen

**bleibende Schwankungen**



25 **00 min** [-1] -1



50



**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 13


# **Einfluss** **Rastmoment** **auf die** **Drehzahl-** **(2)**

Die DrehzahlAbweichungen
steigen linear mit
dem
Rastmoment.


Niedrige
Periodizitäten
wirken stärker.


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 14


# **Einfluss** **Rastmoment** **auf die** **Drehzahl-** **Abweichung** **(3)**

Die DrehzahlAbweichungen
sind bei kleinen
Drehzahlen am
größten,
Abweichungen
steigen linear mit
dem Rastmoment,
niedrige
Periodizität
kritischer.


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 15


# **Einfluss Oberschwingungen auf die Drehzahl-** **Abweichung (1)**

Frequenzen:


Beschreibung mit
winkelabhängigen
Flussverkettungen:


Die Schwankungen der
Flussverkettungen führen
zu DrehmomentSchwankungen.
Der Strom entsteht auch
im Leerlauf durch die
induzierte
OberschwingungsSpannung.


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 16


# **Einfluss Oberschwingungen auf die Drehzahl-** **Abweichung (2)**





SolSo lwertsprung von 0 auf 100 min **l** wertsprung von 0 auf 500 min [-1][-1],,
Oberschwingung 5%, 7p, 20ms, Drehzahl Oberschwingung 5%, 13p, 150ms, Drehzahl
hat bleibende Schwankungenhat bleibende Schwankungen


Zeit _t_



**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 17


# **Einfluss Oberschwingungen auf die Drehzahl-**

Die DrehzahlAbweichungen
steigen linear
mit der
Spannung der
Oberschwingung.


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 18


# **Einfluss Oberschwingungen auf die Drehzahl-**

Die Drehzahl
steigen etwa
linear mit der
Drehzahl.


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 19


# **Vergleich Einfluss von Rastmoment und** **Oberschwingung**

 Bei kleinen Drehzahlen dominiert der Einfluss des
Rastmoments
 Bei hohen Drehzahlen dominiert der Einfluss der
Oberschwingungen
 Im Beispiel wird über den Drehzahlbereich ab 100min [-1] eine
relative Drehzahlschwankung von weniger als 1% erreicht
bei

###  M M

cog < 1% N

###  U U

7p < 5% p


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 20


# **Zusammenfassung**

 Rastmomente und Oberschwingungen führen zu
Drehzahlschwankungen, die vom Regler nicht vollständig
ausgeregelt werden. Der Einfluss wurde an einem konkreten Antrieb
simuliert.

 Etwa linearer Anstieg der Drehzahlschwankungen mit den
Oberschwingungen und dem Rastmoment
 Niedrige Periodizität des Rastmoments hat stärkeren Einfluss
 Bei kleinen Drehzahlen dominiert der Einfluss des Rastmoments,
bei hohen Drehzahlen dominiert der Einfluss der
Oberschwingungen.
 Im Beispiel wird über den Drehzahlbereich ab 100min [-1] eine relative
Drehzahlschwankung von weniger als 1% erreicht bei
_M_ _M_ _U_ _U_
cog < 1% N und 7p < 5% p
 Nur geringe Rastmomente und Oberschwingungen führen zu
präzisen Bewegungen.


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 21


**Prof. Dr.-Ing. Carsten Fräger**
Elektrische Antriebe - Mechatronik
Electrical Drives - Mechatronic


**IKME**
**Institut für Konstruktionselemente, Mechatronik, Elektromobilität**
Bismarckstr. 2
30173 Hannover


**Hochschule Hannover**
**University of Applied Sciences and Arts**
Fakultät II Maschinenbau und Bioverfahrenstechnik
Ricklinger Stadtweg 120
30459 Hannover


Telefon ++49 (0) 511-9296-1383
E-Mail: Carsten.Fraeger@HS-Hannover.de


**Hochschule Hannover** - Fakultät II · Elektrische Antriebe · Prof. Dr.-Ing. Carsten Fräger 22


