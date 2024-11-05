This will contain the model used for the project that based on the input information will give the social workers the clients baseline level of success and what their success will be after certain interventions.

The model works off of dummy data of several combinations of clients alongside the interventions chosen for them as well as their success rate at finding a job afterward. The model will be updated by the case workers by inputing new data for clients with their updated outcome information, and it can be updated on a daily, weekly, or monthly basis.

This also has an API file to interact with the front end, and logic in order to process the interventions coming from the front end. This includes functions to clean data, create a matrix of all possible combinations in order to get the ones with the highest increase of success, and output the results in a way the front end can interact with.

## Run the FastAPI project

- Clone the git repo

```bash
# clone the project from git repo
git clone https://github.com/JiayangLJY/CommonAssessmentTool-Group-Thoughtful.git
```



* Prepare the virtual environment

```bash
# cd to the project root dir
cd CommonAssessmentTool-Group-Thoughtful

# create a virtual env for the current project
python3 -m venv venv

# activate the virtual env
source venv/bin/activate

# install denpendency packages
pip install -r requirements.txt

# export python path
export PYTHONPATH=$(pwd):$PYTHONPATH
```

> - to deactivate the current virtual env:
>
>   ```bash
>   deactivate
>   ```



- Run Fastapi application

```bash
# cd to the {project}/app dir
cd app

# run project in dev mode
fastapi dev main.py 
```

- Then open the url `http://127.0.0.1:8000/docs` in the browser to view the doc page of the current running project

