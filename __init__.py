from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

def get_client_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux résultats comme un dictionnaire
    return conn

def get_bibliotheque_db_connection():
    conn = sqlite3.connect('bibliotheque.db')
    conn.row_factory = sqlite3.Row
    return conn

def est_authentifie():
    return session.get('authentifie', False)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  # À remplacer par une vérification sécurisée
            session['authentifie'] = True
            return redirect(url_for('ReadBDD'))
        else:
            flash('Identifiants incorrects', 'error')
    return render_template('formulaire_authentification.html')

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = get_client_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchone()
    conn.close()
    if data:
        return render_template('read_data.html', data=data)
    flash('Client introuvable', 'error')
    return redirect(url_for('ReadBDD'))

@app.route('/consultation/')
def ReadBDD():
    conn = get_client_db_connection()
    data = conn.execute('SELECT * FROM clients').fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET', 'POST'])
def enregistrer_client():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = get_client_db_connection()
        conn.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)',
                     (created, nom, prenom, "ICI"))
        conn.commit()
        conn.close()
        flash('Client enregistré avec succès', 'success')
        return redirect(url_for('ReadBDD'))
    return render_template('formulaire.html')

@app.route('/livres')
def livres():
    conn = get_bibliotheque_db_connection()
    livres = conn.execute('SELECT * FROM Livres').fetchall()
    conn.close()
    return render_template('livres.html', livres=livres)

@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        isbn = request.form['isbn']
        genre = request.form['genre']
        date_publication = request.form['date_publication']
        quantite_disponible = request.form['quantite_disponible']

        conn = get_bibliotheque_db_connection()
        conn.execute('INSERT INTO Livres (titre, auteur, isbn, genre, date_publication, quantite_disponible) VALUES (?, ?, ?, ?, ?, ?)',
                     (titre, auteur, isbn, genre, date_publication, quantite_disponible))
        conn.commit()
        conn.close()
        flash('Livre ajouté avec succès', 'success')
        return redirect(url_for('livres'))
    return render_template('ajouter_livre.html')

@app.route('/supprimer_livre/<int:id>', methods=['POST'])
def supprimer_livre(id):
    conn = get_bibliotheque_db_connection()
    conn.execute('DELETE FROM Livres WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Livre supprimé avec succès', 'success')
    return redirect(url_for('livres'))

@app.route('/recherche_livre', methods=['GET', 'POST'])
def recherche_livre():
    livres = []
    if request.method == 'POST':
        mot_cle = request.form['mot_cle']
        conn = get_bibliotheque_db_connection()
        livres = conn.execute('SELECT * FROM Livres WHERE titre LIKE ? OR auteur LIKE ?',
                              (f'%{mot_cle}%', f'%{mot_cle}%')).fetchall()
        conn.close()
    return render_template('recherche_livre.html', livres=livres)

@app.route('/emprunter_livre/<int:id>', methods=['GET', 'POST'])
def emprunter_livre(id):
    conn = get_bibliotheque_db_connection()
    livre = conn.execute('SELECT * FROM Livres WHERE id = ?', (id,)).fetchone()
    if not livre:
        flash('Livre introuvable', 'error')
        return redirect(url_for('livres'))
    
    if request.method == 'POST':
        utilisateur_id = request.form['utilisateur_id']
        if livre['quantite_disponible'] > 0:
            conn.execute('UPDATE Livres SET quantite_disponible = quantite_disponible - 1 WHERE id = ?', (id,))
            conn.execute('INSERT INTO Emprunts (id_utilisateur, id_livre) VALUES (?, ?)',
                         (utilisateur_id, id))
            conn.commit()
            flash('Livre emprunté avec succès', 'success')
        else:
            flash('Ce livre n'est plus disponible', 'error')
        conn.close()
        return redirect(url_for('livres'))
    return render_template('emprunter_livre.html', livre=livre)

if __name__ == "__main__":
    app.run(debug=True)
