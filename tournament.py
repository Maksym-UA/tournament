#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# tournament.py -- implementation of a Swiss-system tournament
#
# PostgreSQL database adapter for the Python programming languagE

import psycopg2


def connect(database_name="tournament"):
    """
    Connect to the PostgreSQL database.  Returns a database connection.
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Couldn't connect to database.")


def registerPlayer(name):
    """
    Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    db, cursor = connect()

    query = 'INSERT INTO swiss_game.players (fullname, wins, matches) values' +
    '(%s, %s, %s) returning player_id;'
    parameter = ((name,), 0, 0)
    cursor.execute(query, parameter)
    player_id = cursor.fetchone()[0]
    db.commit()
    # print "Records created successfully"
    db.close()


def deletePlayers():
    """
    Remove all the player records from the database.
    """

    db, cursor = connect()

    # c.execute("alter table swiss_game.total_score drop
    # constraint total_score_player_id_fkey;")

    cursor.execute('TRUNCATE swiss_game.players CASCADE;')
    db.commit()

    print("All records from players deleted")

    db.close()


def deleteMatches():
    """
    Remove all the match records from the database.
    """

    db, cursor = connect()
    cursor.execute('update swiss_game.players set matches = 0, wins = 0;')
    db.commit()

    # print("All records from round_pairs deleted")

    db.close()


def countPlayers():
    """
    Returns the number of players currently registered.
    """

    db, cursor = connect()
    cursor.execute('select count(*) as Total_players from swiss_game.players;')
    number = cursor.fetchone()
    print("Total number of registered players: %s" % number[0])
    db.close()
    return number[0]


def playerStandings():
    """
    Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db, cursor = connect()
    cursor.execute('select * from swiss_game.players order by wins desc;')
    result = cursor.fetchall()
    i = 0
    for player in result:
        result[i] = (player[0], player[1], player[2], player[3])
        i += 1
    db.commit()
    db.close()
    print (result)
    return result


def reportMatch(winner, loser):
    """
    Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db, cursor = connect()
    query1 = 'insert into swiss_game.round_score (id_winner, id_loser) ' +
    'values(%s, %s);'
    cursor.execute(query1, (winner, loser))
    query2 = 'update swiss_game.players set wins = wins + 1,' +
    'matches = matches + 1  where player_id = %s;'
    cursor.execute(query2, [winner])
    query3 = 'update swiss_game.players set matches = matches + 1  where' +
    'player_id = %s;'
    cursor.execute(query3, [loser])
    db.commit()
    db.close()


def swissPairings():
    """
    Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    pairs = []
    db, cursor = connect()
    cursor.execute('select * from swiss_game.players order by wins desc;')
    allplayers = cursor.fetchall()
    print("players", allplayers)
    search_range = len(allplayers)

    for i in range(0, search_range, 2):
        # choose only player id and name from tuple
        player1 = (allplayers[i])[:-2]
        player2 = (allplayers[i + 1])[:-2]
        pair = player1 + player2
        pairs.append(pair)
    print(pairs)
    db.close()
    return pairs


deletePlayers()
registerPlayer('Kate')
registerPlayer('Antony')
registerPlayer('Max')
registerPlayer('Inna')
registerPlayer('Andriy')
registerPlayer('Ievgen')
registerPlayer('Vlad')
registerPlayer('Yuri')
countPlayers()
swissPairings()
playerStandings()

