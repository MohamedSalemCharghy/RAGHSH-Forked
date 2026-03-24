---
source_url: "https://f4.hs-hannover.de/fileadmin/HsH/Forms/Fakultaet_IV/Ueber_Uns/Personen/Arbeitspapiere/sk-03-09.pdf"
title: "sk-03-09"
crawl_date: "2026-03-07"
content_type: "pdf"
---

Fakultät IV – Wirtschaft und Informatik

## **Arbeitspapier / Abteilung Wirtschaft** **Stephan König** **Erfolgsfaktoren in Business Intelligence Projekten**


Arbeitspapier 03-2009
ISSN Nr. 1436-1035 (print) ISSN Nr. 1436-1507 (Internet)

www.fh-hannover.de/f4


Arbeitspapier (Forschungsbericht)

# **Erfolgsfaktoren in** **Business Intelligence Projekten**


**Prof. Dr. Stephan König**


Fakultät IV (Abteilung Wirtschaft)


Fachhochschule Hannover


Wintersemester 2008/09


i

### **Inhaltsverzeichnis**


**Inhaltsverzeichnis** **...................................................................................................i**


**Abbildungsverzeichnis** **............................................................................................iii**


**1** **Einleitung** **.............................................................................................1**


**2** **Business Intelligence** **.............................................................................3**


**3** **Business Intelligence Projektmanagement** **..............................................5**


**4** **Real Time Data Warehousing** **................................................................7**
4.1 Begriffsdefinition Real Time Data Warehousing ........................................7
4.2 Fachliche Anforderungen an ein Real Time Data Warehouse .......................8
4.3 Real Time Data Warehouse Architekturen .................................................12
4.3.1 Szenario 1: (Near) Real Time Data Warehouse ........................................12
4.3.2 Szenario 2: Operational Data Store .........................................................13
4.3.3 Szenario 3: Event Stream Processing ......................................................14
4.4 Zusammenfassung ..................................................................................17


**5** **Der Kimball Lifecycle** **...........................................................................18**
5.1 Einführung ............................................................................................18
5.2 Gesamtüberblick ....................................................................................19

5.2.1 Program/Project Planning ......................................................................20
5.2.2 Program/Project Management ................................................................20
5.2.3 Business Requirements Definition ..........................................................20
5.2.4 Technologie: Technical Architecture Design ...........................................21
5.2.5 Technologie: Product Selection and Installation .......................................21
5.2.6 Daten: Dimensional Modelling ..............................................................21
5.2.7 Daten: Physical Design .........................................................................21
5.2.8 Daten: ETL-Design and Development ....................................................22
5.2.9 BI-Anwendungen: BI Application Design ...............................................22
5.2.10 BI-Anwendungen: BI Application Development ......................................22
5.2.11 Deployment .........................................................................................22
5.2.12 Maintenance ........................................................................................22
5.2.13 Growth ...............................................................................................23
5.3 Zusammenfassung ..................................................................................23


ii


**6** **Real Time Data Warehousing Projektmanagement** **................................24**
6.1 Einführung ............................................................................................24
6.2 Launching and Managing the Project/Program ...........................................26
6.2.1 Project Definition .................................................................................27
6.2.2 Project Planning ...................................................................................31
6.2.3 Manage the Project ...............................................................................35
6.2.4 Manage the Program .............................................................................37
6.2.5 Zusammenfassung ................................................................................38
6.3 Business Requirements Definition ............................................................39

6.3.1 Overall Approach to Requirements Definition .........................................41
6.3.2 Prepare for the Interview .......................................................................41
6.3.3 Conduct the Interview ...........................................................................42
6.3.4 Wrap up the Interview ..........................................................................42
6.3.5 Review the Interview Results .................................................................42
6.3.6 Prepare and Publish Requirements Deliverables .......................................42
6.3.7 Prioritize and Agree on Next Steps .........................................................42
6.3.8 Zusammenfassung ................................................................................43
6.4 Technical Architecture ............................................................................44

6.4.1 TA: Gesamtüberblick ............................................................................45
6.4.2 TA: Back Room ...................................................................................46
6.4.3 TA: Presentation Server Architecture ......................................................49

6.4.4 TA: Front Room Architecture ................................................................50
6.4.5 TA: Infrastruktur ..................................................................................53

6.4.6 TA: Security ........................................................................................54
6.4.7 Zusammenfassung ................................................................................55

6.5 Creating the Technical Architecture Plan ...................................................56
6.5.1 Prozessschritte .....................................................................................56
6.5.2 Select Products ....................................................................................59

6.5.3 Zusammenfassung ................................................................................61


**7** **Zusammenfassung und Ausblick** **...........................................................62**


**8** **Literaturverzeichnis** **..............................................................................64**


**9** **Anhang** **.................................................................................................66**
9.1 Anhang A ..............................................................................................66
9.2 Anhang B ..............................................................................................67
9.3 Anhang C ..............................................................................................68
9.4 Anhang D ..............................................................................................69


iii

### **Abbildungsverzeichnis**


**Abbildung 2.1: Ordnungsrahmen Business Intelligence (Gluchowski08)** **................................ 3**


**Abbildung 2.2: Klassische BI-Architektur (Kemper06)** **.......................................................... 4**


**Abbildung 4.1: Data Warehouse Entwicklungsstufen (Turban07)** **.......................................... 10**


**Abbildung 4.2: Wertverlust der Information mit der Zeit (Gluchowski08, Hackathorn03)** **..... 11**


**Abbildung 4.3: Architektur für ein (Near) Real Time Data Warehouse** **.................................. 13**


**Abbildung 4.4: Architektur für einen Operational Data Store** **................................................ 14**


**Abbildung 4.5: Event Stream Processing** **................................................................................ 15**


**Abbildung 4.6: Blue Print für eine Real Time BI-Architektur (Gluchowski08)** **....................... 16**


**Abbildung 4.7: Integration von BI und SOA (Gluchowski08)** **................................................. 17**


**Abbildung 5.1: Der Kimball Lifecycle (Kimball08)** **................................................................. 19**


**Abbildung 6.1: Launching and Managing the Project/Program** **.............................................. 26**


**Abbildung 6.2: Aufgaben im Bereich Launching and Managing the Project/Program** **............ 27**


**Abbildung 6.3: Projektrollen für ein RTDW-Projekt** **............................................................. 32**


**Abbildung 6.4: Business Requirements Definition** **.................................................................. 40**


**Abbildung 6.5: TA Design und Product Selection and Installation** **.......................................... 44**


**Abbildung 6.6: (Logisches) Gesamtmodell Systemarchitektur DW/BI-System (Kimball08)** **.... 46**


**Abbildung 6.7: Back Room Architecture DW/BI-System (Kimball08)** **.................................... 47**


**Abbildung 6.8: Presentation Server System Architektur DW/BI-System (Kimball08)** **............. 50**


**Abbildung 6.9: Front Room Architecture DW/BI-System System (Kimball08)** **....................... 51**


**Abbildung 6.10: DW/BI Application Architecture Top-Down Approach** **................................ 57**


**Abbildung 9.1: Teradata’s Real-Time Enterprise Reference Architecture (Hedegard07)** **........ 66**


**Abbildung 9.2: Übersicht aller Aufgaben und die ihnen zugeordneten Rollen aus dem Bereich**

**Launching und Managing the Project/Program (Kimball08)** **................... 67**


**Abbildung 9.3: Übersicht aller Aufgaben und die ihnen zugeordneten Rollen aus dem Bereich**

**Business Requirements Definition (Kimball08)** **........................................ 68**


**Abbildung 9.4: Übersicht aller Aufgaben und die ihnen zugeordneten Rollen aus dem Bereich**

**Technical Architecture (Kimball08)** **........................................................ 70**


Kapitel 1 - Einleitung 1

### **1 Einleitung**


Das Thema Business Intelligence (BI) hat in den vergangenen Jahren sowohl in der Forschung als
auch in der unternehmerischen Praxis eine sehr hohe Dynamik bewiesen und dabei stark an Komplexität – insbesondere was die fachlichen Anwendungsszenarien angeht – zugenommen.


BI-Einführungsprojekte weisen in den meisten Fällen eine sehr große Komplexität und Dynamik auf.
Dies führt zu Herausforderungen im BI-Projektmanagement, die in aller Regel deutlich über denen
von typischen Anwendungsentwicklungsprojekten liegen.


Im Rahmen dieser Arbeit werden auf Basis der vorhandenen Literatur Erfolgsfaktoren im Projektmanagement von BI-Einführungsprojekten zu identifiziert und für eine spezielle Form von BIProjekten, den Real Time Data Warehousing Projekten, erweitert. Diese Fragestellung wurde bisher
in der Literatur noch nicht im Detail untersucht.


Im Mittelpunkt steht dabei das folgende Szenario: Ein Unternehmen möchte seine existierende Business Intelligence Lösung aufgrund neuer fachlicher Anforderungen nach Echtzeitdaten zu einem
Real Time Data Warehouse (RTDW) erweitern.


Untersucht wird dabei insbesondere, welche speziellen Fragen und Aspekte zu Beginn eines RTDWProjektes zu berücksichtigen sind:


Welche besonderen Herausforderungen sind in den Bereichen Projektplanung und Projektmanagement für ein RTDW-Projekt zu erwarten?


Welche fachlichen Anforderungen liegen typischerweise einem RTDW zu Grunde und wie
können diese systematisch ermittelt und priorisiert werden?


Wie und an welchen Stellen muss die Technische Architektur (TA) der existierenden BILösung für ein RTDW erweitert werden?


Über weite Bereiche wird dabei der Kimball Lifecycle (Kimball08) - eine Vorgehensweise für BIProjekte - als Ausgangspunkt verwendet. Von ihm aus werden die für die oben genannten Fragestellungen wichtigen Erweiterungen im Rahmen dieser Arbeit herausgearbeitet. [1]


Dazu wird in Kapitel 2 zunächst kurz das im folgenden verwendete Verständnis des Begriffes Business Intelligence definiert, bevor in Kapitel 3 ein Überblick über das Thema BI-Projektmanagement
gegeben wird. Kapitel 4 geht näher auf fachliche Überlegungen zur Einführung eines Real Time
Data Warehouse ein. In diesem Zusammenhang werden mögliche Einsatzszenarien exemplarisch
vorgestellt und grundlegende Technische Architekturalternativen aufgezeigt. Der Kimball Lifecycle


1 Nicht im Mittelpunkt dieser Arbeit stehen (aus Zeitgründen) die sich im Projektverlauf anschließenden Themen Datenmodellierung, ETL-Prozesses und die eigentlichen BI Anwendungen.


Kapitel 1 - Einleitung 2


wird in Kapitel 5 vorgestellt bevor in Kapitel 6 spezifische Anforderungen an das Projektmanagement von RTDW-Projekten im Detail untersucht werden. Die Arbeit schließt in Kapitel 7 mit Zusammenfassung und Ausblick.


Diese Arbeit ist im Wintersemester 2008/09 im Rahmen eines Forschungsprojektes an der Fachhochschule Hannover entstanden. Das Forschungsprojekt wurde seitens der Hochschule dankenswerterweise mit einer Lehrdeputatsermäßigung von 2 LVS gefördert.


Kapitel 2 - Business Intelligence 3

### **2 Business Intelligence**


Business Intelligence (BI) umfasst die Integration von Strategien, Prozessen und Technologien, um
im Umfeld der entscheidungsunterstützenden Systeme aus fragmentierten, inhomogenen Unternehmens-, Markt- und Wettbewerberdaten erfolgskritisches Wissen über Status, Potenziale und Perspektiven zu generieren und dies für Analyse-, Planungs- und Steuerungszwecke geeignet darzustellen
(siehe auch: Weites BI-Verständnis in Abbildung 2.1).


Abbildung 2.1: Ordnungsrahmen Business Intelligence (Gluchowski08)


Eine flexible BI-Architektur, die diesen Ansprüchen gerecht wird, weist in aller Regel eine große
Komplexität auf. Bewährt hat sich ein Drei-Schichten Modell bestehend aus einer Datenbereitstellungsschicht, einer Analyseschicht und einer Präsentationsschicht (siehe Abbildung 2.2). Kommerziell erhältliche Lösungen decken häufig nur Teilfunktionalitäten ab, so dass sich in der Praxis häufig
weitere Herausforderung bei der Integration verschiedener Produkte ergeben.


Kapitel 2 - Business Intelligence 4


Abbildung 2.2: Klassische BI-Architektur (Kemper06)


Für eine weiterführende Einführung in das Thema Business Intelligence siehe zum Beispiel
(Bauer09, Chamoni06, Gluchowski08, Kemper06, Lusti02, Mucksch00, Oehler06, Schütte01, Turban07).


Kapitel 3 - Business Intelligence Projektmanagement 5

### **3 Business Intelligence Projektmanagement**


BI-Projekte weisen in den meisten Fällen eine große Komplexität und Dynamik auf. Dies ergibt sich
insbesondere aus den abteilungsübergreifenden (Anwender-) Anforderungen, den verwendeten
Technologien und Produkten und insbesondere auch der Interdisziplinarität resultierend aus fachlichen und technischen Fragestellungen. Daraus ergeben sich in den meisten Fällen sehr lange Projektlaufzeiten (3+ Jahre) und hohe Kosten (Mio. Euro). Damit liegen die Herausforderungen an das BIProjektmanagement in aller Regel deutlich über denen von typischen Anwendungsentwicklungsprojekten.


Auch erfordert das grundsätzlich unterschiedliche Anwenderverhalten im analytischen BI-Umfeld
(im Gegensatz zu operativen Anwendungssystemen) Projektvorgehensweisen, die vom klassischen
Wasserfallmodell abweichen. Dabei muss der explorative Charakter des stark subjektiven Anwenderrverhaltens mit bewusst ungewissem Ausgang und flexiblen Navigationsräumen - im Gegensatz
zu den klar definierten, standardisierten und anwenderunabhängigen Use Cases der operativen Systeme - berücksichtigt werden.


Angehende BI-Projektmanager sind daher gut beraten, sich vor dem Projektstart über Erfolgsfaktoren und bewährte Vorgehensweisen (Best Practices) im BI-Projektmanagement zu informieren. Dies
erlaubt es ihnen, Risiken, Kosten und Komplexitäten besser zu beherrschen und auf Erfahrungen
anderer Projekte aufzubauen.


Zahlreiche deutsch- und englischsprachige Lehrbücher zum Thema Business Intelligence (Bauer09,
Chamoni06, Gluchowski08, Kemper06, Lusti02, Mucksch00, Oehler06, Schütte01, Turban07) widmen sich auch dem Thema BI-Projektmanagement.


Speziell auf das Thema BI-Projektmanagement ausgerichtet sind die Lehrbücher von Atre, Inmon,
Kimball und Westermann (Atre07, Inmon96, Kimball08, Westermann01).


Während Westermann (Westermann01) eher einen historischen Abriss über eines der ersten großen
Data Warehouse Projekte darstellt, geben die drei anderen Autoren (Atre07, Inmon96, Kimball08)
einen umfassenden Gesamtüberblick über das Thema BI-Projektmanagement.


Dabei spricht sich Inmon deutlich gegen das klassische Wasserfallmodell aus und propagiert, in einem iterativen Ansatz erst im Anschluss an die Datenzusammenführung und Anwendungsentwicklung die Anforderungen der Anwender zu erfassen (Inmon96). Kimball hingegen plädiert deutlich
dafür, zunächst die Anforderungen der zukünftigen Anwender an die analytischen Anwendungen zu
erheben und erst dann mit der Umsetzung zu beginnen (Kimball08). Bereits an diesem Beispiel wird
deutlich, dass sich aufgrund der Aktualität der Fragestellung noch keine einheitlichen Vorgehensweisen herausgebildet haben.


Weiterhin seien exemplarisch die folgenden Veröffentlichungen zum Themenumfeld BIProjektmanagement genannt: (Goeken04, Lehmann97, Schirp01, Sen05).


Kapitel 3 - Business Intelligence Projektmanagement 6


Sen et al. haben 15 verschiedene Data Warehouse Methodologien untersucht und nach verschiedenen
Kriterien (u.a. Kernkompetenzen, Anforderungsmodellierung, Datenmodellierung, Umsetzungsstrategie, Skalierbarkeit, Änderungsmanagement) bewertet. Auch sie kommen zum Schluss, dass sich
noch keine allgemein akzeptierten Standards herausgebildet haben und erwarten für die Zukunft im
Rahmen eines Reifeprozesses eine Konvergenz der verschiedenen Methodologien (Sen05).


Goeken skizziert eine Methode zur referenzgestützten Einführung von Führungsinformationssystemen (Goeken04).


Zwar können diese Lehrbücher und Veröffentlichungen einen groben Rahmen für die im folgenden
zu untersuchenden RTDW-Projekte vorgeben, sie erreichen aber für diese spezielle Form von BIProjekten keine ausreichende Detailtiefe. Diese Lücke soll im folgenden durch diese Arbeit geschlossen werden. Dabei wird im wesentlichen auf die Arbeiten von Kimball (Kimball08) aufgebaut
werden.


Kapitel 4 - Real Time Data Warehousing 7

### **4 Real Time Data Warehousing**


In diesem Kapitel wird erläutert, was ein Real Time Data Warehouse ist und aus welchen Gründen in
der unternehmerischen Praxis immer häufiger ein Real Time Data Warehouse (RTDW) in Erweiterung eines bereits bestehenden Data Warehouse als sinnvoll erachtet wird:


Welche fachlichen Anforderungen sind Ausgangspunkt für ein RTDW?


Wie sehen typische Einsatzszenarien aus und welche Technischen Architekturen bieten sich
für ein RTDW an?


Diese Überlegungen stellen die Basis für die in Kapitel 6 folgenden Ausführungen zu speziellen
Aspekten des Projektmanagements von RTDW-Projekten dar. Eine Einführung in das Thema
RTDW findet sich auch in (Gluchowski08, Oehler06, Turban07).

#### **4.1 Begriffsdefinition Real Time Data Warehousing**


Data Warehousing bezeichnet den Gesamtprozess von der Datenbeschaffung bis zur Datenanalyse in
einem Data Warehouse. Typischerweise wird dabei der ETL-Prozess (Extract, Transform, Load) zur
Befüllung des Data Warehouse aus den operativen Systemen etwa im Tages- oder Wochenrhythmus
durchgeführt. Steigen die fachlichen Anforderungen an die Aktualität der Daten im Data Warehouse,
kann dies durch eine Erhöhung der Frequenz der ETL-Prozesse erreicht werden. Damit lassen sich
die Latenzzeiten zwischen der Abbildung eines Geschäftsereignisses in den operativen Systemen und
der Analysemöglichkeit der korrespondierenden Daten im Data Warehouse senken. Man spricht
dann von Real Time Data Warehousing.


Typischerweise bewegen sich die Anforderungen an die Latenzzeit für ein RTDW im Bereich von
Minuten bis Stunden. Dies stellt eine erhebliche Verkürzung gegenüber den oben genannten ursprünglichen Anforderungen dar.


Gelegentlich wird korrekterweise auch von Right Time Data Warehousing (oder Near Real Time
Data Warehousing) gesprochen, um auszudrücken, dass Real Time im technischen Sinne (Latenzzeit
Null) oft nicht - oder nur mit unverhältnismäßig hohen Kosten - im Data Warehouse Umfeld realisierbar ist und aus fachlichen Gründen bei genauerer Analyse in den meisten Fällen auch nicht wirklich erforderlich ist. [2] Kimball (Kimball08) unterscheidet auf der Zeitachse instantaneous, frequently
und daily. Er betont, dass bereits in der fachlichen Anforderungsanalyse frühzeitig geklärt werden


2 Auch der Begriff Active Data Warehouse wird in diesem Zusammenhang verwendet. Im engeren
Sinne enthält er aber einen zusätzlichen Aspekt: Die aktive Zustellung der Echtzeitdaten an den Anwender im Sinne einer Push-Technologie.


Kapitel 4 - Real Time Data Warehousing 8


muss, welche Variante für eine gegebene Situation sinnvoll ist. Letztendlich hat diese Grundentscheidung - wie im folgenden dargestellt wird - erhebliche Auswirkungen insbesondere auf das Design der Technischen Architektur (siehe 4.3).


Data Warehouse Architekturen sind ursprünglich nicht für den Echtzeitbetrieb konzipiert worden.
Zum einen lag dies an der ursprünglichen fachlichen Ausrichtung des Data Warehouse als Analysewerkzeug für primär strategische Entscheidungen. In diesem Zusammenhang spielten Echtzeitdaten
eher eine untergeordnete Rolle.


Entscheidend waren aber zum anderen sicher auch die verfügbaren Hardwareressourcen, die zum
Beispiel einen untertägigen ETL-Prozess nicht zuließen. Hiefür stand nur das nächtliche Batchfenster zur Verfügung, häufig sogar nur das Wochenende. Wichtiger war eine gleichmäßige Auslastung
der begrenzten Ressourcen durch ein geschicktes Verteilen der Online- und Batch-Workloads. Andererseits erlaubten diese recht langen Batchfenster dann aber zeitaufwendige ETL-Prozesse mit Store
and Forward Architekturen, Persistenz in allen Verarbeitungsstufen, sequenzieller Verarbeitung von
Full Table Loads und qualitätssichernden Maßnahmen. Es wird zu prüfen sein, inwieweit sich diese
Anforderungen auch in einer RTDW-Architektur aufrechterhalten lassen.

#### **4.2 Fachliche Anforderungen an ein Real Time Data Warehouse**


Real Time Data Warehousing ist eine der Schlüsseltechnologien für ein Real Time Enterprise (RTE).
Unter einem Real Time Enterprise versteht man nach Hugos (Hugos04) ein Unternehmen, dass


gelernt hat, unter sich ständig verändernden Randbedingungen flexibel und zeitnah auf die
Anforderungen seiner Zulieferer und Kunden zu reagieren,


kontinuierlich Informationen über seine Märkte und seine internen Geschäftsprozesse sammelt, analysiert und für die Entscheidungsfindung verwendet,


sich einem ständigen Prozess der Geschäftsprozessoptimierung befindet und neue Marktchancen und Trends schnell erkennt und umgehend nutzen kann.


Eine ähnliche Definition von Gartner wird in (Hedegard07) genannt:


The RTE monitors, captures, and analyzes root-cause and overt events that are critical to its
success the instant those events occur, to identify new opportunities, avoid mishaps, and
minimize delays in core business processes.


The RTE will then exploit that information to progressively remove delays in the management and execution of its critical business processes.


Drei Beispiele mögen den durch ein RTDW generierten Mehrwert verdeutlichen. Dieser Mehrwert
muss bei der Investitionsentscheidung für ein RTDW eine entscheidende Rolle spielen.


Ein Unternehmen möchte auf Basis der aktuellen Kundenprofitabilität die Service Levels
und Cross Selling Angebote für seine Kunden mit Hilfe einer Rules Engine automatisiert in
Echtzeit differenzieren.


Kapitel 4 - Real Time Data Warehousing 9


Nach Untersuchungen von Saitz et al. (Saitz02) sind Fondsmanager bereit, für transparent
berichtende Unternehmen 15 bis 20% höhere Kurse zu bezahlen. Als Beispiele werden Cisco
und Motorola aufgeführt, die nahezu in Echtzeit einen virtuellen Abschluss erstellen können.
Somit dient eine schnellere Berichterstattung als ein mögliches Werkzeug zur Wertschöpfung und somit zur Steigerung des Shareholder Value.


Anderson et al. stellen in (Anderson04) ein Flight Management Dashboard von Continental
Airlines vor. Dies ermöglicht es bei verspätet ankommenden Flugzeugen diese an solche Gates zu dirigieren, so dass umsteigende hochprofitable Statuskunden einen möglichst kurzen
Weg zu ihren Anschlussflügen haben, um diese so doch noch erreichen können.


Weitere Anwendungsfelder für ein RTDW finden sind typischerweise in den folgenden Bereichen:


Analytisches Customer Relationship Management (Beispiel: Kampagnenmanagement in
Echtzeit auf Basis verschiedener Anwendungen und Datenquellen)(Gluchowski08).


Financial Performance Management (Beispiel: Fast Close / Virtual Close)(Oehler06,
Saitz02)


Bereitstellung und Analyse von Finanzmarktdaten in Echtzeit (Kemper04)


Customer Service


Marketing


Integrierte Logistik (Supply Chain Management)(Hedegard07)


Fraud Detection / Corporate Security


Weitere Beispiele finden sich in (Bucher08).


Damit wird deutlich, dass ein RTDW nicht mehr - wie ursprünglich für das Date Warehouse gedacht

- primär für strategische Entscheidungen der obersten Führungsebene eines Unternehmens verwendet wird. Gesucht wird vielmehr eine Entscheidungsunterstützung auch für Entscheidungen mit
überwiegend taktischem und sogar operativem Charakter.


Gleichzeitig ist damit ein signifikanter Anstieg in der Anzahl der zu treffenden Entscheidungen in
einem häufig zunehmend härteren Wettbewerbsumfeld zu verzeichnen. Es werden mehr Geschäftsereignisse aktiv registriert und verstärkt werden mit einem Data Warehouse nicht nur Analysen der
Vergangenheit durchgeführt, sondern auch Vorhersagen in die Zukunft gemacht. Es wird daher deutlich, dass auch die vielen kleinen Entscheidungen im täglichen Kundenkontakt Profitabilität und
Reputation eines Unternehmens maßgeblich mitbestimmen.


Die Entwicklung zu schnelleren Entscheidungen im Real Time Enterprise vergrößert gleichzeitig
auch die Anwenderzielgruppe für das RTDW. Zunehmend benötigen auch Fach- und Führungskräfte
mittlerer und unterer Hierarchieebenen analytische Werkzeuge. Es ist nicht mehr akzeptabel, dass
solche Entscheider aktuelle Informationen mühsam manuell aus verschiedenen operativen Systemen
zusammentragen müssen.


Kapitel 4 - Real Time Data Warehousing 10


Die historische Entwicklung von einer eher vergangenheitsorientierten Betrachtungsweise (Reporting - What happened?) über das RTDW (Operationalizing - What is happening?) hin zu einer auf
Regelbasis automatisierten Entscheidungsfindung (Activating - Make it happen) ist auch in Abbildung 4.1 dargestellt.


Abbildung 4.1: Data Warehouse Entwicklungsstufen (Turban07)


Insgesamt zeichnet sich also ab, dass sich durch Echtzeit-Analytik zusätzliche Wertschöpfung generieren lässt und somit Business Intelligence zunehmend in den Kontext gestellt wird, in dem der
größte Nutzen erzielbar ist: Business Process Management (BPM). Diese Verknüpfung wird in der
Literatur (Oehler06) auch mit dem Begriff Corporate Performance Management (CPM) zum Ausdruck gebracht.


Zusammenfassend ist festzuhalten, dass sich durch ein RTDW zahlreiche neue fachliche Optionen
eröffnen:


Entscheidungsunterstützung nahezu in Echtzeit auf Basis operativer Performancekennzahlen.


Steuerungskompetenz der Analyseergebnisse für das BPM: Optimierte Geschäftsprozesse.


Realisierung eines Closed Loop: Rückkopplung der analytischen Ergebnisse in operative
Prozesse durch einen geschlossenen Kreislauf zwischen dispositiven und operativen Systemen (Gluchowski08), wobei die Grenzen zwischen operativen und analytischen Anwendungen zunehmend verwischen.


Kapitel 4 - Real Time Data Warehousing 11


Active Business Intelligence: Automatisierte Aktionen auf Basis einer Rules Engine.


In diesem Zusammenhang sollte allerdings auch nicht unerwähnt bleiben, dass ein RTDW in aller
Regel lediglich die technische Voraussetzung für ein Real Time Enterprise darstellt. Entscheidend ist
letztendlich auch der erforderliche organisatorische und kulturelle Wandel im Unternehmen, wie er
zum Beispiel durch ein Business Process Re-Engineering angestoßen werden kann. Erst dann wird es
gelingen, die durch ein RTDW schneller bereitgestellten Daten (Verkürzung der Data Latency) auch
zeitnah zu analysieren (Analysis Latency) und in Entscheidungen und Aktionen einfließen zu lassen
(Decision Latency). Nur so wird die letztendlich endscheidende Gesamtzeit zwischen dem Geschäftsereignis und der daraus resultierenden Aktion auf ein Minimum reduziert und somit auch der
mit der Verzögerung einhergehende Wertverlust der Informationen mit der Zeit minimiert. Dieser
Zusammenhang ist in Abbildung 4.2 dargestellt. [3]


Abbildung 4.2: Wertverlust der Information mit der Zeit (Gluchowski08, Hackathorn03)


3 Allerdings sollte auch beachtet werden, dass der Wert einer Information im Laufe der Zeit auch
zunehmen kann. Zum Beispiel werden Auswirkungen eines Ereignisses oft erst nach einer gewissen
Zeit in ihrem vollen Ausmaße deutlich.


Kapitel 4 - Real Time Data Warehousing 12


Für die Wirtschaftlichkeitsbetrachtung eines RTDW müssen die tatsächlichen Anforderungen an die
Latenzzeiten fachlich sehr sorgfältig analysiert werden. Nur in wenigen Fällen wird das technisch
(mit hohen Kosten) machbare, auch aus fachlicher Sicht vertretbar sein. In aller Regel wird ein Senkung der Latenzzeiten in die Größenordnung von Stunden völlig ausreichend sein.


Eine Übersicht über aktuelle Entwicklungstendenzen im RTDW-Umfeld auf Basis einer Marktstudie
bei verschiedenen Unternehmen findet sich in (Ventana07).

#### **4.3 Real Time Data Warehouse Architekturen**


Im diesem Abschnitt werden exemplarisch drei verschiedene RTDW-Architekturen vorgestellt und
ihre Vor- und Nachteile erläutert. Diese Darstellung basiert auf (Forrester08) und ist weder umfassend und vollständig. Sie soll lediglich einige Kernentscheidungen beim Entwurf einer RTDWArchitektur andeuten, um die in Kapitel 6 folgenden Ausführungen zu speziellen Aspekten des Projektmanagements von RTDW-Projekten auf eine sinnvolle Basis zu stellen.


Grundsätzlich offerieren sowohl der ETL-Prozess als auch die Verarbeitung im Data Warehouse
bzw. in den Analysesystemen Beschleunigungspotenzial. Der ETL-Prozess lässt sich zum Beispiel
durch eine Erhöhung der Ladefrequenzen und/oder die Verkürzung der Ladedauer (inkrementelle
oder Delta Loads, parallele Verarbeitung) beschleunigen.


**4.3.1** **Szenario 1: (Near) Real Time Data Warehouse**


Die in Abbildung 4.3 dargestellte Architektur für ein (Near) Real Time Data Warehouse stellt den
Ausbau eines existierenden Data Warehouse zu einem (Near) RTDW dar. Damit lassen sich Latenzzeiten im Bereich von Stunden bis Minuten realisieren. Diese Lösung ist inkrementell realisierbar
und wird für die meisten Unternehmen die beste Lösung darstellen.


Beschleunigungspotenziale gegenüber dem klassischen Data Warehouse lassen über die folgenden
Mechanismen realisieren:


Datenbank-Trigger, die Datenänderungen in den operativen Systemen sofort registrieren.


Erhöhung der ETL-Frequenz.


Reduktion des ETL-Datenvolumens durch inkrementelle Batches (Trickle Feed).


Schnellere Verarbeitung der Daten im Data Warehouse und in den Analysesystemen.


Ausbau der Hardwareressourcen.


Evolutionäre Verbesserungen der Middleware und des Workload Managements.


Kapitel 4 - Real Time Data Warehousing 13


Abbildung 4.3: Architektur für ein (Near) Real Time Data Warehouse


Die Vorteile dieses Szenarios bestehen darin, dass durch die inkrementelle Vorgehensweise bisherige Data Warehouse Investitionen und Know How weiter genutzt werden können. Zudem sind die
Auswirkungen auf die operativen Systeme minimal. Echtzeitdaten und historische Daten werden
auch weiter in einem einzigen Data Warehouse gespeichert. Letzteres vereinfacht zum Beispiel das
Datenqualitätsmanagement.


Der Hauptnachteil dieses Szenarios besteht darin, dass es nicht für ein echtes RTDW mit garantierten
Sub-Second, End-to-End Datenlatenzzeiten geeignet ist.


**4.3.2** **Szenario 2: Operational Data Store**


Abbildung 4.4 ist eine Architektur dargestellt, in der das RTDW über einen zusätzlichen Operational
Data Store (ODS) realisiert wird. Der ODS enthält nur die aktuellen, aber keine historischen Daten,
ist nicht persistent und die Daten liegen in hoher Granularität (Transaktionsdetails, kaum Integration)
vor. Somit existiert eine zentrale Datenbasis für Analysen in Echtzeit Diese Datenbasis beruht auf
einem beschleunigten ETL-Prozess zur Befüllung des ODS.


Kapitel 4 - Real Time Data Warehousing 14


Abbildung 4.4: Architektur für einen Operational Data Store


Der Hauptvorteil dieser Architektur besteht darin, dass sie einen separaten Pfad aufweist, der schnell
einzurichten ist und für das DW keinen zusätzliche Workload bedeutet.


Nachteile bestehen in der Erweiterung der bisherigen Architektur. Dies erhöht die Wartungskosten
aufgrund der gewachsenen Komplexität. Zudem ergeben sich neue Herausforderungen im Bereich
Datenqualitätsmanagement, da der ODS nicht in das bisherige Datenqualitätsmanagement integriert
ist. Beachtet werden muss auch, dass der ODS im Normalfall keine integrierten und/oder historischen Daten enthält.


**4.3.3** **Szenario 3: Event Stream Processing**


Die architektonisch aufwendigste Lösung ist in Abbildung 4.5 skizziert. Sie ermöglicht ein echtes
RTDW im garantierten Sub-Second Bereich End-to-End. Dies lässt sich durch eine Integration der
Ideen moderner Enterprise Application Integration (EAI) Architekturen in den ETL-Prozess erreichen. So lassen sich (Geschäfts-) Ereignisse (Events) in Echtzeit registrieren und von der Datenintegrationsplattform sofort weiterverarbeiten.


Kapitel 4 - Real Time Data Warehousing 15


Traditionelle ETL-Prozesse zeichnen sich dadurch aus, dass sie mit oft komplexen Transformationen
aggregierte Datenmengen verarbeiten. Dies ermöglicht eine Subjekt- und Analyseorientierung, führt
aber zu Verzögerungen, die im RTDW-Umfeld nicht akzeptabel sind.


EAI-Architekturen hingegen sehen von vornherein eine zeitnahe Übertragung kleinerer, isolierter,
ereignisorientierter Datenmengen vor (und sind somit deutlich transaktionsorientierter und weniger
qualitätsgesichert).


Abbildung 4.5: Event Stream Processing


Es handelt sich um eine recht flexible, dezentralisierte und verteilte Architektur. Verschiedene Subscriber oder Services können jederzeit an die Datenintegrationsplattform angekoppelt werden. Indem
die Analytik als Service in eine Service Orientierte Architektur (SOA) eingebunden wird erhöht sich
die Agility der BI-Services, die so im Sinne von Corporate Performance Management (CPM) und
Business Activity Monitoring (BAM) besser bei der Orchestrierung der Geschäftsprozesse unterstützen können. Im Regelfall können bisherige EAI und DW Investitionen werden weiter genutzt.


Von Nachteil ist bei dieser Architektur, dass sie eine erhebliche Erweiterung der bisherigen DW
Architektur darstellt. Sie erhöht die Komplexität und das damit verbundene erforderliche Know How


Kapitel 4 - Real Time Data Warehousing 16


zum Aufbau und zur Wartung deutlich. Zudem müssen mit EAI und ETL zwei bisher weitgehend
getrennte Konzepte zusammengeführt werden. Nicht zu vernachlässigen sind auch die Performance
Auswirkungen auf die operativen Systeme. Weiterhin muss die neue Datenintegrationsplattform in
das bisherige Datenqualitätsmanagement integriert werden.


Eine ausführliche Diskussion der Verknüpfung von EAI und ETL im Kontext RTDW findet sich
auch in (Chamoni06). Gluchowski (Abbildung 4.6) schlägt eine an einen Enterprise Service Bus
gekoppelte Staging Area vor, aus der das Enterprise Data Warehouse in regelmäßigen Ladezyklen
gemäß den Echtzeitanforderungen befüllt wird. Abbildung 4.7 zeigt die mögliche Integration von BI
in eine SOA über BI und analytische Services. Eine vollständige Diskussion einer Real Time Enterprise Referenzarchitektur findet sich zum Beispiel in (Hedegard07) (Siehe auch Abbildung 9.1 auf
Seite 66).


Abbildung 4.6: Blue Print für eine Real Time BI-Architektur (Gluchowski08)


Kapitel 4 - Real Time Data Warehousing 17


Abbildung 4.7: Integration von BI und SOA (Gluchowski08)

#### **4.4 Zusammenfassung**


In diesem Kapitel wurde gezeigt, was ein RTDW auszeichnet und welche fachlichen Überlegungen
den Einsatz eines RTDW in der unternehmerischen Praxis rechtfertigen. Drei beispielhafte RTDW
Architekturen wurden mit ihren Vor- und Nachteilen vorgestellt. Auf dieser Basis sollen in Kapitel 6
spezielle Aspekte des Projektmanagements von RTDW-Projekten untersucht werden.


Zunächst wird jedoch in Kapitel 5 mit dem Kimball Lifecycle eine Methodologie für BI-Projekte
vorgestellt.


Kapitel 5 - Der Kimball Lifecycle 18

### **5 Der Kimball Lifecycle**


Wie bereits in Kapitel 3 angedeutet, stellt Kimball mit dem Data Warehouse Lifecycle Toolkit
(Kimball08) (kurz: Kimball Lifecycle) eine sehr praxisnahe und pragmatische Methodologie für
Projekte im Umfeld von Data Warehousing und Business Intelligence bereit. In diesem Kapitel wird
ein Gesamtüberblick über den Kimball Lifecycle vorgestellt, bevor anschließend spezielle Aspekte
von RTDW-Projekten in den Bereichen


Program/Project Planning,


Program/Project Management,


Business Requirements Definition,


Technical Architecture Design und


Product Selection und Installation


untersucht werden.

#### **5.1 Einführung**


Einer der zentralen Grundgedanken von Kimball besteht im Lifecycle Ansatz von DW/BI-Projekten [4]
und ihrer starken Ausrichtung an den fachlichen Anforderungen. Der Lifecycle Ansatz folgt zwingend aus der Erkenntnis, das sich DW/BI-Systeme in aller Regel ständig weiterentwickeln und eine
nicht zu unterschätzende Dynamik entwickeln können, die in Verbindung mit der typischerweise
großen fachlichen, technischen und politischen Komplexität hohe Anforderungen an das DW/BIProjektmanagement stellt. Diese Dynamik ist positiv zu sehen, da sie doch in aller Regel Indiz für
ein wachsendes Interesse der fachlichen Anwender und den daraus resultierenden neuen Wünschen
an das DW/BI-System ist. Für nicht zielführend hält Kimball in diesem Zusammenhang einen Big
Bang Ansatz oder einen Ansatz, der zu sehr auf technische Aspekte ausgerichtet ist.


Damit liegen die Herausforderungen an das DW/BI-Projektmanagement in aller Regel deutlich über
denen von typischen Anwendungsentwicklungsprojekten (siehe auch die Ausführungen in Kapitel
3). Dies führt zur Notwendigkeit, flexible und adaptierbare Designtechniken zu verwenden und von
Beginn an vorzusehen, dass DW/BI-Projekte im Normalfall kein eindeutig definiertes Ende besitzen.


4 Kimball verwendet durchgehend den Begriff DW/BI um das Gesamtsystem zu bezeichnen. Dies
entspricht dem weiten BI-Verständnis aus Abbildung 2.1. Die zu analysierenden Daten befinden sich
im Enterprise Data Warehouse (EDW) und die Schnittstelle zum Anwender bezeichnet Kimball als
BI Applications.


Kapitel 5 - Der Kimball Lifecycle 19


Stark im Vordergrund steht bei Kimball auch die mehrdimensionale Datenmodellierung. Sie bestimmt entscheidend, wie die Daten den Anwendern zur Verfügung gestellt werden und stellt gleichzeitig eine wichtige Schnittstelle zwischen fachlichen und technischen Anforderungen dar.


Seine Ursprünge hat der Kimball Lifecycle in den 80er Jahren. Er wurde in den Folgejahren ständig
weiterentwickelt. Die aktuelle Auflage, die Basis für die folgenden Untersuchungen darstellt, stammt
aus dem Jahre 2008 (Kimball08).

#### **5.2 Gesamtüberblick**


Der gesamte Kimball Lifecycle ist in Abbildung 5.1 dargestellt. Charakteristisch für den Kimball
Lifecycle ist die enge Verknüpfung verschiedenster Aufgabenbereiche und ihre Gruppierung in drei
Hauptzweige: Technologie, Daten und BI-Anwendungen. Dabei ist es wichtig, alle Aspekte eines
DW/BI-Projektes ausreichend zu berücksichtigen. DW/BI-Projekte, die ein übermäßiges Gewicht
auf Einzelaspekte legen, laufen ein hohes Risiko zu scheitern. Einige Aufgaben in den verschiedenen
Zweigen sind in Abbildung 5.1 bewusst übereinander angeordnet, da sie auch zeitlich parallel durchgeführt werden sollen. Allerdings soll die Tatsache, dass alle Kästen i.w. die gleiche Breite haben,
nicht implizieren, dass damit auch gleiche Aufwände und Dauern verbunden sind. Dies ist sicher zu
stark projektabhängig, als dass es sich für solch einen Überblick verallgemeinern ließe.


Abbildung 5.1: Der Kimball Lifecycle (Kimball08)


Kapitel 5 - Der Kimball Lifecycle 20


Im folgenden werden alle Hauptaufgabenbereiche aus Abbildung 5.1 kurz skizziert Für die sich anschließenden Untersuchungen von RTDW-Projekten stehen die Bereiche Program/Project Planning,
Program/Project Management, Business Requirements Definition, Technical Architecture Design
und Product Selection und Installation im Vordergrund (siehe auch Fußnote 1 auf Seite 1).


**5.2.1** **Program/Project Planning**


Auf Basis erster ungefährer Ideen für das zu entwickelnde DW/BI-System werden im Project Planning der grobe Projektumfang festgelegt, zu erledigende Aufgaben identifiziert, die damit verbundenen Aufwände geschätzt und ihre Reihenfolge ermittelt. Zudem müssen die dafür benötigten Ressourcen akquiriert werden. Hauptergebnis - und Grundlage für alle folgenden Schritte - ist der Gesamtprojektplan, der die wesentlichen Ergebnisse zusammenfasst.


Es besteht eine enge, wechselseitige Beziehung zur folgenden Business Requirements Definition, da
dort gefällte Entscheidungen Rückwirkungen auf den Projektplan haben können.


Gemäß Kimball ist ein Projekt der einmalige Durchlauf des Lifecycle während unter Programm die
übergeordnete und fortlaufende Koordination mehrerer Projekte/Durchläufe verstanden wird.


**5.2.2** **Program/Project Management**


Das Program/Project Management muss dafür sorgen, dass die im Projektverlauf zu erledigenden
Aufgaben auch tatsächlich zum richtigen Zeitpunkt und in der richtigen Reihenfolge ausgeführt werden. Dazu muss der Projektstatus kontinuierlich überwacht werden und ggf. korrigierend eingegriffen werden. Zudem ist darauf zu achten, dass Änderungen am Projektumfang nur nach Genehmigung
erfolgen. Erwartungsmanagement und aktive Kommunikation ergänzen die Aufgaben im Program/Project Management. Diese Aufgabe erstreckt sich i.w. über den gesamten Projektverlauf.


**5.2.3** **Business Requirements Definition**


Der Projekterfolg hängt im wesentlichen von einem genauen Verständnis der Anforderungen und
Wünsche der zukünftigen Anwender ab. Sonst droht das Projekt zur technischen Spielwiese der ITAbteilung zu verkommen.


Daher müssen die fachlichen Anforderungen sorgfältig erfasst werden. Dafür ist ein detailliertes
Wissen über das Geschäftsfeld des Unternehmens unbedingt Voraussetzung. Defizite in diesem Bereich werden sich in allen folgenden Aufgabenbereichen negativ auswirken und zu Mehraufwänden
und späteren Akzeptanzproblemen führen.


Ein wichtiges Ergebnis ist die Data Warehouse Bus Matrix. Diese verknüpft die Kernprozesse der
Organisation mit ihnen Datendimensionen.


Kapitel 5 - Der Kimball Lifecycle 21


Im Anschluss an die Definition der fachlichen Anforderungen folgen die bereits oben erwähnten drei
parallelen Zweige: Technologie, Daten und BI-Anwendungen.


**5.2.4** **Technologie: Technical Architecture Design**


Die erste Aufgabe im Technologiezweig liefert ein Gesamtkonzept für die zukünftige Technische
Architektur (TA). Neben der bereits existierenden technischen Umgebung müssen hierbei auch die
fachlichen Anforderungen und die Technologiegesamtstrategie des Unternehmens berücksichtigt
werden. Hier geht es zunächst vor allem um die Frage, welche Services zukünftig bereitgestellt werden sollen.


**5.2.5** **Technologie: Product Selection and Installation**


Aufbauend auf dem Design für die Technische Architektur wird nun das „Wie“ definiert: Welche
Hardware, Datenbanksysteme, ETL-Tools und Datenzugriffs- und Reportingtools werden benötigt
und genügen den Anforderungen? Nach der Auswahl müssen diese Produkte installiert und getestet
werden.


**5.2.6** **Daten: Dimensional Modelling**


Auf Basis der Enterprise Data Warehouse Bus Matrix aus der Business Requirements Definition
beginnt der Datenzweig mit dem Design des (mehrdimensionalen) Datenmodells. Das Datenmodell
ist wesentliche Grundlage für flexible und performante Datenanalysen und Reports. Hierzu werden
im Dimensional Modelling die benötigten Faktentabellen und ihre Dimensionen identifiziert.


**5.2.7** **Daten: Physical Design**


In diesem Schritt wird das zuvor definierte mehrdimensionale (logische) Datenmodell in ein physikalisches Modell in einer relationalen Datenbank übersetzt (Star Schema). Darüber hinaus werden
Sicherheitsaspekte und Performancefragen adressiert. Falls erforderlich, werden hier auch die benötigten OLAP-Datenbanken angelegt, die das mehrdimensionale Datenmodell in Würfelform abbilden.


Kapitel 5 - Der Kimball Lifecycle 22


**5.2.8** **Daten: ETL-Design and Development**


Schlussendlich müssen die analytischen Datenbanken mit Daten gefüllt warden. Die dazu erforderlichen Schritte Extraktion, Transformation und Laden (ETL) werden in diesem Arbeitspaket entworfen und umgesetzt. Gemäß Kimball liegen etwa 70% des Aufwandes und der Risiken eines DW/BIProjektes in diesem Bereich. Ursachen hierfür sind sicherlich in den heterogenen Quellsystemen, den
oft mangelhaften Dokumentationen derselben und politischen Herausforderungen zu suchen. Dabei
gilt es nicht nur die Erstbefüllung sicherzustellen, sondern auch einen regelmäßigen inkrementellen
Updateprozess zu implementieren.


**5.2.9** **BI-Anwendungen: BI Application Design**


Sobald die fachlichen Anforderungen bekannt sind, kann gemäß Kimball parallel zu den beiden o.g.
Zweigen auch bereits mit der Identifikation der erforderlichen BI-Anwendungen begonnen und geeignete Anwenderschnittstellen entworfen werden. Dabei sollte berücksichtigt werden, dass aus Anwendersicht nicht die Daten an sich, sondern ihre fachliche Aussagenkraft (Business Value), im
Vordergrund stehen.


**5.2.10** **BI-Anwendungen: BI Application Development**


Nach ihrem Design müssen die BI-Anwendungen konfiguriert und getestet werden. Dies ist die
Hauptaufgabe in diesem Arbeitsschritt, der den BI-Anwendungszweig abschließt.


**5.2.11** **Deployment**


Abschließend gilt es die Ergebnisse aus den drei verschiedenen Zweigen zusammenzuführen und
dem Anwender zur Verfügung zu stellen. Dies setzt eine umfangreiche Planung sehr verschiedener
Aktivitäten voraus. Dazu gehören zum Beispiel die Durchführung von Integrationstests, Schulungsmaßnahmen für die Anwender und der Aufbau einer geeigneten Supportstruktur. Sollte es zu Verzögerungen in einem dieser Bereiche kommen, steht das Startdatum der gesamten DW/BIAnwendung in Frage.


**5.2.12** **Maintenance**


Um den täglichen produktiven Betrieb der DW/BI-Anwendung sicherzustellen, sind geeignete Betriebsführungsabläufe vorzusehen. Dazu gehören zum Beispiel ein effizientes Monitoring und Performance Tuning, die Wartung der Indizes und die Durchführung regelmäßiger Backups. Ebenso


Kapitel 5 - Der Kimball Lifecycle 23


sind klassische Prozesse des IT Service Managements wie zum Beispiel ein Sevice Desk, Incident
Management etc. aufzusetzen.


**5.2.13** **Growth**


Ist das DW/BI-System von den Anwendern angenommen worden, werden schnell Wünsche nach
weiteren Funktionalitäten laut. Dies sollte nicht als Zeichen von Mängeln des aktuellen Systems
verstanden werden, sondern als Erfolg und Zeichen der Akzeptanz. Diese Erweiterungswünsche
müssen nun gesammelt, analysiert und priorisiert werden. Somit beginnt der Lifecycle wieder von
vorne.

#### **5.3 Zusammenfassung**


Damit ist der Kimball Lifecycle mit seinen Hauptaufgabenbereichen aus Abbildung 5.1vorgestellt.
Für die sich anschließenden Untersuchungen von RTDW-Projekten stehen nun die Bereiche Prog
ram/Project Planning, Program/Project Management, Business Requirements Definition, Technical
Architecture Design und Product Selection und Installation im Vordergrund.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 24

### **6 Real Time Data Warehousing Projektmanagement**

#### **6.1 Einführung**


In den vorangegangenen Kapiteln wurde erläutert, aus welchen fachlichen Überlegungen heraus ein
RTDW eine lohnenswerte Investition sein kann und welche IT-Architekturen denkbar sind. Anschließend wurde ein Gesamtüberblick über den Kimball Lifecycle vorgestellt.


Spezielle Aspekte des Projektmanagements von RTDW-Projekten werden in der Literatur bisher nur
an wenigen Stellen erwähnt (Brobst05). Eine detailliertere und systematische Betrachtung der
RTDW spezifischen Aspekte des Projektmanagements auf Basis einer umfassenden BIProjektmanagement Methodologie gibt es sich bisher nicht. Deshalb wird im folgenden der Kimball
Lifecycle um spezielle Aspekte des Projektmanagements von Real Time Data Warehouse Projekten
erweitert.


Dazu werden nun drei wichtige Bereiche des Kimball Lifecycle näher untersucht. Dabei sollen die in

(Kimball08) für beliebige DW/BI-Projekte vorgeschlagenen Arbeitspakete und Empfehlungen auf
ihre Anwendbarkeit und Relevanz für RTDW-Projekte untersucht werden. Wo es sinnvoll ist, werden spezifische Erweiterungen zum Kimball Lifecycle vorgeschlagen. Dabei stehen eindeutig Aspekte des Projektmanagementprozesses im Vordergrund. Es ist nicht beabsichtigt, konkrete technische oder fachliche Lösungsvorschläge zu erarbeiten.


Im Detail werden die folgenden Bereiche betrachtet:


Launching and Managing the Project/Program (umfasst die Arbeitspakete Program/Project
Planning und Program/Project Management).


Collecting the Requirements (umfasst das Arbeitspaket Business Requirements Definition).


Creating the Architecture Plan and Selecting Products (umfasst die Arbeitspakete Technical
Architecture Design und Product Selection & Installation).


Diese Auswahl umfasst mit Launching and Managing the Project/Program und Collecting the Requirements die für die Anfangsphase eines RTDW-Projektes entscheidenden Bereiche und wird ergänzt
durch die für ein RTDW-Projekt wichtigen Architekturaspekte.


Der nächste logische Schritt wäre eine Untersuchung der Zweige Daten und BI-Anwendungen und
der sich daran anschließenden Bereiche Deployment, Growth und Maintenance auf spezifische Aspekte von RTDW-Projekten (Siehe auch Fußnote 1 auf Seite 1 und der Ausblick in Kapitel 7).


Im folgenden werden nicht alle Einzelaspekte aus dem Kimball Lifecycle dargestellt. Diese werden
in (Kimball08) ausführlich und anschaulich beschrieben. Im Rahmen dieser Arbeit werden lediglich
die Hauptaufgaben auf oberster Ebene zur Orientierung kurz skizziert. Auf darunterliegende Aufga

Kapitel 6 - Real Time Data Warehousing Projektmanagement 25


ben wird nur dann eingegangen, wenn sich im Rahmen des Untersuchungsgegenstandes dieser Arbeit Änderungen oder Ergänzungen ergeben.


Kimball geht in (Kimball08) nur kurz auf RTDW-Aspekte ein. Dies geschieht im Zusammenhang
mit Detailfragen zu ETL-Prozessen. Für andere Bereiche des Lifecycle finden sich keine spezifischen Hinweise für RTDW-Projekte.


Für die folgenden Betrachtungen wird von einem fiktiven Unternehmen ausgegangen, das bereits
eine DW/BI-Lösung besitzt und nun vor der Frage steht, ob es dies zu einem RTDW erweitern
möchte und wie eine geeignete Vorgehensweise aussehen könnte.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 26

#### **6.2 Launching and Managing the Project/Program**


Die zum Launching and Managing the Project/Program gehörenden Arbeitspakete Program/Project
Planning und Program/Project Management sind in der Gesamtübersicht zum Kimball Lifecycle in
Abbildung 6.1 hervorgehoben.


Abbildung 6.1: Launching and Managing the Project/Program


Gemäß Kimball sind im Launching and Managing the Project/Program die in Abbildung 6.2 aufgeführten Hauptaufgaben und Aufgaben zu berücksichtigen. [5]


5 Dabei ist zu beachten, dass sich die Hauptaufgaben nicht 1:1 in die Arbeitspakete aus Abbildung
6.1 übersetzen lassen. Die Zuordnung sollte dem Leser aber trotzdem keine Schwierigkeiten bereiten. Aus Gründen der Vergleichbarkeit lehnt sich diese Arbeit aber an die Darstellung von Kimball
an.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 27







|PROJECT DEFINITION|Col2|
|---|---|
||Assess DW/BI-Readiness|
||Develop preliminary Project Scope/Charter|
||Build Business Justification|
|**PROJECT PLANNING & MANAGEMENT**|**PROJECT PLANNING & MANAGEMENT**|
|**PLAN**|Establish Project Identity|
|**PLAN**|Identify Project Resources|
|**PLAN**|Prepare Project Plan|
|**PLAN**|Develop Project Communication Plan|
|**MANAGE**|Conduct Project Team Kick Off & Planning|
|**MANAGE**|Develop Process to manage Scope. Control Changes|
|**MANAGE**|Develop Process to measure Success|
|**MANAGE**|User Acceptance/Project Review|
|**MANAGE**|Ongoing Project Management|
|**PROGRAM PLANNING & MANAGEMENT**|**PROGRAM PLANNING & MANAGEMENT**|
||Establish Governance Responsibility/Process|
||Establish Program Communication Plan|
||Establish Enterprise Data Stewardship|
||Establish Program Best Practices|
||Conduct Periodic Program Assessments|
||Ongoing Program Management|


Abbildung 6.2: Aufgaben im Bereich Launching and Managing the Project/Program


Diese Aufgaben werden im folgenden genauer auf ihre RTDW-Spezifika hin untersucht.


**6.2.1** **Project Definition**


Entsteht in einem Unternehmen, das bereits eine DW/BI-Lösung besitzt, die Idee zu einem RTDW,
sollten zunächst im Rahmen der Projektdefinition einige grundsätzliche Startvoraussetzungen geklärt
werden und anschließend der Projektumfang grob festgelegt werden. Wichtig in diesem Zusammenhang ist insbesondere auch die Beantwortung der Frage nach dem wirtschaftlichen Nutzen des
RTDW.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 28


6.2.1.1 Assess DW/BI-Readiness


Drei Voraussetzungen sollten bei einem RTDW-Projekt erfüllt sein, bevor die Projektdefinition
ernsthaft in Angriff genommen wird. Ansonsten läuft das Projekt Gefahr, von vornherein keine sinnvolle Basis zu besitzen.


1. Die Kernvoraussetzung besteht darin, dass mindestens ein einflussreicher Sponsor aus dem

oberen Management gefunden werden kann, der von der Idee eines RTDW überzeugt ist.
Sollte es nicht gelingen, einen solchen zu finden, liegt dies möglicherweise in einer unzureichenden Analyse der fachlichen Motivation des Projektes (siehe 2.).


2. Aus fachlichen Überlegungen heraus muss es einen zwingenden Grund für das RTDW ge
ben. In Kapitel 4 wurden Beispiele aufgeführt, aus denen ersichtlich wurde, weshalb die
Verfügbarkeit von Echtzeitinformationen einen Mehrwert für ein Unternehmen darstellen
kann. Insbesondere ist in diesem Zusammenhang genau zu untersuchen, wie zeitnah die Informationen wirklich zur Verfügung stehen müssen. In aller Regel wird man hier sorgfältig
zwischen den Grenzkosten für eine weitere Senkung der Latenzzeiten und dem erzielbaren
Grenznutzen abwägen. Oft spielen aber auch externe Gründe (Wettbewerbssituation, Marktchancen, gesetzliche Vorgaben) eine entscheidende Rolle. Hilfreich bei der Analyse der
Notwendigkeit eines RTDW sind oft auch die Unternehmensstrategie und die durch schneller verfügbare Informationen möglichen Verbesserungen in den KPIs der Hauptgeschäftsprozesse.


3. Weniger als die technische Machbarkeit sollte die Qualität der zur Verfügung stehenden Da
ten im Rahmen eines Data Profiling bereits in dieser frühen Phase überprüft werden. Stehen
die Daten in den Quellsystemen nicht im geforderten Umfang in der geforderten Aktualität
zur Verfügung, fehlt dem RTDW die entscheidende Basis. Kein noch so guter ETL-Prozess
wird dies ausgleichen können. Daher ist im Rahmen des Data Profiling grob zu untersuchen,
welche Daten aus welchen Quellsystemen in welcher Aktualität für das RTDW benötigt
werden, und ob die Quellsysteme diese Anforderungen erfüllen können (oder die operativen
Systeme zum Beispiel schon durch den OLTP-Betrieb derart unter Last sind, dass einige für
das RTDW zeitnah benötigte Transaktionsdaten erst mit unakzeptabler Verzögerung zur
Verfügung gestellt werden können.


Weitere Aspekte wie das Verhältnis der IT-Abteilung zur Fachabteilung oder die Frage nach einer
grundsätzlichen Offenheit der Unternehmenskultur in Hinblick auf analytische Systeme sollten im
Rahmen dieser Überlegungen zu RTDW-Projekten keine besondere Rolle spielen, da (gemäß der
Grundannahme) das Unternehmen bereits DW/BI-Systeme einsetzt.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 29


6.2.1.2 Develop preliminary Project Scope/Charter


Im nächsten Schritt muss der Projektumfang festgelegt werden. Dies kann nur in enger Anlehnung
an die Business Requirements Definition im nächsten Arbeitspaket geschehen (siehe Kapitel 6.3).


Ähnlich wie bei DW/BI-Projekten ist es auch für ein RTDW-Projekt sinnvoll, sich zunächst auf die
Real-Time Analysemöglichkeit eines einzigen (Kern-) Geschäftsprozesses zu konzentrieren, um die
fachliche Komplexität zu reduzieren. Dieser Geschäftsprozess wird häufig auch durch ein einziges
operatives Quellsystem abgebildet, was auch die technische Realisierung zusätzlich erleichtern sollte. Wichtig ist, dass dieser Geschäftsprozess einerseits nicht zu komplex ist (um den Projektumfang
nicht unnötig zu vergrößern), andererseits seine Einbindung in ein RTDW aber genügend Mehrwert
generiert, um die hohen Projektkosten für ein RTDW zu rechtfertigen.


Gerade für RTDW-Projekte, die auf einer existierenden DW/BI-Lösung aufsetzen, besteht die Gefahr, dass die Anwender die mit einer Verkürzung der Latenzzeiten einhergehenden Aufwände und
Herausforderungen unterschätzen. Daher ist rechtzeitig ein aktives Erwartungsmanagement aufzusetzen, um die Gründe für die Konzentration auf zunächst nur einen Geschäftsprozess zu kommunizieren.


Eng mit der Definition des Projektumfanges sollte auch die Identifizierung von (messbaren) Erfolgsfaktoren für das Projekt einhergehen.


Am Ende diese Schrittes steht das Scope Dokument, das die gerade beschriebenen Aspekte zusammenfasst und ein einheitliches Verständnis über den Projektumfang bei allen Stakeholdern ermöglicht. Auch ist von vornherein einzuplanen, dass sich das Scope Dokument im Projektverlauf verändern wird. Allerdings sollte darauf geachtet werden, dass der Projektumfang sich dabei nicht unkontrolliert ausweitet (Scope Creep).


6.2.1.3 Build Business Justification


In diesem Schritt wird der Business Case für das RTDW-Projekt ausgearbeitet. Eine zentrale Rolle
spielt dabei die Gegenüberstellung der zu erwartenden Kosten mit dem zukünftigen Nutzen. Dazu
werden meist Finanzkennzahlen wie ROI (Return on Investment), NPV (Net Present Value) oder
IRR (Internal Rate of Return) verwendet. Viele Unternehmen besitzen Vorgaben zur Berechnung
dieser Finanzkennzahlen (zum Beispiel Discount Rate), um verschiedene Projektskizzen besser vergleichen zu können.


Ein RTDW-Projekt wird hier an den Business Case für das DW/BI-System anknüpfen können.
Trotzdem ist es zum jetzigen (frühen) Zeitpunkt wahrscheinlich nur möglich, relativ grobe Schätzungen abzugeben.


Auf der Kostenseite stehen im Zusammenhang mit einem RTDW-Projekt insbesondere folgende
Überlegungen an:


Kapitel 6 - Real Time Data Warehousing Projektmanagement 30


Hardware-Kosten: Welche zusätzlichen Hardware Investitionen fallen im Zusammenhang
mit dem RTDW an? Dazu sollte eine grobe Entscheidung für eine der in Kapitel 4.3 aufgeführten IT-Architekturvarianten bereits gefallen sein. Insbesondere bei der möglichen Verwendung einer Datenintegrationsplatform (EAI) können erhebliche zusätzliche Kosten anfallen. Hier ist zu prüfen, inwieweit ähnliche Technologien bereits anderweitig im Unternehmen eingesetzt werden. Zusätzliche Kosten für Datenbankserver, Speicherplatz und erforderliche Netzwerkkapazitäten sollten auf Basis des bestehenden DW/BI-Systems relativ gut abschätzbar sein.


Software-Kosten: Hier gilt es grob zu prüfen, inwieweit vorhandene ETL- und AnalysisSoftware wahrscheinlich auch im Kontext des RTDW weiterverwendet werden können, oder
ob sie den Anforderungen nach Echtzeitfähigkeit nicht genügen und daher Alternativprodukte angeschafft werden müssen. Eine detaillierte Analyse dazu folgt in Kapitel 6.4. In anderen
Bereichen (Reporting, Data Profiling, Metadata-Management, OS, DBMS) sind die zusätzlichen Investitionen vermutlich eher gering.


Personalkosten: Erfahrungsgemäß ist dies auch im Rahmen eines RTDW-Projektes der größte Kostenblock. Neben internen Mitarbeitern sind je nach Architekturvariante auch externe
Berater vorzusehen.


Betriebskosten: Neben den einmaligen Projektkosten müssen auch die - oft nicht unerheblichen - zukünftigen Betriebskosten abgeschätzt werden. Allerdings sollten hier nur die zusätzlich zum bisherigen Betrieb der DW/BI-Lösungen anfallenden Kosten aufgeführt werden: Wartungskosten, Supportkosten und Kosten für ein mögliches Wachstum und potenzielle Erweiterungen (steigende Anwenderzahlen, Upgrades, Performance-Tuning). Aufgrund der höheren Zeitkritikalität eines RTDW ist insbesondere im Support Bereich mit gesteigerten Anforderungen (SLA) an die Reaktionszeiten bei Störungen zu rechnen.


Während sich die Kostenseite oftmals relativ einfach abschätzen lässt, ist die Quantifizierung der
Nutzenseite oft deutlich schwieriger. Bei einer soliden Fundierung des RTDW-Projektes auf fachlichen Anforderungen - verbunden mit der Konzentration auf einen (Kern-) Geschäftsprozess - sollte
es aber möglich sein, auch diesen Aspekt ausreichend in Zahlen zu fassen. Im Kern muss versucht
werden, die durch das RTDW erzielten Umsatzsteigerungen und Kosteneinsparungen abzuschätzen.
Die in Kapitel 4 aufgeführten Beispiele zeigen mögliche Ansatzpunkte auf. Auch hier ist davon auszugehen, dass die bereits für das DW/BI-System ermittelten Zahlen zumindest als Ausgangspunkt
weiterverwendet werden können.


Im Vordergrund der Nutzenanalyse stehen dabei natürlich solche Bereiche, in denen die Zeitkritikalität eine entscheidende Rolle spielt. Als Beispiel könnten hier Umsatzsteigerungen durch eine kürzere
Reaktionszeit auf veränderte Wettbewerbssituationen oder eine höhere Zufriedenheit - und damit
höhere Umsätze - von Statuskunden (siehe Anderson04) dienen. Eventuell ist es auch sinnvoll, die
Opportunitätskosten bei Fehlen eines RTDW oder externe Faktoren wie gesetzliche Vorgaben mit
ins Kalkül zu ziehen.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 31


Damit ist die Projekt Planung abgeschlossen und die Entscheidung über die Projektdurchführung
sollten zeitnah fallen.


**6.2.2** **Project Planning**


Ist das RTDW-Projekt in groben Zügen definiert und wurde genehmigt, besteht die nächste wichtige
Hauptaufgabe nun darin, eine detaillierten Projektplan zu erstellen.


6.2.2.1 Establish Project Identity


Hier ergeben sich für ein RTDW keine spezifischen Aufgaben, die von denen für ein DW/BI-Projekt
abweichen.


6.2.2.2 Identify Project Ressources


Ein wichtiges Erfolgskriterium für jedes Projekt besteht darin, die richtigen Personen für die zu erledigenden Aufgaben zu identifizieren und für das Projekt zu gewinnen. Meistens besteht dabei keine
1:1 Beziehung zwischen Personen und Rollen, sondern eine Person nimmt häufig mehrere Rollen
wahr. Typischerweise besteht ein RTDW-Projekt etwa aus 5 bis 20 Mitgliedern. Natürlich variiert
diese Größe sehr stark mit den Randbedingungen des Projektes und seinem Umfang.


In Abbildung 6.3 sind die nach (Kimball08) für ein DW/BI-Projekt zu besetzenden Rollen aufgeführt. Die Rollen, auf die im Rahmen eines RTDW-Projektes besondere Aufgaben zukommen, sind
hervorgehoben. Diese werden im folgenden genauer erläutert.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 32






|Fans|Business Users|
|---|---|
|**Front Office**<br>|Business Sponsor / Business Driver|
|**Front Office**<br>|DW/BI-Director / Program Manager|
|**Coaches**<br>|Project Manager|
|**Coaches**<br>|Business Project Lead|
|**Regular Line-Up**<br> <br> <br> <br> <br>|Business Analyst|
|**Regular Line-Up**<br> <br> <br> <br> <br>|Data Steward / QA Analyst|
|**Regular Line-Up**<br> <br> <br> <br> <br>|Data Architect / Data Modeler / DBA|
|**Regular Line-Up**<br> <br> <br> <br> <br>|Metadata Manager|
|**Regular Line-Up**<br> <br> <br> <br> <br>|ETL-Architect / ETL-Developer|
|**Regular Line-Up**<br> <br> <br> <br> <br>|BI-Architect / BI-Application Developer / Portal Developer|
|**Special Teams**<br> <br> <br> <br>|Technical Architect / Tech Support Specialist|
|**Special Teams**<br> <br> <br> <br>|Security Manager|
|**Special Teams**<br> <br> <br> <br>|Lead Tester|
|**Special Teams**<br> <br> <br> <br>|Data Mining / Stats Specialist|
|**Special Teams**<br> <br> <br> <br>|Educator|



Abbildung 6.3: Projektrollen für ein RTDW-Projekt


Im wesentlichen gelten beim Staffing für ein RTDW-Projekt die gleichen Überlegungen, wie von
Kimball in (Kimball08) für ein allgemeines DW/BI-Projekt beschrieben. Daher ist es wünschenswert, wenn möglichst viele der am Aufbau das DW/BI-Systems beteiligten Personen auch in das
RTDW-Projekt miteinbezogen werden.


Folgende Aspekte sind jedoch im Rahmen eines RTDW-Projektes besonders zu beachten:


Data Steward / Quality Assurance Analyst: In einem RTDW werden erhöhte Ansprüche an
die Aktualität der Daten gestellt. Die benötigten Echtzeitdaten müssen identifiziert und definiert werden, die Geschäftsregeln für die Daten müssen formuliert werden und gültige Wertebereiche vereinbart werden. Dies setzt ein hohes fachliches Know How voraus und erfordert in aller Regel Durchsetzungsvermögen und gute Kommunikationsfähigkeiten, da verschiedene Abteilungen an dieser Stelle zusammenarbeiten müssen. Ebenso muss der Quality
Assurance Prozess für die Bedürfnisse des RTDW erweitert werden.


Data Architect / Data Modeler / DBA: Je nach der gewählten Technischen Architektur für
das RTDW kommen auf den Data Architect, den Data Modeler und den Datenbankadministrator verschiedene Aufgaben zu. Das mehrdimensionale Datenmodell muss erweitert oder
angepaßt werden und in das physikalische relationale Modell übersetzt werden. Schlussend

Kapitel 6 - Real Time Data Warehousing Projektmanagement 33


lich müssen die Datenbanksysteme auch unter den Rahmenbedingungen deutlich höherer
ETL-Frequenzen betrieben werden. Folgende grundsätzliche Ansätze sind dabei denkbar
(Langseth04):


`o` Modellierung „as usual“: Bei Trickle & Flip sowie Direct Trickle Feed (Details

hierzu sind im nächsten Punkt beschrieben) wird kein spezieller Modellierungsansatz benötigt, da historische und Echtzeit-Daten in den gleichen Faktentabellen gespeichert werden.


`o` Separate Real-Time Partition: Echtzeit-Daten werden in separaten Faktentabellen

gespeichert. Dies erfordert den Einsatz intelligenter Abfrage-Tools, die Tabellenpartition unterstützen.


`o` Integrated Real-Time durch Views: Kombination der getrennten historischen Daten

und Echtzeit-Daten durch Views. Die Datenspeicherung erfolgt in kleineren Tabellen, diese können im Cache gelagert werden.


`o` Modellierung mit externem Real-Time Datencache: Keine spezielle Modellierung

erforderlich, da der externe Real-Time Datencache ein identisches Datenschema wie
das Data Warehouse hat.


ETL-Architect / ETL-Developer: Eine der Hauptherausforderungen in einem RTDW-Projekt
besteht in der Beschleunigung des ETL-Prozesses. Die Laufzeit muss durch Maßnahmen wie
zum Beispiel inkrementelle Loads verkürzt werden und die Frequenzen müssen gemäß den
Anforderungen an die Latenzzeit verkürzt werden. Dies setzt ein detailliertes Verständnis
der operativen Quellsysteme und der verwendeten ETL-Tools voraus. Ein Großteil der Aufwände für das RTDW-Projekt sind in diesem Bereich zu erwarten. Die Komplexität der
ETL-Prozesse lässt es auch ratsam erscheinen, ein sorgfältiges modulares Design derselben
zu entwerfen. Neben den bereits in Kapitel 4.3 genannten Technischen Architekturvarianten
beschreibt (Langseth04) die folgenden Ansätze:


`o` Near Real-Time ETL: Die einfachste und billigste Lösung durch Frequenzerhöhung

der Updates.


`o` Direct Trickle Feed: Das Data Warehouse wird mit aktuellen Daten der Quellsyste
me gefüllt. Dies läßt sich im allgemeinen durch eine Integrationsplatform wie in
4.3.3 beschrieben, realisieren Allerdings müssen Probleme in den Bereichen Skalierbarkeit und Performanz adressiert werden.


`o` Trickle & Flip: Die Echtzeit-Daten werden in Zwischentabellen geladen, anschlie
ßend werden diese Tabellen dupliziert und die Kopie mit der Zieltabelle ausgetauscht (= Flip).


`o` Externer Real-Time Daten-Cache (RTDC): Speicherung der Echtzeit-Daten außer
halb des traditionellen Data Warehouse, zum Beispiel in einem zusätzlichen Datenbank-Server, der nur für das ETL der Echtzeitdaten zuständig ist. Die Abfrage von


Kapitel 6 - Real Time Data Warehousing Projektmanagement 34


Echtzeit-Daten wird direkt an den RTDC geleitet (dies ist im Sinne des ODS in Kapitel 4.3.2).


BI-Architect / BI-Application Developer / Portal Developer: Auch die BI-Anwendungen
müssen an die neuen Analysemöglichkeiten angepasst werden. Diese Aufgabe umfasst die
Analyse der fachlichen Anforderungen und deren Abbildung in die BI-Anwendungen. Typischerweise handelt es sich dabei um die Konfiguration von kommerziellen BI-Lösungen
(und nur selten um eine selbst programmierte Software). Insbesondere die OLAP-Tools
wurden ursprünglich für Operationen auf statischen, unveränderlichen Daten entwickelt. Daher können bei schnell veränderlichen Daten Inkonsistenzprobleme auftreten. Folgende Lösungsansätze sind denkbar (Langseth04):


`o` Der Near Real-Time Ansatz: Verzicht auf wirkliche Echtzeit-Daten im OLAP Um
feld.


`o` Risikominderung für „true“ Real-Time: Anwendern hochkomplexe Abfragen auf

Echzeit-Daten verbieten


`o` Nutzung eines externen RTDC: Strikte Trennung der Echtzeit-Daten von den histo
rischen Daten.


Technical Architect / Tech Support Specialist: Wie bereits in Kapitel 4.3 angedeutet und aus
den vorhergehenden Punkten ersichtlich, spielt die Wahl einer zu den fachlichen Anforderungen passenden Technischen Architektur eine große Rolle. Sie bestimmt maßgeblich den
zukünftigen Erfolg des RTDW und muss die bereits für das DW/BI-System existierende
Technische Architektur sinnvoll ergänzen. Daher hat der technische Architekt in einem
RTDW-Projekt eine besonders wichtige Aufgabe. Er muss eine passende Architektur entwerfen, darauf achten, dass alle Komponenten zusammenpassen und die richtigen Produkte
auswählen. Der Technische Architekt kann kein Experte in Detailfragen zu allen Technologien sein. Daher wird er durch Technical Support Specialists unterstützt. Sollte die Architekturvariante einer Datenintegrationsplattform (siehe 4.3.3) gewählt werden, ist zu prüfen, inwieweit die EAI-Architekten des Unternehmens direkt in das RTDW-Projekt eingebunden
werden.


Schlussendlich muss der RTDW-Projektmanager aus diesen Einzelspezialisten ein funktionierendes
Team formen. Diese Aufgabe sollte sich aber bei einem RTDW-Projekt nicht wesentlich von der auf
anderen IT-Projekten unterscheiden.


6.2.2.3 Prepare Project Plan


Auch ein RTDW-Projekt benötigt einen detaillierten und integrierten Projektplan. Die in Kimball
(Kimball08) beschriebene Vorgehensweise für DW/BI-Projekte ist genauso für ein RTDW-Projekt
anwendbar. Die vermutlich größte Unsicherheit in der Aufwandsschätzung liegt im ETL-Bereich.
Trotzdem ist davon auszugehen, dass die Erfahrungen bei der Projektplanung für das bestehende


Kapitel 6 - Real Time Data Warehousing Projektmanagement 35


DW/BI-System eine wertvolle Basis darstellen. Insbesondere wenn zu Projektabschluss der ursprüngliche Projektplan rückblickend noch einmal kritisch mit den Ist-Werten in Beziehung gesetzt
wurde.


6.2.2.4 Project Communication Plan


Die im Rahmen des Kommunikationsplans für ein RTDW-Projekt zu beachtenden Aspekte und zu
erledigenden Aufgaben sind identisch mit denen für ein DW/BI-Projekt. Insofern ergeben sich keine
Ergänzungen oder Erweiterungen zu den Ausführungen von Kimball.


Damit sind die planerischen Aufgaben abgeschlossen.


**6.2.3** **Manage the Project**


Nachdem der Projektplan erstellt und das Projektteam zusammengestellt wurde, kann mit der eigentlichen Projektdurchführung begonnen werden. Dabei stehen auch für ein RTDW-Projekt die typischen Managementaufgaben einer Projektdurchführungsphase an, die im wesentlichen darauf abzielen, den Projektstatus zu erfassen und - falls notwendig - korrigierend einzugreifen, um die Projektziele (Termin, Kosten, Qualität) wie geplant zu erreichen.


Zu den Aufgaben gehören insbesondere:


Statusüberwachung


Umfangsmanagement


Erwartungsmanagement


DW/BI-Projekte, und somit auch RTDW-Projekte, unterscheiden sich dabei in vielen Aspekten nicht
von anderen IT-Projekten. Somit sind allgemeingültige Projektmanagementtechniken im allgemeinen gut anwendbar.


Kimball führt aber vier Charakteristika von DW/BI-Projekten auf, die aus Projektmanagementsicht
besonderer Beachtung bedürfen:


Die Projektteams sind stärker interdisziplinär ausgerichtet als bei vielen anderen Projekten.


Der iterative Entwicklungszyklus der mehrere DW/BI-Projekte umfasst und zu einer sehr
langen Programmlaufzeit führt.


Die häufigen und oft komplexen Probleme im Bereich der Daten, hier insbesondere im
Rahmen des ETL-Prozesses.


Die aufgrund der großen Bedeutung meist prominente Rolle von DW/BI-Projekten innerhalb des Unternehmens. Dies ist oft mit hohen Erwartungen an ihren Erfolg verknüpft.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 36


Auf RTDW-Projekte trifft wahrscheinlich der dritte Punkt besonders zu. Deshalb wurde ihm bereits
in Kapitel 5.2.1 im Abschnitt Assess DW/BI-Readiness besondere Aufmerksamkeit geschenkt.


Innerhalb von Manage the Project sind gemäß Kimball die folgenden Aufgaben zu:


Conduct Project Team Kick-Off & Planning


Develop Process to manage Scope. Control Changes


Develop Process to measure Success


User Acceptance / Project Review


Ongoing Project Management


Der korrespondierende Abschnitt in (Kimball08) weist eine leicht andere Struktur auf, die sich aber
leicht auf die o.g. Aufgaben abbilden lässt:


Conduct the Project Team Kick-Off Meeting


Monitor Project Status


Maintain the Project Plan


Consolidate the Project Documentation


Manage the Scope


Manage Expectations


Recognize Project Trouble Signs


Während diese Projektmanagementaufgaben in einem RTDW-Projekt weit gehend ähnlich denen in
anderen DW/BI-Projekten sind - und deshalb hier nicht weiter ausgeführt werden - gibt es unter den
von Kimball aufgeführten Frühindikatoren für entstehende Probleme zwei, die für RTDW-Projekte
besonders relevant sind:


Start oder Fortführung des Projektes, obwohl deutlich wird, dass die Quelldaten in den operativen Systemen keine ausreichende Qualität aufweisen: Im Zusammenhang mit einem
RTDW-Projekt könnte dies insbesondere der Fall sein, falls sich herausstellt, dass die Quellsysteme nicht in der Lage sind, die Daten mit den geforderten geringen Latenzzeiten und
Frequenzen bereitzustellen. Deshalb wurde diesem Aspekt bereits in Kapitel 6.2.1 im Abschnitt Assess DW/BI-Readiness besondere Aufmerksamkeit geschenkt.


Die Herausforderungen im ETL-Bereich führen dazu, dass die Anwenderschnittstelle in den
BI-Anwendungen vernachlässigt wird: Diese Gefahr droht sicher auch in einem RTDWProjekt, da ein Großteil der Aufwände im ETL-Bereich angesiedelt sein werden. Gleichzeitig sind aber auch an der Anwenderschnittstelle umfangreiche Änderungen erforderlich, sollen die durch die Senkung der Latenzzeiten entstandenen neuen fachlichen Möglichkeiten
auch realisiert werden.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 37


**6.2.4** **Manage the Program**


Die bisherigen Ausführungen bezogen sich auf ein einzelnes Projekt und somit einen Durchlauf des
Kimball Lifecycle. Meist wird ein DW/BI-Projekt mit seinem Abschluss „nur“ eine Version 1.0 bereitstellen. Sehr schnell erkennen die Anwender den durch die DW/BI-Systeme generierten Mehrwert und fordern zusätzliche Funktionalitäten und Erweiterungen. Diese führen in aller Regel zu
einem Folgeprojekt.


Somit entsteht die Notwendigkeit, eine Organisationsstruktur über mehrere Projekte hinweg zu
schaffen: Das Programmmanagement.


Zu Hauptaufgabe des Programmmanagements zählt es, Erfahrungen und Ergebnisse über Projektgrenzen hinweg weiterzutragen und somit steilere Lernkurven der Folgeprojekte sicherzustellen.


Davon kann auch ein RTDW-Projekt sehr stark profitieren. Typischerweise wird die Senkung der
Latenzzeiten in einem ersten DW/BI-Projekt keine Priorität besitzen. Zusätzlich stehen andere Fragestellungen im Vordergrund, um überhaupt ein erstes DW/BI-System bereitzustellen. Erst in der
Folge wird der Wunsch nach einem RTDW entstehen. Somit sollte ein RTDW-Projekt - sichergestellt durch ein Programmmanagement - auf den vorhergehenden DW/BI-Projekten aufbauen und
von den dort gemachten Erfahrungen profitieren. Beispiele wurden in den vorhergehenden Kapiteln
bereits genannt. Dies wird es dem RTDW-Projekt gerade in der Anfangsphase ermöglichen, besser
zu planen und sich so auf seine eigentlichen Herausforderungen konzentrieren zu können.


Nach Kimball fallen folgende Aufgaben in den Bereich Programmmanagement:


Establish Governance Responsibility/Process


Establish Program Communication Plan


Establish Enterprise Data Stewardship


Establish Program Best Practices


Conduct Periodic Program Assessments


Ongoing Program Management


Von besonderer Bedeutung für ein RTDW-Projekt ist sicherlich, dass der Data Steward bereits möglichst frühzeitig eine Verfügbarkeit von Echtzeitdaten in seinem Aufgabenbereich berücksichtigt.


Im allgemeinen stehen bei einem RTDW-Projekt allerdings eher die Projektaspekte im Vordergrund,
so dass an dieser Stelle nicht weiter auf Details des Programmmanagements eingegangen werden
muss.


Es ist davon auszugehen, dass das RTDW-Projekt - je nach Anzahl der zu unterstützenden Geschäftsprozesse - in einem, oder maximal zwei Projekten, realisiert werden kann.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 38


**6.2.5** **Zusammenfassung**


Zusammenfassend lässt sich festhalten, das im Aufgabenpaket Launching und Managing the Project/Program bereits einige wichtige Ergänzungen für RTDW-Projekte zu beachten sind.


Bei der Projektdefinition gilt es insbesondere im Rahmen von Assess DW/BI-Readiness auf die fachliche Begründung für ein RTDW zu achten und durch ein Data Profiling die Verfügbarkeit der erforderlichen (Echtzeit-) Daten abzuschätzen.


Zudem sollte im Rahmen der Aufgabe Develop preliminary Project Scope / Charter darauf geachtet
werden, sich zunächst auf die Real-Time Analysemöglichkeit eines einzigen (Kern-) Geschäftsprozess zu konzentrieren


Eine fundierte Kosten-/Nutzenanalyse ist das Ergebnis der Aufgabe Build Business Justification.


Im Rahmen der Projektplanung wird ein geeignetes Projektteam zusammengestellt. Für ein RTDWProjekt sind insbesondere die folgenden Rollen von besonderer Wichtigkeit, weshalb sie sorgsam
besetzt werden müssen:


Data Steward / QA-Analyst


Data Architect / Data Modeler / DBA


ETL-Architect / ETL-Developer


BI-Architect / BI-Application Developer / Portal Developer


Technical Architect / Tech Support Specialist


Die Durchführung eines RTDW-Projektes (Manage the Project) unterscheidet sich im Kern nicht
von anderen (DW/BI-) Projekten. Allerdings ist auch hierbei wieder ein besonderes Augenmerk auf
die Bereiche Datenqualität und ETL-Prozess zu legen, da sie sich oft als besonders kritisch herausstellen.


Ein RTDW-Projekt kann stark von einem guten Programmmanagement profitieren. Insbesondere die
Rolle des Data Steward kann in Hinblick auf die Datenqualitätsthematik sehr hilfreich sein. Ansonsten sollte ein gutes Programmmanagement vor allem einen schnellen Start des RTDW-Projektes
ermöglichen, da viele wichtige Informationen und Erfahrungen aus vorhergehenden Projekten wiederverwendet werden können.


Eine Übersicht aller Aufgaben aus dem Bereich Launching und Managing the Project/Program sind
in Anhang B in Tabellenform dargestellt. Zusätzlich sind dort den Aufgaben Rollen zugeordnet.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 39

#### **6.3 Business Requirements Definition**


„Business requirements sit at the centre of the universe“. Damit beginnt Kimball in (Kimball08)
seine Ausführung zum Arbeitspaket Business Requirements Definition. Es verdeutlicht den Stellenwert, den er diesem Thema zuordnet. Damit ist aber auch von vornherein deutlich, dass ein DW/BIProjekt, und gleiches muss für ein RTDW-Projekt gelten, kein technisches Spielzeug der ITAbteilung sein kann, sondern es ganz klar auf fachlichen Anforderungen beruhen muss. Deshalb
kommt der detaillierten fachlichen Anforderungsanalyse ein überragender Stellenwert zu.


Dies wird auch dadurch deutlich, dass die fachlichen Anforderungen direkte Auswirkungen auf nahezu jeden Aspekt des Projektes haben:


Project / Program Planning / Management


Technical Architecture


Dimensional Modelling


Physical Design


ETL-Design / Development


BI-Application Design / Development


Deployment


Maintenance & Growth


Deshalb ist eine möglichst frühe detaillierte Erfassung der fachlichen Anforderungen sehr wichtig.
Spätere Änderungen lassen sich oftmals nur schwer in einem laufenden Projekt berücksichtigen.


Trotz ihrer Wichtigkeit sollte die Anforderungsanalyse jedoch zeitlich auch nicht zu sehr ausgedehnt

werden und auf ein definiertes Enddatum geachtet werden. Je nach Projektumfang ist etwa eine
Dauer von drei bis vier Wochen vorzusehen. Am Ende muss zwischen dem Projekt, der Fach- und
der IT-Abteilung Einvernehmen darüber bestehen, welche Anforderungen wesentlich sind und welche lediglich mögliche Ergänzungen darstellen. Eine wichtige Rolle kommt in dieser Phase neben
dem Projektmanager dem Business Analyst zu.


Während im Arbeitspaket Project Definition mit der Business Justification bereits wesentliche Gründe für die fachliche Notwendigkeit des RTDW-Projektes identifiziert wurden, gilt es nun, diese weiter zu detaillieren und damit eine solide Ausgangsbasis für die in den drei Zweigen Technische
Architektur, Daten und BI-Anwendungen folgenden Aufgaben zu haben (siehe Abbildung 6.4).


Kapitel 6 - Real Time Data Warehousing Projektmanagement 40


Abbildung 6.4: Business Requirements Definition


Fachliche Anforderungen können sowohl auf Programm- als auch auf Projektebene erhoben werden.
Auch wenn es auf inhaltlicher Ebene Unterschiede im Detailgrad und in der Gesamtausrichtung gibt,
ist der eigentliche Prozess der Anforderungsanalyse in beiden Fällen ähnlich. Folgende Prozessschritte sind zu durchlaufen:


Preparation


Participants Selection


Business Questioning


Data Audit


Documentation


Next Steps


Im Rahmen eines RTDW-Projektes wird man sich auf der Projektebene bewegen. Ziel ist es, detaillierte fachliche Anforderungen für den in der Project Definition identifizierten Geschäftsprozess zu

ermitteln.


Ein Großteil der von Kimball in (Kimball08) beschriebenen Vorgehensweisen liefert sehr wertvolle
praktische Hinweise und Interviewtechniken und ist unverändert auch für RTDW-Projekte gültig.
Speziell sollte aber im Rahmen eines RTDW-Projektes in den einzelnen Arbeitsschritten auf die im
folgenden beschriebenen Aspekte geachtet werden:


Kapitel 6 - Real Time Data Warehousing Projektmanagement 41


**6.3.1** **Overall Approach to Requirements Definition**


Hier ergeben sich für ein RTDW keine spezifischen Aufgaben, die von denen für ein DW/BI-Projekt
abweichen.


**6.3.2** **Prepare for the Interview**


Hier gilt es u.a. geeignete Interviewpartner zu identifizieren. Neben Vertretern der fachlichen Seite

werden dies auch Mitglieder der IT-Abteilung sein. Im Rahmen eines RTDW-Projektes wird insbesondere auch letzteren eine wichtige Rolle bei den Interviews zukommen. Eine zentrale Fragestellung wird die Fähigkeit der operativen Quellsysteme sein, Echtzeitdaten in geeigneter Weise zur
Verfügung stellen zu können. Darüber hinaus kann das IT-Management eventuell auch noch weitere
mögliche Anwendungsszenarien für ein RTDW aufzeigen.


Sollten sich durch das RTDW neue - über die bereits im Rahmen der DW/BI-Lösung diskutierten Fragen bezüglich Compliance und/oder Security ergeben, sind entsprechende Vertreter ebenfalls für
Interviews einzuplanen.


Bei der Erstellung der Interview-Leitfäden ist darauf zu achten, dass spezifische Fragen nach dem
durch das RTDW angestrebten Mehrwert vorgesehen sind. Beispiele für ergänzende Fragen zum
Leitfaden für fachliche Interviews in (Kimball08) könnten wie folgt aussehen:


Welche bereits heute durchgeführten Reports und Datenanalysen sind besonders zeitkritisch?
Wie häufig werden sie durchgeführt? Welche zusätzlichen Möglichkeiten würden sich eröffnen, falls Sie die Analysen häufiger durchführen könnten?


Was sind die wichtigsten geschäftlichen Erfolgskriterien? Wie oft werden Informationen
darüber benötigt? Wie lassen sie sich quantifizieren? Welche Ausgangsdaten werden für ihre
Berechnung benötigt? Wie aktuell ist das in DW dazu vorhandene Zahlenmaterial?


Wozu könnten Analysen aus dem RTDW eingesetzt werden? Wie zeitnah werden Marktentwicklungen heute erkannt? Welche Möglichkeiten eröffnen sich durch Echtzeitdaten?
Welche finanziellen Vorteile (Umsatz, Gewinn, Kosten) ließen sich dadurch realisieren?


Was sind zentrale Erfolgskriterien für das RTDW? Wie lassen sie sich quantifizieren? Gibt
es strategische Geschäftsziele, die im Zusammenhang mit dem RTDW stehen?


Hauptziel der Interviews mit der IT-Abteilung muss es sein, die durch die fachlichen Interviews aufgezeigten Möglichkeiten auf ihre grundsätzliche Machbarkeit hin zu überprüfen:


Stehen die benötigten Daten rechtzeitig zur Verfügung oder wie könnte man sie bereitstellen? Welche Anwendungssysteme sind einzubeziehen?


Stehen auch die Daten aus anderen Quellsystemen für eine Gesamtintegration der Daten zur
Verfügung (Data Warehouse Datenbestände sind subjektorientiert)?


Kapitel 6 - Real Time Data Warehousing Projektmanagement 42


**6.3.3** **Conduct the Interview**


Hier ergeben sich für ein RTDW keine spezifischen Aufgaben, die von denen für ein DW/BI-Projekt
abweichen.


**6.3.4** **Wrap up the Interview**


Hier ergeben sich für ein RTDW keine spezifischen Aufgaben, die von denen für ein DW/BI-Projekt

abweichen.


**6.3.5** **Review the Interview Results**


Hier ergeben sich für ein RTDW keine spezifischen Aufgaben, die von denen für ein DW/BI-Projekt
abweichen.


**6.3.6** **Prepare and Publish Requirements Deliverables**


Die in diesem Schritt zu erstellenden Anforderungskataloge müssen die in den Interviews zutage
getretenen fachlichen Anforderungen nach Geschäftsprozessen aufgegliedert zusammenfassen und in
einer Data Warehouse Bus Matrix zusammenstellen. Die Data Warehouse Bus Matrix verknüpft die
Geschäftsprozesse mit den sie beschreibenden Datendimensionen. Auf Basis der Interviews mit der
IT-Abteilung lässt sich so abschätzen, wie realistisch die Abbildung dieser Geschäftsprozesse in
einem RTDW ist.


**6.3.7** **Prioritize and Agree on Next Steps**


Sollte sich in dem oben beschriebenen Prozess herausstellen, dass die gesammelten Anforderungen
einen sinnvollen RTDW-Projektumfang sprengen, ist ein Priorisierung erforderlich. Dazu schlägt
Kimball vor, die Geschäftsprozesse auf Basis der Anforderungskataloge in einem Treffen mit den
verantwortlichen Führungskräften nach fachlichem Nutzen und der Umsetzbarkeit hin zu priorisieren. [6]


6 Die Auswahl eines einzigen Geschäftsprozesses bedeutet natürlich nicht, dass damit auch nur eine
einzige Abteilung in dem RTDW-Projekt eingebunden ist.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 43


Abschließend sollte nicht vergessen werden, den im vorherigen Schritt (Launching and Managing
the Project / Program, siehe Kapitel 6.2) definierten Projektumfang ggfs. an diese Ergebnisse des
Business Requirements Definition anzupassen.


**6.3.8** **Zusammenfassung**


Damit stehen die detaillierten fachlichen Anforderungen als Basis für folgenden Arbeitspakete im
Kimball Lifecycle zur Verfügung. Abbildung 9.4 im Anhang C gibt einen Überblick über alle Aufgaben aus dem Bereich Business Requirements Definition und die daran beteiligten Rollen.


Zusammenfassend lässt sich festhalten, dass die Vorgehensweise für ein RTDW-Projekt im Arbeitspaket Business Requirements Definition in den meisten Punkten mit der für ein DW/BI-Projekt identisch ist. Insbesondere die Interviewleitfäden müssen aber um die spezifischen Fragen nach den fachlichen Anforderungen für das RTDW erweitert werden.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 44

#### **6.4 Technical Architecture**


Nachdem die fachlichen Anforderungen an das RTDW bekannt sind (Was soll das RTDW leisten?)
(siehe Kapitel 6.3), folgen im Kimball Lifecycle darauf aufbauend drei parallel verlaufende Zeige
(siehe Abbildung 6.5):


Das Aufsetzen einer passenden Technische Architektur für die RTDW Anwendung (samt
der dazu erforderlichen Infrastruktur).


Die Modellierung der Daten mit den dazu erforderlichen ETL-Prozessen in der Datenarchitektur.


Der Entwurf der BI-Anwendungen für den Anwender.


Wie bereits in der Einleitung erläutert, liegt der Schwerpunkt dieser Arbeit im Bereich der Technischen Architektur. Hier steht die Frage, wie die fachlichen Anforderungen technisch umgesetzt werden können, im Vordergrund.


Im folgenden wird zunächst beschrieben warum eine sorgfältige Definition der Technischen Architektur wichtig ist und welche Komponenten der Technischen Architektur eines DW/BI-Systems im
Kontext eines RTDW genauer betrachtet werden müssen.


In Kapitel 6.5 steht dann der Prozess, wie im Rahmen eines RTDW-Projektes eine passende Technische Architektur entworfen und umgesetzt werden kann, im Vordergrund.


Abbildung 6.5: TA Design und Product Selection and Installation


Kapitel 6 - Real Time Data Warehousing Projektmanagement 45


**6.4.1** **TA: Gesamtüberblick**


Die Hauptvorteile einer sauber definierten Technischen Architektur liegen in den folgenden Aspekten:


Bessere Umsetzung der fachlichen Anforderungen


Darstellung der technischen Anforderungen und ihrer Abhängigkeiten


Kommunikationswerkzeug für alle Beteiligten


Zentrale Basis für eine detaillierte Projektplanung


Flexibilität, Wartbarkeit und Skalierbarkeit der Lösung


Einfachere Einarbeitungsmöglichkeit (zum Beispiel für neue Projektmitglieder)


Kernbereiche einer Technischen Architektur für eine DW/BI-Lösung - und damit i.w. auch für ein
RTDW - sind:


ETL-Prozesse


Der Präsentationsserver mit den analytischen Daten


BI-Anwendungen und Services


Die Technische Infrastruktur


Metadaten


Sicherheitsaspekte


Somit umfasst die Technische Architektur den gesamten Datenfluss von den Quellsystemen über die
Transformationsprozesse und Datenspeicher bis zu den Anwendern.


Auch wenn viele grundlegende Aspekte der Technischen Architektur für alle DW/BI-Anwendungen
sehr ähnlich sind, ergeben sich doch auf Detailebene je nach den spezifischen fachlichen Anforderungen sehr unterschiedlichen Lösungen.


Im folgenden stehen die spezifische Anforderungen eines RTDW im Vordergrund.


In Abbildung 6.6 ist das (logisches) Gesamtmodell einer Systemarchitektur für ein DW/BI-System
dargestellt. Ausgehend von den Quellsystemen auf der linke Seite laufen die Daten durch die ETLProzesse in die Präsentationsserver. Dort werden die Daten für den Endanwenderzugriff durch die
verschiedenen BI-Werkzeuge und Anwendungen in mehrdimensionalen Datenmodellen gespeichert.
Eine wesentliche Rolle bei der Steuerung des Gesamtprozesses spielen die Metadaten. [7] Kimball geht
so weit, die Architektur für ein DW/BI-System als Metadata Driven zu bezeichnen.


7 Unter Metadaten versteht man die Informationen, die die Strukturen, Operationen und Inhalte des
DW/BI-Systems beschrieben. Kimball unterscheidet dabei zwischen technischen, fachlichen und


Kapitel 6 - Real Time Data Warehousing Projektmanagement 46


Im folgenden werden die einzelnen Bereiche der DW/BI-Architektur auf Erweiterungen bzw. Anpassungen für ein RTDW untersucht.


Abbildung 6.6: (Logisches) Gesamtmodell Systemarchitektur DW/BI-System (Kimball08)


**6.4.2** **TA: Back Room**


Im Back Room der Technischen Architektur finden die ETL-Prozesse statt. Diese extrahieren die
erforderlichen Daten zum richtigen Zeitpunkt aus den Quellsystemen, transformieren sie und schreiben sie anschließend in den Presentation Server. ETL-Tools können bei der Automatisierung wesentlich unterstützen. Trotzdem ist dies aufgrund der Vielzahl, Heterogenität, Komplexität und Dynamik
der Quellsysteme ein Bereich, der sich nicht nur beim Aufbau, sondern auch im späteren Betrieb in
aller Regel als sehr aufwendig erweist.


Kimball (Kimball08) schätzt, dass durchschnittlich ca. 70% der Entwicklungszeit für ein DW/BIProjekt dem ETL-Prozess zuzuordnen sind. Der Aufbau eines komplett neuen ETL-Prozesses für
einen Geschäftsprozess sollte demnach mit etwa 6 Monaten veranschlagt werden. Wesentliche Aufwandstreiber sind dabei:


Prozess-orientierten Metadaten. Idealerweise sind diese alle in einem zentralen Metadata Repository
gespeichert.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 47


Identifizierung und Dokumentation der Quellsysteme (Data Profiling)


Datenextraktion


Data Cleansing und Conforming


Laden der Daten in den Presentation Server


Aufsetzen eines Management Prozesses für den ETL-Prozess


Eine Detaillierung der Back Room Architecture ist in Abbildung 6.7 dargestellt.


Abbildung 6.7: Back Room Architecture DW/BI-System (Kimball08)


Der Entwurf einer Technischen Architektur mit einem ETL-Prozess, der nicht nur mit deutlich höherer Frequenz stattfindet, sondern auch wesentlich schneller durchlaufen wird, ist eine der Hauptaufgaben im Bereich der Technischen Architektur für ein RTDW-Projekt.


Im Rahmen dieser Untersuchung, soll der ETL-Process nur aus Architektursicht beleuchtet werden.
Tiefer gehende Designfragen stehen hier nicht im Fokus. [8]


8 Details hierzu finden sich zum Beispiel in (Kimball08).


Kapitel 6 - Real Time Data Warehousing Projektmanagement 48


Im Rahmen einer RTDW-Architektur müssen insbesondere folgende Aspekte im Back Room besonders berücksichtigt werden: [9]


Inwieweit erfüllt das bereits für das DW/BI-System verwendete ETL-Tool die neuen Anforderungen nach Frequenzerhöhung und Beschleunigung? Gibt es alternative Tools?


Welche internen und externen Quellsysteme werden für das RTDW (zusätzlich) benötigt?
Stellen sie die Daten in der erforderlichen Aktualität zur Verfügung? Können die Daten parallel zum Onlinebetrieb extrahiert werden?


Gibt es bereits einen Operational Data Stores (ODS), in den detaillierte operative Transaktionsdaten, zum Beispiel für ein operatives Reporting, (nahezu) in Echtzeit geladen werden?
Stellt dieser ein mögliches Quellsystem für ein RTDW dar (oder sollte er im Rahmen des
RTDW-Projektes in das RTDW integriert werden, da die technische Notwendigkeit einer
Trennung aufgrund verbesserter HW inzwischen weitgehend entfallen ist)?


Ist im Unternehmen bereits eine Service-orientierte Architektur (SOA) oder eine Enterpise
Application Integration (EAI) Architektur realisiert? Können diese in das RTDW-Projektes
einbezogen werden? Kann das RTDW an einen Message Bus oder Enterprise Service Bus,
über den operative Transaktionsdaten in Echtzeit laufen (siehe auch 4.3.3), angeschlossen
werden? Dies sind mögliche (revolutionäre) Alternativen zu dem Versuch, existierende
ETL-Batchläufe (evolutionär) zu beschleunigen.


Wie lassen sich veränderte Daten im Rahmen des Extract identifizieren? Diese Frage wurde
vermutlich bereits für das existierende DW/BI-System beantwortet. Sie muss aber für ein
RTDW präziser beantwortet werden, da es im RTDW aus Performancegründen nicht mehr
möglich ist, alle Daten, die bereits einmal den ETL-Prozess durchlaufen haben, beim nächsten ETL-Lauf in identischer Form erneut zu verarbeiten. Wird über die Einbeziehung einer
SOA oder EAI nachgedacht (s.o.), müssen eventuell ganz neue Change Data Capture Ansätze gesucht werden.


Beim Clean and Conform müssen die verwendeten Regeln auf ihre Effizienz hin überprüft
werden. Zudem ist vorzusehen, dass die Fehlerbehandlung beschleunigt werden muss, um
keinen zu großen Rückstau entstehen zu lassen.


Im Arbeitsschritt Deliver werden die Daten in den Presentation Server geschrieben. Die dazugehörigen Funktionen sind ebenfalls auf ihre Echtzeitfähigkeit hin zu überprüfen (zum
Beispiel Late arriving Data Handler, Aggregate Builder. Details siehe (Kimball08)).


Schlussendlich sind die ETL Management Prozesse an die gesenkten Latenzzeiten anzupassen. Dazu gehören insbesondere die folgenden Funktionen: Job Scheduler, Backup System,
Workflow Monitor, Problem Escalating, Paralleling and Pipelining.


9 Für eine vollständige Diskussion aller für ein DW/BI-System relevanten Back Room Aspekte siehe
(Kimball08).


Kapitel 6 - Real Time Data Warehousing Projektmanagement 49


Weisen die ETL System Data Stores und die Data Quality Data Stores auch für ein RTDW
ausreichende Kapazitäten und Performanz auf?


Sind die ETL Process Metadata (zum Beispiel ETL Operational Statistics, Quality Screen
Results) auch für die Anforderungen des RTDW ausreichend? Wurden die ETL Technical
Metadata (zum Beispiel Processing Schedules) und ETL Buisness Metadata (zum Beispiel
Data Quality Screen Specifications) angepasst?


Die Beantwortung dieser Fragen sollte die wesentlichen Änderungsbedarfe für die Back Room
Technical Architecture aufzeigen. Diese werden einen großen Teil der Aufwände für das gesamte
RTDW ausmachen.


**6.4.3** **TA: Presentation Server Architecture**


Am Ende des ETL-Prozesses werden die Daten in den Presentation Server geschrieben. Hier stehen
sie dann für Abfragen der Endanwender, für Reports und andere BI-Anwendungen zur Verfügung.
Aus fachlicher Sicht ist der Zugriff auf alle Daten für alle Anwender (eventuell aus verschiedenen
Blickwinkeln) erforderlich. Darüber hinaus sollen nicht nur aggregierte sondern auch atomare Daten
für Detailanalysen bereitstehen. Zudem sollte es nach Kimball nur einen einzigen Single Point of

Truth geben (und daher zum Beispiel keine abteilungsspezifischen Data Marts).


Um diesen Anforderungen zu genügen, muss die Presentation Server Architecture auf Atomic Level
Business Process Dimensional Models in einer relationalen Datenbank beruhen (siehe auch Abbildung 6.8).


Lassen sich Aggregate für Anwenderanalysen aufgrund des Datenvolumens nicht mehr mit realistischen Antwortzeiten zur Laufzeit zusammenstellen, müssen sie im Rahmen des Ladeprozesses vorberechnet werden. Dies stellt eine zusätzliche logische Schicht dar. Die Implementierung kann zum
Beispiel in relationalen Datenbanken oder OLAP Servern erfolgen.


Aus Sicht eines RTDW-Projektes sind im Bereich Presentation Server Architecture folgende Aspekte zu berücksichtigen:


Während die atomaren Daten aus RTDW-Sicht eher unproblematisch sind, stellt sich bei den
Aggregaten die (aus Performanceüberlegungen entscheidende) Frage, in welchen Zeitabständen welche Aggregate auf Basis welcher fachlichen Anforderungen neu generiert werden sollen. Letztendlich muss eine RTDW-Architektur hierfür eine (automatische) Optimierung auf Basis des tatsächlichen Analyseverhaltens der Anwender vorsehen.


Bei der Verwendung eines OLAP-Servers ist auch zu überlegen, ob aus Performancegründen
nicht auch die atomaren Daten in die OLAP Datenbank übernommen werden sollten.


Der Presentation Server ist kein normaler Datenbankserver. Er ist im Rahmen des DW/BISystems bereits auf die Belange mehrdimensionaler Datenmodelle ausgerichtet worden. Aus


Kapitel 6 - Real Time Data Warehousing Projektmanagement 50


RTDW-Sicht sind insbesondere Performanceaspekte zu hinterfragen: Zum Beispiel die Einrichtung zusätzlicher spezieller Hot Partitions (siehe Kimball08).


Die Presentation Server Metadata müssen auf ihre Eignung für ein RTDW hin untersucht
werden. Zum Beispiel wird es erforderlich sein, aus dem Bereich der Process Metadata die
Database Monitoring System Tables und bei den Technical Metadata die Aggregate Definitions (Wie oft sollen die Aggregates erzeugt werden?) anzupassen.


Die wesentlichen Aufwände im Bereich der Presentation Server Architecture für ein RTDW sind in
der Bereitstellung geeigneter Aggregate zu erwarten.


Abbildung 6.8: Presentation Server System Architektur DW/BI-System (Kimball08)


**6.4.4** **TA: Front Room Architecture**


Der Front Room ist die Schnittstelle des DW/BI-Systems zum Anwender und stellt somit eine Zwischenschicht für BI-Anwendungen zwischen den Daten im Presentation Server und dem Anwender
dar. Abbildung 6.9 zeigt die dazugehörigen Services und Datenspeicher.


Der Front Room muss auf die fachlichen Anforderungen ausgerichtet sein und eine intuitive Benutzerführung vorsehen, so dass die Anwender schnell finden, was sie suchen. Im Zusammenhang mit
einem RTDW ist zu untersuchen, inwieweit bereits existierende Tools und Reports in diesem Zusammenhang erweitert bzw. angepasst werden müssen.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 51


Abbildung 6.9 listet die wichtigsten BI-Anwendungen auf. Für ein RTDW ist insbesondere das Operational BI relevant. Dabei handelt es sich um Echtzeitabfragen und -analysen über den aktuellen
Status des operativen Geschäfts. Instantaneous BI (oder Enterprise Information Integration, EII) sieht
einen direkten Kanal von den operativen Quellsystemen zum Analystenbildschirm vor und zielt damit in eine ähnliche Richtung.


Abbildung 6.9: Front Room Architecture DW/BI-System System (Kimball08)


Weiter finden sich in Abbildung 6.9 die BI-Management Services. Aus RTDW Sicht sind dabei insbesondere folgende Services zu betrachten:


Usage Monitor: Hier werden Nutzungsstatistiken über das RTDW erstellt. Dies ist ein wichtiger Ausgangspunkt für die Analyse von Performanceengpässen: Woraus setzt sich die
Antwortzeit der RTDW Anwendungen zusammen? Wo gibt es Beschleunigungspotenzial?


Kapitel 6 - Real Time Data Warehousing Projektmanagement 52


Welche Real Time Aggregate werden häufig abgefragt? Welche Akzeptanz hat das RTDW
bei seinen Anwendern gefunden (Marketing)? Zeichnen sich zukünftige Performanceengpässe ab? Wie entwickelt sich das ETL-Volumen?


Query Management: Das Query Management übersetzt die Benutzerabfrage in die für den
Presentation Server passende Syntax. Hier sind im Zusammenhang mit dem RTDW Anpassungen zu erwarten. Es kommen neue Abfragen hinzu und existierende Abfragen müssen
umpriorisiert werden. Eventuell müssen spezielle User Accounts für Echtzeitabfragen mit
höherer Priorisierung eingerichtet werden. Durch das RTDW kommen neue Datenbanken
hinzu. Somit müssen die Metadaten erweitert werden, damit die für die Beantwortung einer
Abfrage benötigten Tabellen auch gefunden werden. Schlussendlich muss bekannt sein, welche (Echtzeit-) Aggregate mit welchen Eigenschaften neu hinzugekommen sind, so dass diese auch für die Beantwortung der Abfragen verwendet werden.


Enterprise Reporting: Hier müssen auf Basis der fachlichen Anforderungen ggf. neue Echtzeit-Reports definiert und in die regelmäßige, automatisierte Generierung eingebaut werden.
Auch hierbei ergeben sich möglicherweise neue Herausforderungen: Die Zeitfenster für die
Erstellung eines zeitkritischen Reports werden möglicherweise recht kurz sein. Zudem muss
der Report vielleicht zu einem Zeitpunkt am Tage erstellt werden, zu die dem Auslastung der
Systeme schon hoch ist.


Web & Portal Services: Im Zusammenhang mit einem RTDW werden Anforderungen entstehen, die die Zugriffsmöglichkeit auf das RTDW von mobilen Endgeräten vorsehen. Dies
stellt neue Herausforderungen an die Darstellung der Ergebnisse, die Navigationsmöglichkeiten und auch die Sicherheitsmechanismen.


Operational BI Write Back: Mit dem RTDW wird auch der Wunsch aufkommen, dass Entscheider nach der Analyse der Echtzeitdaten im RTDW ihre Entscheidungen direkt in Transaktionen in den operativen Systemen münden lassen können. Dieser - auch als Closed-Loop
bezeichnete - Ansatz bedeutet einen Paradigmenwechsel. Historisch war der Datenfluss aus
den operativen Systemen über den ETL-Prozess in das Data Warehouse eine Einbahnstraße.
Mit der Senkung der Latenzzeiten und der damit einhergehenden Operationalisierung der
Entscheidungen in einem RTDW erscheint eine Rückkopplungsmöglichkeit zurück in die
operativen Systeme aber sinnvoll. Dies stellt aber eine nicht zu unterschätzende neue Herausforderung an die Technische Architektur dar.


Theoretisch sollte es im Front Room keine größeren Datenspeicher geben. Der für die Datenspeicherung vorgesehene Ort ist der Presentation Server. Trotzdem tauchen in Abbildung
6.9 BI Data Stores auf. Diese werden typischerweise für eine (kurzfristige) lokale Speicherung und Weiterverarbeitung der Daten beim Anwender benötigt. Im Zusammenhang mit
dem RTDW ist zu prüfen, inwiefern Replikationsmechanismen, die die Aktualität der Daten
in den BI Data Stores gewährleisten sollen, angepasst werden müssen und können. Es sollte
aber auch darüber nachgedacht werden, diese BI Data Stores auf ein Minimum zu reduzieren, da sie aus vielen Aspekten der Idee eines zentralen Single Point of Truth zuwiederlau

Kapitel 6 - Real Time Data Warehousing Projektmanagement 53


fen. Meistens lässt sich die fachliche Anforderung, die ursprünglich zu ihrem Entstehen geführt hat, auch mit einem Enterprise Data Warehouse lösen.


Sind Downstream Systems (zum Beispiel ERP-Systeme) an das RTDW angekoppelt sind
auch hier die geänderten Anforderungen durch die Senkung der Latenzzeiten zu prüfen und
ggf. umzusetzen.


Auch im Front Room spielen Metadaten eine wichtige Rolle. Dazu gehören statistische Nutzungsdaten im Bereich der Prozess Metadaten, technische Metadaten und fachliche Metadaten. Diese sollten auch sorgfältig auf ihren Änderungsbedarf in Hinblick auf ein RTDW
überprüft werden.


Es wird deutlich, dass es auch im Bereich der Front Room Architecture zu wichtigen Erweiterungen
im Zusammenhang mit dem RTDW-Projekt kommen wird.


**6.4.5** **TA: Infrastruktur**


In diesem Abschnitt werden die für ein RTDW benötigten Infrastrukturkomponenten betrachtet.
Dazu gehören insbesondere Hardware, Netzwerke und grundlegende Sicherheitsdienste.


Im Bereich Hardware und Netzwerke ergeben sich bei sorgfältiger Analyse Beschleunigungspotenziale für ein RTDW. Grundsätzlich sollten DW/BI-Anwendungen aber lediglich als ein Abnehmer
von Infrastruktur Services im Unternehmen angesehen werden. Insofern gilt es, die im folgenden
beschriebenen Aspekte mit dem Infrastruktur Provider zu besprechen. Auch für ein RTDW ist es nur
in wenigen Ausnahmefällen sinnvoll, eine komplett eigene Infrastrukturplattform aufzubauen. Die
damit verbundenen Aufwände für Hardware, Software, Betrieb und Schulungen sind im Normalfall
unvertretbar hoch.


Auch bei Infrastrukturfragen sollten weiterhin die fachlichen Anforderungen Grundlage für alle Entscheidungen sein. Für ein RTDW ist dies in jedem Falle die Frage nach der aus den fachlichen Überlegungen abgeleiteten Latenzzeit. Aus dieser müssen sich die Infrastrukturanforderungen ergeben.
Weiterhin sollten Skalierungsüberlegungen (zum Beispiel: Wachstum der Benutzerzahlen) mit berücksichtigt werden.


Zu beachten sind allerdings im Infrastrukturbereich auch Standardisierungsbemühungen, IT-Policies
und Plattform- und Vendor-Strategien des Unternehmens.


Folgende Aspekte sollten im Zusammenhang mit einem RTDW-Projekt untersucht werden:


Data Size: Wie verändern sich die Datenvolumina durch die beabsichtigte Senkung der Latenzzeiten?


Volatility: Wie verändern sich die dynamischen Aspekte der Datenbank? Wie oft soll die
Datenbank (oder Teile derselben) aktualisiert werden? Welches Datenvolumen wird dabei
verändert? Wie lange darf der Ladeprozess dauern? Wann muss der Ladeprozess durchgeführt werden?


Kapitel 6 - Real Time Data Warehousing Projektmanagement 54


Number of Users: Kommen durch das RTDW neue Anwendergruppen hinzu? Wie wird sich
das Anwenderverhalten ändern? Wie viele Anwender werden parallel auf das RTDW zugreifen? Welche Lastspitzen sind zu erwarten?


Service Level Agreements: Für das RTDW sind gestiegene Verfügbarkeits- und Performanceanforderungen zu erwarten. Diese sollten in SLAs gefasst werden. Dazu gehören auch die
höheren Anforderungen an die verkürzten Reaktionszeiten von Service Desk und Incident
Management bei möglichen Störungen.


Die Umsetzung dieser Anforderungen für ein RTDW ist oft nur durch eine Hardwarearchitektur mit
paralleler Verarbeitung realisierbar. Dazu stehen verschiedene Varianten zur Verfügung (und wurden
vielleicht schon im Rahmen des DW/BI-Systems realisiert): Zum Beispiel Symmetric Multiprocessing (SMP) oder Massively Parallel Processing (MPP). Auf Basis der zu erwartenden Lastcharakteristika gilt es eine geeignete Variante auszuwählen. Dazu muss geklärt werden, ob eher Ad-hoc Abfragen oder mehr Standard Reports zu erwarten sind. Schlussendlich muss das DBMS die HWArchitektur nutzen können.


Eine grundsätzliche Architekturentscheidung wird die über einen separaten Datenspeicher für das
RTDW sein (siehe ODS in Kapitel 4.3.2). Es ist zu klären, wie mit Abfragen, die neben den aktuellen Daten aus dem ODS gleichzeitig (zum Beispiel historische) Daten aus dem Enterprise Data Warehouse benötigen, zu verfahren ist. Welche Replikations- und Lock-Mechanismen sollen dafür vorgesehen werden?


Entscheidende Beschleunigungspotenziale lassen sich typischerweise auch im Bereich der Platten
(I/O Bandbreiten), des Hauptspeichers und der CPUs realisieren. Dort haben sich Storage Area Networks (SAN) und RAID-Systeme bewährt. Vermutlich wurden diese schon für das bestehende
DW/BI-System angeschafft, so dass sich hier für das RTDW keine grundsätzlich neuen Überlegungen ergeben.


Auch die Frage nach der (physikalischen) Datenbankplattform (Relational oder Multidimensional/OLAP) wurde schon beim Aufbau des bestehenden DW/BI-Systems getroffen und wird im
Rahmen des RTDW vermutlich nicht erneut in Frage gestellt werden.


Es wird deutlich, dass die für das DW/BI-System aufgebaute Infrastruktur sorgsam an die Anforderungen eines RTDW angepasst werden muss, um mögliche Beschleunigungspotenziale zu realisieren.


**6.4.6** **TA: Security**


Im Bereich der Security ergeben sich durch das RTDW keine grundsätzlich neuen Anforderungen
gegenüber einem bestehenden DW/BI-System. Es wird neue Anwender(gruppen) geben. Diese lassen sich aber meist leicht in die bestehenden Strukturen abbilden. Eng damit verknüpft ist auch die
Frage der Zugriffsrechte auf die Echtzeitdaten. Aber auch diese Frage sollte sich mit den bereits zur


Kapitel 6 - Real Time Data Warehousing Projektmanagement 55


Verfügung stehenden Konzepten lösen lassen. Schließlich handelt es sich ja beim RTDW primär um
eine Senkung der Latenzzeiten und nicht um die Bereitstellung völlig andersartiger Daten.


Es muss aber zeitig eingeplant werden, wie zukünftig Backups für das RTDW organisiert werden
sollen. Insbesondere muss die Frage geklärt werden, welche Zeitfenster dafür zur Verfügung stehen
und zu welchem Zeitpunkt ein Backup (Snapshot) in einem sich ständig aktualisierenden RTDW
konsistent durchführbar ist.


**6.4.7** **Zusammenfassung**


In diesem Kapitel wurden wesentliche Fragen der Technischen Architektur im Zusammenhang mit
einem RTDW diskutiert. Der Schwerpunkt lag dabei nicht auf einer kompletten Beschreibung aller
bereits im Zusammenhang mit der DW/BI-Lösung geklärten Fragen, sondern auf den Spezifika eines
RTDW-Projektes.


Als wesentliche haben sich dabei die Bereiche


Back Room Architecture


Presentation Server


Front Room Architecture


Infrastructure


herausgestellt. Für diese wurden wichtige Fragestellungen, die es im Rahmen eines RTDW-Projektes
zu untersuchen gilt, erläutert und Lösungsansätze aufgezeigt.


Im folgenden Kapitel steht nach diesen eher Technischen Überlegungen wieder die Prozesssicht im
Vordergrund. Es wird beschrieben, auf welchem Wege man in einem RTDW-Projekt zu einem passenden Architekturplan kommt.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 56

#### **6.5 Creating the Technical Architecture Plan**


Nachdem im vorhergehenden Kapitel Komponenten und Services eine DW/BI-Architektur auf ihren
Anpassungsbedarf für ein RTDW hin untersucht wurden, steht nun darauf aufbauend der Entwurf
eines Architekturplans für ein RTDW im Vordergrund. Dabei wird wieder davon ausgegangen, das
ein DW/BI-System bereits existiert und dies zu einem RTDW erweitert werden soll. Im Vordergrund
steht also nun eine prozessorientierte Projektvorgehensweise, insbesondere beim Architekturdesign.


Dabei stellt der Architekturplan (das Hauptergebnis) die technische Übersetzung der fachlichen Anforderungen dar. Er beantwortet die Frage: Welche Funktionalitäten müssen bereitgestellt werden,
damit die Anforderungen der Anwender erfüllt werden? Dazu müssen ausgehend von den wichtigsten fachlichen Anforderungen, diejenigen Funktionalitäten einer Technischen Architektur identifiziert werden, die für Umsetzung dieser Anforderungen erforderlich sind.


Der Application Architecture Plan beschreibt die Vision für die zukünftige Struktur der RTDWArchitektur. Dabei ist davon auszugehen, dass der zu erstellende Application Architecture Plan auf
dem für das bestehende DW/BI-System aufbaut und ihn an den für das RTDW relevanten Stellen
erweitert. Für die Erstellung des Application Architecture Plan sollte ein Zeitraum von etwa 4 bis 6
Wochen eingeplant werden.


Typischerweise wird man für die Definition einer DW/BI-Architektur nur in Ansätzen auf eines der
großen Architektur-Frameworks (zum Beispiel Zachman Framework oder The Open Group Architecture Framework) zurückgreifen. Dies trifft erst recht auch für ein RTDW-Projekt zu. Wir orientieren uns daher am Architecture Development Process, wie er von Kimball in (Kimball08) vorgeschlagen wird. Zu beachten ist, dass es sich dabei prinzipiell um einen iterativen Prozess handelt, das
RTDW-Projekt aber wahrscheinlich nur eine (maximal zwei) Iteration darstellt.


Die Anwendungsarchitektur stellt nur einen Teil der Gesamtarchitektur dar. Dazu gehören auch noch
die Datenarchitektur und die Infrastruktur, die aber im Rahmen dieser Arbeit nicht weiter untersucht
werden.


**6.5.1** **Prozessschritte**


Folgende Prozessschritte sind im Rahmen des DW/BI Application Architecture Top-Down Approaches zu durchlaufen:


1. Business Requirements and Data Audit


2. Architecture Implications and Models


3. Detailed Models and Specifications


4. Product Selection and Implementation


Kapitel 6 - Real Time Data Warehousing Projektmanagement 57


Diese Schritte werden getrennt für den Back Room und den Front Room betrachtet, da diese beiden
Bereiche sehr unterschiedliche Anforderungen an die Architektur stellen.


In Abbildung 6.10 sind die für die beiden Bereiche wichtigsten Fragen im Zusammenhang mit einem
RTDW-Projekt aufgeführt.








|Col1|Back Room|Front Room|
|---|---|---|
|**Business Re-**<br>**quirements and**<br>**Data Audit**|Welche Daten sind aus fachlicher<br>Sicht in Echtzeit erforderlich?<br>Woher kommen die für das RTDW<br>erforderlichen Echtzeitdaten?|Was sind die wichtigsten Geschäfts-<br>ziele, die in Echtzeit überwacht wer-<br>den sollen?<br>Wie lassen diese sich messen und<br>analysieren?|
|**Architecture**<br>**Implications and**<br>**Models**|Welche Funktionen und Kompo-<br>nenten sind erforderlich, um die<br>Daten zum richtigen Zeitpunkt in<br>der richtigen Form am richtigen Ort<br>zu haben?<br>Welche Datenspeicher und Services<br>werden dazu benötigt?<br>Welche Metadaten sind erforder-<br>lich?|Welche Entscheider werden mit dem<br>RTDW arbeiten?<br>Welche Informationen müssen ihnen<br>in Echtzeit zur Verfügung gestellt<br>werden?<br>Welche BI-Anwendungen brauchen<br>sie zur Datenanalyse in Echtzeit?|
|**Detailed Models**<br>**and Specifica-**<br>**tions**|Was im Detail steht in den Daten-<br>speichern?<br>Welche Funktionalitäten müssen<br>die einzelnen Services genau be-<br>reitstellen?|Wie sehen die in Echtzeit zu erstel-<br>lenden Reports und Templates im<br>Detail aus?<br>Wie und wann werden sie dem An-<br>wender zur Verfügung gestellt?|
|**Product Selec-**<br>**tion and Imple-**<br>**mentation**|Welche kommerziellen Produkte<br>stellen welche der benötigten Funk-<br>tionalitäten bereit?<br>Wie lassen sich die Produkte integ-<br>rieren?<br>Wie lässt sich der ETL-Prozess<br>implementieren und betreiben?|Welche Produkte stellen die benötig-<br>ten Funktionalitäten bereit?<br>Wie lassen sich die Produkte integ-<br>rieren?<br>Wie lassen sich die vorhandenen BI-<br>Anwendungen für die Anforderungen<br>des RTDW modifizieren oder erwei-<br>tern?<br>Wie sieht der spätere Betrieb aus?|



Abbildung 6.10: DW/BI Application Architecture Top-Down Approach


Kimball schlägt im Detail folgende Vorgehensweise bei der Entwicklung des Application Architecture Plans vor (Kimball08). Wo erforderlich, wird er um die für ein RTDW spezifischen Fragestellungen ergänzt.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 58


6.5.1.1 Form an Architecture Task Force


Idealerweise sollte zumindest ein Teil der Mitglieder bereits Mitglied der Architecture Task Force
für das DW/BI-System gewesen sein. Nur so können die damals gefällten Entscheidungen und Überlegungen in die Erweiterungen für das RTDW einfließen.


6.5.1.2 Gather Architecture Related Requirements


Die spezifischen Anforderungen an die Architektur des RTDW sollten sich aus den fachlichen Anforderungen ableiten lassen. Wichtig sind insbesondere die fachlichen Erwartungen an die Aktualität
der Daten und die Granularität der geplanten Auswertungen.


Darüber hinaus sollte ermittelt werden, welche IT-Strategie das Unternehmen verfolgt (zum Beispiel
in Hinblick auf SOA und/oder EAI). Welche Infrastrukturprojekte, die Auswirkungen auf das
RTDW haben könnten, sind geplant? Welche Produkt- und Plattform-Standards sind einzuhalten?
Wo könnte es in der Infrastruktur im Zusammenhang mit dem RTDW zu Engpässen kommen? Welche Alternativen sind denkbar? Gibt es Vorgaben durch eine zentrale Architekturgruppe?


6.5.1.3 Create a Draft Architectural Implications Document


Welche fachlichen Anforderungen gibt es an die Architektur und was sind konkrete Auswirkungen
auf die Anwendungsarchitektur? Welche SLAs ergeben sich aus erhöhten Anforderungen an Performance, Verfügbarkeit und Latency?


6.5.1.4 Create the Architecture Model


Ziel dieses Schrittes ist es, in Anlehnung an die generische Abbildung 6.6 ein konkretes Modell für
die RTDW-Architektur zu entwickeln, dass die spezifischen Anforderungen des Unternehmens berücksichtigt. Dies geschieht auf Basis einer geeigneten Gruppierung der Architecture Implications
aus dem vorhergehenden Schritt 3.


6.5.1.5 Determine the Architecture Implementation Phases


Wie lassen sich die fachlichen Anforderungen phasenweise in den Lebenszyklus der Architektur
einordnen? Es ist zu erwarten, dass sich die RTDW-Architektur in einer, maximal zwei Phasen/Iterationen umsetzen lässt, da sie lediglich eine Erweiterung der bestehenden DW/BI-Architektur
bedeutet.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 59


6.5.1.6 Design and Specify the Subsystems


Hier ergeben sich für ein RTDW keine spezifischen Aufgaben, die von denen für ein DW/BI-Projekt
abweichen.


6.5.1.7 Create the Application Architecture Plan Document


Hier erfolgt eine detaillierte Beschreibung der für ein RTDW benötigten Architekturkomponenten

und Services und deren Ableitung aus den fachlichen Anforderungen.


6.5.1.8 Review the Draft


Hier ergeben sich für ein RTDW keine spezifischen Aufgaben, die von denen für ein DW/BI-Projekt
abweichen.


**6.5.2** **Select Products**


Nachdem die RTDW-Architektur definiert wurde, müssen dazu geeignete Produkte ausgewählt werden. [10] Auch der Produktauswahlprozess ist stark an den fachlichen Anforderungen auszurichten. Es
muss insbesondere ein geeigneter Zeitpunkt gefunden werden, zu dem die Anforderungen ausreichend stabil sind.


Für ein RTDW-Projekt sind Produkte aus den Bereichen HW und DBMS Plattformen sowie ETLund BI-Tools zu untersuchen. In vielen Fällen werden existierende Komponenten aus dem DW/BISystem weiterverwendet werden können.


Der Evaluationsprozess ist im wesentlichen unabhängig von den zu evaluierenden Produkten. Daher

kann im RTDW-Projekt hier auf Erfahrungen aus dem DW/BI-Projekt zurückgegriffen werden. Typischerweise werden die folgenden Schritte durchlaufen (Kimball08):


1. Understand the Purchasing Process


2. Develop the Product Evaluation Matrix


3. Conduct Market Research


4. Narrow your Options to a short List


10 Grundsätzlich ist dabei davon auszugehen, dass es effizienter ist, verfügbare kommerzielle Produkte zu kaufen und diese für die spezifischen Anforderungen zu konfigurieren, als von Grund auf
eigene Anwendungen zu bauen.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 60


5. Evaluate the Candidates


6. Recommend a Product


7. Trial


8. Contract Negotiations


Dabei werden die Performanceaspekte der untersuchten Produkte eine deutlich stärkere Rolle spielen, als dies für das DW/BI-Projekt der Fall war. Ansonsten haben die sehr hilfreichen Hinweise in
(Kimball08) weiterhin Gültigkeit.


Folgende inhaltliche Aspekte sollten bei dem Evaluationsprozess aus RTDW-Sicht speziell berücksichtigt werden (Details wurden bereits in Kapitel 6.4 vorgestellt):


Hardware Plattform: Welche Anforderungen an Skalierbarkeit, Performance und Kapazität
ergeben sich für Speicher, CPUs, Platten und Netzwerk? Können diese durch die existierende Plattform erfüllt werden? Sind Design- und Konfigurationsänderungen erforderlich? Ist
ein Testsystem erforderlich um das Lastverhalten zu simulieren?


DBMS Plattform: Sind die für das DW/BI-System gefällten Entscheidungen hinsichtlich relationalen- und mehrdimensionalen/OLAP Datenbanken weiterhin gültig? Gerade bei
OLAP-Datenbanken gibt es große Unterschiede was Skalierbarkeit und Performance angeht.
Gibt es Anpassungsbedarf im Bereich Datenmodelle, Indizes, Partitionen und Views? Welche Performanceverbesserungen bietet das RDBMS (zum Beispiel Star Join Optimization,
Bit-mapped Indizes).


ETL-Tool: Kann das vorhandene ETL-System die neuen Anforderungen an UpdateFrequenzen und Laufzeiten erfüllen?


Front Room: Können die vorhandenen BI-Tools auch für ein RTDW weiterverwendet werden? Sowohl aus funktionaler Sicht als auch aus Architektursicht? Wo sind Anpassungen für
das Standardreporting und die Ad-hoc Analysen erforderlich? Gibt es Spezialanbieter, die
bessere Lösungen anbieten? Hier sollten die zukünftigen Anwender eng einbezogen und ein

prototypisches Testsystem aufgebaut werden.


Darüber hinaus müssen die durch das RTDW erweiterten Anforderungen an das Metadaten Management untersucht werden. Auch hier geht es primär darum, Erweiterungsbedarf zum DW/BISystem zu erkennen. Die grundsätzlichen Vorteile eines Metadatenmanagements sollten zu diesem
Zeitpunkt im Unternehmen bereits akzeptiert sein und somit gibt es einen Metadatenmanager, der
sich dieser Ergänzungen am Metadatenkatalog annehmen kann. Werden im Zuge des RTDWProjektes neue Tools angeschafft, müssen diese in das Metadatenmanagement integriert werden.


Ein weiterer wichtiger Aspekt, der im Rahmen des RTDW-Projektes zu überprüfen ist, stellt das
Sicherheitskonzept für das RTDW dar. Hier sind allerdings keine wesentlichen Änderungen gegenüber dem DW/BI-System zu erwarten. Am kritischsten sind vermutlich die komplexeren Anforderungen an die regelmäßig zu erstellenden Backups.


Kapitel 6 - Real Time Data Warehousing Projektmanagement 61


Am Ende des gesamten Architekturprozesses steht die Infrastructure Map. In dieser werden alle Server-, Platten-, Netzwerk- und Desktopkomponenten mit ihren wesentlichen Softwarekomponenten
dargestellt. Sie ist ein wichtiges Kommunikationsvehikel, um alle auf Architektur und Infrastruktur
aufbauenden weiteren Prozesse - insbesondere auch den Betrieb - in geeigneter Weise zu informieren. Ein Beispiel findet sich in (Kimball08). Die Infrastructure Map stellt eine wichtige Basis für die
spätere Installation aller Komponenten dar.


**6.5.3** **Zusammenfassung**


Ein RTDW-Projekt sollte nicht ohne einen Architecture Plan durchgeführt werden. Dazu muss der
bereits für das DW/BI-System erstellte Architecture Plan in einem mehrstufigen Prozess um die Spezifika des RTDW erweitert werden. Dabei sollte darauf geachtet werden, dass die fachlichen Anforderungen die Basis für alle Entscheidungen darstellen, der Aufwand zur Erstellung des Architecture
Plans und der sich anschließenden Produktauswahl sinnvoll gewählt wird und neue Produkte einem
Praxistest unterzogen werden. Die Hauptverantwortung kommt dabei der Rolle des Technischen
Architekten für das RTDW zu. Die in diesem Zusammenhang anfallenden Aufgaben sind in Anhang
C aufgeführt. Dabei ist jeweils für das konkrete RTDW-Projekt zu überprüfen, inwieweit die Aufga
be erforderlich ist.


Kapitel 7 - Zusammenfassung und Ausblick 62

### **7 Zusammenfassung und Ausblick**


Im Rahmen dieser Arbeit wurden auf Basis der vorhandenen Literatur Erfolgsfaktoren im Projektmanagement von Real Time Data Warehouse Projekten erarbeitet. Der Hauptfokus lag dabei auf den
frühen Projektphasen Projektplanung und -management, Anforderungsanalyse und technische Architektur.


Verwendet wurde dabei ein Szenario, bei dem ein Unternehmen sein bestehendes DW/BI-System in
ein Real Time Data Warehouse erweitern möchte.


Zunächst wurden fachlichen Gründe für eine Senkung der Latenzzeiten aufgezeigt und mögliche
Architekturvarianten für ein Real Time Data Warehouse skizziert.


Aufbauend auf dem Kimball Lifecycle (Kimball08) - einer bewährten Vorgehensweise für BI- Projekte - wurden dann Bereiche identifiziert, die im Rahmen eines Real Time Data Warehouse Projektes besondere Beachtung erfordern:


Im Bereich Launching und Managing the Project/Program gilt es bei der Projektdefinition
insbesondere im Rahmen von Assess DW/BI-Readiness auf die fachliche Begründung für
ein RTDW zu achten und durch ein Data Profiling die Verfügbarkeit der erforderlichen
(Echtzeit-) Daten abzuschätzen. Zudem sollte im Rahmen der Aufgabe Develop preliminary
Project Scope/Charter darauf geachtet werden, sich zunächst auf die Real-Time Analysemöglichkeit eines einzigen (Kern-) Geschäftsprozess zu konzentrieren Eine fundierte Kosten-/Nutzenanalyse sollte Ergebnis der Aufgabe Build Business Justification sein.


Die Business Requirements Definition ist in den meisten Punkten mit der für ein DW/BIProjekt identisch. Insbesondere die Interviewleitfäden sind aber um die spezifischen Fragen
nach den fachlichen Anforderungen für das Real Time Data Warehouse zu erweitern.


Im Bereich der technischen Architektur müssen insbesondere die Bereiche Back Room
Architecture, Presentation Server und Front Room Architecture auf spezielle Anforderungen
eines RTDW-Projektes hin untersucht werden.


`o` Im Back Room sind die ETL-Prozesse und Tools an die geforderte Senkung der La
tenzzeiten anzupassen. Dies erfordert eine genaue Analyse der operativen Quellsysteme und bei einem möglichen Wechsel zu einer Datenintegrationsplattform (EAI)
die Verwendung grundsätzlich neuer Technologien im DW/BI-Zusammenhang.


`o` Für den Presentation Server steht die Frage im Vordergrund, wie häufig Aggregate

aus fachlicher Sicht neu generiert werden müssen.


`o` Die BI-Anwendungen im Front Room müssen für Echtzeitanalysen der Anwender

angepasst werden. Zudem ist zu untersuchen, wie sich Closed Loop Ansätze realisieren lassen (soweit sie aus fachlicher Sicht gewünscht sind).


Kapitel 7 - Zusammenfassung und Ausblick 63


Aus Prozesssicht ist zu beachten, dass ein RTDW-Projekt nicht ohne einen Architecture Plan
durchgeführt werden sollte. Dazu muss der bereits für das DW/BI-System erstellte Architecture Plan in einem mehrstufigen Prozess um die Spezifika des RTDW erweitert werden. Dabei sollte darauf geachtet werden, dass die fachlichen Anforderungen die Basis für alle Entscheidungen darstellen, der Aufwand zur Erstellung des Architecture Plans und der sich anschließenden Produktauswahl sinnvoll gewählt wird und neue Produkte einem Praxistest unterzogen werden.


Insgesamt wird deutlich, das Real Time Data Warehouse Projekte zwar in vielen Bereichen große
Ähnlichkeiten mit DW/BI-Projekten aufweisen und somit auf diesen aufbauen können. Im Detail
gibt es aber wichtige Erweiterungen und Ergänzungen, die sorgsam analysiert und geplant werden
müssen.


Eine sinnvolle Fortführung dieser Arbeit wäre die Erweiterung insbesondere auf die Zweige Daten
und BI-Anwendungen im Kimball Lifecycle (siehe Abbildung 5.1). Darüber hinaus ist eine detaillierte Untersuchung von Real Time Data Warehouse Projekten in der Praxis wünschenswert. Dies
würde es erlauben, die theoretischen Überlegungen mit Erfahrungen aus der Praxis abzugleichen.


Kapitel 8 - Literaturverzeichnis 64

### **8 Literaturverzeichnis**


(Anderson04) Anderson-Lehman, R., Watson, H. J., Wixom, B. H., Hoffer, J. A., Continental
Airline flies high with Real-Time Business Intelligence, MIS Quarterly Executive
3 (4), 2004.


(Atre07) Atre, S., Moss, L. T., Business Intelligence Roadmap: The Complete Project
Lifecycle for Decision-Support-Applications, Addison-Wesley, 2007.


(Bauer09) Bauer, A., Günzel, H., Data Warehouse Systeme: Architektur, Entwicklung, Anwendung, dpunkt.verlag, 2009.


(Brobst05) Brobst, S., Twelve Mistakes to Avoid When Constructing a Real-Time Data
Warehouse. In: Schelp, J., Winter, R., Auf dem Weg zur Integration Factory.
Proceedings der DW2004, Physica Verlag, 2005.


(Bucher08) Bucher, T., Dinter, B., Anwendungsfälle der Nutzung analytischer Informationen
im operativen Kontext. In: Bichler, M. et al., Multikonferenz Wirtschaftsinformatik 2008, GITO-Verlag, 2008.


(Chamoni06) Chamoni, P., Gluchowski, P., Analytische Informationssysteme: BusinessIntelligence-Technologien und -Anwendungen, Springer, 2006.


(Forrester08) Forrester, Really Urgent Analytics. The Sweet Spot For Real-Time Data Warehousing, Forrester Teleconference, 2008.


(Gluchowski08) Gluchowski, P., Gabriel, R., Dittmar, C., Management Support Systeme und Business Intelligence: Computergestützte Informationssysteme für Fach- und Führungskräfte, Springer, 2008.


(Goeken04) Goeken, M., Referenzmodellbasierte Einführung von Führungsinformationssystemen - Grundlagen, Anforderungen, Methode, Wirtschaftsinformatik 2004 (05),
2004.


(Hackathorn03) Hackathorn, R., Minimizing Action Distance, The Data Administrator Newsletter, 2003.


(Hedegard07) Hedegard, L., Teradata’s Real-Time Enterprise. Reference Architecture., Teradata, 2007.


(Hugos04) Hugos, M., Building the Real-Time Enterprise. An Executive Briefing, Wiley &
Sons, 2004.


(Inmon96) Inmon, W.H., Building the data warehouse, Wiley, 1996.


(Kemper06) Kemper, H.-G., Mehanna, W., Unger, C., Business Intelligence - Grundlagen und
praktische Anwendungen : eine Einführung in die IT-basierte Managementunterstützung, Vieweg, 2006.


(Kimball08) Kimball, R., The data warehouse lifecycle toolkit : Practical techniques for building data warehouse and business intelligence systems, Wiley, 2008.


(Langseth04) Langseth, J., Real-Time Data Warehousing: Challenges and Solutions, DSSResources.com, 2004.


(Lehmann97) Lehmann, P., Ellerau, P., Implementierung eines Data Warehouse für die Verpackungsindustrie, HMD, Heft 195, 1997.


Kapitel 8 - Literaturverzeichnis 65


(Lusti02) Lusti, M., Data Warehousing und Data Mining : Eine Einführung in entscheidungsunterstützende Systeme, Springer, 2002.


(Mucksch00) Mucksch, H.,Das Data Warehouse-Konzept: Architektur, Datenmodelle, Anwendungen, Gabler, 2000.


(Oehler06) Oehler, K., Corporate Performance Management mit Business-IntelligenceWerkzeugen, Hanser, 2006.


(Saitz02) Saitz, B., Wolbert, J., Value Reporting – Einstieg in eine neue Dimension der
kapitalmarktorientierten Unternehmensberichterstattung, Controlling 2002 (6),
2002.


(Schirp01) Schirp, G., Anforderungsanalyse im Data-Warehouse-Projekt: Ein Erfahrungsbericht aus der Praxis, HMD, Heft 222, 2001.


(Schütte01) Schütte, R., Data Warehouse Managementhandbuch : Konzepte, Software, Erfahrungen, Springer, 2001.


(Sen05) Sen, A., Sinha, A. P., A comparison of data warehousing methodologies, Communications of the ACM 48 (3), 2005.


(Töpfer08) Töpfer, J., Winter, R., Active Enterprise Intelligence, Springer, 2008.


(Turban07) Turban, E., Aronson, J., Liang, T., Sharda, R., Decision Support Systems and
Business Intelligence Systems, Prentice Hall, 2007.


(Ventana07) Ventana Research, Operational Business Intelligence - Assessing Market Trends
and the use of BI in Operations, 2007.


(Westermann01) Westermann, P., Data Warehousing, Morgan Kaufmann, 2001.


Kapitel 9 - Anhang 66

### **9 Anhang**

#### **9.1 Anhang A**


Abbildung 9.1: Teradata’s Real-Time Enterprise Reference Architecture (Hedegard07)


Kapitel 9 - Anhang 67

#### **9.2 Anhang B**


Abbildung 9.2: Übersicht aller Aufgaben und die ihnen zugeordneten Rollen aus dem Bereich Laun
ching und Managing the Project/Program (Kimball08)


Kapitel 9 - Anhang 68

#### **9.3 Anhang C**


Abbildung 9.3: Übersicht aller Aufgaben und die ihnen zugeordneten Rollen aus dem Bereich Busi
ness Requirements Definition (Kimball08)


Kapitel 9 - Anhang 69

#### **9.4 Anhang D**


Kapitel 9 - Anhang 70


Abbildung 9.4: Übersicht aller Aufgaben und die ihnen zugeordneten Rollen aus dem Bereich Tech
nical Architecture (Kimball08)


