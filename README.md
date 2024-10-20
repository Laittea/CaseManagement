This will contain the model used for the project that based on the input information will give the social workers the clients baseline level of success and what their success will be after certain interventions.

The model works off of dummy data of several combinations of clients alongside the interventions chosen for them as well as their success rate at finding a job afterward. The model will be updated by the case workers by inputing new data for clients with their updated outcome information, and it can be updated on a daily, weekly, or monthly basis.

This also has an API file to interact with the front end, and logic in order to process the interventions coming from the front end. This includes functions to clean data, create a matrix of all possible combinations in order to get the ones with the highest increase of success, and output the results in a way the front end can interact with.



## Running the FastAPI project

- The project was opened and edited in PyCharm, an virtual environment was created and Python 3.10 was selected as the default inpterpretor
- Dependencies defined in the `/app/requirements.txt` file will be auto-installed PyCharm when the project was opened for the first time, this may take a while to complete
- To run the FastAPI project, open the terminal in PyCharm and
  - change the working directory into `/app`
  - run the command `fastapi dev main.py`

```bash
(venv) (base) ➜  CommonAssessmentTool-Group-Thoughtful git:(criteria2) ✗ pwd
/Users/jiayangliu/Documents/neu_csa/CS5500/CommonAssessmentTool-Group-Thoughtful

(venv) (base) ➜  CommonAssessmentTool-Group-Thoughtful git:(criteria2) ✗ cd ./app 

(venv) (base) ➜  app git:(criteria2) ✗ fastapi dev main.py 
```

By running the commands above, the FastAPI project will run in a dev environment and you can see outputs in the terminal like this:

```bash
...
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [74554] using WatchFiles
...
...
INFO:     Started server process [74558]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Which means the application was successfully started up at the port 8000 on your local machine

- Then open the url `http://127.0.0.1:8000/docs` in the browser to view the doc page of the current running project
