CREATE TABLE diplomas (
    id SERIAL PRIMARY KEY,
    aluno_nome VARCHAR(255) NOT NULL,
    curso VARCHAR(255) NOT NULL,
    data_conclusao DATE NOT NULL,
    pdf BYTEA
);
