import sqlite3

# Connexion à la base de données (elle sera créée si elle n'existe pas)
connection = sqlite3.connect('bibliotheque.db')

# Lecture et exécution du fichier schema.sql
with open('schema2.sql') as f:
    connection.executescript(f.read())

# Création d'un curseur pour exécuter des requêtes SQL
cur = connection.cursor()

# Insertion de données de test dans la table Livres
cur.execute("INSERT INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible) VALUES (?, ?, ?, ?, ?, ?)",
            ('Le Petit Prince', 'Antoine de Saint-Exupéry', '9782070408504', 'Littérature', '1943-04-06', 5))

cur.execute("INSERT INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible) VALUES (?, ?, ?, ?, ?, ?)",
            ('1984', 'George Orwell', '9782070368228', 'Science-Fiction', '1949-06-08', 3))

cur.execute("INSERT INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible) VALUES (?, ?, ?, ?, ?, ?)",
            ('Le Seigneur des Anneaux', 'J.R.R. Tolkien', '9782266282362', 'Fantasy', '1954-07-29', 7))

cur.execute("INSERT INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible) VALUES (?, ?, ?, ?, ?, ?)",
            ('Harry Potter à l\'école des sorciers', 'J.K. Rowling', '9782070584628', 'Fantasy', '1997-06-26', 10))

cur.execute("INSERT INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible) VALUES (?, ?, ?, ?, ?, ?)",
            ('Les Misérables', 'Victor Hugo', '9782070409228', 'Classique', '1862-01-01', 4))

cur.execute("INSERT INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible) VALUES (?, ?, ?, ?, ?, ?)",
            ('Orgueil et Préjugés', 'Jane Austen', '9782070413553', 'Romance', '1813-01-28', 6))

cur.execute("INSERT INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible) VALUES (?, ?, ?, ?, ?, ?)",
            ('Le Comte de Monte-Cristo', 'Alexandre Dumas', '9782070413560', 'Aventure', '1844-01-01', 2))

cur.execute("INSERT INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible) VALUES (?, ?, ?, ?, ?, ?)",
            ('Crime et Châtiment', 'Fiodor Dostoïevski', '9782070413577', 'Philosophie', '1866-01-01', 3))

# Validation des changements
connection.commit()

# Fermeture de la connexion
connection.close()

print("Base de données 'bibliotheque.db' initialisée avec succès et données de test insérées !")
