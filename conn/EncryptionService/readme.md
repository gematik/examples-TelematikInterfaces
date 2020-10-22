Dieses Verzeichnis enthält Testvektoren für die ECIES-Verschlüsselung wie sie in der gemSpec_Krypt spezifiziert ist.

Der Output kann als Vergleichsmuster verwendet werden, nachdem der hier enthaltene Input mit Hilfe der ebenfalls enthaltenen Schlüssel über eine zu testende Implementierung verschlüsselt wurde.

Auch die umgekehrte Testrichtung ist mit den Testvektoren möglich.

Zusätzlich befinden sich in dem Verzeichnis Testvektoren für die RSA-Verschlüsselung.

# Struktur

|Verzeichnis|Inhalt|
|---|---|
|EncryptDocumentCMS|Enthält Testvektoren für die CMS-Verschlüsselung|
|EncryptDocumentXML|Enthält Testvektoren für die XML-Verschlüsselung|
HBA_G21_80276883110000129111-C_HP_ENC_E256.crt|Zertifikat für ECIES in beiden obigen Verzeichnissen|
|HBA_G21_80276883110000129111-C_HP_ENC_R2048.crt|Zertifikat für RSA in beiden obigen Verzeichnissen|
|EncryptDocumentCMS/String/Daten|Input/Output für CMS-Verschlüsselung eines Strings|
|EncryptDocumentXML/String/Daten|Input/Output für XML-Verschlüsselung eines XML-Knotens|
|EncryptDocumentCMS/File/Daten|Inputbeschreibung/Output für CMS-Verschlüsselung einer Datei|
|EncryptDocumentXML/File/Daten|Inputbeschreibung/Output für XML-Verschlüsselung einer XML-Datei|
|EncryptDocumentCMS/File/Textdokument_standard.txt|Input für CMS-Verschlüsselung einer Datei|
|EncryptDocumentXML/File/SampleBase64XMLDocument.xml|Input für XML-Verschlüsselung einer XML-Datei|