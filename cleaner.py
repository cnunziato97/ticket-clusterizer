import re


def regex_cleaner(descrizione):

    descrizione = regex_shortener(descrizione)
    descrizione = regex_rimozione_dati_sensibili(descrizione)

    # errore opeatore già in descrizione
    descrizione = re.sub(
        "err operatore: gi. in descrizione", "", descrizione, flags=re.I | re.M
    )

    # Cortesemente/Gentilmente
    descrizione = re.sub("(cortese|gentil)mente|cortesia", "", descrizione, flags=re.M)

    # le cortesie degli operatori o urgenze
    descrizione = re.sub(
        "gr(azi|aiz)e[\\W]{0,3}(mille)?|grz|buon[\\W]{0,3}lav(oro)?|(con)?[\\W]{0,3}urgen(te|za)|preg[ao](si)?",
        "",
        descrizione,
        flags=re.I | re.M,
    )

    # Sollecito
    descrizione = re.sub("sollecit.", "", descrizione, flags=re.I)

    # saluti
    descrizione = re.sub(
        "(buona?)?[\\W]{0,3}(giorn(ata|o)|sera|pomeriggio|ciao|salve)",
        "",
        descrizione,
        flags=re.I | re.M,
    )
    descrizione = re.sub("buond[iì]", "", descrizione, flags=re.I | re.M)

    # articoli determinativi
    descrizione = re.sub("\b(gli|i?l[aeo]|i)\b", "", descrizione, flags=re.I | re.M)

    # richiesta di verifica, bonifica, sblocco
    descrizione = re.sub(
        "(rich)?[\\W]{0,3}(di[\\W]{0,3})?(verifica|sblocca|bonifica|all?inea|ripristin[ao])(re)?",
        "",
        descrizione,
        flags=re.I | re.M,
    )

    # Cliente
    descrizione = re.sub("\bcliente|clt|cl\b", "", descrizione, flags=re.I | re.M)

    # Data in formato NN\NN\NNNN o NNNN\NN\NN
    descrizione = re.sub(
        "(d[aei][li]?[\\W]{0,3}(giorn[oi]?|gg)?|data[\\W]{0,3}creaz(ione)?[\\W]{0,3}ordine.?)?[\\W]{0,3}[0-9]{1,4}[\/-][0-9]{1,2}([\/-][0-9]{1,4})?",
        "",
        descrizione,
        flags=re.M,
    )

    # Data con mese in testo
    descrizione = re.sub(
        "(d[aei][li]?[\\W]{0,3}(giorn[oi]?|gg)?|data[\\W]{0,3}creaz(ione)?[\\W]{0,3}ordine.?)?[\\W]{0,3}[0-3]?[0-9][\\W]{0,3}(gen(naio)?|febb?(raio)?|mar(zo)?|apr(ile)?|mag(gio)?|giu(gno)?|lug(lio)?|ago(sto)?|sett?(embre)?|ott(obre)?|nov(embre)?|dic(embre)?)",
        "",
        descrizione,
        flags=re.I | re.M,
    )

    # Orario
    descrizione = re.sub("\\d{1,2}[.:]\\d{2}([.:]\\d{2})?", "", descrizione, flags=re.M)

    # Tipo/Stato di lavorazione
    descrizione = re.sub(
        "(tipo|stato)[\\W]{0,3}Lav(orazione)?.?", "", descrizione, flags=re.I | re.M
    )

    # Causale/Nota
    descrizione = re.sub(
        "(causale|not[ae]|causale[\\W]{0,3}not[ae])[\\W]{0,3}evento.?",
        "",
        descrizione,
        flags=re.I | re.M,
    )

    # Allego Print
    descrizione = re.sub(
        "(si|vedi|come)?[\\W]{0,3}(da)?[\\W]{0,3}alleg(ato|[ao])?(.*print)?",
        "",
        descrizione,
        flags=re.M | re.I,
    )
    descrizione = re.sub(
        "(vedi|come)?[\\W]{0,3}(da)?[\\W]{0,3}print.*alleg(ato|[ao])?",
        "",
        descrizione,
        flags=re.M | re.I,
    )

    # finale
    descrizione = re.sub("finale", "", descrizione, flags=re.I)

    # schermata
    descrizione = re.sub(
        "(quest.|mi)?[\\W]{0,3}(schermat.|esce?)[\\W]{0,3}(di)?",
        "",
        descrizione,
        flags=re.I,
    )

    # bloccante, sbloccare, sblocca
    descrizione = re.sub("s?blocca(nte|are)?", "", descrizione, flags=re.I)

    # Tag addizionali dentro ##
    descrizione = re.sub("#.*#", "", descrizione, flags=re.I)

    # gli spazi e punteggiature
    descrizione = re.sub(
        "[ .,:;!?#<>§'*()\n\t]",  # [\\W]",
        "",
        descrizione,
        flags=re.M,
    )

    return descrizione


def regex_rimozione_dati_sensibili(descrizione):
    # Codice Fiscale
    descrizione = re.sub(
        "(cod(ice)?[\\W]{0,3}fiscale|cf)?[\\W]{0,3}[A-Z]{6}[0-9]{2}[ABCDEHLMPRST][0-9]{2}[A-Z]{1}[0-9]{3}[A-Z]{1}",
        "",
        descrizione,
        flags=re.M | re.I,
    )

    # numero fisso
    descrizione = re.sub(
        "(numero|linea:?)?[\\W]{0,3}(fiss[ao])?[\\W]{0,3}(0[0-9]{2,3})[0-9]{6,8}",
        "fisso",
        descrizione,
        flags=re.M,
    )

    # numero mobile
    descrizione = re.sub(
        "(numero|linea:?)?[\\W]{0,3}(mobile)?[\\W]{0,3}(3[0-9]{1,2})[0-9]{6,9}",
        "mobil",
        descrizione,
        flags=re.M,
    )

    # numeri con almeno 11 digit, come Partita IVA
    descrizione = re.sub(
        "\\d{11}",
        "11num",
        descrizione,
        flags=re.M,
    )

    # numeri con almeno 5 digit, come il CAP
    descrizione = re.sub("\\d{5}", "5num", descrizione)

    return descrizione


def regex_shortener(descrizione):

    # OFFERTA -> OFF
    descrizione = re.sub("offert.", "off", descrizione, flags=re.I | re.M)

    # PER -> X
    descrizione = re.sub("\bper", "x", descrizione, flags=re.I)

    # NON -> NN
    descrizione = re.sub("non", "nn", descrizione, flags=re.I)

    # ATTIVAZIONE/ATTIVATO -> ATTIVAZ/ATTIVAT
    descrizione = re.sub("attivazione", "attivaz", descrizione, flags=re.I)
    descrizione = re.sub("attivat[aoe]", "attivat", descrizione, flags=re.I)
    descrizione = re.sub("attivare", "attivar", descrizione, flags=re.I)

    # AGGIUNTA -> AGGIUN
    descrizione = re.sub(
        "(all?)[\\W]{0,3}aggiun(gere|t.)", "aggiun", descrizione, flags=re.I
    )

    # CAMBIO -> CAMB
    descrizione = re.sub("cambi(are|o)", "camb", descrizione, flags=re.I)

    # CESSAZIONE -> CES
    descrizione = re.sub("cessa(t[ao]?|zione)", "ces", descrizione, flags=re.I)

    # TENTATIVO -> TENTA
    descrizione = re.sub(
        "(si)?[\\W]{0,3}tenta(tivo|t[aio])?", "tenta", descrizione, flags=re.I
    )

    # RICHIESTA -> RICH
    descrizione = re.sub(
        "(si)?[\\W]{0,3}(ri)?c?hie(d[aeo]|st[aeio])", "rich", descrizione, flags=re.I
    )

    # MESSAGGIO -> MSG
    descrizione = re.sub("mess?agg?io?", "msg", descrizione, flags=re.I)

    # LAVORAZIONE -> LAV
    descrizione = re.sub("lavora(zion[ei]|t[aio])?", "lav", descrizione, flags=re.I)

    # ALLA/AL/ALL -> A
    descrizione = re.sub("\bal(la|l)?a?", "a", descrizione, flags=re.I)

    # VOCE/RECLAMO/ERRORE -> ERR
    descrizione = re.sub(
        "voc[ei]|recl(am[io])?|error[ei]", "err", descrizione, flags=re.I
    )

    # SULLA -> SU
    descrizione = re.sub("sull?[ae]|sugli", "su", descrizione, flags=re.I | re.M)

    return descrizione
