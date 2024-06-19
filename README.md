# LYXUX

## Getting Started

### Cloning repo

To begin, the following command should be entered into your terminal:

```bash
git clone https://github.com/purple-mustache/LYXUX.git
```


### Setting up 

To set up, first you could create a virtual environment. 

>if you don't have a python virtual environment, it can be installed using the command below:

```bash
pip install virtualenv
```

To initialize the virtual environment, you then use:
```bash
python -m venv myenv
```

Now you can install all the packages required by entering the following command:
```bash
pip install requirements.txt
```

## Running the Test Script
Now that the setup is complete, you can run the flask app with thi command:
```bash
cd airflow-projects/<path to directory to be worked with>/tests

python3 -m pytest -v <test_script>.py
```
