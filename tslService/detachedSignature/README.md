# Motivation

Für den Download der TSL (PU) über einen HTTP-Server im Internet wurde nach
Gesprächen mit dem BSI entschieden neben der schon über XMLDSig signierten TSL
eine detached-Signatur als separate Datei ebenfalls auf dem Download-Punkt zur
Verfügung zu stellen. Diese detached-Signatur signiert die TSL in ihrere Gänze,
d. h. die TSL-XML-Datei wird inkl. der dort enthaltenen XMLDSig-Signatur
nochmal durch den TSL-Signer signiert. Diese zusätzliche Signatur wird als
detached-Signatur neben der TSL-XML-Datei auf dem Download-Punkt verfügbar
gemacht.

Ein Konnektor verwendet bei der Signaturprüfung einer TSL, die über das
Internet bezogen wurde, dann die detachted-Signatur für die Signaturprüfung.

Ziel ist, dass diese detached-Signatur aus Sicherheitsperspektive einfacher
prüfbar ist, i. S. v. sicherer prüfbar ist.  D. h., die TSL muss als XML-File
nicht dekodiert werden und die relativ komplexe XMLDSig-Signatur -- die
potentiell vom Angreifer modifiziert ist -- nicht auswerten.

# Designüberlegung

Sicherer prüfbar sein, heißt in dem Zusammenhang, dass

1. möglichst nur feste offset bekannt sein müssen,
2. es keine optionalen Felder gibt, und
3. nur genau die notwendige Funktionalität abgebildet wird.

Allgemeine PKCS#7/CMS/[RFC-5652](https://tools.ietf.org/html/rfc5652)-
Signaturen leisten dies nicht, denn sie sind zu flexibel
(mehrere Signer-Blocks möglich, Parallel-Signaturen, zusätzliche signierte 
Attribute (Signaturzeit), zusätzliche unsignierte Attribute, Zertifikatsketten,
CRLs etc.).

Deshalb wird der Weg gewählt, der auch für die Signatur von X.509-Zertifikaten
und OCSP-Responses verwendet wird.

Die Signatur besteht aus einer Sequence, die aus _drei_Elementen_ besteht:

## 1. OID für den Signaturtyp 

   Für ECDSA:

        SEQUENCE {
          OBJECT IDENTIFIER ecdsaWithSHA256 (1 2 840 10045 4 3 2)
          }

   Für RSA (= bei der RSA-TSL genauer RSASSA-PSS):

        SEQUENCE {
          OBJECT IDENTIFIER rsaPSS (1 2 840 113549 1 1 10)
          SEQUENCE {
            [0] {
              SEQUENCE {
                OBJECT IDENTIFIER sha-256 (2 16 840 1 101 3 4 2 1)
                }
              }
            [1] {
              SEQUENCE {
                OBJECT IDENTIFIER pkcs1-MGF (1 2 840 113549 1 1 8)
                SEQUENCE {
                  OBJECT IDENTIFIER sha-256 (2 16 840 1 101 3 4 2 1)
                  }
                }
              }
            [2] {
              INTEGER 32
              }
            }
          }

## 2. kryptographische Signatur


   Für ECDSA:

        BIT STRING, encapsulates {
          SEQUENCE {
            INTEGER
              07 33 3E 48 3B FB DB DA 07 BA B4 49 59 96 A4 36
              B1 45 D1 21 AE D8 F6 8D 9A CF 15 36 9C 22 EF C9
            INTEGER
              00 8F 4F 66 D2 99 0E F3 16 57 27 52 71 16 6B 13
              61 B5 C4 BB 1B 3E 4D D8 05 DE E4 D8 23 5A EF 2F
              1E
            }

   Für RSA (bei uns 2048-Bit-Schlüssel => 256 Byte kryptographische 
   Signaturgröße):

        BIT STRING
          2B 5B 0A CE 83 D4 C6 40 87 0E 38 6E 2D EA 11 DE
          49 E4 41 FC 1B DA 49 0E 8D 49 7B D3 14 8D 6F C4
          F4 34 EB 00 E2 AE DB BF 31 18 C8 12 49 90 D7 39
          8F D4 7F 3D 7F AA 9F 73 98 DF F6 13 AA 19 57 A2
          20 E3 D3 42 B3 4C EF F0 05 D8 E5 D4 DF 96 96 D1
          5D 9C 78 96 90 CF ED CC B1 6C 0E BD 43 8C 47 3F
          5D 01 B0 7B 51 38 B5 1C 69 02 BC 69 E9 1D D1 61
          89 1D 27 1D C2 E3 70 22 E0 36 6C C0 80 B0 3C 2A
          3F C9 F7 44 F8 50 FF BD D3 3B 64 89 77 C2 8C 7A
          85 B3 66 16 B8 E3 78 79 B5 27 EF 17 01 DD 80 4B
          89 2C 99 E0 D0 F3 67 15 29 93 39 9C 4E 06 86 C8
          97 EB 11 09 82 61 68 4F 47 17 F5 41 88 F3 C3 33
          7F DF 9B FD 63 B9 D4 32 CF CC 0A E4 66 7B B0 3E
          0F 64 0D 52 38 88 83 E2 FC 51 8A 93 40 76 93 9E
          B9 1D 70 97 A7 8A B5 E8 F6 EB 8E 4D 0A 6C A7 BE
          ED EF D5 72 5D B1 58 2A BA D1 3B 25 E1 95 D8 07
        }

## 3. Zertifikat des Signierenden (TSL-Signer)

Genau das und kein Bit mehr.

Nach Prüfung der Signatur kann sich der Prüfende sich über die Integrität und
Authentzität der TSL-Daten sicher sein, und beim Parsen der XML-Daten der 
TSL-Datei davon ausgegen, dass diese wohlformatiert und vertrauenswürdig sind.

# Signatur der ECC-RSA-TSL mittels ECDSA (ECC-TSL-Signer)

Hinweis: ECDSA ist ein randomisiertes Signaturverfahren, deshalb erzeugt jeder 
Aufruf von ./sign\_ecdsa.py einen neuen Signaturwert, obwohl sich die TSL-Daten
nicht ändern.

    [a@h detached-signature]$ ./sign_ecdsa.py 

    [a@h detached-signature]$ base64 ECC-RSA_TSL-dummy.sig 
    MIICjTAKBggqhkjOPQQDAjBEAiAnYhoFDfZ1nxL4DyGGEEL3S2Uhjem9m/c+PyH9YOqdeQIgT6Gz
    IVuILAU8Sn2Mw4DrOJo+LVbGF2Z5kjkoR73WnqwwggI3MIIB3qADAgECAhREXB/TGHF4vg/n/OnM
    nryBY1ANpTAKBggqhkjOPQQDAjBxMQswCQYDVQQGEwJERTEPMA0GA1UECAwGQmVybGluMQ8wDQYD
    VQQHDAZCZXJsaW4xEDAOBgNVBAoMB2dlbWF0aWsxEDAOBgNVBAsMB2dlbWF0aWsxHDAaBgNVBAMM
    E1Rlc3QgVFNMLVNpZ25lciBFQ0MwHhcNMjAwOTI2MTAwMDM2WhcNMjEwOTI2MTAwMDM2WjBxMQsw
    CQYDVQQGEwJERTEPMA0GA1UECAwGQmVybGluMQ8wDQYDVQQHDAZCZXJsaW4xEDAOBgNVBAoMB2dl
    bWF0aWsxEDAOBgNVBAsMB2dlbWF0aWsxHDAaBgNVBAMME1Rlc3QgVFNMLVNpZ25lciBFQ0MwWjAU
    BgcqhkjOPQIBBgkrJAMDAggBAQcDQgAEfOIX+urijuTgucFDbKYO8KLq13U7ouRisdhPveh+zAMk
    YgVUgDSheUlRgFJ1iYtO9b0A+GUR9veZfMJkogj/pqNTMFEwHQYDVR0OBBYEFMoyVCSzINnY6w0B
    skVFOSY6YqKRMB8GA1UdIwQYMBaAFMoyVCSzINnY6w0BskVFOSY6YqKRMA8GA1UdEwEB/wQFMAMB
    Af8wCgYIKoZIzj0EAwIDRwAwRAIgOi4H9KxarCKupkz0FnZ1XRnlfraHmrSOMBvGr6W0bsYCIAL2
    RrDIoy0GBw/+eN7MzZjmHIR/mMFEiMTR/9BXAJTr

    [a@h detached-signature]$ dumpasn1 ECC-RSA_TSL-dummy.sig 

      0 653: SEQUENCE {
      4  10:   SEQUENCE {
      6   8:     OBJECT IDENTIFIER ecdsaWithSHA256 (1 2 840 10045 4 3 2)
           :     }
     16  68:   SEQUENCE {
     18  32:     INTEGER
           :       27 62 1A 05 0D F6 75 9F 12 F8 0F 21 86 10 42 F7
           :       4B 65 21 8D E9 BD 9B F7 3E 3F 21 FD 60 EA 9D 79
     52  32:     INTEGER
           :       4F A1 B3 21 5B 88 2C 05 3C 4A 7D 8C C3 80 EB 38
           :       9A 3E 2D 56 C6 17 66 79 92 39 28 47 BD D6 9E AC
           :     }
     86 567:   SEQUENCE {
     90 478:     SEQUENCE {
     94   3:       [0] {
     96   1:         INTEGER 2
           :         }
     99  20:       INTEGER 44 5C 1F D3 18 71 78 BE 0F E7 FC E9 CC 9E BC 81 63 50 0D A5
    121  10:       SEQUENCE {
    123   8:         OBJECT IDENTIFIER ecdsaWithSHA256 (1 2 840 10045 4 3 2)
           :         }
    133 113:       SEQUENCE {
    135  11:         SET {
    137   9:           SEQUENCE {
    139   3:             OBJECT IDENTIFIER countryName (2 5 4 6)
    144   2:             PrintableString 'DE'
           :             }
           :           }
    148  15:         SET {
    150  13:           SEQUENCE {
    152   3:             OBJECT IDENTIFIER stateOrProvinceName (2 5 4 8)
    157   6:             UTF8String 'Berlin'
           :             }
           :           }
    165  15:         SET {
    167  13:           SEQUENCE {
    169   3:             OBJECT IDENTIFIER localityName (2 5 4 7)
    174   6:             UTF8String 'Berlin'
           :             }
           :           }
    182  16:         SET {
    184  14:           SEQUENCE {
    186   3:             OBJECT IDENTIFIER organizationName (2 5 4 10)
    191   7:             UTF8String 'gematik'
           :             }
           :           }
    200  16:         SET {
    202  14:           SEQUENCE {
    204   3:             OBJECT IDENTIFIER organizationalUnitName (2 5 4 11)
    209   7:             UTF8String 'gematik'
           :             }
           :           }
    218  28:         SET {
    220  26:           SEQUENCE {
    222   3:             OBJECT IDENTIFIER commonName (2 5 4 3)
    227  19:             UTF8String 'Test TSL-Signer ECC'
           :             }
           :           }
           :         }
    248  30:       SEQUENCE {
    250  13:         UTCTime 26/09/2020 10:00:36 GMT
    265  13:         UTCTime 26/09/2021 10:00:36 GMT
           :         }
    280 113:       SEQUENCE {
    282  11:         SET {
    284   9:           SEQUENCE {
    286   3:             OBJECT IDENTIFIER countryName (2 5 4 6)
    291   2:             PrintableString 'DE'
           :             }
           :           }
    295  15:         SET {
    297  13:           SEQUENCE {
    299   3:             OBJECT IDENTIFIER stateOrProvinceName (2 5 4 8)
    304   6:             UTF8String 'Berlin'
           :             }
           :           }
    312  15:         SET {
    314  13:           SEQUENCE {
    316   3:             OBJECT IDENTIFIER localityName (2 5 4 7)
    321   6:             UTF8String 'Berlin'
           :             }
           :           }
    329  16:         SET {
    331  14:           SEQUENCE {
    333   3:             OBJECT IDENTIFIER organizationName (2 5 4 10)
    338   7:             UTF8String 'gematik'
           :             }
           :           }
    347  16:         SET {
    349  14:           SEQUENCE {
    351   3:             OBJECT IDENTIFIER organizationalUnitName (2 5 4 11)
    356   7:             UTF8String 'gematik'
           :             }
           :           }
    365  28:         SET {
    367  26:           SEQUENCE {
    369   3:             OBJECT IDENTIFIER commonName (2 5 4 3)
    374  19:             UTF8String 'Test TSL-Signer ECC'
           :             }
           :           }
           :         }
    395  90:       SEQUENCE {
    397  20:         SEQUENCE {
    399   7:           OBJECT IDENTIFIER ecPublicKey (1 2 840 10045 2 1)
    408   9:           OBJECT IDENTIFIER brainpoolP256r1 (1 3 36 3 3 2 8 1 1 7)
           :           }
    419  66:         BIT STRING
           :           04 7C E2 17 FA EA E2 8E E4 E0 B9 C1 43 6C A6 0E
           :           F0 A2 EA D7 75 3B A2 E4 62 B1 D8 4F BD E8 7E CC
           :           03 24 62 05 54 80 34 A1 79 49 51 80 52 75 89 8B
           :           4E F5 BD 00 F8 65 11 F6 F7 99 7C C2 64 A2 08 FF
           :           A6
           :         }
    487  83:       [3] {
    489  81:         SEQUENCE {
    491  29:           SEQUENCE {
    493   3:             OBJECT IDENTIFIER subjectKeyIdentifier (2 5 29 14)
    498  22:             OCTET STRING, encapsulates {
    500  20:               OCTET STRING
           :                 CA 32 54 24 B3 20 D9 D8 EB 0D 01 B2 45 45 39 26
           :                 3A 62 A2 91
           :               }
           :             }
    522  31:           SEQUENCE {
    524   3:             OBJECT IDENTIFIER authorityKeyIdentifier (2 5 29 35)
    529  24:             OCTET STRING, encapsulates {
    531  22:               SEQUENCE {
    533  20:                 [0]
           :                   CA 32 54 24 B3 20 D9 D8 EB 0D 01 B2 45 45 39 26
           :                   3A 62 A2 91
           :                 }
           :               }
           :             }
    555  15:           SEQUENCE {
    557   3:             OBJECT IDENTIFIER basicConstraints (2 5 29 19)
    562   1:             BOOLEAN TRUE
    565   5:             OCTET STRING, encapsulates {
    567   3:               SEQUENCE {
    569   1:                 BOOLEAN TRUE
           :                 }
           :               }
           :             }
           :           }
           :         }
           :       }
    572  10:     SEQUENCE {
    574   8:       OBJECT IDENTIFIER ecdsaWithSHA256 (1 2 840 10045 4 3 2)
           :       }
    584  71:     BIT STRING, encapsulates {
    587  68:       SEQUENCE {
    589  32:         INTEGER
           :           3A 2E 07 F4 AC 5A AC 22 AE A6 4C F4 16 76 75 5D
           :           19 E5 7E B6 87 9A B4 8E 30 1B C6 AF A5 B4 6E C6
    623  32:         INTEGER
           :           02 F6 46 B0 C8 A3 2D 06 07 0F FE 78 DE CC CD 98
           :           E6 1C 84 7F 98 C1 44 88 C4 D1 FF D0 57 00 94 EB
           :         }
           :       }
           :     }
           :   }

    0 warnings, 0 errors.

# Signatur der RSA-TSL mittels RSASSA-PSS (RSA-TSL-Signer)

Hinweis: RSASSA-PSS ist ein randomisiertes Signaturverfahren, deshalb erzeugt
jeder Aufruf von ./sign\_ecdsa.py einen neuen Signaturwert, obwohl sich die
TSL-Daten nicht ändern.

    [a@h detached-signature]$ ./sign_rsassa-pss.py 

    [a@h detached-signature]$ base64 TSL-dummy.sig
    MIIFazA9BgkqhkiG9w0BAQowMKANMAsGCWCGSAFlAwQCAaEaMBgGCSqGSIb3DQEBCDALBglghkgB
    ZQMEAgGiAwIBIAOCAQEAj9Z6J/jrEXW5zC8Dy6zxGwrcuUrwutf50rFiHt3fuvWtvS0QHaHpFKq2
    cr0YFN2k1L+RvHM4mtVWKPdUoxXp/Y7TjDXSJvPX2KJVGfULuD0lIndryaJJpLZebpZC350o54vr
    SNgyipPoWbHCLwi2g+cy/Fc12xQvIsh9IVcm7zyxKHsof043wvb9gUPAMoVI0fvJ5uUzFznjmA4N
    IL0N+0+U3quJ8alsgZY0suidaltxQDS6NpoqcS8DzMIeMeLYgOeZ0a4834l+m62aT0zhAZBsKaUK
    zCd9YkaE30uncOp2HdwcNl4M+C2UY5VbKw2qRlyZo8SJ6OC4wGXIvXTzfzCCBCMwggLboAMCAQIC
    FE33RajUagI38aqRLrovR90bKJj0MD0GCSqGSIb3DQEBCjAwoA0wCwYJYIZIAWUDBAIBoRowGAYJ
    KoZIhvcNAQEIMAsGCWCGSAFlAwQCAaIDAgEgMHExCzAJBgNVBAYTAkRFMQ8wDQYDVQQIDAZCZXJs
    aW4xDzANBgNVBAcMBkJlcmxpbjEQMA4GA1UECgwHZ2VtYXRpazEQMA4GA1UECwwHZ2VtYXRpazEc
    MBoGA1UEAwwTVGVzdCBUU0wtU2lnbmVyIEVDQzAeFw0yMDA5MjYxNDMzMDRaFw0yMTA5MjYxNDMz
    MDRaMHExCzAJBgNVBAYTAkRFMQ8wDQYDVQQIDAZCZXJsaW4xDzANBgNVBAcMBkJlcmxpbjEQMA4G
    A1UECgwHZ2VtYXRpazEQMA4GA1UECwwHZ2VtYXRpazEcMBoGA1UEAwwTVGVzdCBUU0wtU2lnbmVy
    IEVDQzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALW1QEiNtEXb/H7Ezfz9zqo8Mlu5
    9GlOSkCMHiRhs0AUQDVO+sU5EhWv74wRnMVnkyxQ83xmwjgasCN6ueWqDQRrQkpkZzOscMw6EYZJ
    6CLUqZ8T0toyRiKsvpOlTG3ldY11yqRo4owpyLBYzPj8x7K1yZgZUvjeiuLCHDfIZYdxRNBehWJh
    TGxIxCXavIOJIdNp2Png8gUYl/BHp0BJM5764H3KCtumvT+VvIvp5zJSErD2zL8OgngVkGeTkCvw
    MHjpnivmn57OlWU4s383uSSH0KhDbXJ0KmD7fTJzMG4IS9R7qEEhMZmg3+Rjsl4oPM7Gm/FKxFHQ
    5G6OdPthdekCAwEAAaNTMFEwHQYDVR0OBBYEFGMJC700NVH9a6riI7ku2BpznyD7MB8GA1UdIwQY
    MBaAFGMJC700NVH9a6riI7ku2BpznyD7MA8GA1UdEwEB/wQFMAMBAf8wPQYJKoZIhvcNAQEKMDCg
    DTALBglghkgBZQMEAgGhGjAYBgkqhkiG9w0BAQgwCwYJYIZIAWUDBAIBogMCASADggEBACtbCs6D
    1MZAhw44bi3qEd5J5EH8G9pJDo1Je9MUjW/E9DTrAOKu278xGMgSSZDXOY/Ufz1/qp9zmN/2E6oZ
    V6Ig49NCs0zv8AXY5dTflpbRXZx4lpDP7cyxbA69Q4xHP10BsHtROLUcaQK8aekd0WGJHScdwuNw
    IuA2bMCAsDwqP8n3RPhQ/73TO2SJd8KMeoWzZha443h5tSfvFwHdgEuJLJng0PNnFSmTOZxOBobI
    l+sRCYJhaE9HF/VBiPPDM3/fm/1judQyz8wK5GZ7sD4PZA1SOIiD4vxRipNAdpOeuR1wl6eKtej2
    645NCmynvu3v1XJdsVgqutE7JeGV2Ac=

    [a@h detached-signature]$ dumpasn1 TSL-dummy.sig 
       0 1387: SEQUENCE {
       4   61:   SEQUENCE {
       6    9:     OBJECT IDENTIFIER rsaPSS (1 2 840 113549 1 1 10)
      17   48:     SEQUENCE {
      19   13:       [0] {
      21   11:         SEQUENCE {
      23    9:           OBJECT IDENTIFIER sha-256 (2 16 840 1 101 3 4 2 1)
             :           }
             :         }
      34   26:       [1] {
      36   24:         SEQUENCE {
      38    9:           OBJECT IDENTIFIER pkcs1-MGF (1 2 840 113549 1 1 8)
      49   11:           SEQUENCE {
      51    9:             OBJECT IDENTIFIER sha-256 (2 16 840 1 101 3 4 2 1)
             :             }
             :           }
             :         }
      62    3:       [2] {
      64    1:         INTEGER 32
             :         }
             :       }
             :     }
      67  257:   BIT STRING
             :     8F D6 7A 27 F8 EB 11 75 B9 CC 2F 03 CB AC F1 1B
             :     0A DC B9 4A F0 BA D7 F9 D2 B1 62 1E DD DF BA F5
             :     AD BD 2D 10 1D A1 E9 14 AA B6 72 BD 18 14 DD A4
             :     D4 BF 91 BC 73 38 9A D5 56 28 F7 54 A3 15 E9 FD
             :     8E D3 8C 35 D2 26 F3 D7 D8 A2 55 19 F5 0B B8 3D
             :     25 22 77 6B C9 A2 49 A4 B6 5E 6E 96 42 DF 9D 28
             :     E7 8B EB 48 D8 32 8A 93 E8 59 B1 C2 2F 08 B6 83
             :     E7 32 FC 57 35 DB 14 2F 22 C8 7D 21 57 26 EF 3C
             :             [ Another 128 bytes skipped ]
     328 1059:   SEQUENCE {
     332  731:     SEQUENCE {
     336    3:       [0] {
     338    1:         INTEGER 2
             :         }
     341   20:       INTEGER 4D F7 45 A8 D4 6A 02 37 F1 AA 91 2E BA 2F 47 DD 1B 28 98 F4
     363   61:       SEQUENCE {
     365    9:         OBJECT IDENTIFIER rsaPSS (1 2 840 113549 1 1 10)
     376   48:         SEQUENCE {
     378   13:           [0] {
     380   11:             SEQUENCE {
     382    9:               OBJECT IDENTIFIER sha-256 (2 16 840 1 101 3 4 2 1)
             :               }
             :             }
     393   26:           [1] {
     395   24:             SEQUENCE {
     397    9:               OBJECT IDENTIFIER pkcs1-MGF (1 2 840 113549 1 1 8)
     408   11:               SEQUENCE {
     410    9:                 OBJECT IDENTIFIER sha-256 (2 16 840 1 101 3 4 2 1)
             :                 }
             :               }
             :             }
     421    3:           [2] {
     423    1:             INTEGER 32
             :             }
             :           }
             :         }
     426  113:       SEQUENCE {
     428   11:         SET {
     430    9:           SEQUENCE {
     432    3:             OBJECT IDENTIFIER countryName (2 5 4 6)
     437    2:             PrintableString 'DE'
             :             }
             :           }
     441   15:         SET {
     443   13:           SEQUENCE {
     445    3:             OBJECT IDENTIFIER stateOrProvinceName (2 5 4 8)
     450    6:             UTF8String 'Berlin'
             :             }
             :           }
     458   15:         SET {
     460   13:           SEQUENCE {
     462    3:             OBJECT IDENTIFIER localityName (2 5 4 7)
     467    6:             UTF8String 'Berlin'
             :             }
             :           }
     475   16:         SET {
     477   14:           SEQUENCE {
     479    3:             OBJECT IDENTIFIER organizationName (2 5 4 10)
     484    7:             UTF8String 'gematik'
             :             }
             :           }
     493   16:         SET {
     495   14:           SEQUENCE {
     497    3:             OBJECT IDENTIFIER organizationalUnitName (2 5 4 11)
     502    7:             UTF8String 'gematik'
             :             }
             :           }
     511   28:         SET {
     513   26:           SEQUENCE {
     515    3:             OBJECT IDENTIFIER commonName (2 5 4 3)
     520   19:             UTF8String 'Test TSL-Signer RSA'
             :             }
             :           }
             :         }
     541   30:       SEQUENCE {
     543   13:         UTCTime 26/09/2020 14:33:04 GMT
     558   13:         UTCTime 26/09/2021 14:33:04 GMT
             :         }
     573  113:       SEQUENCE {
     575   11:         SET {
     577    9:           SEQUENCE {
     579    3:             OBJECT IDENTIFIER countryName (2 5 4 6)
     584    2:             PrintableString 'DE'
             :             }
             :           }
     588   15:         SET {
     590   13:           SEQUENCE {
     592    3:             OBJECT IDENTIFIER stateOrProvinceName (2 5 4 8)
     597    6:             UTF8String 'Berlin'
             :             }
             :           }
     605   15:         SET {
     607   13:           SEQUENCE {
     609    3:             OBJECT IDENTIFIER localityName (2 5 4 7)
     614    6:             UTF8String 'Berlin'
             :             }
             :           }
     622   16:         SET {
     624   14:           SEQUENCE {
     626    3:             OBJECT IDENTIFIER organizationName (2 5 4 10)
     631    7:             UTF8String 'gematik'
             :             }
             :           }
     640   16:         SET {
     642   14:           SEQUENCE {
     644    3:             OBJECT IDENTIFIER organizationalUnitName (2 5 4 11)
     649    7:             UTF8String 'gematik'
             :             }
             :           }
     658   28:         SET {
     660   26:           SEQUENCE {
     662    3:             OBJECT IDENTIFIER commonName (2 5 4 3)
     667   19:             UTF8String 'Test TSL-Signer RSA'
             :             }
             :           }
             :         }
     688  290:       SEQUENCE {
     692   13:         SEQUENCE {
     694    9:           OBJECT IDENTIFIER rsaEncryption (1 2 840 113549 1 1 1)
     705    0:           NULL
             :           }
     707  271:         BIT STRING, encapsulates {
     712  266:           SEQUENCE {
     716  257:             INTEGER
             :               00 B5 B5 40 48 8D B4 45 DB FC 7E C4 CD FC FD CE
             :               AA 3C 32 5B B9 F4 69 4E 4A 40 8C 1E 24 61 B3 40
             :               14 40 35 4E FA C5 39 12 15 AF EF 8C 11 9C C5 67
             :               93 2C 50 F3 7C 66 C2 38 1A B0 23 7A B9 E5 AA 0D
             :               04 6B 42 4A 64 67 33 AC 70 CC 3A 11 86 49 E8 22
             :               D4 A9 9F 13 D2 DA 32 46 22 AC BE 93 A5 4C 6D E5
             :               75 8D 75 CA A4 68 E2 8C 29 C8 B0 58 CC F8 FC C7
             :               B2 B5 C9 98 19 52 F8 DE 8A E2 C2 1C 37 C8 65 87
             :                       [ Another 129 bytes skipped ]
     977    3:             INTEGER 65537
             :             }
             :           }
             :         }
     982   83:       [3] {
     984   81:         SEQUENCE {
     986   29:           SEQUENCE {
     988    3:             OBJECT IDENTIFIER subjectKeyIdentifier (2 5 29 14)
     993   22:             OCTET STRING, encapsulates {
     995   20:               OCTET STRING
             :                 63 09 0B BD 34 35 51 FD 6B AA E2 23 B9 2E D8 1A
             :                 73 9F 20 FB
             :               }
             :             }
    1017   31:           SEQUENCE {
    1019    3:             OBJECT IDENTIFIER authorityKeyIdentifier (2 5 29 35)
    1024   24:             OCTET STRING, encapsulates {
    1026   22:               SEQUENCE {
    1028   20:                 [0]
             :                   63 09 0B BD 34 35 51 FD 6B AA E2 23 B9 2E D8 1A
             :                   73 9F 20 FB
             :                 }
             :               }
             :             }
    1050   15:           SEQUENCE {
    1052    3:             OBJECT IDENTIFIER basicConstraints (2 5 29 19)
    1057    1:             BOOLEAN TRUE
    1060    5:             OCTET STRING, encapsulates {
    1062    3:               SEQUENCE {
    1064    1:                 BOOLEAN TRUE
             :                 }
             :               }
             :             }
             :           }
             :         }
             :       }
    1067   61:     SEQUENCE {
    1069    9:       OBJECT IDENTIFIER rsaPSS (1 2 840 113549 1 1 10)
    1080   48:       SEQUENCE {
    1082   13:         [0] {
    1084   11:           SEQUENCE {
    1086    9:             OBJECT IDENTIFIER sha-256 (2 16 840 1 101 3 4 2 1)
             :             }
             :           }
    1097   26:         [1] {
    1099   24:           SEQUENCE {
    1101    9:             OBJECT IDENTIFIER pkcs1-MGF (1 2 840 113549 1 1 8)
    1112   11:             SEQUENCE {
    1114    9:               OBJECT IDENTIFIER sha-256 (2 16 840 1 101 3 4 2 1)
             :               }
             :             }
             :           }
    1125    3:         [2] {
    1127    1:           INTEGER 32
             :           }
             :         }
             :       }
    1130  257:     BIT STRING
             :       2B 5B 0A CE 83 D4 C6 40 87 0E 38 6E 2D EA 11 DE
             :       49 E4 41 FC 1B DA 49 0E 8D 49 7B D3 14 8D 6F C4
             :       F4 34 EB 00 E2 AE DB BF 31 18 C8 12 49 90 D7 39
             :       8F D4 7F 3D 7F AA 9F 73 98 DF F6 13 AA 19 57 A2
             :       20 E3 D3 42 B3 4C EF F0 05 D8 E5 D4 DF 96 96 D1
             :       5D 9C 78 96 90 CF ED CC B1 6C 0E BD 43 8C 47 3F
             :       5D 01 B0 7B 51 38 B5 1C 69 02 BC 69 E9 1D D1 61
             :       89 1D 27 1D C2 E3 70 22 E0 36 6C C0 80 B0 3C 2A
             :               [ Another 128 bytes skipped ]
             :     }
             :   }
     0 warnings, 0 errors.

