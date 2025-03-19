from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('bibliotheque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Page d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')

# Authentification
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password':  # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

# Fiche client
@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

# Consultation des clients
@app.route('/consultation/')
def ReadBDD():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

# Enregistrer un client
@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = get_db_connection()
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement

# Page d'accueil
@app.route('/accueil')
def accueil():
    return render_template('base.html')

# Lister tous les livres
@app.route('/livres')
def livres():
    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM Livres').fetchall()
    conn.close()
    return render_template('livres.html', livres=livres)

# Ajouter un livre
@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        isbn = request.form['isbn']
        genre = request.form['genre']
        date_publication = request.form['date_publication']
        quantite_disponible = request.form['quantite_disponible']

        conn = get_db_connection()
        conn.execute('INSERT INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible) VALUES (?, ?, ?, ?, ?, ?)',
                     (titre, auteur, isbn, genre, date_publication, quantite_disponible))
        conn.commit()
        conn.close()
        flash('Livre ajouté avec succès !')
        return redirect(url_for('livres'))

    return render_template('ajouter_livre.html')

# Supprimer un livre
@app.route('/supprimer_livre/<int:id>', methods=['POST'])
def supprimer_livre(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Livres WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Livre supprimé avec succès !')
    return redirect(url_for('livres'))

# Rechercher des livres
@app.route('/recherche_livre', methods=['GET', 'POST'])
def recherche_livre():
    if request.method == 'POST':
        mot_cle = request.form['mot_cle']
        conn = get_db_connection()
        livres = conn.execute('SELECT * FROM Livres WHERE titre LIKE ? OR auteur LIKE ?', 
                             (f'%{mot_cle}%', f'%{mot_cle}%')).fetchall()
        conn.close()
        return render_template('recherche_livre.html', livres=livres)

    return render_template('recherche_livre.html')

# Emprunter un livre
@app.route('/emprunter_livre/<int:id>', methods=['GET', 'POST'])
def emprunter_livre(id):
    if request.method == 'POST':
        utilisateur_id = request.form['utilisateur_id']
        conn = get_db_connection()
        livre = conn.execute('SELECT * FROM Livres WHERE id = ?', (id,)).fetchone()

        if livre['quantite_disponible'] > 0:
            conn.execute('UPDATE Livres SET quantite_disponible = quantite_disponible - 1 WHERE id = ?', (id,))
            conn.execute('INSERT INTO Emprunts (id_utilisateur, id_livre) VALUES (?, ?)', 
                         (utilisateur_id, id))
            conn.commit()
            flash('Livre emprunté avec succès !')
        else:
            flash('Ce livre n\'est plus disponible.')

        conn.close()
        return redirect(url_for('livres'))

    return render_template('emprunter_livre.html', livre_id=id)

# Gestion des utilisateurs
@app.route('/gestion_utilisateurs')
def gestion_utilisateurs():
    conn = get_db_connection()
    utilisateurs = conn.execute('SELECT * FROM Utilisateurs').fetchall()
    conn.close()
    return render_template('gestion_utilisateurs.html', utilisateurs=utilisateurs)

# Gestion des stocks
@app.route('/gestion_stocks')
def gestion_stocks():
    conn = get_db_connection()
    stocks = conn.execute('SELECT * FROM Livres').fetchall()
    conn.close()
    return render_template('gestion_stocks.html', stocks=stocks)

if __name__ == "__main__":
    app.run(debug=True)
