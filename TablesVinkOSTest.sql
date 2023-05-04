CREATE DATABASE IF NOT EXISTS VISITASWEB;

USE VISITASWEB;

DROP TABLE IF EXISTS visitante;
CREATE TABLE visitante (
	email CHAR(30),
    fechaPrimeraVisita DATE,
    fechaUltimaVisita DATE,
    visitasTotales INT,
    visitasAnioActual INT,
    visitasMesActual INT
);

DROP TABLE IF EXISTS estadistica;
CREATE TABLE estadistica (
	email CHAR(30),
    jyv CHAR(30),
    Badmail CHAR(10),
    Baja CHAR(5),
    fechaEnvio DATE,
    fechaOpen DATE,
    Opens INT,
    OpensVirales INT,
    FechaClick DATE,
    Clicks INT,
    ClicksVirales INT,
    Links INT,
    IPs VARCHAR(50),
    Navegadores CHAR(30),
    Plataformas CHAR(30)
);

DROP TABLE IF EXISTS errores;
CREATE TABLE errores (
	registros CHAR(30)
);