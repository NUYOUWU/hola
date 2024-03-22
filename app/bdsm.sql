
CREATE DATABASE Agenda777;
USE Agenda777;

CREATE TABLE personas (
    userId INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nombreper VARCHAR(100) NOT NULL,
    apellidoper VARCHAR(100) NOT NULL,
    emailper VARCHAR(255) NOT NULL, 
    dirper VARCHAR(255) NOT NULL,
    telper VARCHAR(20) NOT NULL,
    usuarioper VARCHAR(60) NOT NULL,
    contraper VARCHAR(255) NOT NULL, 
    roles VARCHAR(20) NOT NULL
);

CREATE TABLE canciones (
    idCan INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    artista VARCHAR(100) NOT NULL,
    genero VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    duracion VARCHAR(10) NOT NULL,
    lanzamiento DATE NOT NULL,
    img BLOB NOT NULL
);


CREATE TABLE compras (
    pk_id_compra INT AUTO_INCREMENT PRIMARY KEY,
    fechaCompra DATE NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    userId INT NOT NULL,
    idCan INT NOT NULL,
    metodoPago VARCHAR(50) NOT NULL,
    FOREIGN KEY (userId) REFERENCES personas(userId),
    FOREIGN KEY (idCan) REFERENCES canciones(idCan)
);


DESCRIBE personas;
describe canciones;
select * from canciones;
describe compras;
