# edit the URI below to add your RDS password and your AWS URL
# The other elements are the same as used in the tutorial
# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)
import os
#SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']

# Load config from the AWS Elastic Beanstalk Environemnt Variables for RDS
# NOTE: all the RDS env variables are automatically set by Beanstalk when
# an RDS database is added. 


# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://spencer:msia_423@db.c70edrasw7bt.us-west-2.rds.amazonaws.com:3306/epl'


# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SECRET_KEY = 'sbQm38a1awYXbmfWLgZaHCupa8egevTiZusvHx/G'