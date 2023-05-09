USE VISITASWEB;

# Agregar llaves primarias
ALTER TABLE visitante
ADD CONSTRAINT pk_visitante
	PRIMARY KEY (email);
    
ALTER TABLE estadistica
ADD CONSTRAINT pk_estadistica
	PRIMARY KEY (fechaEnvio, fechaOpen);
