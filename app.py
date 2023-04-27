from project import create_app, db
from flask_migrate import Migrate

from project.models import CustomUser,Admin,Staff,Student,UserRole





app = create_app()
migrate = Migrate(app, db)





@app.shell_context_processor
def make_shell_context():
    return dict(
        
        db=db,
        CustomUser=CustomUser,
        Admin=Admin,
        Staff=Staff,
        Student=Student,
        UserRole=UserRole
        
       
    )


if __name__ == "__main__":
    # run with debug as false using gunicorn in production
    # and debug as true locally
    db.create_all(app)
    app.run(debug=False, port=7000)


