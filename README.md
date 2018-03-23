# BUDO
Buildings Unified Data point naming schema for Operation management

***GERMAN VERSION BELOW*

Contact persons:

E.ON Energy Research Center
Florian Stinner
fstinner@eonerc.rwth-aachen.de

Fraunhofer Institute for Solar Energy Systems ISE
Nicolas Réhault
Nicolas.Rehault@ise.fraunhofer.de


Building energy systems are often incorrectly controlled and therefore unnecessarily consume too much energy. Especially in non-residential buildings, Building automation systems offer the possibility to influence the control. A distinctive mark for the description of data points is their name. The scheme is often specified by the client or the scheme of the building automation manufacturer is used. In some cases, these are not even named according to a scheme. This individual designation makes it difficult to use automatic algorithms (analysis, error detection, operational management). 

A joint team from E.ON ERC and Fraunhofer ISE has tackled this problem and developed a standardized method for naming data points. This method is based on a method originally developed at Fraunhofer ISE for the designation of data points. This was further developed by E.ON ERC with the support of Fraunhofer ISE. It is entitled "Buildings Unified Data point naming schema for Operation management" (or BUDO for short) and is specially designed for the demands of energy system analysis and operational management. It can be used in new and existing buildings. This means that developed automated methods can be implemented in both new and existing buildings.

To make this key practical, an easy-to-use Excel tool has been developed. This allows the original name to be inserted and then named using the standardized naming scheme. The individual parts of the data point key can be selected in a dropdown menu and thus the name of a data point can be compiled. The tool can be called up under the following link: https://github.com/RWTH-EBC/BUDO.


The structure of the data point is very simple. There is space at the beginning for an individual name. This means that every operator can map his organizational structure in the schema. This is separated from the standardized part of the data point key by a "//". Then the categories "System", "Component/Subsystem", "Medium/Position", "Type" and "Function type" can be selected. These have several specifications, so that it is possible to select very precisely to which plant and system a data point is assigned, where it is located and what type it represents.

By selecting optional designations or numbering, the designations used in the database can be integrated. This means that the individual data points can still be recognized on existing plans. These manual specifications can also be used for the data visualization of customers.


***German version***

Gebäudeenergiesysteme sind oftmals falsch geregelt und verbrauchen deshalb unnötigerweise zu viel Energie. Gebäudeautomationssysteme bieten insbesondere in Nichtwohngebäuden die Möglichkeit einen Einfluss auf die Regelung zu nehmen. Ein Erkennungszeichen für die Beschreibung von Datenpunkten ist ihr Name. Das Schema wird häufig vom Bauherr vorgegeben oder das Schema des Gebäudeautomationsherstellers wird verwendet. Teilweise werden diese auch gar nicht nach einem Schema benannt. Diese individuelle Bezeichnung erschwert die Anwendung von automatischen Algorithmen (Analyse, Fehlererkennung, Betriebsführung). 

Ein gemeinsames Team vom E.ON ERC und Fraunhofer ISE hat sich dieser Problematik angenommen und ein standardisiertes Verfahren für die Benennung von Datenpunkten entwickelt. Dieses Verfahren basiert auf einem ursprünglich am Fraunhofer ISE entwickeltem Verfahren für die Bezeichnung von Datenpunkten. Dieser wurde vom E.ON ERC unter Unterstützung des Fraunhofer ISE weiterentwickelt. Er trägt den Titel "Buildings Unified Data point naming schema for Operation management" (oder kurz BUDO) und ist speziell für die Ansprüche in der Energiesystemanalyse und der Betriebsführung konzipiert. Er kann in Neubauten und in bestehenden Gebäuden angewendet werden. So können entwickelte automatisierte Methoden gleichermaßen im Neubau und im Bestand ausgeführt werden.

Damit dieser Schlüssel auch einfach praktisch angewendet werden kann, wurde ein einfach zu bedienendes Excel-Tool entwickelt. Hiermit kann der Original-Name eingefügt werden und dann mit dem standardisierten Benennungsschema benannt werden. Hierbei kann in einem Dropdown-Menü die einzelnen Teile des Datenpunktschlüssels ausgewählt und somit der Name eines Datenpunktes zusammengestellt werden. Das Tool kann unter folgendem Link abgerufen werden: https://github.com/RWTH-EBC/BUDO.


Die Struktur des Datenpunktes ist sehr einfach. Es gibt am Anfang Platz für eine individuelle Bezeichnung. Somit kann jeder Betreiber seine Organisationsstruktur im Schema abbilden. Diese wird durch ein "//" von dem standardisierten Teil des Datenpunktschlüssels abgetrennt. Danach können die Kategorien "System", "Bauteil/Subsystem", "Medium/Position" , "Typ" und "Funktionsart" ausgewählt werden. Diese haben mehrere Spezifizierungen, so dass sehr genau ausgewählt werden kann, zu welcher Anlage und System ein Datenpunkt zugewiesen ist, wo sich dieser befindet und was für einen Typ er wiedergibt.

Durch die Auswahl von optionalen Bezeichnungen bzw. Nummerierungen können die im Bestand verwendeten Bezeichnungen integriert werden. Somit können die einzelnen Datenpunkten auch weiterhin auf vorhandenen Plänen erkannt werden. Auch können diese manuellen Angaben für die Datenvisualisierung von Kunden genutzt werden.

 
We thank the BMWi (Federal Ministry of Economics and Energy) for their financial support, 
Contribution numbers 03ET1022A, 03SBE0006A, 03ET1373A.
