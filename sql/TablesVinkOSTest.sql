DROP DATABASE VISITASWEB;

CREATE DATABASE IF NOT EXISTS VISITASWEB;

USE VISITASWEB;

DROP TABLE IF EXISTS visitante;
CREATE TABLE visitante (
	email CHAR(50),
    fechaPrimeraVisita DATE,
    fechaUltimaVisita DATE,
    visitasTotales INT,
    visitasAnioActual INT,
    visitasMesActual INT
);

DROP TABLE IF EXISTS estadistica;
CREATE TABLE estadistica (
	email CHAR(50),
    jyv CHAR(30),
    Badmail CHAR(10),
    Baja CHAR(5),
    Fechaenvio DATE,
    Fechaopen DATE,
    Opens INT,
    Opensvirales INT,
    Fechaclick DATE,
    Clicks INT,
    Clicksvirales INT,
    Links INT,
    IPs VARCHAR(50),
    Navegadores CHAR(50),
    Plataformas CHAR(50)
);

DROP TABLE IF EXISTS errores;
CREATE TABLE errores (
	registros TEXT(500)
);