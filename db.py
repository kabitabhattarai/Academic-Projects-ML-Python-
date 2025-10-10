#This module is used to connect to a sql database, select, insert, update and delete are used for the UI command menu options.



import sqlite3
from contextlib import closing
from objects import *


conn= None

#Establishes connection to database
def connect():
    global conn
    if not conn:
        DB_FILE="player_db.sqlite"
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

#Reads players from database and returns lineup object containing player objects
def get_players():
    connect()

    query='''SELECT * FROM Player ORDER BY batOrder'''

    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    lineup=Lineup()

    for row in results:
        player= Player(
            row["playerID"],
            row["batOrder"],
            row["firstName"],
            row["lastName"],
            row["position"],
            row["atBats"],
            row["hits"]
        )
        lineup.add_player(player)

    return lineup

#Grabs single player object using playerID
def get_player(playerID):
    connect()
    query='''SELECT * FROM Player WHERE playerID=?'''


    with closing(conn.cursor()) as c:
        c.execute(query, (playerID,))
        results = c.fetchone()

    if results:
        return Player(
            results["playerID"],
            results["batOrder"],
            results["firstName"],
            results["lastName"],
            results["position"],
            results["atBats"],
            results["hits"]
        )
    else:
        return None

#Adds a new player to database by using Player attributes and Player object
def add_player(player):
    connect()

    query= '''INSERT INTO Player (batOrder, firstName, lastName, position, atBats, hits) VALUES(?,?,?,?,?,?)'''

    with closing(conn.cursor()) as c:
        c.execute(query, (player.batOrder,player.first_name,player.last_name,player.position,player.at_bats, player.hits))
        conn.commit()

#Deletes player from database by using playerID
def delete_player(player):
    connect()
    sql = '''DELETE FROM Player WHERE playerID=?'''
    with closing (conn.cursor()) as c:
        c.execute(sql, (player.playerID,))
        conn.commit()

#Updates bat order from given object through playerID
def update_bat_order(lineup):
    connect()

    for i, player in enumerate(lineup):
        player.batOrder = i + 1
        query='''UPDATE Player SET batOrder=? WHERE playerID=?'''

        with closing(conn.cursor()) as c:
            c.execute(query, (player.batOrder,player.playerID))

    conn.commit()

#Update players information by setting new attributes given through user input
def update_player(player):
    connect()

    query='''UPDATE Player 
             SET firstName=?, lastName=?, position=?, atBats=?, hits=? 
             WHERE playerID=?'''

    with closing(conn.cursor()) as c:
        c.execute(query,
                  (player.first_name,
                   player.last_name,
                   player.position,
                   player.at_bats,
                   player.hits,
                   player.playerID))

    conn.commit()

def main():
    connect()
    players= get_players()
    if players != None:
        for player in players:
            print(player.batOrder, player.first_name, player.last_name, player.position, player.at_bats, player.hits, player.get_batting_average())

    else:
        print("Code is needed for the get_players function.")

if __name__ == '__main__':
    main()