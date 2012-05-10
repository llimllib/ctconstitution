#!/usr/bin/env python
from os import system
from csv import reader
from os.path import expanduser
from pystache import render

def intorzero(n):
    if not n: return 0
    else:     return int(n)

def create_team_page():
    totals = reader(open('total.csv', 'rb'))

    #skip header
    totals.next()
    totals.next()

    players = []

    for name, num, assists, goals, tos, ds, dnp in totals:
        #break on the empty row before the sums
        if not any([name, num, assists, goals, tos, ds, dnp]):
            break

        num, assists, goals, tos, ds, dnp = map(intorzero,
            [num, assists, goals, tos, ds, dnp])

        players.append({
            "name": name,
            "number": num,
            "assists": assists,
            "goals": goals,
            "turnovers": tos,
            "blocks": ds,
            "dnps": dnp
        })

    import pystache

    out = file("test.html", "w")
    in_ = file("test.mustache.html").read()

    out.write(render(in_, {"players": players}))
    out.close()

    dropbox = expanduser("~/Dropbox/Public/ctconstitution/")
    system("cp sorttable.js %s" % dropbox)
    system("cp test.html %s" % dropbox)

def create_player_pages():
    pass

if __name__=="__main__":
    create_team_page()
    create_player_pages()
