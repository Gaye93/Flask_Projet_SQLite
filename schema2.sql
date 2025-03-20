-- schema2.sql
CREATE TABLE IF NOT EXISTS Livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    genre TEXT,
    date_publication DATE,
    quantite_disponible INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mot_de_passe TEXT NOT NULL,
    role TEXT CHECK(role IN ('utilisateur', 'administrateur')) DEFAULT 'utilisateur'
);

CREATE TABLE IF NOT EXISTS Emprunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER,
    id_livre INTEGER,
    date_emprunt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id),
    FOREIGN KEY (id_livre) REFERENCES Livres(id)
);
