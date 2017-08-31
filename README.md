This repo contains two seeds with bokeh app that can be built upon:
* Bokeh server app - a simpler approach implementing a sample app based on Bokeh server. Basically all of the code is
 in `app.py`. This is quick to make with no need for any HTML/CSS/JS, but less flexible (e.g. it may be hard/difficult
 to react to the interaction with the charts)
    * see [https://bokeh-server-app-seed.herokuapp.com/serve_app](the app online)
* Flask app - a bit more verbose, but more robust and flexible approach that uses Flask as the primary server. This 
demonstrates how bokeh charts can be embedded (first page) as well as how a full bokeh server app can be embedded 
on a website (second page)
    * see [https://flask-app-seed.herokuapp.com/](the app online)

### setup

You need to have:
* Python3
* anaconda3

Then:
* set PYTHONPATH to contain the root of the project 
* create a new virtual environment `conda create --yes -n <name> python=3.5.2`
* activate the environment
* install dependencies `pip install -r requirements.txt`


### deploying

You need to have:
* A Heroku account. Free tier should be sufficient, although many items in conda-requirements may break 
the allowed limit

Then:
* Run the `deploy-setup.sh` script (in deploy folder) with first argument pointing to `deploy-settings.sh` of 
 the app you want to deploy
* Follow by running `deploy.sh` script with the same argument
    
