from app import db
from app.models import Account
from app import app  # Déplacez cet import en bas

# Définissez d'autres modèles ici si nécessaire
with app.app_context():
    # Maintenant, vous pouvez effectuer des opérations liées à la base de données
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
    app.register_blueprint(main_bp)
