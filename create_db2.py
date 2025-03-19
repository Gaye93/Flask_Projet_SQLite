import sqlite3

# Connexion à la base de données
connection = sqlite3.connect('bibliotheque.db')

# Lecture et exécution du fichier schema2.sql
with open('schema2.sql') as f:
    connection.executescript(f.read())

# Création d'un curseur pour exécuter des requêtes SQL
cur = connection.cursor()

# Liste des livres à insérer
livres = [
    ('Le Petit Prince', 'Antoine de Saint-Exupéry', '9782070408504', 'Littérature', '1943-04-06', 5),
    ('1984', 'George Orwell', '9782070368228', 'Science-Fiction', '1949-06-08', 3),
    ('Le Seigneur des Anneaux', 'J.R.R. Tolkien', '9782266282362', 'Fantasy', '1954-07-29', 7),
    ('Harry Potter à l\'école des sorciers', 'J.K. Rowling', '9782070584628', 'Fantasy', '1997-06-26', 10),
    ('Les Misérables', 'Victor Hugo', '9782070409228', 'Classique', '1862-01-01', 4),
    ('Orgueil et Préjugés', 'Jane Austen', '9782070413553', 'Romance', '1813-01-28', 6),
    ('Le Comte de Monte-Cristo', 'Alexandre Dumas', '9782070413560', 'Aventure', '1844-01-01', 2),
    ('Crime et Châtiment', 'Fiodor Dostoïevski', '9782070413577', 'Philosophie', '1866-01-01', 3),
]

# Insertion des livres avec INSERT OR IGNORE
for livre in livres:
    cur.execute("INSERT OR IGNORE INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible) VALUES (?, ?, ?, ?, ?, ?)", livre)

# Liste des utilisateurs à insérer
utilisateurs = [
    ('Dupont', 'Jean', 'jean.dupont@example.com', 'motdepasse123'),
    ('Martin', 'Alice', 'alice.martin@example.com', 'motdepasse456'),
    ('Durand', 'Pierre', 'pierre.durand@example.com', 'motdepasse789'),
]

# Insertion des utilisateurs avec INSERT OR IGNORE
for utilisateur in utilisateurs:
    cur.execute("INSERT OR IGNORE INTO Utilisateurs (nom, prenom, email, mot_de_passe) VALUES (?, ?, ?, ?)", utilisateur)

# Liste des emprunts à insérer
emprunts = [
    (1, 1),  # Utilisateur 1 emprunte le livre 1
    (2, 3),  # Utilisateur 2 emprunte le livre 3
]

# Insertion des emprunts avec INSERT OR IGNORE
for emprunt in emprunts:
    cur.execute("INSERT OR IGNORE INTO Emprunts (id_utilisateur, id_livre) VALUES (?, ?)", emprunt)

# Validation des changements
connection.commit()

# Fermeture de la connexion
connection.close()

print("Base de données 'bibliotheque.db' initialisée avec succès et données de test insérées !")
