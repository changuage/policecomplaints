from App import db

class beatcomplaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beat = db.Column('beat',db.String(100), unique=False, nullable=False)
    complaint_date = db.Column('complaint_date',db.String(100), unique=False, nullable=False)
    current_category = db.Column('current_category',db.String(100), unique=False, nullable=True)
    log_no = db.Column('log_no',db.String(100), unique=False, nullable=True)
    race_of_complainant = db.Column('race_of_complainant',db.String(100), unique=False, nullable=True)


    def __repr__(self):
        return '<Track %r>' % self.title