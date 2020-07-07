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

Ensure you have the aws cli installed and configured before trying to deploy you code to AWS.

*Note that AWS lambda has a hard limit that the unzipped size of your lambda function cannot exceed 262 144 000 bytes. This can quickly lead to issues if you have many dependencies.*

 For example, the file ```api/classifier.py``` imports ```pandas``` and ```sklearn``` in order to load some data and train the model but the combination of these two dependencies causes the total size to exceed the limit. I have identified two different workarounds to get the code deployed:
1. Uninstall pandas before deploying (```pip uninstall -y pandas```). This makes the most sense as you shouldn't be performing training within the lambda execution.
1. (Advanced) Uninstall both scipy and numpy before deploying and then add the AWS provided SciPy lambda layer once the function has been deployed. (```$ pip uninstall -y scipy numpy```). The included ```zappa_settings_example.json``` file shows how to automate this step using code in ```deployment.py```.

Install zappa and initialize it.

```bash
$ pip install zappa
$ zappa init
```
This will run through the initial configuration, you can accept the defaults but **make sure** you enter ```api.app.app``` when it asks for your app's function.

```
                                                                                                                                                                                                  
███████╗ █████╗ ██████╗ ██████╗  █████╗                                                                                                                                                           
╚══███╔╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗                                                                                                                                                          
  ███╔╝ ███████║██████╔╝██████╔╝███████║                                                                                                                                                          
 ███╔╝  ██╔══██║██╔═══╝ ██╔═══╝ ██╔══██║                                                                                                                                                          
███████╗██║  ██║██║     ██║     ██║  ██║                                                                                                                                                          
╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝  ╚═╝                                                                                                                                                          
                                                                                                                                                                                                  
Welcome to Zappa!                                                                                                                                                                                 
                                                                                                                                                                                                  
Zappa is a system for running server-less Python web applications on AWS Lambda and AWS API Gateway.                                                                                              
This `init` command will help you create and configure your new Zappa deployment.                                                                                                                 
Let's get started!                                                                                                                                                                                
                                                                                                                                                                                                  
Your Zappa configuration can support multiple production stages, like 'dev', 'staging', and 'production'.                                                                                         
What do you want to call this environment (default 'dev'):                                       
                                                
AWS Lambda and API Gateway are only available in certain regions. Let's check to make sure you have a profile set up in one that will work.                                                       
Okay, using profile default!        
                                                
Your Zappa deployments will need to be uploaded to a private S3 bucket.                          
If you don't have a bucket yet, we'll create one for you too.                                    
What do you want to call your bucket? (default 'zappa-ulrkfykgd'):                               
                                                
It looks like this is a Flask application.
What's the modular path to your app's function?
This will likely be something like 'your_module.app'.                                            
Where is your app's function?: api.app.app
                                                
You can optionally deploy to all available regions in order to provide fast global service.      
If you are using Zappa for the first time, you probably don't want to do this!                   
Would you like to deploy this application globally? (default 'n') [y/n/(p)rimary]:               
                                                
Okay, here's your zappa_settings.json:
                                                
{        
    "dev": {
        "app_function": "api.app.app",
        "aws_region": "eu-west-1",
        "profile_name": "default",
        "project_name": "ml-spam-precict",
        "runtime": "python3.8",
        "s3_bucket": "zappa-ulrkfykgd"
    }                                  
}
```

Once you have setup the initialized zappa you are ready to deploy the code to AWS API Gateway.

```bash
$ zappa deploy dev
```

Zappa will now download any required dependencies and package them into a zip file which it will then deploy. After a while you will see something similar to the below:

```
Scheduling..
Scheduled 79c8de8d4b3876838570569d3356efd0c9df8-handler.keep_warm_callback with expression rate(4 minutes)!
Uploading ml-spam-predictor-dev-template-1593965358.json (1.6KiB)..
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.65k/1.65k [00:00<00:00, 3.36kB/s]
Waiting for stack ml-spam-predictor-dev to create (this can take a bit)..
 75%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████▌                                       | 3/4 [00:10<00:03,  3.37s/res]
Deploying API Gateway..
Deployment complete!: https://somerandomstring.execute-api.eu-west-1.amazonaws.com/dev
```

If everything went smoothly you should be able to access your API via the generated URL https://somerandomstring.execute-api.eu-west-1.amazonaws.com/dev
