from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from .import db
import uuid  


def hexid():
    return uuid.uuid4().hex

class UserRole(Enum):
    ADMIN = 'admin'
    STAFF = 'staff'
    STUDENT = 'student'

class CustomUser(db.Model):
    __tablename__ = 'customuser'
    id = db.Column(db.String(223), primary_key=True, default=hexid)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'customuser',
        'polymorphic_on': role
    }

    #def set_password(self, password):
        #self.password_hash = generate_password_hash(password)

    #def check_password(self, password):
        #return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f"CustomUser(id='{self.id}', email='{self.email}')"

class Admin(CustomUser):
    __tablename__ = 'admins'
    id = db.Column(db.String(223), db.ForeignKey('customuser.id'), primary_key=True, default=hexid)

    __mapper_args__ = {
        'polymorphic_identity': UserRole.ADMIN.value
    }

    

class Staff(CustomUser):
    __tablename__ = 'staff'
    id = db.Column(db.String(223), db.ForeignKey('customuser.id'), primary_key=True, default=hexid)

    __mapper_args__ = {
        'polymorphic_identity': UserRole.STAFF.value
    }

    

class Student(CustomUser):
    __tablename__ = 'students'
    id = db.Column(db.String(223), db.ForeignKey('customuser.id'), primary_key=True, default=hexid)

    __mapper_args__ = {
        'polymorphic_identity': UserRole.STUDENT.value
    }

    