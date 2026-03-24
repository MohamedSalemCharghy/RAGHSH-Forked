---
source_url: "https://www.hs-hannover.de/forschung/forschungsfinder-forschungsprojekte/forschungsfinder/projekt/400"
title: "Entwicklung von Energiemanagementschnittstellen für IoT-Technologien - IoT_EnRG"
crawl_date: "2026-03-07"
content_type: "html"
---

[ Hochschule  
Hannover  University of  
applied sciences  
and arts  ](https://www.hs-hannover.de/forschung/forschungsfinder-forschungsprojekte/forschungsfinder/projekt/400)
[Zum Forschungsfinder](https://www.hs-hannover.de/forschung/forschungsfinder-forschungsprojekte/forschungsfinder "Zum Forschungsfinder")
# Entwicklung von Energiemanagementschnittstellen für IoT-Technologien - IoT_EnRG
##  Projektbeschreibung 
Die Erfassung, Speicherung und Visualisierung von Energiedaten gewinnt zunehmend an Bedeutung, weil hierdurch ein Fundament für die Steigerung der Energieeffizienz und damit für die Einsparung von Energie gelegt wird. Um die Erfassung von Energiedaten zu vereinfachen, sind standardisierte Schnittstellen von besonderer Bedeutung, insbesondere beim Einsatz von IoT-Technologien im Kontext von Industrie 4.0. Im Rahmen des IoT_EnRG-Forschungsprojektes sollen Energiedatenschnittstellen für IoT-Kommunikationstechnologien konzipiert, prototypisch implementiert und getestet werden. Als Basis kommen hierfür wurden im Vorfeld beiden auf Ethernet basierenden Technologien OPC UA und MQTT sowie die Technologie IO-Link identifiziert. Im Rahmen des Projektes soll zunächst ein Kommunikationstechnologie-unabhängiges Datenmodell konzi¬piert werden. Auf Basis dieses Modells sollen dann Energieschnittstellen für die Technologien IO-Link, OPC UA und MQTT konzipiert und prototypisch implementiert werden. Anschließend sollen die prototypischen Implementierungen in einer Referenzplattform zusammengefasst werden. In dieser Plattform soll eine Abbildung (Mapping) zwischen den Energieschnittstellen der unterschiedlichen IoT-Technologien stattfinden.
  
  

#  Kurzübersicht 
  * **Laufzeit**
01.09.2020 - 31.05.2023
  * **Fakultäten**
Fak. I Elektro- und Informationstechnik 
  * **Projektleitung**
Prof. Dr.-Ing. Karl-Heinz Niemann 
  * **Drittmittelgeber**
BMWi - Bundesministerium für Wirtschaft und Energie (216.682,70 €) 
  * **Kooperations- und Verbundpartner**
Helmut Schmidt Universität / Hochschule der Bundeswehr 


## Beschreibung der Forschungsinhalte
Mit der Anwendung der Norm ISO 50001 und der einhergehenden Einführung eines Energiemanagementsystems (kurz EnMS) kann eine sukzessive Erhöhung der Energieeffizienz erreicht werden. Die für den Betrieb des EnMS erforderlichen Soft- und Hardwarekomponenten werden unter dem Begriff technisches Energiemanagement (kurz tEnMS) zusammengefasst. Die Komponenten eines tEnMS dienen zum Sammeln, Kommunizieren, Speichern, Bewerten und Anzeigen von Energieinformationen.
Im Rahmen des tEnMS werden Energieinformationen in der Feldebene bereitgestellt und müssen mittels eines Energie-SPS- oder Edge-Device-Programms ggf. im Datenformat angepasst, skaliert und auf eine etablierte Kommunikationsschnittstelle (z.B. eine OPC UA-Schnittstelle) abgebildet werden. Die auf diesem Weg verarbeiteten Daten können somit in einer adäquaten Form dem Energiemanagementsystem bereitgestellt werden. Die Erstellung dieser Energie-SPS- oder Edge-Device-Programme geht mit einem hohen Engineering-Aufwand einher, denn die Feldgeräte aus der heterogenen Feldebene stellen die Energieinformationen nicht in einer standardisierten Form bereit. Bei der Erstellung eines Energie-SPS- oder Edge-Device-Programms muss den individuellen Gerätehandbüchern entnommen werden, in welcher Semantik die Energieinformationen in Rohdatenform auf der SPS oder dem Edge-Device eintreffen. Auf Grundlage dieser Information über die Semantik muss ermittelt werden, welche Verarbeitungsschritte für die jeweiligen Energieinformationen anzuwenden sind, damit diese mit geringem Aufwand in die Energiemanagement-Anwendung einzubinden sind. Um diesem Engineering-Aufwand entgegenzuwirken, wird im Rahmen des Forschungsprojekts IoT_EnRG ein Konzept für ein universelles Energieinformationsmodell (kurz UEIM) verfolgt. Dieses Konzept sieht die Bereitstellung der Energieinformationen an das EnMS in einer semantisch standardisierten Form vor.
Abbildung 1 zeigt die Platzierung des UEIM in der Kommunikationshierarchie. Auf Ebene (1) können Feldgeräte Energieinformationen über unterschiedliche Kommunikationsschnittstellen in unterschiedlichen, teils proprietären, Semantiken bereitstellen. In den Fällen (A) und (B) werden die Energieinformationen über das jeweilige Ethernet-basierte oder nicht-Ethernet-basierte Kommunikationssystem (2) an Edge-Devices oder SPSen weitergeleitet. In der Steuerungsebene (3) kann eine Umrechnung der eingehenden Energieinformationen stattfinden, sodass die Energieinformationen auf das UEIM (4) abgebildet und über OPC UA- oder MQTT-Schnittstellen der Energiemanagement-Applikation (5) in einer standardisierten Semantik bereitgestellt werden können. In Fall (C) können IIoT-Geräte die Energieinformationen auf direktem Weg der Energiemanagement-Applikation (5) in der standardisierten Semantik des UEIM bereitstellen, da diese Geräte über geeignete Schnittstellen, wie OPC UA- oder MQTT-Schnittstellen, verfügen.
![Universelles Energieinformationsmodell in der Kommunikationshierarchie](https://www.hs-hannover.de/fileadmin/HsH/Hochschule_Hannover/Forschung/Forschung/08_Forschungscluster/Industrie_4.0/Universelles_Energieinformationsmodell_in_der_Kommunikationshierarchie.png?rbiFocus=mobile)
_Abbildung 1: Universelles Energieinformationsmodell in der Kommunikationshierarchie_
## Ziele des Forschungsprojekts
  * Vereinheitlichung von Energieinformationen (z.B. Energiezählwerte) in einem universellen Energieinformationsmodell (kurz UEIM)
  * Nutzung der Energieinformationen aus der heterogenen Feldebene, die sich durch ein Spektrum von Kommunikationssystemen (z.B. PROFINET, Modbus TCP) auszeichnet
  * Reduzierung des Engineering-Aufwands bei der Einbindung und Weiterverarbeitung auf der Steuerungsebene (z.B. auf dem Edge-Device/ der SPS)
  * Entwicklung des UEIM auch für Geräte des Industrial Internet of Things (IIoT-Devices)
  * Entwicklung des UEIM für den Einsatz von geeigneten Kommunikationssystemen wie OPC UA oder MQTT


* * *
## Allgemeine Informationen
Das IoT_EnRG-Forschungsprojekt wird im Rahmen der industriellen Gemeinschaftsforschung (IGF) gefördert und in den Forschungseinrichtungen der Helmut-Schmidt Universität / Universität der Bundeswehr Hamburg und der Hochschule Hannover bearbeitet. Die Laufzeit des Forschungsvorhabens beträgt 29 Monate (01.09.2020 bis 28.02.2023). Der Projektbegleitende Ausschuss wird durch die nachfolgend abgebildeten Partnerfirmen unterstützt.
![Projektpartner IoT_EnRG](https://www.hs-hannover.de/fileadmin/HsH/Hochschule_Hannover/Forschung/Forschung/08_Forschungscluster/Industrie_4.0/Projektpartner_IoT_EnRG.png?rbiFocus=mobile)
* * *
![Logo IoT_EnRG](https://www.hs-hannover.de/fileadmin/HsH/Hochschule_Hannover/Forschung/Forschung/08_Forschungscluster/Industrie_4.0/Logo_IoT_EnRG.png?rbiFocus=mobile)
### Ansprechpartner
Nicht-Öffentliche Person 
