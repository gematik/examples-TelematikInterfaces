Auf dem Downloadpunkt muss man bei Update darauf achten, dass die XML-Datei
(TSL) und die zugehörige detached-Signatur zueinander konsistent sind. Beim
Upate (sowohl im primären Download-Punkt als auch bei den sekundären
Download-Punkten) muss man darauf achten, dass man nicht für wenige
Milisekunden eine "neue" TSL hat und eine "alte" detachted-Signatur-Datei.

Thema: Race-Conditions


Tipp: atomares rename() mittels des "mv -T" Befehls

    mkdir a b
    ln -s a z
    ln -s b z.new
    mv -T z.new z

    Annahme in "a" liegt ein Stand vor. Dann synchoniert der DL-Punkt in die
    Zieldaten nach/in b. Ggf. Konsistenz prüfen. Anschließend den symlink z
    atomar auf b wechseln.
    Dies alternierend (a<->b) beim nächsten durchführen.

