Visualizing Complaint About Chicago Police
==========================

Flask app that is used to create spatial correlated hotspots maps of complaints about chicago police. Find the Sphinx docuentation in the /Docs folder

Currently hosted at: http://ec2-54-149-202-29.us-west-2.compute.amazonaws.com:5000/

Suggested Steps to Reproduce
--------------------------

1. Clone policecomplaints repository.

2. Create conda environment. 

    `conda create -n myenv python=2.7`
    
3. Activate environment.

    `source activate myenv`
	
   Windows Users:

    `activate myenv`

4. Install required packages. 

    `pip install -r requirements.txt`

5. Navigate to AnimalOutcomes/ and create a config.py file with the information necessary to create your database connection. **Do not commit this file.** 
     
    ```python
	import os
	basedir = os.path.abspath(os.path.dirname(__file__))

	import os
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<username>:<pasword>@<end point>.citpvzdsvfxn.us-west-2.rds.amazonaws.com:3306/<database name>'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	socrataKey = 'Socrata API Key'
    ``` 

6. Run policecomplaints/createmap.py This will pull the complaint data from the Chicago Open Data Portal. You can get an API key on their website and place in your config.py file. I have mine set up on a crontab to pull once every week.

	`python createmap.py'
	

7. Stop. flask time.

	`python application.py`
	

8. Go to the ip address of your flask app and look at some interactive maps of spatially autocorrelated hotspot maps of complaints about police.

Appendix
--------------------------

Find Makefile in the /Docs Folder. Also run pytest for unit test of the createmap.py script.



Team Members
--------------------------

<p>Project owner: Emma "Killa Bee" Li</p>
<p>Developer: Patrick Chang</p>
<p>QA: Brooke "Der Hammer" Kennedy</p>

--------

<p><small>Pivotal tracker link: https://www.pivotaltracker.com/n/projects/2142888</small></p>

--------


