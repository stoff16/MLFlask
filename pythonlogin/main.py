# Importez les modules nécessaires, assurez-vous d'avoir installé scikit-learn et joblib
from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
#from passlib.hash import pbkdf2_sha256 as sha256
import joblib  # Pour charger le modèle
import numpy as np  # Si vous avez besoin de manipuler les données
import MySQLdb.cursors
import re
import MySQLdb
import joblib  # Pour charger le modèle
import numpy as np  # Si vous avez besoin de manipuler les données
from sklearn.ensemble import RandomForestClassifier
#from flask_babel import Babel, _
import os
from user import User  # Importez votre modèle User
import mysql.connector
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta



# Créez une instance de l'application Flask
app = Flask(__name__, instance_relative_config=True)
main_bp = Blueprint('main', __name__)
app.config['SECRET_KEY'] = '19581024'

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:19581024@localhost/pythonlogin'
app.config ["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)
db = SQLAlchemy(app)

# Initialisation des extensions
migrate = Migrate(app, db)
#bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)  # 'app' est votre instance Flask
login_manager.login_view = 'login'

# Initialisez votre connexion à la base de données MySQL
connection = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="19581024",
    db="pythonlogin"
)
cursor = connection.cursor(MySQLdb.cursors.DictCursor)
# Modèle User pour la base de données

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    # Ajoutez d'autres champs de modèle ici

    def set_password(self, password):
        self.password = sha256.hash(password)

    def check_password(self, password):
        return sha256.verify(password, self.password)

	
with app.app_context():
    # Maintenant, vous pouvez effectuer des opérations liées à la base de données
    db.create_all()

# Classe de formulaire de connexion
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

@login_manager.request_loader
def load_user_from_request(request):
    # Implémentez votre logique pour charger l'utilisateur depuis la requête
    # Par exemple, en utilisant des données dans la session
    user_id = session.get('user_id')  # Vous devez avoir stocké l'ID de l'utilisateur dans la session lors de la connexion
    if user_id:
        user = Account(user_id)  # Initialisez l'utilisateur à partir de l'ID
        return user

class Account(db.Model, UserMixin):
    def __init__(self, id):
        self.id = id


# Gestion de l'accueil
@app.route('/pythonlogin/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', username=current_user.username)
    else:
        return redirect(url_for('login'))
		


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Traitez les données du formulaire ici (par exemple, ajoutez l'utilisateur à la base de données)
        new_user = Account(username=form.username.data, email=form.email.data, 
                           first_name=form.first_name.data, last_name=form.last_name.data, dob=form.dob.data)
        new_user.set_password(form.password.data)  # Utilisez la fonction pour hasher le mot de passe
        db.session.add(new_user)
        db.session.commit()
        flash('Inscription réussie !', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)
	
# Classe de formulaire d'inscription
class RegistrationForm(FlaskForm):
    # ... (votre code actuel)

    def validate_username(self, field):
        cursor.execute("SELECT * FROM users WHERE username = %s", (field.data,))
        user = cursor.fetchone()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')

    def validate_email(self, field):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', field.data):
            raise ValidationError('Adresse email invalide.')


# Gestion de la connexion
#@app.route('/pythonlogin/', methods=['GET', 'POST'])
#def login():
#    if current_user.is_authenticated:
#        return redirect(url_for('home'))

#    form = LoginForm()

#    if form.validate_on_submit():
#        user = Account.query.filter_by(username=form.username.data).first()
#        if user and user.check_password(form.password.data):  # Vérifiez le mot de passe
#            login_user(user)
#            return redirect(url_for('home'))
#        else:
#            flash('Identifiant ou mot de passe incorrect. Veuillez vérifier vos informations.', 'error')

#    return render_template('login.html', form=form)

# Gestion de la connexion
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    msg = ''  # Initialisez un message vide

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        account = cursor.fetchone()

        if account and check_password_hash(account['password'], password):
            # Utilisez login_user pour gérer la connexion de l'utilisateur
            login_user(account)
            return redirect(url_for('home'))
        else:
            msg = 'Identifiant ou mot de passe incorrect. Veuillez vérifier vos informations.'
            flash(msg, 'error')  # Utilisez flash pour stocker le message d'erreur

    return render_template('home.html', msg=msg)  # Passez la variable msg dans le contexte


@app.route('/pythonlogin/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        flash('Vous avez été déconnecté avec succès.', 'success')
        return redirect(url_for('login'))
    
    # Si la demande n'est pas POST, affichez la page normale de déconnexion
    return render_template('logout.html')

#@main_bp.route('/pythonlogin/about')

@app.route('/pythonlogin/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
	
	
#@app.route('/pythonlogin/about', methods=['GET', 'POST'])
#def about():
#	if request.method == 'POST':
#        # Traitez ici les données du formulaire (non inclus dans cet exemple)
#		pass  # Remplacez par le code de traitement du formulaire
#		
#	return render_template('about.html')



@app.route('/pythonlogin/contact')
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


@app.route('/pythonlogin/some_page')
def some_page():
    if something_went_wrong:
        raise Exception("Quelque chose s'est mal passé.")

    return render_template('error.html')

@app.route('/pythonlogin/language', methods=['GET', 'POST'])
def language():
    if request.method == 'POST':
        selected_language = request.form.get('language')
        session['language'] = selected_language
        return redirect(url_for('home'))

    return render_template('language.html')

from flask import render_template

@app.route('/faq')
def faq():
    # Votre logique pour la page FAQ
    faq_data = {...}  # Obtenir les données pour la FAQ
    return render_template('faq.html', faq_data=faq_data)

	
# Ajout de la fonction get_languages au contexte global pour le rendu des templates
@app.context_processor
def inject_languages():
    return dict(get_languages=get_languages)

# Exemple de définition de la fonction get_languages
def get_languages():
    # Logic to retrieve languages
    languages = [('en', 'English'), ('fr', 'French')]  # Example language list
    return languages

# Page de profil
@app.route('/pythonlogin/profile')
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
        cursor.execute("SELECT * FROM Account WHERE username = %s", (field.data,))
        user = cursor.fetchone()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')

    def validate_email(self, field):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', field.data):
            raise ValidationError('Adresse email invalide.')



@app.route('/dashboard')
def dashboard():
    # Vous pouvez passer les variables 'username' et 'email' depuis votre application
    username = "Nom d'utilisateur"  # Remplacez par la valeur appropriée
    email = "exemple@email.com"  # Remplacez par la valeur appropriée

    return render_template('dashboard.html', username=username, email=email)

# Chargez votre modèle préalablement entraîné
model = joblib.load('C:/Users/HP/Documents/flask_app/backend/pythonlogin/models/random_forest_model.pkl')  # Assurez-vous de fournir le bon chemin


@app.route('/pythonlogin/machine_learning_models')
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

@app.route('/')
def index():
    return render_template('prediction_form.html')

@app.route('/make_prediction', methods=['POST'])
def predict():
    features = ['Azote', 'Phosphore', 'Potassium', 'pH', 'Rainfall', 'Temperature']
    form_values = [float(request.form[feature]) for feature in features]

    # Utiliser le modèle pour faire une prédiction
    prediction = model.predict([form_values])[0]

    return render_template('prediction_result.html', prediction=prediction)

@app.route('/make_prediction', methods=['POST'])
def make_prediction():
    # Votre logique de prédiction ici
    pass


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
@app.route('/pythonlogin/blog')
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


@app.route('/pythonlogin/historique')
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
@app.route('/pythonlogin/politique_confidentialite')
def politique_confidentialite():
    # Dans cette fonction, vous pouvez ajouter la logique pour afficher la page de politique de confidentialité.
    # Par exemple, vous pouvez passer le contenu de votre page de politique de confidentialité (HTML) en tant que modèle (template).
    # Voici un exemple :
    contenu_politique_confidentialite = """
    <!-- Le contenu HTML de votre page de politique de confidentialité va ici -->
    """
    return render_template('politique_confidentialite.html', contenu=contenu_politique_confidentialite)

# Route pour la page "settings.html"
@app.route('/pythonlogin/settings', methods=['GET', 'POST'])
def settings():
	if request.method == 'POST':
        # Traitez ici les données du formulaire (non inclus dans cet exemple)
		pass  # Remplacez par le code de traitement du formulaire
		
	return render_template('settings.html')

# Fermez le curseur et la connexion à la base de données lorsque l'application se termine
@app.teardown_appcontext
def close_db_connection(exception=None):
    if cursor:
        cursor.close()
    if connection:
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)
    app.register_blueprint(main_bp)