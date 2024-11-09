USE diplomas;
DROP TABLE IF EXISTS certificados;

CREATE TABLE IF NOT EXISTS certificados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    nacionalidade VARCHAR(255) NOT NULL,
    estado VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    rg VARCHAR(255) NOT NULL,
    data_conclusao DATE NOT NULL,
    curso VARCHAR(255) NOT NULL,
    carga_horaria INT NOT NULL,
    data_emissao DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO certificados (nome, nacionalidade, estado, data_nascimento, rg, data_conclusao, curso, carga_horaria, data_emissao)
VALUES ('Nome Exemplo', 'Brasileiro', 'SP', '1990-01-01', '123456789', '2023-01-01', 'Curso Exemplo', 40, '2023-01-02')
ON DUPLICATE KEY UPDATE
    nome = VALUES(nome),
    nacionalidade = VALUES(nacionalidade),
    estado = VALUES(estado),
    data_nascimento = VALUES(data_nascimento),
    rg = VALUES(rg),
    data_conclusao = VALUES(data_conclusao),
    curso = VALUES(curso),
    carga_horaria = VALUES(carga_horaria),
    data_emissao = VALUES(data_emissao);
