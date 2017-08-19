-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- \c tournament.sql

CREATE SCHEMA SWISS_GAME;

CREATE TABLE SWISS_GAME.PLAYERS(PLAYER_ID SERIAL PRIMARY KEY UNIQUE,
								FULLNAME VARCHAR(30) NOT NULl);

CREATE TABLE SWISS_GAME.ROUND_PAIRS(PAIR_ID INT PRIMARY KEY NOT NULl,
									FIRST_PLAYER_ID INT REFERENCES SWISS_GAME.PLAYERS(PLAYER_ID),
									FIRST_PLAYER_NAME TEXT NOT NULL,
									SECOND_PLAYER_ID INT REFERENCES SWISS_GAME.PLAYERS(PLAYER_ID),
									SECOND_PLAYER_NAME TEXT NOT NULL);

CREATE TABLE SWISS_GAME.ROUND_SCORE(ID_WINNER INT REFERENCES SWISS_GAME.PLAYERS(PLAYER_ID),								
									ID_LOSER INT REFERENCES SWISS_GAME.PLAYERS(PLAYER_ID));

CREATE TABLE SWISS_GAME.TOTAL_SCORE(PLAYER_ID INT REFERENCES SWISS_GAME.PLAYERS(PLAYER_ID),
									FULLNAME VARCHAR(30) NOT NULl,
									WINS INT NOT NULL,
									MATCHES INT NOT NULL);

CREATE VIEW GAME_RESULTS AS SELECT P.FULLNAME, T.WINS 
            FROM SWISS_GAME.PLAYERS AS P, SWISS_GAME.TOTAL_SCORE AS T 
            WHERE P.PLAYER_ID = T.PLAYER_ID ORDER BY WINS DESC;




