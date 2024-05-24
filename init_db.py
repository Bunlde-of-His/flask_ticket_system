from app import app, db
from app.models import Role, Group


def create_roles():
    roles = ['Admin', 'Manager', 'Analyst']
    for role_name in roles:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.session.add(role)
    db.session.commit()


def create_groups():
    groups = ['Client 1', 'Client 2', 'Client 3']
    for group_name in groups:
        group = Group.query.filter_by(name=group_name).first()
        if not group:
            group = Group(name=group_name)
            db.session.add(group)
    db.session.commit()


def init_db():
    with app.app_context():
        db.create_all()
        create_roles()
        create_groups()


if __name__ == "__main__":
    init_db()
