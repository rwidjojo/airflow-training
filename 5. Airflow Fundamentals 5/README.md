# Spark jobs to EMR cluster from Airflow

# Prerequisites

1. [AWS account](https://aws.amazon.com/) to set up required cloud services.
2. [Install](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config) AWS CLI on your machine.

# Data

From the project directory do

```bash
wget https://www.dropbox.com/sh/amdyc6z8744hrl5/AADS8aPTbA-dRAUjvVfjTo2qa/movie_review
mkdir ./dags/data
mv movie_review ./dags/data/movie_review.csv
```

# Setup and run

If this is your first time using AWS, make sure to check for presence of the `EMR_EC2_DefaultRole` and `EMR_DefaultRole` default role as shown below.

```bash
aws iam list-roles | grep 'EMR_DefaultRole\|EMR_EC2_DefaultRole'
# "RoleName": "EMR_DefaultRole",
# "RoleName": "EMR_EC2_DefaultRole",
```

If the roles not present, create them using the following command

```bash
aws emr create-default-roles
```

Also create a bucket, using the following command.

```bash
aws s3api create-bucket --acl public-read-write --bucket <your-bucket-name>
```

Replace `<your-bucket-name>` with your bucket name. eg.) if your bucket name is `rezaprimasatya` then the above command becomes `aws s3api create-bucket --acl public-read-write --bucket rezaprimasatya`

and press `q` to exit the prompt

After use, you can delete your S3 bucket as shown below

```bash
aws s3api delete-bucket --bucket <your-bucket-name>