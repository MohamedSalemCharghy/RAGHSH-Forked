---
source_url: "https://f4.hs-hannover.de/fileadmin/HsH/Forms/Fakultaet_IV/StudServ/OFI/IT-Service/Anleitung_Einrichtung_eduroam__Android_HsH.pdf"
title: "Anleitung_Einrichtung_eduroam__Android_HsH"
crawl_date: "2026-03-07"
content_type: "pdf"
---

# Einrichtung der eduroam Verbindung unter Android

## **Verfahrensbeschreibung**

**Version: 1.0**

**Datum: 12.06.2019**

**Ansprechpartner: IT-Team-W (F4-W-IT-Team@hs-hannover.de)**


### **Inhaltsverzeichnis**

**1** **Einleitung ............................................................................................................................. 3**

1.1 Hinweise .................................................................................................................................. 3

**2** **Installation ........................................................................................................................... 3**

2.1 Schritt 1 – Zertifikat herunterladen ........................................................................................ 3

2.2 Schritt 2 – Zertifikat installieren .............................................................................................. 4

2.3 Schritt 3 – WLAN Einstellungen öffnen ................................................................................... 4

2.4 Schritt 4 – eduroam einrichten ............................................................................................... 5


### 1 Einleitung

eduroam (Education Roaming) stellt weltweites Wireless LAN Roaming zur Verfügung. Über eduroam
können Studierende und Mitarbeiter das WLAN nicht nur an der Hochschule Hannover,
sondern auch an anderen wissenschaftlichen Einrichtungen nutzen. Ebenso steht unseren Gästen
von anderen Hochschulen das Netzwerk eduroam zur Verfügung.

#### 1.1 Hinweise

Nützliche Links zum Thema eduroam:


Übersichtskarte zur eduroam Verbreitung in Deutschland:
[https://map.eduroam.de/leaflet/eduroam/eduroam-map.html](https://map.eduroam.de/leaflet/eduroam/eduroam-map.html)


Weltweite Karte:
[https://www.eduroam.org/where/](https://www.eduroam.org/where/)

### 2 Installation

Nachfolgend wird die Installation des „T-TeleSec GlobalRoot Class 2“ Zertifikates zur Verwendung ab
dem 19.06.2019 beschrieben. Dabei wird in Schritt 4 in A) Neuinstallation und B) Update einer
vorhandenen Installation mit dem vorher verwendetem „Deutsche Telekom Root CA 2“ Zertifikat
unterschieden.

#### 2.1 Schritt 1 – Zertifikat herunterladen

Laden Sie sich das „T-TeleSec GlobalRoot Class 2“ Zertifikat herunter.


Öffnen Sie dazu den nachfolgenden Link:


[https://pki.pca.dfn.de/dfn-ca-global-g2/cgi-bin/pub/pki?cmd=getStaticPage;name=index;id=2&RA_ID=2610](https://pki.pca.dfn.de/dfn-ca-global-g2/cgi-bin/pub/pki?cmd=getStaticPage;name=index;id=2&RA_ID=2610)


und wählen Sie „Wurzelzertifikat“:


#### 2.2 Schritt 2 – Zertifikat installieren

Öffnen Sie das heruntergeladene Zertifikat. Je nach Browser, kann das heruntergeladene Zertifikat
direkt geöffnet werden. Sollte dies nicht möglich sein, öffnen Sie dieses über einen Datei-Explorer.
Geben Sie unter Zertifikatname den Namen „T-TeleSec GlobalRoot Class 2“ ein.


Unter bestimmten Android-Versionen, ist es erforderlich, den Verwendungszeck anzugeben.
**Wählen Sie hier unbedingt WLAN aus!** Klicken Sie anschließend auf OK.

#### 2.3 Schritt 3 – WLAN Einstellungen öffnen

Gehen Sie in die Einstellungen und wählen Sie WLAN aus (bei neueren Android-Versionen unter
„Netzwerk&Internet“):


#### 2.4 Schritt 4 – eduroam einrichten Variante A: Neu einrichten (Verbindung getrennt)

Unter Phase 2-Authentifizierung wählen Sie „MSCHAPV2“ aus.

Unter CA-Zertifikat wählen Sie das in Schritt 1 und 2 heruntergeladene und benannte Zertifikat „TTeleSec GlobalRoot Class 2“ aus.
Unter Domain „hs-hannover.de“ eintragen.

Unter Identität geben Sie ihren Benutzernamen in der Form „username@hs-hannover.de“ ein (z.B.
abc-123-u1@hs-hannover.de) ein.
Unter Anonyme Identität geben Sie „anonymous@hs-hannover.de“ ein
Unter Passwort geben Sie das Passwort Ihres Hochschulkontos ein.

Klicken Sie anschließend auf „Verbinden“. Danach wird eine Verbindung zum Netzwerk hergestellt.


#### Variante B: Zertifikatswechsel (Verbindung bereits eingerichtet bzw. verbunden)

Wählen Sie das eduroam Netzwerk zum Bearbeiten mittels Radsymbol oder kurzem gedrückt halten
des Verbindungsnamens aus:


Es öffnen sich die Netzwerkdetails.
Unter „Netzwerkdetails“ mittels Stiftsymbol bearbeiten wählen:


Es öffnet sich die Detailseite der Eduroam Verbindung mit dem vorher installiertem „Deutsche
Telekom Root CA 2“ – Zertifikat unter dem Punkt „CA-Zertifikat“:


Unter „CA-Zertifikat“ das unter Schritt 1 und 2 heruntergeladene und benannte Zertifikat „T-TeleSec
GlobalRoot Class 2“ auswählen:


Einstellungen mittels „Speichern“ übernehmen:


Alle anderen Einstellungen bleiben erhalten und müssen nicht neu eingegeben werden!


EAP-Methode: PEAP
Phase 2-Authentifizierung: MSCHAPV2

CA-Zertifikat: T-TeleSec GlobalRoot Class 2
Domain: hs-hannover.de
Identität: username@hs-hannover.de (z.B. abc-123-u1@hs-hannover.de)
Anonyme Identität: anonymous@hs-hannover.de
Passwort: Geben Sie das Passwort Ihres Hochschulkontos ein.


**Anmerkung:**


Das Zertifikat „T-TeleSec GlobalRoot Class 2“ kann bereits ab sofort heruntergeladen und installiert
werden (Schritte 1 und 2). Die Umstellung in Schritt 4B sollte jedoch erst am 19.06.2019 erfolgen, da
es erst zu diesem Zeitpunkt an der Hochschule Hannover aktiviert wird.


12.06.2019/RHG


