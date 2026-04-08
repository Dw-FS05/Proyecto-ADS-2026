from app import app, db
from src.models import Usuario

with app.app_context():
    admin = Usuario.query.filter_by(email="admin@admin.com").first()
    if not admin:
        admin = Usuario(nombre="Administrador", email="admin@admin.com", rol="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        
    user = Usuario.query.filter_by(email="usuario@usuario.com").first()
    if not user:
        user = Usuario(nombre="Usuario Asistente", email="usuario@usuario.com", rol="asistente")
        user.set_password("usuario123")
        db.session.add(user)
        
    db.session.commit()
    print("Usuarios creados exitosamente")
