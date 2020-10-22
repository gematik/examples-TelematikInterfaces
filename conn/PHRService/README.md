# PHRService Beispielnachrichten
Zur Erleichterung der Implementierung der ePA Funktionalität in den Primärsystemen stellt die gematik Beispielnachrichten des PHRService für Release 3.1.3 bereit. 

*Disclaimer:* Die Beispielnachrichten wurden einmalig mit dem Aktor:4PS Beispielmandanten erzeugt (Aktor 1.25.0-5051, Instanz 1) und dienen zur Veranschaulichung. Bitte verwenden Sie die aktuellen Versionen der bereitgestellten WSDL und XML Dateien für Ihre Implementierung.

Weitere Informationen zu unserem Angebot **Aktor:4PS** finden Sie im Fachportal der gematik (https://fachportal.gematik.de/service/epa-aktensystemsimulator/aktor4ps/).

Der Ordner *Document_Lifecycle* enthält zeitlich sortierte Beispiel-Request und -Response Nachrichten für einen Lebenszyklus eines Arztbriefes:
- erste Suche nach Arztbriefen in der Akte 
    - es sind keine Arztbriefe in der Akte enthalten
- Hochladen eines Arztbriefes in die Akte
- zweite Suche nach Arzbriefen in der Akte 
    - es ist ein Arztbrief in der Akte enthalten
- Herunterladen des gefundenen Arztbriefes
- dritte Suche nach Arztbriefen in der Akte
     - es ist ein Arztbrief in der Akte enthalten
- Löschen des gefundenen Arztbriefes

Der Ordner *Document_Restricted_Update* enthält zeitlich sortierte Beispiel-Request und -Response Nachrichten für
- das Hochladen eines Dokumentes in die Akte
- die Suche des Dokumentes in der Akte
- das Umklassifizieren "äquivalent zu LE-Dokument"