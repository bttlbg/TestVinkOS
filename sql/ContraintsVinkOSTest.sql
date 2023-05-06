USE VISITASWEB;

# Agregar llaves primarias
ALTER TABLE visitante
ADD CONSTRAINT pk_visitante
	PRIMARY KEY (email);
    
ALTER TABLE estadistica
ADD CONSTRAINT pk_estadistica
	PRIMARY KEY (fechaEnvio);
    
# Agregar llaves foraneas
ALTER TABLE estadistica
ADD CONSTRAINT fk_estadistica
	FOREIGN KEY (email)
    REFERENCES visitante(email);