# Gesture Recognition 


## Train the model:

1. Launch the test.ipynb in Jupyter Notebook.
2. Folder structure of notebook folder is:
   Datasets/   -> Containing the dataset with json file names starting with gesture name followed by a number
   models/     -> models where pickle files will be stored
3. Once folder structure is ready and Datasets folder has the required datasets, go to Jupyter Notebook and do the below:
   Click on Cell -> Run All

## Server setup: 

   Link to send POST JSON REQUESTS : https://cse535-group17.herokuapp.com/upload

1. The Server is set-up using free cloud platform offered by Heroku and pushed into Heroku GIT repository
2. The Procfile and requirements.txt file are required for this application hosting service. 
3. The requirements.txt file has a list of required pip packages for the deploy.py application
4. The test.py contains the data processing and testing functions of the application.
5. The application was tested using Postman (https://www.postman.com/downloads/) where HTTP POST JSON requests was send and JSON response was received.