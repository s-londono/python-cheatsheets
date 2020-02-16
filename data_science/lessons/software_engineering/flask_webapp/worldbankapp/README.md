### Deployment

Deploying to Heroku:

1. Put all files in a new folder:
   mv -t web_app worldbankapp wrangling_scripts worldbank.py data
   
2. Create a virtual environment containing only the libraries required by the webapp.
   
   conda update python
   
   python3 -m venv worldbankenv
   
   source worldbankenv/bin/activate
   
   pip install flask pandas plotly gunicorn

3. Install Heroku CLI. Sign up for a Heroku account: 
   [Heroku installation](https://devcenter.heroku.com/articles/heroku-cli#standalone-installation)

   curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

   heroku --version

   heroku login
   
4. Prepare app to run in a server

   Remove app.run from worldbank.py
   
   Add a Procfile with:   
   web gunicorn worldbank:app
   
5. Create requirements file:   

   pip freeze > requirements.txt
   
6. Commit to a git repository:

   git init
   
   git add .
   
   git commit -m "First commit"
   
7. Create a webapp in Heroku (this also creates a git repository in Heroku and a web address)

   heroku create dsnd-slondono-udacity-webapp
   
   git remote -v
   
   git push heroku master
   
8. App is ready!
   [https://dsnd-slondono-worldbank-webapp.herokuapp.com](https://dsnd-slondono-worldbank-webapp.herokuapp.com/)