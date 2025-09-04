-- Crear base de datos
CREATE DATABASE IF NOT EXISTS observatorio
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE observatorio;

-- Tabla de usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'editor', -- admin | editor
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de flashes informativos
CREATE TABLE flashes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(100),         -- Ej: Convocatoria, Evento, Oportunidad, Info estratégica
    title VARCHAR(255) NOT NULL,
    description TEXT,
    entity VARCHAR(255),           -- Institución/empresa
    link VARCHAR(512),             -- URL
    start_date DATE,
    end_date DATE,
    location VARCHAR(255),         -- Ciudad/Lugar
    cost VARCHAR(100),             -- Ej: Gratuito
    modality VARCHAR(60),          -- Virtual | Presencial | Híbrido
    schedule VARCHAR(120),         -- Horario
    deadline DATE,                 -- Fecha de cierre
    visible BOOLEAN DEFAULT TRUE,
    featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insertar usuario administrador inicial
INSERT INTO users (name, email, password_hash, role, active)
VALUES (
    'Administrador',
    'admin@observatorio.com',
    '$2b$12$WZpTY4Ex0VJByS7gXQya4OaR5yQ/3W5Xo8gZP5Ex7X2Dx4lqL0c3G', -- clave: admin123
    'admin',
    TRUE
);

-- (La contraseña se generó con bcrypt: "admin123")
 