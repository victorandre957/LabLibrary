CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    user_photo_url VARCHAR,
    role VARCHAR NOT NULL CHECK (role IN ('MEMBER', 'ADMIN'))
);

CREATE TABLE IF NOT EXISTS Books (
    isbn SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    category VARCHAR NOT NULL CHECK (category IN ('ROMANCE', 'COMEDY', 'DRAMA', 'SCIFI', 'HORROR')),
    date_acquisition DATE NOT NULL,
    conservation_status DEFAULT 'NEW' NOT NULL CHECK (status IN ('NEW', 'AVERAGE', 'OLD', 'DAMAGED')),
    physical_location VARCHAR NOT NULL,
    book_cover_url VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'AVAILABLE' NOT NULL CHECK (status IN ('AVAILABLE', 'BORROWED')),
);

CREATE TABLE IF NOT EXISTS TeachingMaterials (
    id SERIAL PRIMARY KEY,
    author VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    category VARCHAR NOT NULL CHECK (category IN ('LAB_EQUIPMENT','EXPERIMENT_KITS', 'DIAGRAMS','SAFETY_EQUIPMENT','PRECISION_TOOLS','REPORT_WRITING_TOOLS','OTHER')),
    date_acquisition DATE NOT NULL,
    conservation_status VARCHAR DEFAULT 'NEW' NOT NULL CHECK (conservation_status IN ('NEW', 'AVERAGE', 'OLD', 'DAMAGED')),
    physical_location VARCHAR NOT NULL,
    material_cover_url VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'AVAILABLE' NOT NULL CHECK (status IN ('AVAILABLE', 'BORROWED'))
);

 CREATE TABLE IF NOT EXISTS Loan (
    id SERIAL PRIMARY KEY,
    loan_date DATE NOT NULL,
    expected_return_date DATE NOT NULL,
    status VARCHAR(255) NOT NULL,
    id_book INT REFERENCES Books(isbn),
    id_material INT REFERENCES Teaching_Materials(id),
    id_user INT REFERENCES Users(id),
    CHECK (
        (id_book IS NOT NULL AND id_material IS NULL) 
        OR 
        (id_book IS NULL AND id_material IS NOT NULL)
    ),
);

-- Descomentar as linhas abaixo apos a criacao de todas as tabelas

-- CREATE OR REPLACE FUNCTION check_return_date() RETURNS TRIGGER AS $$
-- BEGIN

--     IF NEW.expected_return_date < NEW.loan_date THEN
--         RAISE EXCEPTION 'A data de devolução não pode ser anterior à data de empréstimo.';
--     END IF;

--     IF (SELECT role FROM Users WHERE id = NEW.id_user) <> 'MEMBER' THEN
--         RAISE EXCEPTION 'Somente membros podem fazer empréstimos.';
--     END IF;

--     IF EXISTS (
--         SELECT 1 FROM Loan
--             WHERE id_user = NEW.id_user AND expected_return_date IS NULL) THEN
--         RAISE EXCEPTION 'Não é permitido realizar um novo empréstimo enquanto
--         houver um empréstimo em andamento.';
--     END IF;

--     IF NEW.id_user IS NOT NULL AND (SELECT status FROM Books WHERE isbn = NEW.id_book) <> 'AVAILABLE' THEN
--         RAISE EXCEPTION 'O livro não está disponível para empréstimo.';
--     END IF;

--     IF NEW.id_material IS NOT NULL AND (SELECT status FROM Teaching_Materials WHERE id = NEW.id_material) <> 'AVAILABLE' THEN
--         RAISE EXCEPTION 'O material técnico não está disponível para empréstimo.';
--     END IF;

--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE OR REPLACE FUNCTION encrypt_password()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     NEW.password := crypt(NEW.password, gen_salt('bf', 8));
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER encrypt_password_trigger
-- BEFORE INSERT OR UPDATE ON Users
-- FOR EACH ROW
-- EXECUTE FUNCTION encrypt_password();

-- CREATE TRIGGER check_return_date_trigger
-- BEFORE INSERT ON Loan
-- FOR EACH ROW
-- EXECUTE FUNCTION check_return_date();