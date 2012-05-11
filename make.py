#!/usr/bin/env python
from os import system
from csv import reader
from os.path import expanduser, isfile
from pystache import render
from datetime import datetime

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
    players = {}
    #for each game, grab the player records:
    i = 1

    filename = lambda i: "game%s.csv" % i

    while isfile(filename(i)):
        print "parsing game %s" % filename(i)

        game = reader(open(filename(i), 'rb'))

        meta = game.next()

        teams = meta[0].split(" vs ")
        if "onstitution" in teams[0]: ct, opponent = teams
        else:                         opponent, ct = teams

        date = datetime.strptime(meta[1], "%B %d %Y")

        #skip header
        game.next()

        for row in game:
            name, num, assists, goals, tos, ds = row[:6]

            #break on the empty row before the sums
            if not any([name, num, assists, goals, tos, ds]):
                break

            dnp = True if row[-1] == "DNP" else False

            num, assists, goals, tos, ds = map(intorzero,
                [num, assists, goals, tos, ds])

            players.setdefault(name, []).append({
                "opponent": opponent,
                "date": date.strftime("%m/%d/%Y"),
                "name": name,
                "number": num,
                "assists": assists,
                "goals": goals,
                "turnovers": tos,
                "blocks": ds,
                "dnp": dnp
            })

        i += 1

    playerid = 0
    for player, games in players.iteritems():
        out = file("players/%s.html" % playerid, 'w')
        in_ = file("player.mustache.html").read()

        out.write(render(in_, {"player": player, "games": games}))
        out.close()

        playerid += 1

if __name__=="__main__":
    create_team_page()
    create_player_pages()
