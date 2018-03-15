from App import db
from App.models import beatcomplaint


# Creates a table in the database provided as the 'SQLALCHEMY_DATABASE_URI'
# configuration parameter in __init__.py with the schema defined by models.Track()
def create_db():
	db.create_all()
	db.session.query(beatcomplaint).delete()
	#track2 = beatcomplaint(id = 1, beat='Emancipator', complaint_date='Dusk to Dawn', current_category='Minor Cause',log_no='test',race_of_complainant='test')
	#track3 = beatcomplaint(id = 3, beat='Emancipator', complaint_date='Dusk to Dawn', current_category='Minor Cause',log_no='test',race_of_complainant='test')

	#db.session.add(track2)
	#db.session.add(track3)
	db.session.commit()

if __name__ == "__main__":
    create_db()