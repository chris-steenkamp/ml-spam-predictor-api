# Create a Flask API and Deploy to AWS API Gateway

Create a simple spam prediction API using Flask which can then be deployed to AWS API Gateway using [zappa](https://github.com/Miserlou/Zappa).

The prediction model used is based off of work done by [Susan Li](https://github.com/susanli2016/SMS-Message-Spam-Detector) and the input dataset is provided by [kaggle](https://www.kaggle.com/uciml/sms-spam-collection-dataset).

## Install Dependencies and Configure Flask

```bash
$ pip install flask scikit-learn pandas
```

## Host API Locally

```bash
$ export FLASK_APP=api.app
$ export FLASK_ENV=development
$ export FLASK_DEBUG=0

$ python -m flask run

 * Serving Flask app "api.app"
 * Environment: development
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Deployment to AWS API Gateway

Ensure you have the aws cli installed and configured.

Install zappa and initialize

```bash
$ pip install zappa
$ zappa init

$ zapp deploy dev
```