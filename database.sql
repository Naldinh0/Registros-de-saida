CREATE DATABASE checklist_db;

USE checklist_db;

CREATE TABLE checklists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tecnico VARCHAR(100),
    descricao TEXT,
    imagens TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
