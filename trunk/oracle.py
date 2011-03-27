#!/usr/bin/python
import answer;

def man_vs_machine(otazka, odpovede):
    otazka_transl = answer.translate(otazka);
    odp_transl = {}
    for odp in odpovede:
        odp_transl[odp] = answer.translate(odp)

    res = answer.vyhodnot(answer.estimate_scores(otazka_transl, odp_transl));
    #if (res[0][0] < 1.0):
    #    return None 
    return res[0][2]
"""
print man_vs_machine("Kto je autorom knihy hobit?",
    ["Dan Brown", "J.R.R tolkien", "Terry Pratchett"]);
"""
