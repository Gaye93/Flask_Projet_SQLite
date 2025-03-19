-- Supprime les tables si elles existent déjà (pour éviter les conflits)
DROP TABLE IF EXISTS Utilisateurs;
DROP TABLE IF EXISTS Livres;
DROP TABLE IF EXISTS Emprunts;
DROP TABLE IF EXISTS Notifications;
DROP TABLE IF EXISTS Recommandations;
DROP TABLE IF EXISTS Statistiques;

-- Table Utilisateurs
CREATE TABLE Utilisateurs (
    id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mot_de_passe TEXT NOT NULL,
    role TEXT CHECK(role IN ('utilisateur', 'administrateur')) DEFAULT 'utilisateur',
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table Livres
CREATE TABLE Livres (
    id_livre INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    genre TEXT,
    date_publication DATE,
    quantite_disponible INTEGER DEFAULT 0,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table Emprunts
CREATE TABLE Emprunts (
    id_emprunt INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER,
    id_livre INTEGER,
    date_emprunt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_retour_prevue DATE,
    date_retour_effectif DATE,
    statut TEXT CHECK(statut IN ('emprunté', 'retourné')) DEFAULT 'emprunté',
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur),
    FOREIGN KEY (id_livre) REFERENCES Livres(id_livre)
);

-- Table Notifications
CREATE TABLE Notifications (
    id_notification INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER,
    id_emprunt INTEGER,
    message TEXT NOT NULL,
    date_notification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur),
    FOREIGN KEY (id_emprunt) REFERENCES Emprunts(id_emprunt)
);

-- Table Recommandations
CREATE TABLE Recommandations (
    id_recommandation INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER,
    id_livre INTEGER,
    date_recommandation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id_utilisateur),
    FOREIGN KEY (id_livre) REFERENCES Livres(id_livre)
);

-- Table Statistiques
CREATE TABLE Statistiques (
    id_statistique INTEGER PRIMARY KEY AUTOINCREMENT,
    id_livre INTEGER,
    nombre_emprunts INTEGER DEFAULT 0,
    date_statistique DATE,
    FOREIGN KEY (id_livre) REFERENCES Livres(id_livre)
);

-- Insertion de données de test (optionnel)
-- Utilisateurs
INSERT INTO Utilisateurs (nom, prenom, email, mot_de_passe, role)
VALUES ('Dupont', 'Jean', 'jean.dupont@example.com', 'motdepasse123', 'utilisateur');

INSERT INTO Utilisateurs (nom, prenom, email, mot_de_passe, role)
VALUES ('Martin', 'Alice', 'alice.martin@example.com', 'motdepasse456', 'administrateur');

-- Livres
INSERT INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible)
VALUES ('Le Petit Prince', 'Antoine de Saint-Exupéry', '9782070408504', 'Littérature', '1943-04-06', 5);

INSERT INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible)
VALUES ('1984', 'George Orwell', '9782070368228', 'Science-Fiction', '1949-06-08', 3);

-- Emprunts
INSERT INTO Emprunts (id_utilisateur, id_livre, date_retour_prevue)
VALUES (1, 1, DATE('now', '+14 days'));

-- Notifications
INSERT INTO Notifications (id_utilisateur, id_emprunt, message)
VALUES (1, 1, 'Rappel : Votre livre "Le Petit Prince" doit être retourné bientôt.');

-- Statistiques
INSERT INTO Statistiques (id_livre, nombre_emprunts, date_statistique)
VALUES (1, 1, DATE('now'));
