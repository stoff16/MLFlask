from flask import render_template, request, redirect, url_for, session, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm
import joblib  # Pour charger le modèle
import numpy as np  # Si vous avez besoin de manipuler les données
from sklearn.ensemble import RandomForestClassifier
#from flask_babel import Babel, _
import os

# Page d'accueil
@app.route('/')
def home():
    return render_template('home.html')

# Gestion de l'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        # Vérification de l'existence de l'utilisateur
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Ce nom d\'utilisateur est déjà utilisé.', 'danger')
        else:
            # Hachage du mot de passe avant de l'enregistrer
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Inscription réussie. Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

# Gestion de la connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Identifiant ou mot de passe incorrect.', 'danger')

    return render_template('login.html', form=form)

# Gestion de la déconnexion
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        flash('Vous avez été déconnecté avec succès.', 'success')
        return redirect(url_for('login'))

    return render_template('logout.html')

# Autres vues et routes peuvent être ajoutées ici
@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

# Gestion des erreurs
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/some_page')
def some_page():
    if something_went_wrong:
        raise Exception("Quelque chose s'est mal passé.")

    return render_template('error.html')

@app.route('/language', methods=['GET', 'POST'])
def language():
    if request.method == 'POST':
        selected_language = request.form.get('language')
        session['language'] = selected_language
        return redirect(url_for('home'))

    return render_template('language.html')


# Page de profil
@app.route('/profile')
def profile():
    if 'logged_in' in session:
        connection = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="19581024",
            db="pythonlogin"
        )

        cursor = connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (session['username'],))
        account = cursor.fetchone()
        connection.close()

        return render_template('profile.html', account=account)

    return redirect(url_for('login'))


# Define the RegistrationForm class here
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    dob = StringField('Date of Birth', validators=[DataRequired()])

    def validate_username(self, field):
        cursor.execute("SELECT * FROM users WHERE username = %s", (field.data,))
        user = cursor.fetchone()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')

    def validate_email(self, field):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', field.data):
            raise ValidationError('Adresse email invalide.')


# Route pour afficher le tableau de bord
@app.route('/pythonlogin1/dashboard')
def dashboard1():
    # Exemple de données pour les graphiques (à personnaliser selon vos besoins)
    crop_statistics_data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        'values': [50, 60, 70, 65, 80]
    }

    irrigation_planning_data = {
        'labels': ['Champ 1', 'Champ 2', 'Champ 3', 'Champ 4', 'Champ 5'],
        'values': [30, 20, 40, 25, 35]
    }

    # Renvoyer les données au modèle dashboard.html
    return render_template('dashboard.html', crop_statistics_data=crop_statistics_data, irrigation_planning_data=irrigation_planning_data)


@app.route('/dashboard')
def dashboard():
    # Vous pouvez passer les variables 'username' et 'email' depuis votre application
    username = "Nom d'utilisateur"  # Remplacez par la valeur appropriée
    email = "exemple@email.com"  # Remplacez par la valeur appropriée

    return render_template('dashboard.html', username=username, email=email)

# Chargez votre modèle préalablement entraîné
model = joblib.load('C:/Users/HP/Documents/flask_app/backend/pythonlogin_1/random_forest_model.pkl')  # Assurez-vous de fournir le bon chemin


@app.route('/machine_learning_models')
def machine_learning_models():
    # Ici, vous devrez obtenir les données de vos modèles depuis la base de données
    # Vous pouvez utiliser une requête SQL pour sélectionner les modèles à afficher
    # Assurez-vous d'ajouter ces données sous forme d'une liste de dictionnaires dans la variable 'models'

    models = [
        {
            'id': 1,
            'model_name': 'Random Forest',
            'description': 'Modèle de classification basé sur Random Forest.',
            'accuracy': 0.92,
            'created_at': '2023-10-27 10:00:00'
        },
        # Ajoutez d'autres modèles ici
    ]

    return render_template('machine_learning_models.html', models=models)


# Créez un dictionnaire pour stocker les résultats des tests (modèle_id: résultat)
test_results = {}


# Prédiction
@app.route('/make_prediction', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Récupérez les caractéristiques à partir du formulaire
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        pH = float(request.form['pH'])
        Rainfall = float(request.form['Rainfall'])
        Temperature = float(request.form['Temperature'])

        # Préparez les caractéristiques pour la prédiction (dans un format adapté à votre modèle)
        features = [[N, P, K, pH, Rainfall, Temperature]]

        # Faites la prédiction
        prediction = model.predict(features)

        # Retournez la prédiction à afficher
        return render_template('predict.html', prediction=prediction[0])


@app.route('/test_models', methods=['POST'])
def test_models():
    # Supposons que vous récupérez les modèles depuis une base de données
    models = retrieve_models_from_database()  # Vous devez implémenter cette fonction

    if request.method == 'POST':
        selected_model_ids = request.form.getlist('selected_models')
        test_results = test_selected_models(selected_model_ids)
    else:
        test_results = {}  # Initialisation des résultats de test

    return render_template('machine_learning_models.html', models=models, test_results=test_results)


# Fonction pour tester les modèles sélectionnés
def test_selected_models(model_ids):
    test_results = {}
    for model_id in model_ids:
        result = perform_model_test(model_id)
        test_results[model_id] = result
    return test_results


# Fonction pour effectuer un test de modèle spécifique (vous devrez implémenter cela)
def perform_model_test(model_id):
    # Votre logique de test de modèle va ici
    # Cela peut impliquer l'utilisation de vos modèles d'apprentissage automatique
    # et le calcul de la précision, etc.
    return "Résultat du test pour le modèle {}".format(model_id)


# Autres routes et fonctions
@app.route('/blog')
def blog():
    # Dans cette fonction, vous pouvez charger les articles de blog depuis une base de données ou un autre endroit
    # puis les transmettre à votre modèle "blog.html" pour les afficher.

    # Exemple de données d'article de blog (remplacez par vos données réelles)
    articles = [
        {
            'title': 'Titre de l\'article 1',
            'date': '15 octobre 2023',
            'summary': 'Un résumé court de l\'article 1. Découvrez les dernières tendances en agriculture durable.',
            'url': '/blog/article1'
        },
        {
            'title': 'Titre de l\'article 2',
            'date': '10 octobre 2023',
            'summary': 'Un résumé court de l\'article 2. Comment améliorer votre exploitation agricole avec GreenTECH.',
            'url': '/blog/article2'
        },
        # Ajoutez d'autres articles ici
    ]

    return render_template('blog.html', articles=articles)


@app.route('/historique')
def historique():
    if 'logged_in' in session:
        # Ici, vous devez récupérer les données de l'historique des prédictions depuis votre source de données (par exemple, la base de données)
        # Assurez-vous de les stocker dans une liste de dictionnaires où chaque dictionnaire représente une prédiction avec des détails tels que la date et les résultats.

        # Exemple de données d'historique (à remplacer par vos données réelles)
        historique_data = [
            {
                'date': '2023-10-26',
                'resultats': 'Récolte de maïs prédite avec succès.',
            },
            {
                'date': '2023-10-20',
                'resultats': 'Récolte de blé prédite avec succès.',
            },
            # Ajoutez d'autres entrées d'historique ici
        ]

        return render_template('historique.html', historique_data=historique_data)
    return redirect(url_for('login'))

# Définir la route pour la page de politique de confidentialité
@app.route('/politique_confidentialite')
def politique_confidentialite():
    # Dans cette fonction, vous pouvez ajouter la logique pour afficher la page de politique de confidentialité.
    # Par exemple, vous pouvez passer le contenu de votre page de politique de confidentialité (HTML) en tant que modèle (template).
    # Voici un exemple :
    contenu_politique_confidentialite = """
    <!-- Le contenu HTML de votre page de politique de confidentialité va ici -->
    """
    return render_template('politique_confidentialite.html', contenu=contenu_politique_confidentialite)

# Route pour la page "setting.html"
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Traitez ici les données du formulaire (non inclus dans cet exemple)
        pass  # Remplacez par le code de traitement du formulaire

    return render_template('setting.html')