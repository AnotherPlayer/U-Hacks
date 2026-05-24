-- Crear base de datos (opcional)
CREATE DATABASE IF NOT EXISTS asistente_nutrimental;
USE asistente_nutrimental;

-- Tabla: pacientes
CREATE TABLE pacientes (
    id VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    peso_kg DECIMAL(5,2) NOT NULL,
    altura_cm INT NOT NULL,
    notas TEXT
);

-- Tabla: usuarios (login)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    paciente_id VARCHAR(50),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
);

-- Tabla: alimentos (catálogo)
CREATE TABLE alimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    carbohidratos_porcion DECIMAL(5,2) NOT NULL DEFAULT 0,
    proteinas_porcion DECIMAL(5,2) NOT NULL DEFAULT 0,
    grasas_porcion DECIMAL(5,2) NOT NULL DEFAULT 0,
    sodio_porcion DECIMAL(5,2) NOT NULL DEFAULT 0
);

-- Tabla: consumos (registro de alimentos consumidos)
CREATE TABLE consumos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id VARCHAR(50) NOT NULL,
    alimento_id INT NOT NULL,
    fecha DATE NOT NULL,
    porciones DECIMAL(4,2) NOT NULL DEFAULT 1,
    nivel_riesgo VARCHAR(10),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (alimento_id) REFERENCES alimentos(id) ON DELETE CASCADE
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_consumos_paciente_fecha ON consumos(paciente_id, fecha);
CREATE INDEX idx_consumos_alimento ON consumos(alimento_id);
CREATE INDEX idx_usuarios_email ON usuarios(email);