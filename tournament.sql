-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE SCHEMA SWISS_GAME;

CREATE TABLE SWISS_GAME.PLAYERS(PLAYER_ID SERIAL PRIMARY KEY UNIQUE,
								FULLNAME VARCHAR(30) NOT NULl,
								WINS INT NOT NULL,
								MATCHES INT NOT NULL);


CREATE TABLE SWISS_GAME.ROUND_SCORE(ROUND_ID SERIAL PRIMARY KEY UNIQUE,
									ID_WINNER INT REFERENCES SWISS_GAME.PLAYERS(PLAYER_ID),								
									ID_LOSER INT REFERENCES SWISS_GAME.PLAYERS(PLAYER_ID));


CREATE VIEW GAME_RESULTS AS SELECT P.FULLNAME, P.WINS 
            FROM SWISS_GAME.PLAYERS AS P ORDER BY WINS DESC;




