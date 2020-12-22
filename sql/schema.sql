-- schema.sql defines the schema or data layout of the database
-- Note: CASCADE makes corresponding changes upon delete/update
PRAGMA foreign_keys = ON;

CREATE TABLE songs(
    id NUMBER NOT NULL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    artist NUMBER NOT NULL,
    album NUMBER NOT NULL,
    popularity NUMBER
);