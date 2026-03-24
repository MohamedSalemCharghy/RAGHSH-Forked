---
source_url: "https://f4.hs-hannover.de/fileadmin/HsH/Forms/Fakultaet_IV/Ueber_Uns/Personen/Arbeitspapiere/arb-sk-04-14.pdf"
title: "arb-sk-04-14"
crawl_date: "2026-03-07"
content_type: "pdf"
---

# **Arbeitspapier / Abteilung WI**

#### Stephan König


#### Untersuchung von Big Data Einsatzszenarien


#### am Beispiel Twitter Sentiment Analyse


#### für Anlageentscheidungen



Arbeitspapier 04-2014
ISSN Nr. 1436-1035 (print) ISSN Nr. 1436-1507 (Internet)


###### Untersuchung von Big Data Einsatzszenarien am Beispiel Twitter Sentiment Analyse für Anlageentscheidungen

April 2014


Arbeitspapier


Prof. Dr. Stephan König


Hochschule Hannover


Fakultät IV (Wirtschaft und Informatik)


Ricklinger Stadtweg 120, 30459 Hannover


stephan.koenig@hs-hannover.de


2


Zusammenfassung


Die Analyse von unstrukturierten Daten aus sozialen Netzwerken ist ein Einsatzszenario von Big


Data. Am Beispiel einer Sentiment Analyse von Twitter Kurznachrichten (Tweets) zur Unterstüt

zung von Anlageentscheidungen im quantitativen Asset Management werden verschiedene Analyse

ansätze auf Basis von R (Bag of Words Classifier, Naive Bayes Classifier) und verschiedenen Fil

termechanismen (z.B. nach der Reputation der Twitterer) untersucht. Erste Korrelationen der Stim

mungssignale mit Marktindices (DJIA, NASDAQ) über mehrere Monate deuten deren Eignung für


Marktprognosen - und damit zur Unterstützung von Analyseentscheidungen - an. Damit liegt eine


Basis für die Untersuchung deutlich längerer Zeitreihen vor.


3


1. Einführung


Unter Big Data werden große und oft unstrukturierte, aber für unternehmerische Fragestellungen


zunehmend interessante Datensammlungen bezeichnet. Diese können mit traditionellen Business


Intelligence Anwendungen meist nur unzureichend analysiert werden. Mit der Verfügbarkeit geeig

neter Technologien (z.B. Apache Hadoop [1] ) sind Fragen zu fachlich sinnvollen Einsatzszenarien in


den Vordergrund gerückt und werden in Forschung und Praxis untersucht (z.B. in [Buhl13], [We

ber12] und [Manyika12]).


Aufgrund der Aktualität der Thematik gibt es noch keine einheitliche Definition des Begriffs Big


Data. Eine weit verbreitete Definition von Big Data lautet [Manyika12]: “Big data refers to datasets


whose size is beyond the ability of typical database software tools to capture, store, manage, and


analyze”. Charakteristisch für Big Data sind die sogenannten 3 V’s (siehe Abbildung 1): Velocity,


Volume und Variety. Big Data zeichnet sich durch ein großes Datenvolumen aus (Volume), ein gro

ßes Spektrum möglicher Strukturen der Daten (Variety) und die Geschwindigkeit, mit der die Daten


erzeugt und verarbeitet werden (Velocity). Eine wichtige Datenquelle für Big Data stellen soziale


Netzwerke im Internet (z.B. Facebook) dar. Welche Potenziale in der Analyse von Daten aus sozia

len Netzwerken liegen, zeigen unter anderem [Lau12] und [Chau12].


Zur Speicherung und Verarbeitung von Big Data wird häufig Apache Hadoop, ein freies, in Java


geschriebenes Framework für skalierbare, verteilt arbeitende Software, verwendet. Es besteht aus


zwei Kernbausteinen:


  - Hadoop Distributed File System (HDFS): Ein hochverfügbares, leistungsfähiges Dateisystem


zur verteilten Speicherung sehr großer Datenmengen auf mehreren Rechnern.


  - MapReduce: Ein von Google eingeführtes Programmiermodell für nebenläufige Berechnun

gen über große Datenmengen auf Computerclustern.


1 hadoop.apache.org


4


Oft kommen zur Verarbeitung von Big Data aber auch Anwendungen aus der statistischen Daten

analyse wie z.B. R oder SAS zum Einsatz.


Abbildung 1: 3 V Modell für Big Data [Klein13]


Big Data weist eine starke inhaltliche Nähe zum Thema Business Intelligence auf. Letzteres dient


primär zur Aufbereitung, Speicherung und Analyse strukturierter Daten auf Basis eines klassischen


Data Warehouses. Big Data wird häufig als ETL-Anwendung [2] zur Voranalyse und Quantifizierung


unstrukturierter Daten betrachtet ([Weber12], [Kimball11]). Das Thema Big Data findet sich auf

grund seiner gesellschaftlichen Relevanz seit Anfang 2013 auch zunehmend in der Presse wieder


(z.B. Titelthema in DER SPIEGEL 20/2013). Dieser Trend wurde durch die Aufdeckung des PRISM


Programms der NSA im Juni 2013 noch einmal verstärkt [Green13]. Dass es sich bei dem Thema


nicht nur um eine Modeerscheinung handelt, sondern die grundsätzliche Frage adressiert wird, wie


wir mit immer größer werdenden Datenmengen in Zukunft umgehen wollen, bezeugen z.B. Untersu

chungen von Gartner [Pettey12], des Bundesverbandes Informationswirtschaft, Telekommunikation


2 Extraktion, Transformation, Laden


5


und neue Medien e.V. (BITKOM) [Weber12] und von Buhl et al. [Buhl13]. Aus Sicht der Wissen

schaft wirft das Thema viele interessante Fragestellungen in den Bereichen Datenmanagement, Da

tenanalyse, Datenqualität und Datenschutz auf. Insbesondere ist aber auch zu klären, was geeignete


betriebswirtschaftliche Fragestellungen sind, die mit Big Data untersucht werden können: „Welche


Zusammenhänge in den Daten bestehen, welche Auswirkungen diese haben und was aus den aufbe

reiteten Daten gewonnen werden kann, übersteigt oft menschliches Fassungsvermögen und neue


Verfahren müssen entwickelt werden, die dies greifbarer machen können“ [Klein13]. Die Wirt

schaftsinformatik mit ihrer Methodenvielfalt und ihrem multidisziplinären Forschungsansatz kann


ideal zur Weiterentwicklung von Big Data beitragen [Buhl13].


6


2. Vorgehen

Im Folgenden soll im Rahmen einer Fallstudie untersucht werden, inwieweit sich Big Data Techno

logien in der unternehmerischen Praxis sinnvoll einsetzen lassen. Dazu wurde ein Unternehmen aus

gewählt, das zu den international führenden quantitativen Asset Managern gehört und für institutio

nelle Anleger seit mehr als 15 Jahren ein erfolgreiches aktives Portfolio Management in den Asset

Klassen Aktien, Renten und Multi Asset Strategien betreibt. Die Finanzbranche eignet sich wegen


des vorhandenen Mitarbeiter Know-Hows und der verfügbaren Daten insbesondere für eine exemp

larische Untersuchung der Einsatzszenarien von Big Data in der Praxis, da sie eine Schlüsselbranche


für moderne Analyseansätze und Big Data darstellt [Manyika12]. Konkret soll die Frage untersucht


werden, inwieweit sich Big Data Technologien eignen, um unstrukturierte Daten aus sozialen Netz

werken (Web 2.0) für Anlageentscheidungen zu nutzen. Dazu wird prototypisch eine Big Data An

wendung (Artefakt) realisiert. Damit folgt die Fallstudie dem Design Science Ansatz (siehe z.B.


[Hevner04], [Winter09] und [Buhl12]). In [Chau12] wird für eine vom Forschungsansatz und The

menumfeld vergleichbare Fragestellung erläutert, wie die in [Hevner04] aufgeführten sieben Richtli

nien [3] für Design Science adressiert werden. Diese Erläuterungen können für diese Fallstudie sinn

gemäß übernommen werden.


Die Vorgehensweise zur Beantwortung der fachlichen Fragestellung gliedert sich - nach einem


Überblick über den Stand der Forschung - in folgende Schritte:


  - Identifikation eines geeigneten sozialen Netzwerkes


  - Aufbau einer Anwendung zur Sammlung unstrukturierter Daten


  - Quantifizierung und Analyse der Daten


  - Untersuchung der Eignung der Daten für Anlageentscheidungen


  - Bewertung der Ergebnisse


3 Design as an Artifact, Problem Relevance, Design Evaluation, Research Contributions, Research Rigor, Design as a
Search Process, Communication of Research.


7


3. Sentiment Analyse in sozialen Netzwerken

Ein soziales Netzwerk ist eine „im Zuge des Web 2.0 entstandene, virtuelle Gemeinschaft, über die


soziale Beziehungen via Internet gepflegt werden können“ [Gabler14]. Die dabei entstehenden In

halte weisen typische Charakteristika von Big Data auf: Die erzeugten Texte sind ein Beispiel für


unstrukturierte Daten (Variety). Es werden sehr große Datenmengen erzeugt (Volume). Die Inhalte


müssen je nach Anwendungsszenario nahezu in Echtzeit analysiert werden (Velocity). Das bekann

teste soziale Netzwerk ist Facebook, dessen Data Warehouse bereits 2010 ein Volumen von 15 PB


aufwies und in dem täglich mehr als 60 TB unstrukturierte Daten u.a. mit Hadoop verarbeitet wur

den [Ashish10].


Welche Potenziale in der Analyse von sozialen Netzwerken liegen, zeigen z.B. [Asur10], [Dodds10],


[Lau12] und [Chau12]: Lau et al. [Lau12] integrieren soziokulturelle und politische Aspekte aus


sozialen Netzwerken in eine Scorecard für Unternehmensfusionsentscheidungen. Chau et al.


[Chau12] entwickeln am Beispiel von zwei Fallstudien (Apple’s Ipod und Starbucks) ein Framework


zur Analyse von Blogs, mit dem sich u.a. Meinungsmacher und Netzwerkstrukturen identifizieren


lassen.


Eine Herausforderung bei der Analyse sozialer Netzwerke ist die automatisierte Verarbeitung sehr


großer Textmengen. In diesem Zusammenhang müssen die qualitativen und unstrukturierten Infor

mationen in den Texten quantifiziert werden, damit sie sich für anschließende Analysen eignen


[Russell11]. Besonders interessant ist dabei die in den Texten zum Ausdruck kommende Stimmung


(Sentiment). Stimmungskennzahlen lassen sich insbesondere mit Verfahren des Text Mining ermit

teln. Man spricht in diesem Zusammenhang auch von Sentiment Analysen (bzw. Sentiment Analy

tics), Sentiment Mining oder Opinion Mining. Beispiele finden sich in [Antweiler01], [McDo

nald11], [Pang02] und [Burdick11].


Stimmungen spielen auch bei Anlageentscheidungen auf Finanzmärkten eine Rolle. Zahlreiche Stu

dien zeigen, dass Aktienpreise nur bedingt der Theorie des vollkommenen Marktes [Fama65] folgen,


8


sondern im Sinne der Verhaltensökonomie [Nofsinger05] durch menschliche Stimmungen beein

flusst und damit zumindest in Ansätzen vorhersagbar werden [Qian07].


Ein klassischer Stimmungsindikator ist der Ifo Geschäftsklimaindex [4], der monatlich die gegenwärti

ge Geschäftslage und die Erwartungen für die nächsten sechs Monate von ca. 7000 deutschen Unter

nehmen wiederspiegelt. In [Henzel13] und [Abberger07] wird gezeigt, wie sich dieser Indikator für


Prognosen nutzen lässt. Moderne Verfahren der Textanalyse erlauben es, vergleichbare Indikatoren


auf Basis sozialer Netzwerke automatisiert und nahezu in Echtzeit zu ermitteln, womit sie sich bes

ser für Anlageentscheidungen eignen. Beispiele finden sich z.B. in [Chen14], [Tetlock08],


[Demers10], [Gilbert10], [Tetlock10], [Gloor11], [Aase11] und [Zhang10a]. Neben sozialen Netz

werken eignen sich auch (Wirtschafts-)Nachrichten für eine automatisierte Analyse ([Mitram11],


[Devitt07]). Dass sich in der quantitativen Finanzmarktanalyse auch Stimmungsfaktoren zunehmend


etablieren, zeigt deren zunehmende Einbindung in kommerzielle Marktanalysesysteme wie z.B.


Eikon [Lunden14].


Ein soziales Netzwerk, das sich insbesondere für Sentiment Analysen eignet, ist Twitter [5] . Dabei


handelt es sich um einen 2006 gegründetes und seit 2013 an der NYSE notiertes Unternehmen, des

sen gleichnamige Anwendung es Benutzern erlaubt, maximal 140 Zeichen lange Kurznachrichten


(Tweets) in Echtzeit öffentlich im Internet zu verbreiten. Im Oktober 2012 wurden täglich etwa 500


Millionen Tweets weltweit versendet [Holt13]. Twitter erlaubt über APIs einen kostenlosen Echt

zeitzugriff auf die Tweets mit der Möglichkeit der Filterung. Beispiele für Sentiment Analysen auf


Basis von Twitter finden sich z.B. in den folgenden Veröffentlichungen: [Kumar13], [Pak10],


[Agarwal11], [Wood12], [Moreno13], [Jmal13], [Helmholz11], [Jansen09] und [Jiang11]. Speziell


auf Sentiment Analysen in der Finanzindustrie ausgerichtet sind folgende Veröffentlichungen:


[Ruiz12], [Yang13a], [Sprenger10], [Zhang13], [Xu12], [Bollen11], [Chen11] und [Zhang10b].


4 cesifo-group.de
5 twitter.com


9


Eine häufig zitierte Veröffentlichung ist dabei die von Bollen et al. [Bollen11]. Darin wird gezeigt,


dass “the accuracy of DJIA [6] predictions can be significantly improved by the inclusion of specific


public mood dimensions but not others. We find an accuracy of 86.7% in predicting the daily up and


down changes in the closing values of the DJIA”. Diese Ergebnisse basieren auf einer Analyse von


knapp 10 Millionen Tweets im Zeitraum Februar bis Dezember 2008. Die Tweets wurden nach ex

pliziten Stimmungsäußerungen (z.B. „I feel“) ausgewählt. Bereiche guter Überlappung zwischen


dem DJIA und dem Stimmungsverlauf sind in Abbildung 2 (oben) grau hinterlegt. In statistischen


Analysen wird gezeigt, dass bestimmte Stimmungsverläufe (Calm z-score) die DJIA Schlusswerte


drei Tage im voraus vorhersagen können.


Abbildung 2: DJIA Verlauf (DJIA z-score, Mitte), Twitter Stimmungsverlauf


(Calm z-score, unten) und deren Korrelation (oben) [Bollen11]


6 Dow Jones Industrial Average


10


Diese Ergebnisse motivierten P. Hawtin, einen Hedge Fund (The Derwent Absolute Return Fund


Ltd.) aufzulegen, der seine Anlageentscheidungen insbesondere aus Twitter Stimmungen ableitet


[Jordan10].


Abbildung 3 zeigt eine klassische Architektur für eine Sentiment Analyse aus [Mitram11]. Links


finden sich mögliche Datenquellen z.B. aus dem Bereich Web 2.0 Social Media. Nach einer Pre

Analysis (i.w. Maßnahmen zur Steigerung der Datenqualität) findet die eigentliche Quantifizierung


statt, indem die unstrukturierten Daten klassifiziert (z.B. in Nachrichten mit einer positiven oder ne

gativen Stimmung) und daraus Stimmungsindikatoren (Sentiment Scores) berechnet werden. Diese


werden im Folgenden z.B. mit Marktindices (z.B. DJIA) (Numeric financial market data) korreliert


(Analysis), um daraus Vorhersagen zu Marktentwicklung (Return predictions) und letztendlich An

lageentscheidungen (Fund management decisions) abzuleiten.


Abbildung 3: Klassische Architektur für eine Sentiment Analyse [Mitram11]


11


4. Auswahl eines geeigneten sozialen Netzwerkes


Für die Fallstudie muss zunächst eine geeignete Datenquelle identifiziert werden. Mit Twitter und


Facebook werden zwei klassische soziale Netzwerke untersucht. Zusätzlich wird Google Trends mit


in die Untersuchung aufgenommen, um festzustellen, ob hier bereits (vor)analysierte Informationen


verfügbar sind. Die Analyse erfolgt am Beispiel des Selbstmordes von Pierre Wauthier, Group CFO


der Zurich Insurance Group, am 26.08.13.


4.1 Google Trends


Google Trends liefert Informationen darüber, welche Suchbegriffe bei Google im Zeitverlauf wie oft


eingegeben werden. Damit ließen sich prinzipiell Stimmungsverläufe im Internet verfolgen und bei


Anlageentscheidungen berücksichtigen. Abbildung 4 zeigt den Verlauf für den Suchbegriff „Zurich“


im relevanten Zeitraum (August 2013). Zwar wird eine deutliche Steigerung des Interesses deutlich.


Weitere Details, sind aber nicht erkennbar (Zum Beispiel: In welchem (Stimmungs-)Kontext wurde


nach dem Begriff gesucht?) Erschwerend kommt hinzu, dass für viele Aktien – z.T. auch mit sehr


großer Marktkapitalisierung (z.B. Fukuoka Financial Group Inc.) – bei Google Trends keine Infor

mationen verfügbar sind („Das Suchvolumen ist zu gering“). Auch gibt es für Google Trends kein


offizielles API, das eine automatisierte Analyse der Daten im größeren Umfange ermöglichen wür

de. Somit schneidet Google Trends als mögliche Datenquelle aus.


Abbildung 4: Google Trends Verlauf für den Suchbegriff „Zurich“ im Zeitraum August 2013


12


4.2 Facebook


Auch bei Facebook finden sich zeitnah Informationen zum untersuchten Ereignis (siehe Abbildung


5). Informationen bei Facebook lassen sich per Graph API automatisiert auswerten. Allerdings ist


der Zugriff auf öffentliche Informationen beschränkt, was eine breit angelegte Stimmungsanalyse


erschwert, weil z.B. Firmenseiten häufig nur gefilterte Informationen bereitstellen und Informatio

nen von Privatpersonen in aller Regel nicht frei zugänglich sind. Zwar gibt es bei Facebook ein


Public Feed API und Keyword Insights API. Diese sind aber „restricted to a limited set of media


publishers“ [7] wie z.B. CNN. Somit scheidet (z.Zt.) auch Facebook als mögliche Datenquelle aus.


Abbildung 5: Informationen zum Tode von P. Wauthier bei Facebook


7 developers.facebook.com/docs/keyword_insights


13


4.3 Twitter


Die SEC erlaubt börsennotierten Unternehmen seit 2013, in Twitter über börsenrelevante Nachrich

ten zu informieren [Gallu13]. So gibt es - mit einem Tag Verzögerung - auch einen Tweet von Zu

rich zum Tode von P. Wauthier (siehe Abbildung 6). Noch zeitnäher wurden Tweets von Nachrich

tenagenturen und -sendern wie z.B. CNBC versendet (siehe Abbildung 7).


Wie in Abschnitt 3 dargestellt, wird für Analysen sozialer Netzwerke häufig Twitter als repräsentati

ves Beispiel verwendet, da es viele Vorteile vereint: Die Tweets sind öffentlich und in Echtzeit zu

gänglich. Die hohe Anzahl an Tweets ermöglicht für viele Untersuchungen eine ausreichende Da

tenbasis. Die maximale Länge der Tweets von 140 Zeichen reduziert die Komplexität der Text Mi

ning Analysen. Mit dem Search API und Streaming API stehen zwei Zugriffsmöglichkeiten zur Ver

fügung, die sich technisch gut umsetzen lassen. Einschränkungen ergeben sich nur aus der Tatsache,


dass es keinen freien Zugriff auf historische Tweets (Archiv) gibt und die APIs Volumenbeschrän

kungen unterliegen. Beide Einschränkungen lassen sich durch kostenpflichtige Angebote von autori

sierten Drittanbietern aufheben (z.B. Gnip und DataSift). Insgesamt stellt Twitter aber eine für die


folgenden Untersuchungen sehr gut geeignete Datenquelle dar.


Abbildung 6: Offizieller Zurich Tweet zum Tode von P. Wauthier bei Twitter


Abbildung 7: Tweets von Nachrichtenagenturen und -sendern zum Tode von P. Wauthier


14


4.4 Eignung verschiedener Asset Klassen für Stimmungsanalysen mit Twitter


Im Rahmen der Voruntersuchungen wurde abschließend die Frage adressiert, welche Asset-Klasse


(Einzelaktien oder Aktienindices) sich im aktiven Portfolio Management insbesondere für Stim

mungsanalysen mit Twitter eignt. Dazu wurde über das Twitter Search API (Garden Hose. Für De

tails siehe Abschnitt 5) das Tweet Volumen für verschiedene Suchbegriffe ermittelt. Für Aktienin

dices wurde nach Tweets gesucht, die Begriffe wie Stock, Stocks, Stock Market, Dow Jones und


DJIA enthalten, da diese eine Gesamtstimmung vermitteln. Für Aktien wurden Tweets zu einzelnen


Unternehmen, die eine hohe Marktkapitalisierung aufweisen, gesammelt. Die Ergebnisse sind in den


Abbildungen 8 und 9 zusammengefasst.


Abbildung 8: Anzahl der Tweets pro Stunde für Suchbegriffe im Bereich Aktienindices


Abbildung 7: Anzahl der Tweets pro Stunde für Unternehmen mit hoher Marktkapitalisierung


15


Es wird deutlich, dass selbst für - nach Marktkapitalisierung - sehr große Unternehmen (z.B. Fukuo

ka Financial Group Inc.) oft nur eine sehr geringe Anzahl von Tweets versendet werden. Für Such

begriffe aus dem Bereich Aktienindices ist hingegen eine für statistische Auswertungen ausreichen

de Anzahl von Tweets zu erwarten. Daher werden im folgenden Tweets zu den folgenden Suchbe

griffen gesammelt: volatility, inflation, equity, emerging markets, central bank, stocks, stock market,


crisis, economy.


Andere Suchbegriffe (z.B. stock) haben sich nicht als sinnvoll erwiesen, da sie z.T. in sehr unter

schiedlichen Kontexten verwendet werden (z.B. „Coke is out of stock“).


Eine Sentiment Analyse für einzelne Aktien erscheint deutlich komplexer. Für einen Großteil der


Unternehmen wäre es erforderlich, eine Beziehung zwischen den Endverbraucherprodukten (z.B.


Lucky Strike), denn nur für diese gibt es eine ausreichende Anzahl Tweets, und dem Unternehmen


(in diesem Falle British American Tobacco) aufzubauen. Dieser Ansatz wird im Rahmen dieser Fall

studie nicht weiter verfolgt.


16


5. Twitter Streaming API

Zur Sammlung von Tweets wird im Folgenden der Public Stream des Twitter Streaming APIs (Ver

sion 1.1) [8] verwendet. Das Search API [9] erwies sich nicht als sinnvoll, da es aufgrund der Rate Limits


bei Suchbegriffen mit einer großen Antwortmenge zu Unterdeckungen auf der Zeitachse kommt.


Das Twitter Streaming API wurde in Java unter Verwendung der Java Library twitter4j [10] implemen

tiert. Zur Authentifizierung wurde OAuth [11] (Application Only Authentication) verwendet. Da die


durch die o.g. Suchbegriffe zurückgelieferte Anzahl an Tweets unter dem Public Streaming Cap [12]


(etwa 1% aller 500 Millionen Tweets pro Tag) verbleibt, werden ALLE Tweets bereitgestellt, die die


Suchbegriffe enthalten. Zu jedem Tweet werden die folgenden Attribute (durch #+# getrennt) in ei

nem txt File aufgezeichnet:


  - status.getCreatedAt()


  - status.getRetweetCount() [13]


  - status.getIsoLanguageCode()


  - status.getUser().getId()


  - status.getUser().getScreenName()


  - status.getText()


Ein aufgezeichneter Tweet sieht damit wie folgt aus:

```
Fri Apr 11 09:05:16 CEST 2014#+#0#+#en#+#374806861#+#FrequentFinance#+#Fitch up
grades Portugal's outlook: In the second half of last year, the economy pulled

out of recession to sho... http://t.co/6kBAourkF4#+#

```

8 dev.twitter.com/docs/api/streaming
9 dev.twitter.com/docs/using-search
10 twitter4j.org
11 dev.twitter.com/docs/auth/oauth
12 dev.twitter.com/docs/faq#6861
13 Wird von Twitter im Streaming API nicht befüllt.


17


Zu beachten ist, dass die Suchbegriffe aufgrund der Funktionsweise des Streaming APIs nicht zwin

gend im Tweet selber auftreten müssen, sondern evtl. erst auf der verlinkten Webseite vorhanden


sein können.


Im Zeitraum 06.12.13 bis 24.04.14 wurden so ca. 20.2 Millionen Tweets gesammelt. Das entspricht


etwa 3 GB unkomprimierter Textfiles. Abbildung 8 zeigt den gemittelten Verlauf der Anzahl der


Tweets pro Tag. Die Anzahl wurde wegen deutlicher Schwankungen im Wochenzyklus über die


letzten 7 Tage gemittelt. Man erkennt, dass es zu den o.g. Suchbegriffen ca. 100.000 bis 200.000


Tweets pro Tag gibt. Der deutliche Anstieg in der Anzahl der Tweets pro Tag Ende Februar 2014 ist


auf die zeitgleichen politischen Ereignisse in der Ukraine zurückzuführen.


Abbildung 8: Gemittelte Anzahl der Tweets pro Tag zu den verwendeten Suchbegriffen


im Zeitraum Dezember 2013 bis April 2014.


18


6. Twitter Sentiment Analyse


Zur Ermittlung einer Stimmung müssen die Tweets klassifiziert werden, d.h. pro Tweet wird ein


Stimmungswert ermittelt (z.B. positiv/negativ/neutral). Dazu bieten sich verschiedene Verfahren an.


Verwendet werden im Folgenden der Bag of Words (oder Naive) Classifier und der Naive Bayes


Classifier. Dies sind einfache, aber sehr robuste und weit verbreitete Verfahren [Mitram11]. Kom

plexere Verfahren wie z.B. Support Vector Machines (SVM) werden nicht verwendet. Aufgrund der


beschränkten Zeichenanzahl [14] enthalten Tweets im Schnitt nur ca. 10 bis 12 Wörter. Damit ähneln


sie eher Überschriften als komplexen Texten, weshalb die gewählten einfacheren Analyseverfahren


ausreichend sein sollten.


Die Analysen wurden mit R (Version 3.0.2) auf einem 64 bit Windows 7 PC mit 32 GB RAM und


einem Intel Xenon Prozessor (E5-2643 mit 3.3 GHz) durchgeführt. Dabei nahmen komplexere Ana

lysen über längere Zeiträume („einige Wochen“) „einige Stunden“ in Anspruch. Die Verwendung


einer Hadoop Architektur war daher bisher nicht erforderlich. Erst bei der Analyse längerer Histo

rien („Jahre“) und komplexerer Analysemodelle könnte dies in Zukunft notwendig werden.


6.1 Bag of Words Classifier


Die Grundidee des Bag of Words Classifiers besteht darin, den Wörtern eines Tweets Stimmungs

werte zuzuordnen und daraus einen Sentiment Score pro Tweet zu bestimmen (siehe auch Abbildung


9). Dieser kann im einfachsten Fall die Klassen positiv, negativ und neutral umfassen oder – wie im


folgenden verwendet – die Summe der Stimmungswerte der einzelnen Wörter des Tweets sein [15] . Der


Bag of Words Classifier setzt die Existenz eines Lexikons für positive und negative Wörter voraus.


Idealerweise ist das verwendete Lexikon domänenspezifisch, da Wörter in unterschiedlichen Kon

texten unterschiedliche Bedeutungen haben können. So ist „vice president“ im Wirtschaftskontext


ein neutraler Begriff, währen „vice“ (= Laster) sonst eher negative belegt ist. Standardmäßig werden

14 Maximal 140 Zeichen
15 Also z.B. +2, wenn der Tweet 4 positive und 2 negative Wörter (mit jeweiligem Gewicht 1) enthält.


19


im Folgenden die Wortlisten von McDonald [McDonald11] mit etwa 2700 Wörtern (2329 negative


und 354 positive Wörter) verwendet [16] . Diese wurden speziell für die Finanzbranche entwickelt.


Abbildung 9: Grundidee des Bag of Word (oder Naive) Classifiers [Jurafsky]: Die positiven und


negativen Wörter im zu betrachtenden Text werden identifiziert und bewertet. In diesem Beispiel


sind die Wörter unterschiedlich stark gewichtet.


Anschließend werden die Stimmungen aller Tweets eines Tages [17] zu einer Tagesstimmung zusam

mengefasst. Im einfachsten Falle geschieht dies durch die Bildung des arithmetischen Mittelwertes.


Die Sentimentberechnungen werden in R durchgeführt. Dazu wird die Score Sentiment Funktion


von Breen aus [Elder12] verwendet [18] . Zu identischen Ergebnissen gelangt man, wenn man mit dem


Text Mining Paket tm in R [19] unter Verwendung eines Dictionaries (= Lexikon) eine Term-Document


16 Diese stehen unter www3.nd.edu/~mcdonald/Word_Lists.html zum Download zur Verfügung.
17 Wenn im Folgenden von einem Tag die Rede ist, ist damit ein Kalendertag in New York City gemeint.
18 Der Code steht auch auf Github zum Download zur Verfügung: github.com/jeffreybreen/twitter-sentiment-analysistutorial-201107
19 Eine Einführung zum tm Package findet sich hier: cran.r-project.org/web/packages/tm/vignettes/tm.pdf


20


Matrix bildet und auf diesem Wege die Stimmungen berechnet. Da die Matrix nur sehr dünn besetzt


ist, benötigt dieses Verfahren allerdings mehr Hauptspeicher (RAM).


Ein mit dem Bag of Words Classifier ermittelter Stimmungsverlauf ist in Abbildung 10 dargestellt.


Folgende Konfigurationsparameter wurden dazu verwendet:


- Score Sentiment Funktion: Breen [Elder12]


- Sentiment Funktion: Arithmetisches Mittel (Mean)


- Lexikon: McDonald [McDonald11]


- Tweets zu allen Suchbegriffen (s.o.)


- Mittelung über 9 Tage


Erkennbar ist eine deutliche Verschlechterung der Stimmung ab dem 22.02.14. Dies entspricht dem


Datum der Absetzung von W. Janukowytsch, dem Ministerpräsidenten der Ukraine und damit dem


Beginn der Ukraine Krise. In Abbildung 8 ist in diesem Zeitraum eine spürbare Zunahme in der An

zahl der Tweets erkennbar.


Abbildung 10: Stimmungsverlauf. Weitere Erläuterungen finden sich im Text.


21


Um die Abhängigkeit des Stimmungsverlaufs von verschiedenen Einflussfaktoren besser beurteilen


zu können, wird nun der Einfluss der Parameter Lexikon, Sentimentfunktion, Suchbegriffe und Re

putation der Twitterer untersucht.


6.1.1 Bag of Words Classifier - Lexikon


Neben dem bisher verwendeten Lexikon von McDonald [McDonald11] stehen weitere Lexika zur


Verfügung [20] . Im Zusammenhang mit Sentiment Analysen im Bereich der Sozialwissenschaften wird


zum einen häufig das Harvard-IV-4 Dictionary [21] genutzt. Es umfasst 4206 Wörter (1915 positive


und 2291 negative Wörter) und wurde z.B. in [Tetlock08] verwendet. Häufig zum Einsatz kommt


auch das Opinion Lexikon [22] von Hu et al. [Hu04] mit ca. 6800 Wörtern. Dies wird z.B. in [Jiang11]


verwendet. Vergleicht man die mit den drei verschiedenen Lexika ermittelten Stimmungskurven


(siehe Abbildung 11), wird deutlich, dass diese sehr ähnlich Verläufe aufweisen. Für alle drei Stim

mungskurven wurde die Score Sentiment Funktion von Breen verwendet, die Sentiment Funktion


Arithmetischer Mittelwert (Mean) und Tweets zu allen Suchbegriffen. In diesem Fall wurde keine


Mittelung der Sentimentwerte über mehrere Tage durchgeführt.


Aufgrund der spezifischen Ausrichtung auf die Finanzbranche wird bei allen folgenden Untersu

chungen das Lexikon von McDonald verwendet. Wegen seines deutlich geringeren Wortumfangs im


Vergleich zu den anderen Lexika weist es zudem Performancevorteile auf.


20 Für eine Sentiment Analyse ohne vordefiniertes Lexikon siehe den Abschnitt zum Naive Bayes Classifier.
21 Die positiven und negativen Wortlisten finden sich unter www.wjh.harvard.edu/~inquirer/homecat.htm
22 Die positiven und negativen Wortlisten von Hu finden sich unter www.cs.uic.edu/~liub/FBS/sentiment-analysis.html


22


Abbildung 11: Stimmungsverläufe für die verschiedenen Lexika


von McDonald (unten), Hu (Mitte) und Harvard (oben) .


6.1.2 Bag of Words Classifier – Sentimentfunktionen

Prinzipiell können Stimmungskennzahlen durch verschiedene Sentimentfunktionen berechnet wer

den. Um deren Auswirkungen auf die Stimmungsverläufe zu untersuchen, werden folgende Senti

mentfunktionen definiert:


McD = Mean(All)


McD1 = -N/(P+N)


McD2 = (P-N)/(P+N)


McD3 = log((1+P)/(1+N))


McD4 = P/N


Wobei Mean(All) das arithmetische Mittel aller Tweets eines Tages berechnet. N steht für die An

zahl der negativen Tweets eines Tages (mit Sentiment ≤-2) und P für die Anzahl positive Tweets


eines Tages (mit Sentiment ≥2). Die verschiedenen Sentimentfunktionen und die Beschränkung auf


23


extreme Tweets (mit Sentiment ≥2 bzw. ≤-2) beruhen auf Ansätzen aus [Tetlock08], [Tetlock10],


[Bollen11] und [Antweiler01].


Aus den Stimmungsverläufen in Abbildung 12 wird deutlich, dass diese i.w. parallel liegen. Wegen


seiner Einfachheit wird daher im Folgenden der arithmetische Mittelwert (Mean) [23] verwendet.


Abbildung 12: Stimmungsverläufe für verschiedene Sentimentfunktionen.


6.1.3 Bag of Words Classifier - Suchbegriffe


Die Stimmungsverläufe für Tweets, die jeweils die Suchbegriffe „central bank“, „stocks“, „stock


market“ und „crisis“ (siehe Kapitel 4) enthalten, sind in Abbildung 13 aufgetragen. Man erkennt


deutliche Unterschiede in den Verläufen. Allerdings ist dabei zu beachten, dass die verschiedenen


Suchbegriffe auch ein sehr unterschiedliches Tweetvolumen aufweisen. Dies ist in Abbildung 14


dargestellt. Sehr viele Tweets pro Tag gibt es mit ca. 30.000 für den Suchbegriff „crisis“. Für „infla

23 Diese entspricht der McD Sentimentfunktion.


24


tion“ sind es hingegen nur knapp 5.000 Tweets pro Tag. So wird deutlich, dass die stark fluktuieren

den Stimmungen für „stock market“ und „central bank“ in Abbildung 13 im Zusammenhang mit


einer sehr geringen Anzahl (< 5.000) Tweets pro Tag stehen. Die deutlich glatteren Stimmungsver

läufe für „crisis“ und „stocks“ hingegen stehen im Zusammenhang mit einer deutlich höheren An

zahl Tweets pro Tag (30.000 bzw. 10.000).


Eine Auswahl bestimmter Suchbegriffe erscheint zunächst nicht sinnvoll. Daher werden im Folgen

den alle Tweets (zu allen Suchbegriffen) in die Sentiment Analyse mit einbezogen.


Abbildung 13: Stimmungsverläufe für verschiedene Suchbegriffe.


25


Abbildung 14: Anzahl Tweets pro Tag in Abhängigkeit vom Suchbegriff.


Die ersten vier Suchbegriffe in der Reihenfolge von oben nach unten sind:


„crisis“, „economy“, „stocks“ und „inflation“.


6.1.4 Bag of Words Classifier - Reputation


Ein weiterer Parameter, der einen Einfluss auf die Stimmungsverläufe haben könnte, ist die Reputa

tion der Twitterer. Trotz Filterung der Tweets durch die Verwendung der oben genannten Suchbe

griffe ist die inhaltliche Relevanz und Aussagekraft der Tweets sehr unterschiedlich. Eine Filtermög

lichkeit zur Verbesserung der Qualität der Tweets bietet die Reputation der Twitterer. Ein erfolgver

sprechender Indikator für die Reputation der Twitterer ist deren Zahl der Follower (follo

26


wers_count) [24] . Sie gibt Auskunft darüber, wie viele Twitter-Nutzer einen Twitterer (also einer Twit

terID) abonniert haben, d.h. alle Tweets dieses Twitterers angezeigt bekommen. Aufgrund der Rate


Limits [25] ist es (zeit)aufwändig, die Zahl der Follower für eine sehr große Zahl [26] von TwitterIDs au

tomatisiert zu ermitteln. Deshalb ist eine Vorfilterung sinnvoll.


Abbildung 15: Anzahl der im Zeitraum von 30 Tagen (12.02.14 - 13.03.14)


versendeten Tweets der Top 100 Twitterer.


Abbildung 15 zeigt die Anzahl der in einem Zeitraum von 30 Tagen (12.02.14 - 13.03.14) versende

ten Tweets der Top 100 Twitterer. Insgesamt gibt es im genannten Zeitraum ca. 65.000 TwitterIDs,


die mindestens 10 Tweets pro Woche versendet haben. Untersucht man die Top 20 TwitterIDs ge

nauer (siehe Abbildung 16), stellt man fest, dass die Zahl der Follower je nach TwitterID sehr stark


schwankt. In der Summe versenden die Top 20 TwitterIDs im o.g. Zeitraum ca. 200.000 Tweets,


was etwa 8% des gesamten Tweetvolumens von 2.4 Millionen Tweets in dem Zeitraum entspricht.


24 Diese Information ist über das Twitter API verfügbar. Siehe: dev.twitter.com/docs/api/1.1/get/users/show
25 Mehr zu den Rate Limits findet sich hier: dev.twitter.com/docs/rate-limiting/1.1
26 Ca. 8 Millionen für das Beispiel in Abbildung 10.


27


Einige TwitterIDs (z.B. @stocknews247) erwecken den Eindruck, dass sie Tweets automatisiert


generieren (Twitter Robot). Damit erscheint die Filtermöglichkeit nach TwitterIDs mit einer großen


Anzahl versendeter Tweets nicht ideal.


Abbildung 16: Detailinformationen zu den Top 20 Twitterern nach Anzahl der versendeten Tweets.


Eine weitere Möglichkeit der Vorfilterung bietet z.B. die Webseite Options Trading IQ. Sie führt


eine Liste mit den „Top 25 Traders On Twitter“ [27] . Untersucht man davon die TOP 20 Trader genau

er (siehe Abbildung 17), weisen diese in der Regel erwartungsgemäß eine hohe Anzahl Follower auf.


Dafür ist aber das Tweetvolumen mit in der Summe ca. 20 Tweets pro Tag für statistische Untersu

chungen zu niedrig. Die beobachteten 610 Tweets entsprechen nur 0,025% des gesamten Tweetvo

lumens von 2.4 Millionen Tweets im betrachteten Zeitraum von 30 Tagen. Damit erscheint auch


diese Filtermöglichkeit nicht sinnvoll.


27 optionstradingiq.com/top-25-traders-on-twitter


28


Abbildung 17: Detailinformationen zu den Top 20 Twitterern nach Reputation.


Eine weitere Filtermöglichkeit bieten Finanznachrichtenagenturen und -sender (Financial News Pro

vider). Deren Tweets sollten eine hohe Qualität aufweisen. In [Yang13b] findet sich eine Liste der


25 Top Financial News Provider, die in Abbildung 18 genauer analysiert werden. Erwartungsgemäß


weisen diese eine z.T. sehr hohe Anzahl von Followern auf (Reputation). Das Tweetvolumen ist mit


gut 80 Tweets pro Tag für statistische Untersuchungen ausreichend. 2524 Tweets entsprechen 0,1%


des Tweetvolumens von 2.4 Millionen im betrachteten Zeitraum (12.02.14 - 13.03.14).


Vergleicht man die Stimmungskurven für alle Tweets (siehe auch Abbildung 10) mit der Stim

mungskurve der Tweets der Top 25 Financial News Provider (siehe Abbildung 19) fallen die unter

schiedlichen Verläufe auf. Gemeinsam ist beiden Kurven der Stimmungsabfall [28] nach dem 22.02.14.


Auffällig sind die stärker ausgeprägten Stimmungsschwankungen in der Kurve der Top 25 Financial


News Provider. Insgesamt erscheint die Stimmungskurve der Tweets der Top 25 Financial News


Provider für erste Korrelationen mit Marktindices am besten geeignet.

28 Ein Erklärungsansatz für den Stimmungsabfall findet sich in der Erläuterung zu Abbildung 10.


29



Abbildung 18: Detailinformationen zu den Top 25 Financial News Providern.


Abbildung 19: Vergleich der Stimmungskurven für alle Tweets mit denen


der Top 25 Financial News Provider.


30


6. Korrelationen

Ob Stimmungskurven auf Twitter Basis eine Prognosekraft für Anlageentscheidungen besitzen, soll


anhand von Korrelationen mit Marktindices überprüft werden. Eine Korrelation untersucht, ob es


zwischen dem zeitlichen Verlauf zweier Messgrößen einen Zusammenhang gibt. Dazu wird zunächst


die Stimmungskurve auf Basis der Tweets der Top 25 Financial News Provider mit dem Verlauf des


DJIA [29] korreliert, um festzustellen, wie stark der Zusammenhang zwischen beiden Größen ist. Gra

fisch aufgetragen sind die Verläufe in Abbildung 20.


Abbildung 20: Stimmungskurve der Tweets der der Top 25 Financial News Provider (schwarz)


und (skalierte) DJIA Schlusskurse (rot).


29 DJIA Schlusskurse zum Download finden sich z.B. auf ariva.de/dow-jones-industrial-average-index/historische_kurse


31


Aufgetragen sind für jeden Werktag die DJIA Schlusskurse (rot, skaliert) und die (nicht gemittelten)


Stimmungskurve der Tweets der Top 25 Financial News Provider (schwarz). Dabei entspricht Tag 1


dem 10.12.13 und Tag 89 dem 17.04.14. Die Ergebnisse einer Korrelation beider Kurven [30] in Ab

hängigkeit vom zeitlichen Versatz sind in Abbildung 21 wiedergegeben.


Abbildung 21: Korrelationen (Levels) der Stimmungskurve der Tweets der Top 25 Financial News


Provider mit den DJIA Schlusskursen. x-Achse: Zeitlicher Versatz der DJIA Kurve gegen die Sen

timent Kurve in Tagen. y-Achse: Korrelationskoeffizient.


30 Levels (s.u.). DJIA unskaliert.


32


Um eine Scheinkorrelation (Spurious Correlation) auszuschließen, werden bei der Korrelationsana

lyse nicht stationärer Zeitreihen (Trends) jedoch statt der Niveauwerte (Levels. Siehe Abbildung 21)


Differenzen [31] (Returns) korreliert (siehe z.B. [Hackl08]). Die Korrelationsergebnisse von DJIA (Re

turns) und Twitter Sentiment (Returns) sind in Abbildung 22 dargestellt.


Abbildung 22: Korrelationen der Stimmungskurve der Tweets der Top 25 Financial News Provider


(Returns) mit den DJIA Schlusskursen (Returns). x-Achse: Zeitlicher Versatz der DJIA Kurve gegen


die Sentiment Kurve in Tagen. y-Achse: Korrelationskoeffizient.


31 Im Folgenden wird die relative Differenz (y(t) - y(t-1)) / y(t-1) verwendet.


33


Die stärkste Korrelation (0,29) findet sich hier für d= -1. Dies bedeutet anschaulich, dass der DJIA


Aktienindex die Twitter Stimmungskurve einen Tag im Voraus vorhersagt. Weitere starke Korrelati

onen gibt es für positive Werte von d. So beträgt der Korrelationskoeffizient für für d = 5 0,27. Das


Ergebnis der Korrelation der Differenzen (Returns) unterscheidet sich deutlich von der Korrelation


der Niveauwerte (Levels) in Abbildung 21.


Geht man davon aus, dass es sich bei den Stimmungskurven um stationäre Zeitreihen handelt, sollten


deren Levels mit den DJIA Returns korreliert werden. Das entsprechende Korrelationsergebnis ist in


Abbildung 23 dargestellt. Hier ergibt sich die stärkste Korrelation kontemporär (d=0) mit einem


Korrelationskoeffizienten von 0,48.


Abbildung 23: Korrelationen der Stimmungskurve der Tweets der Top 25 Financial News Provider


(Levels) mit den DJIA Schlusskursen (Returns). x-Achse: Zeitlicher Versatz der DJIA Kurve gegen


die Sentiment Kurve in Tagen. y-Achse: Korrelationskoeffizient.


34


In Abbildung 24 ist zum Vergleich eine Korrelation mit dem NASDAQ Index dargestellt. Ansonsten


sind die Parameter identisch zu denen in Abbildung 23. Auch für die Korrelation mit dem NASDAQ


tritt die stärkste Korrelation kontemporär (d=0) auf. Der Korrelationskoeffizient ist aber mit 0,40


etwas schwächer.


Abbildung 24: Korrelationen der Stimmungskurve der Tweets der Top 25 Financial News Provider


(Levels) mit den NASDAQ Schlusskursen (Returns). x-Achse: Zeitlicher Versatz der NASDAQ


Kurve gegen die Sentiment Kurve in Tagen. y-Achse: Korrelationskoeffizient.


In Abbildung 25 ist abschließend eine Korrelation der Stimmungskurve ALLER Tweets (Levels) mit


dem DJIA (Returns) aufgetragen. Die kontemporäre Korrelation (d=0) fällt hier mit einem Korrela

tionskoeffizienten von 0,08 deutlich schwächer aus als in der vergleichbaren Abbildung 23. Dies


zeigt, dass sich die Qualität der Tweets - und damit die Korrelationsergebnisse - durch eine geeigne

te Filterung (z.B. Top 25 Financial News Provider) verbessert.


35


Abbildung 25: Korrelationen der Stimmungskurve ALLER Tweets (Levels) mit den DJIA Schluss

kursen (Returns). x-Achse: Zeitlicher Versatz der DJIA Kurve gegen die Sentiment Kurve in Tagen.


y-Achse: Korrelationskoeffizient.


Für fundierte Aussagen ist es nötig, den Beobachtungszeitraum (bisher 89 Tage) deutlich, z.B. auf


mehrere Jahre, auszudehnen (siehe Kapitel 9) und weitere Marktindices (z.B. S&P500 oder


BMUS10Y) in die Analyse mit einzubeziehen.


36


8. Naive Bayes Classifyer


Wie in Kapitel 6 beschrieben, bietet sich neben dem Bag of Words Classifier auch der Naive Bayes


Classifier zur Klassifikation von Tweets an. Beispiele für die Verwendung des Naive Bayes Classifi

er finden sich z.B. in den folgenden Veröffentlichungen: [Mitram11], [Antweiler01], [Pang02] und


[Sprenger10]. Ein Naive Bayes Classifier wird im Folgenden in R auf Basis des e1071-Packages


implementiert, um seine Eignung zu untersuchen.


Das benötigte Trainings- und Testset von klassifizierten Tweets besteht aus 2000 Tweets vom


21.02.14, die mit Hilfe des Bag of Words Classifiers (Lexikon: McDonald [McDonald11]) als posi

tiv bzw. negativ klassifiziert wurden [32] . Zunächst erfolgt ein Preprocessing der in einen Corpus über

führten Tweets mit Hilfe der tm_map Funktion des tm-Packages. Anschließend werden für das Trai

ningset gleichverteilt insgesamt 200 positive und negative Tweets zufällig ausgewählt, daraus ein


Dictionary gebildet und mit Hilfe der Naive Bayes-Funktion die a-posteriori-Wahrscheinlichkeiten


der Wörter im Dictionary berechnet. Diese werden anschließend dazu genutzt, die Tweets des Test

sets zu klassifizieren und die Güte des Ergebnisses anhand der Wahrheitsmatrix (engl. Confusion


Matrix) zu beurteilen. Ein exemplarisches Ergebnis ist in Abbildung 26 wiedergegeben. Mann er

kennt z.B., dass 809 negative Tweets korrekterweise als negativ klassifiziert (true negatives) wurden,


9 negative Tweet (gemäß Bag of Words) aber vom Naive Bayes Classifier als positiv (false positi

ves) klassifiziert wurden. Die in Abbildung 26 ebenfalls abgebildete Error Rate ist definiert als:


Error Rate = (false pos + false neg) / (true pos + true neg + false pos + false neg)


32 Siehe Kapitel 6.1. Aus Zeitgründen wurde im Rahmen dieser Untersuchung davon abgesehen, diese Tweets manuell
zu klassifizieren.


37


Abbildung 26: Wahrheitsmatrix und Error Rate zum Naive Bayes Classifier


Ein vom Naive Bayes Classifier ermitteltes Dictionary ist in Abbildung 27 wiedergegeben. Der Um

fang des Dictionaries variiert stark mit den Konfigurationsparametern des Naive Bayes Classifiers


und wurde aus Performancegründen bewusst klein gehalten. Trotz der ursprünglichen Klassifizie

rung der Tweets auf Basis des Lexikons von McDonald [McDonald11] (siehe Fußnote 28), weist das


aus dem Naive Bayes Classifier hervorgegangene Dictionary nur wenige Gemeinsamkeiten mit dem


Lexikon von McDonald [McDonald11] auf.


Abbildung 27: Das vom Naive Bayes Classifier auf Basis des Trainingssets ermittelte Dictionary


38


Mithilfe der durch den Naive Bayes Classifier ermittelten a-posteriori-Wahrscheinlichkeiten der


Wörter im Dictionary lassen sich nun alle Tweets eines Tages klassifizieren und daraus der arithme

tische Mittelwert der Stimmungen aller Tweets eines Tages ermitteln (Mean). Der so berechnete


Stimmungsverlauf ist in Abbildung 27 dargestellt (obere Kurve, NB). Deutlich erkennbar ist der


grundsätzlich sehr ähnliche Verlauf im Vergleich zum Bag of Words Classifier (untere Kurve,


BoW), wobei der Naive Bayes Classifier stärkere Ausschläge aufweist. Trotz der fundamental unter

schiedlichen Ansätze beider Classifier sind die Ergebnisse vergleichbar. Dies ist neben den Untersu

chungen in Kapitel 6.1 (zu den Parametern Lexikon, Sentimentfunktion, Suchbegriffe und Reputati

on der Twitterer) ein weiteres Indiz für die Robustheit und Aussagekraft der verwendeten Verfahren.


Damit steht ein sehr gutes Instrumentarium für die Analyse von Tweets zur Verfügung. Im folgen

den Abschnitt wird der Beobachtungszeitraum ausgedehnt, um zukünftig Korrelationsanalysen auf


längeren Zeiträumen zu ermöglichen.


39


Abbildung 27: Stimmungsverlauf auf Basis des Naive Bayes Classifiers (oben, rot) im Vergleich


zum dem auf Basis des Bag of Words Classifiers (unten, schwarz). Letzterer entspricht Abbildung


10. Für beide Verläufe erfolge für den Tag d eine Mittelung aller Stimmungswerte im Zeitraum


(d-4) bis (d+4).


40


9. Twitter Archiv


Eine fundierte Beantwortung der Frage, ob sich Tweets für Anlageentscheidungen nutzen lassen, ist


nur möglich, wenn der Beobachtungszeitraum (bisher Dezember 2013 bis April 2014) signifikant


ausgedehnt wird. Das für die Fallstudie ausgewählte Unternehmen verfolgt einen fundamentalen


Portfoliomanagementansatz, bei dem Informationen in ihrem langfristigen historischen Kontext ana

lysiert werden. Twitter stellt jedoch keine historischen Tweets bereit. Kostenpflichtige Zugriffe auf


ein Tweet-Archiv sind nur über autorisierte Zwischenhändler (z.B. Datasift oder Gnip) möglich.


Abbildung 28 zeigt einen analog zu Abbildung 10 ermittelten Stimmungsverlauf über 4 Jahre. Dieser


basiert auf einer von Gnip bereitgestellten 20%-igen Zufallsstichprobe aller Tweets im Zeitraum


01.01.10 bis 31.01.14 zu den bisher schon verwendeten Suchbegriffen [33] . Die Stichprobe umfasst ca.


30 Millionen Tweets. Die unkomprimierten Textfiles haben einen Umfang von ca. 10 GB. Unten ist


in schwarz der ermittelte Stimmungsverlauf aufgetragen (linke Skala). Folgende Parameter wurden


dabei verwendet:


    - Score Sentiment Funktion: Breen (Bag of Words Classifier) [Elder12]


    - Sentiment Funktion: Arithmetischer Mittelwert (Mean)


    - Lexikon: McDonald [McDonald11]


    - Tweets zu allen Suchbegriffen


    - Mittelung über 9 Tage


Oben ist in rot die mit den gleichen Parametern berechnete Standardabweichung in den Stimmungen


aufgetragen (rechte Skala). Die Standardabweichung ist ein Maß für die Streuung der Stimmungen


der Tweets eines Tages.


33 Aufgrund der bisherigen Ergebnisse wurden die Suchbegriffe unverändert beibehalten: volatility, inflation, equity,
emerging markets, central bank, stocks, stock market, crisis, economy.


41


Abbildung 28: Stimmungsverlauf (unten, schwarz, linke Skala) und Standardabweichung (oben, rot,


rechte Skala) der ausgewählten Tweets im Zeitraum Anfang 2010 bis Anfang 2014.


Durch die vertikalen Linien soll angedeutet werden, dass Ausschläge beider Kurven an vielen Tagen


Koinzidenzen aufweisen. Dies ist ein Hinweis darauf, dass es sich bei den Ausschlägen um echte


Signale handelt. Einen weiteren Hinweis für die Signifikanz der Verläufe zeigt Abbildung 28. Dort


sind für den Zeitraum Dezember 2013 bis Januar 2014 die Stimmungsverläufe der aus dem Gnip


Archiv stammenden Tweets mit denen aus dem Streaming API von Twitter gegenübergestellt [34] . Man


erkennt, dass die Kurven nahezu parallel verlaufen [35] . Dies ist ein sehr starkes Indiz für die Robust

heit und Aussagekraft der Signale, da diese auf Basis unterschiedlicher Tweet-Stichproben berechnet


wurden: Einerseits auf Basis aller Tweets zu den beschriebenen Suchbegriffen, die über das


Streaming API bereitgestellt wurden [36] . Andererseits auf Basis einer 20%-igen Stichprobe zu den


Suchbegriffen aus dem Twitter-Archiv von Gnip.


34 Nur für diesen Zeitraum liegen Tweets aus beiden Quellen vor.
35 Für die unterschiedlichen Stimmungsniveaus der beiden Verläufe wurde bisher keine Erklärung gefunden. Eventuell
ist dies auf einen unterschiedlichen prozentualen Anteil des Suchbegriffs „crisis“ in beiden Stichproben zurückzuführen.
36 Dies sind aufgrund der Selektivität der Suchbegriffe ALLE Tweets zu den Suchbegriffen, da die Antwortmenge unter
dem Rate Limit bleibt.


42


Abbildung 28: Vergleich der Stimmungsverläufe auf Basis der Tweets aus dem


Twitter-Archiv (Gnip) und den Tweets aus dem Twitter Streaming API


Mit den historischen Tweets liegt damit eine für längerfristige Korrelation sehr gut geeignete Basis


vor. Damit sind fundierte Aussagen, ob sich Tweets für Anlageentscheidungen nutzen lassen, realis

tisch.


43


10. Zusammenfassung und Ausblick


Die Analyse von unstrukturierten Daten aus sozialen Netzwerken ist ein Einsatzszenario von Big


Data. Am Beispiel einer Sentiment Analyse von Twitter Kurznachrichten (Tweets) zur Unterstüt

zung von Anlageentscheidungen im quantitativen Asset Management wurden verschiedene Analyse

ansätze auf Basis von R (Bag of Words Classifier, Naive Bayes Classifier) und verschiedene Filter

mechanismen (z.B. nach der Reputation der Twitterer) untersucht. Erste Korrelationen der Stim

mungssignale mit Marktindices (DJIA, NASDAQ) über mehrere Monate deuten deren Eignung für


Marktprognosen - und damit zur Unterstützung von Analyseentscheidungen - an.


Eine Fortführung der Untersuchungen in folgende Richtungen erscheint lohnenswert:


  - Ausdehnung der Korrelationen auf größere Zeiträume (siehe Kapitel 9) und ein breiteres


Spektrum von Marktindices (z.B. S&P500 oder BMUS10Y).


  - Verbesserung des Reputationsfilters durch Verwendung eines Reputationsmaßes aus einer


Kombination von Follower Count und Anzahl der Tweets.


  - Verbesserung der Performance der Analysen durch Verwendung einer (Cloud basierten) Ha

doop Architektur.


44


11. Literatur


[Aase11] Aase, K. G. (2011) Text Mining of News Articles for Stock Price Predictions.


Master Thesis. Norwegian University of Science and Technology


[Abberger07] Abberger, K., Nierhaus, W. (2007) Das ifo Geschäftsklima: Ein zuverlässiger


Frühindikator der Konjunktur. ifo Schnelldienst. 2007(5)


[Agarwal 11] Agarwal, A., Xie, B., Vovsha, I., Rambow, O., Passonneau, R. (2011) Sentiment


analysis of twitter data. Proc. ACL 2011 Workshop on Languages in Social Media


[Antweiler01] Antweiler, W., Frank, W. Z. (2001) Is all that talk just noise? The information content


of internet Stock message boards. The Journal of Finance. Volume 59(3)


[Ashish10] Ashish T., Zheng S., Suresh A. et al. (2010) Data Warehousing and Analytics


Infrastructure at Facebook. In SIGMOD '10 Proceedings of the 2010 International


Conference on Management of data. ACM. New York, NY, USA


[Asur10] Asur, S., Huberman, B. A. (2010). Predicting the future with social media.


IEEE/WIC/ACM International Conference on Web Intelligence and Intelligent Agent Tech

nology (WI-IAT)


[Bollen11] Bollen, J., Mao, H., Zeng, X. (2011). Twitter mood predicts the stock market.


Journal of Computational Science, 2(1)


[Buhl12] Buhl, U., Fridgen, G., Müller, G., Röglinger, M. (2012) Von Dinosauriern, Tonnen

ideologen, Separatisten und glücklichen Seelen. Vorschlag und Begründung eines Wegs, um


die weltweite IS/WI-Community glücklich zumachen. WIRTSCHAFTSINFORMATIK 6


(2012)


[Buhl13] Buhl, H., Röglinger, M., Moser, F., Heidemann, J. (2013) Big Data - Ein (ir-)relevanter


Modebegriff für Wissenschaft und Praxis? WIRTSCHAFTSINFORMATIK 2/2013


45


[Burdick11] Burdick, D., Hernández, M. A., Ho, H., Koutrika, G., Krishnamurthy, R., Popa, L.,


Das, S. R. (2011). Extracting, Linking and Integrating Data from Public Sources: A Financial


Case Study. IEEE Data Eng. Bull., 34(3)


[Chau12] M. Chau, Xu, J. (2012) Business Intelligence in Blogs: Understanding Consumer


Interactions and Communities. MIS Quarterly 36(4)


[Chen11] Chen, R., Lazer, M. Sentiment Analysis of Twitter Feeds for the Prediction of Stock


Market Movement


[Chen14] Chen, H., De, P., Hu, Y. J. et al. (2014) Wisdom of Crowds: The value of stock opinions


transmitted through social media. Review of Financial Studies (RFS), Forthcoming


[Demers10] Demers, E., Vega, C. (2008). Soft information in earnings announcements: News or


noise? Federal Reserve Board


[Devitt07] Devitt, A., Ahmad, K.(2007) Sentiment Polarity Identification in Financial News:


A Cohesion-based Approach. Proceedings of the 45th Annual Meeting of the Association of


Computational Linguistics


[Dodds10] Dodds, P. S., Danforth, C. M. (2010). Measuring the happiness of large-scale written


expression: Songs, blogs, and presidents. Journal of Happiness Studies, 11(4)


[Elder12] Elder IV, J., Hill, T., Delen, D., Fast, A. (2012) Practical text mining and statistical


analysis for non-structured text data applications. Academic Press


[Fama65] Fama, E. F. (1965) The behavior of stock-market prices. The Journal of Business 38(1)


[Gabler14] Gabler Wirtschaftslexikon, Stichwort: Soziales Netzwerk, Springer Verlag, Online


im Internet: http://wirtschaftslexikon.gabler.de/Archiv/1020869/soziales-netzwerk-v4.html


(Zugriff am 02.04.14)


[Gallu13] Gallu, J. (2013) SEC Approves Using Facebook, Twitter for Company Disclosures


http://www.bloomberg.com/news/2013-04-02/sec-approves-social-media-use-for-companies

material-disclosure.html (Zugriff am 02.04.14)


46


[Gilbert10] Gilbert, E., Karahalios, K. (2010) Widespread Worry and the Stock Market.


Proceedings of the Fourth International AAAI Conference on Weblogs and Social Media


[Gloor11] Gloor, P. A., Krauss, J., Nann, S., Fischbach, K., Schoder, D. (2009). Web science 2.0:


Identifying trends through semantic social network analysis. IEEE International Conference


on Computational Science and Engineering. CSE'09


[Green13] Greenwald, G., MacAskillet, E. (2013) NSA Prism Program taps in to User Data of


Apple, Google and others. The Guardian. 7. Juni 2013


[Hackl08] Hackl, P. (2008). Einführung in die Ökonometrie. Pearson Studium. 2. Auflage


[Helmholz11] Helmholz, P., Böhringer, M., Robra-Bissantz, S. (2011) Meinungen und Prognosen in


Twitter – das Ohr an der Masse. HMD Praxis der Wirtschaftsinformatik. Volume 48(4)


[Henzel13] Henzel, S. R., Rast, S. (2013) Prognoseeigenschaften von Indikatoren zur Vorhersage


des Bruttoinlandsprodukts in Deutschland. ifo Schnelldienst. 2013(17)


[Hevner04] Hevner, A. R., March, S. T., Park, J., Ram, S. (2004) Design Science in Information


Systems Research. MIS Quarterly 28(1)


[Holt13] Holt, R. (2013) Twitter in numbers. The Telegraph. 21.03.13


http://www.telegraph.co.uk/technology/twitter/9945505/Twitter-in-numbers.html


(Zugriff am 02.04.14)


[Hu04] Hu, M., Liu, B. (2004) Mining and summarizing customer reviews. Proceedings of the ACM


SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD-2004)


[Jansen09] Jansen, B. J., Zhang, M., Sobel, K., Chowdury, A. (2009). Twitter power: Tweets as


electronic word of mouth. Journal of the American society for information science and tech

nology, 60(11)


47


[Jiang11] Jiang, L., Yu, M., Zhou, M., Liu, X., Zhao, T. (2011) Target-dependent twitter sentiment


classification. In Proceedings of the 49th Annual Meeting of the Association for Computa

tional Linguistics: Human Language Technologies-Volume 1. Association for Computational


Linguistics


[Jmal13] Jmal, J., Faiz, R. (2013) Customer Review Summarization Approach using Twitter and


SentiWordNet. WIMS '13 Proceedings of the 3rd International Conference on Web Intelli

gence, Mining and Semantics


[Jordan10] Jordan, J. (2010) Hedge Fund Will Track Twitter to Predict Stock Moves.


Bloomberg. http://www.bloomberg.com/news/2010-12-22/hedge-fund-will-track-twitter-to

predict-stockmarket-movements.html (Zugriff am 02.04.14)


[Jurafsky] Jurafsky, D., Text Classification and Naïve Bayes. Vorlesungsskript


http://www.stanford.edu/class/cs124/lec/naivebayes.pdf (Zugriff am 02.04.14)


[Kimball11] R. Kimball (2011) The Evolving Role of the Enterprise Data Warehouse in the Era of


Big Data Analytics. A Kimball Group White Paper


[Klein13] Klein, D., Tran-Gia, P., Hartmann, M. (2013) Big Data (Aktuelles Schlagwort).


Informatik Spektrum 36(3)


[Kumar13] Kumar, S., Morstatter, F.,Liu, H. (2013) Twitter Data Analytics. SpringerBriefs


in Computer Science


[Lau12] Lau, R. Y. K, Liao, S. S. Y, Wong, K. F., Chiu, D. K. Y (2012) Web 2.0 Environmental


Scanning and Adaptive Decision Support for Business Mergers and Acquisitions.


MIS Quarterly 36(4)


[Lunden14] Lunden, I. (2014) Thomson Reuters Taps Into Twitter For Big Data Sentiment Analysis.


Techcrunch. 03.02.2014 http://techcrunch.com/2014/02/03/twitter-raises-its-enterprise-cred

with-thomson-reuters-sentiment-analysis-deal/ (Zugriff am 02.04.14)


48


[Manyika12] Manyika, J., Chui, M., Brown, B., Bughin, J., Dobbs, R., Roxburgh, C., Byers, H. A.


(2012) Big Data: The next Frontier for innovation, Competition, and Productivity.


McKinsey Global Institute


[McDonald11] McDonald, B., Loughran, T. (2011) When is a liability not a liability? Textual


Analysis, dictionaries, and 10-Ks: The Journal of Finance. Volume 66(1)


[Mitram11] Mitram, G., Mitram, L. (2011) The Handbook of News Analytics in Finance.


John Wiley & Sons


[Moreno13] Moreno, M., Cuesta, A., Barrero, D. (2013) Twitter Stream Analysis in Spanish.


WIMS '13 Proceedings of the 3rd International Conference on Web Intelligence, Mining and


Semantics


[Nofsinger05] Nofsinger, J. R. (2005). Social mood and financial economics. The Journal of


Behavioral Finance, 6(3)


[Pak10] Pak, A., Paroubek, P. (2010) Twitter as a corpus for sentiment analysis and opinion mining.


Proceedings of the Seventh Conference on International Language Resources and Evaluation


[Pang02] Pang, B., Lee, L., Vaithyanathan, S. (2002) Thumbs up?: sentiment classification using


machine learning techniques. Proceedings of the ACL-02 conference on Empirical methods


in natural language processing


[Pettey12] Pettey, C., van der Meulen, R. (2012) Gartner's 2012 Hype Cycle for Emerging


Technologies Identifies "Tipping Point" Technologies That Will Unlock Long-Awaited


Technology Scenarios. Gartner.


[Qian07] Qian, B., Rasheed, K. (2007). Stock market prediction with multiple classifiers. Applied


Intelligence, 26(1), 25-33


[Ruiz12] Ruiz, E. J., Hristidis, V., Castillo, C., Gionis, A., Jaimes, A. (2012) Correlating financial


time series with micro-blogging activity. Proceedings of the fifth ACM international


conference on Web search and data mining, Seattle, Washington, USA


49


[Russell11] Russell, M. A. (2013) Mining the Social Web: Data Mining Facebook, Twitter,


LinkedIn, Google+, GitHub, and More. O'Reilly & Associates


[Sprenger10] Sprenger, T. O., Tumasjan, A., Sandner, P. G., Welpe, I. M. (2013). Tweets and trades:


The information content of stock microblogs. European Financial Management


[Tetlock08] Tetlock, P. C., Saar-Tsechansky, M. A. Y. T. A. L., Macskassy, S. (2008). More than


words: Quantifying language to measure firms' fundamentals. The Journal of Finance, 63(3)


[Tetlock10] Tetlock, P. C. (2011). All the news that's fit to reprint: Do investors react to stale


information?. Review of Financial Studies, 24(5)


[Weber12] Weber, M. (2012) Big Data im Praxiseinsatz – Szenarien, Beispiele, Effekte. Bitkom


[Winter09] Winter, R. (2009) Interview mit Alan R. Hevner zum Thema „Design Science“


WIRTSCHAFTSINFORMATIK 1 (2009)


[Wood12] R. Wood, I. Zheludev, P. Treleaven (2012) Mining Social Data with UCL’s


SocialSTORM Platform. world-comp.org


[Xu12] Xu, W., Li, T., Jiang, B., Cheng, C. (2012). Web Mining For Financial Market Prediction


Based On Online Sentiments. PACIS12 Proceedings


[Yang13a] Yang, S. Y., Mo, S. Y. K., Xiaodi, Z. (2013) An Empirical Study of the Financial


Community Network on Twitter. Available at SSRN: http://ssrn.com/abstract=2358679


[Yang13b] Yang, S. Y., Mo, S. Y. K., Zhu, X. (2013) An Empirical Study of the Financial


Community Network on Twitter. Available at SSRN: http://ssrn.com/abstract=2358679


[Zhang10a] Zhang, W., Skiena, S. (2010). Trading Strategies to Exploit Blog and News Sentiment.


ICWSM


[Zhang10b] Zhang, X., Fuehres, H., Gloor, P. A. (2011). Predicting stock market indicators through


twitter “I hope it is not as bad as I fear”. Procedia-Social and Behavioral Sciences, 26


[Zhang13] Zhang, L. (2013). Sentiment analysis on Twitter with stock price and significant keyword


correlation. Doctoral dissertation. University of Texas


