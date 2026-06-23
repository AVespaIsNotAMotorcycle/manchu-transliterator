ABKAI = {
    " " : " ", # EMPTY
    "ᠸ" : "w", # MONGGOLIAN LETTER WA
    "ᡝ" : "e", # MONGGOLIAN LETTER SIBE E
    "ᡳ" : "i", # MONGGOLIAN LETTER MANCHU I
    "ᠯ" : "l", # MONGGOLIAN LETTER LA
    "ᠪ" : "b", # MONGGOLIAN LETTER BA
    "ᡩ" : "d", # MONGGOLIAN LETTER SIBE DA
    "ᡵ" : "r", # MONGGOLIAN LETTER MANCHU RA
    "ᠵ" : "j", # MONGGOLIAN LETTER JA
    "ᠠ" : "a", # MONGGOLIAN LETTER A
    "ᠩ" : "ng", # MONGGOLIAN LETTER ANG
    "ᡤ" : "g", # MONGGOLIAN LETTER SIBE GA
    "ᠨ" : "n", # MONGGOLIAN LETTER NA
    "ᡴ" : "k", # MONGGOLIAN LETTER MANCHU KA
    "ᠴ" : "q", # MONGGOLIAN LETTER CHA
    "ᡠ" : "u", # MONGGOLIAN LETTER SIBE UE
    "ᡥ" : "h", # MONGGOLIAN LETTER SIBE HA
    "ᡡ" : "v", # MONGGOLIAN LETTER SIBE U
    "ᠮ" : "m", # MONGGOLIAN LETTER MA
    "ᠣ" : "o", # MONGGOLIAN LETTER O
    "ᡧ" : "x", # MONGGOLIAN LETTER SIBE SHA
    "ᡶ" : "f", # MONGGOLIAN LETTER MANCHU FA
    "ᠶ" : "y", # MONGGOLIAN LETTER YA
    "ᠰ" : "s", # MONGGOLIAN LETTER SA
    "ᡬ" : "g'", # MONGGOLIAN LETTER SIBE GAA
    "ᡨ" : "t", # MONGGOLIAN LETTER SIBE TA
    "ᡰ" : "r'", # MONGGOLIAN LETTER SIBE RAA
    "ᡦ" : "p", # MONGGOLIAN LETTER SIBE PA
    "᠈" : ",", # MONGGOLIAN MANCHU COMMA
    "" : "", # MONGGOLIAN FREE VARIATION SELECTOR ONE
    "᠉" : ".", # MONGGOLIAN MANCHU FULL STOP
    "ᠺ" : "k'", # MONGGOLIAN LETTER KA
    "ᡮ" : "c", # MONGGOLIAN LETTER SIBE TSA
    "ᡟ" : "y'", # MONGGOLIAN LETTER SIBE IY
    "ᡯ" : "z", # MONGGOLIAN LETTER SIBE ZA
    "ᡱ" : "q", # MONGGOLIAN LETTER SIBE CHA
    "ᡭ" : "h'", # MONGGOLIAN LETTER SIBE HAA
    "" : "", # MONGGOLIAN VOWEL SEPARATOR
    "ᡷ" : "zh", # MONGGOLIAN LETTER MANCHU ZHA
    "\u180b" : "", # MONGOLIAN FREE VARIATION SELECTOR ONE
}

def manchu_to_abkai(manchu):
    abkai = ""
    for char in manchu:
        latin = ABKAI[char]
        abkai += latin
    return abkai

