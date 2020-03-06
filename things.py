import re
import subprocess


def extract(pattern, iter):
    for m in map(lambda x: re.search(pattern=pattern, string=x), iter):
        if m:
            yield m.group(1)

subs = {
    ' ': '%20',
    ',': '%2C',
    'ß': '%C3%9F',
    ':': '%3A'
}


def addTask(tasks, group=None):
    for pat, sub in subs.items():
        tasks = [t.replace(pat, sub) for t in tasks]
    url_scheme = "".join([
        'things:///add?titles=',
        r'%0A'.join(tasks),
    ])
    if group:
        url_scheme = f'{url_scheme}&list={group}'
    print(url_scheme)


# n = [x for x in r"""
# 1 Kurzfragen Ersatzstrom- und Ersatzspannungsquellen 2
# 2 Wiederholung Superpositionsverfahren 2
# 3 Zusatzaufgabe Superpositionsverfahren 3
# 4 Ersatzstrom- und Ersatzspannungsquelle in komplexen Netzwerken 4
# 5 Kurzfragen Knotenpotentialanalyse 5
# 6 T-Notch-Filter mit (modifizierter) Knotenpotentialanalyse 5
# 7 Knotenpotentialanalyse mit gesteuerter Stromquelle 6
# 8 Kurzfragen - Der MOS-Transistor 7
# 9 Kurzfragen - Linearisierung und Arbeitspunkt 9
# 10 Sourceschaltung, Common Source, CS 11
# 11 Kurzfragen: Kleinsignalgroeßen des MOSFET, Dynamisches Kleinsignalersatzschaltbild 13
# 12 Inverter, dynamisches Kleinsignalersatzschaltbild 14
# 13 Gateschaltung 17
# 14 Sourceschaltung, Millereffekt, Kaskodeschaltung 19
# 15 Drainschaltung 20
# 16 Sourceschaltung mit Stromgegenkopplung 22
# 17 Stromspiegel 23
# 18 Einfuehrung Differenzverstaerker 24
# 19 DV - Gleichtaktverstaerkung 26
# 20 Digitale Grundschaltungen""".split('\n')]

# pattern = r'^\d+?\s(.+)\s\d+$'
# addTask(extract(pattern, n), group='Schalte')
# print("\n".join(extract(pattern,n)))


