# ML model uploader

## Description
This application will fit a LightGBM regressor model than it will upload the model files to an S3 Bucket.

## Configuration files
To be able to use the project, some configuration files are needed (a single one for now):
* .env file at the project root

### .env file
The `.env` file is used to store credentials for connections to databases for instance and connection to s3 bucket. 
Since passwords are sensitive, this file should never be committed as is. Instead, a CI system will be implemented to 
insert the sensitive data in a template `.env` file.

To setup your local environment, create at the project root a `.env` file with:
```dotenv
# AWS connection
AWS_REGION=
AWS_BUCKET_NAME=
```
Fill the missing fields with their appropriate values.
