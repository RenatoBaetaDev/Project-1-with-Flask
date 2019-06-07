<html>
  <body>
    <h1>Read me - Running the Application (NOT IN WINDOWS)</h1>
    <p>
      In order to run this application , you must have python3 installed.
    </p>
    <p>
      <li> First, you need to run <b>python3 -m venv name-of-virtual-enviroment</b> . </li> </br> 
      <li> Then, you need to activate the virtual enviroment using: <b>source name-of-virtual-enviroment/bin/activate</b> .</li> </br> 
      <li> Once the virtual enviroment is on, we need to install all the dependencies: <b>pip install -r requirements.txt</b> .</li> </br> 
      <li> Then: <b>export FLASK_APP=main.py</b> </li> </br> 
      <li> To run the application: <b>flask run</b> . Then go to your favorite browser and go to localhost:5000 .</li> </br>
      <li> To deactivate the venv, you can use <b>deactivate</b> .</li>
    </p>
  </body>
</html>
