# Data Pipeline with Docker and Airflow
## Loading from AWS S3 to AWS Redshift

The main goal of this project is to transform raw event and log data stored in json files on AWS S3 into an analytics ready data model on AWS Redshift.

### Data Pipeline
![DAG](./data-pipeline-dag.PNG)

## Data Model
![model](./data-model.PNG)

### Installing
1. Install [Docker](https://www.docker.com/get-started).

2. Set up AWS:
    1. Create an [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)
    2. Generate [AWS access keys](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html)
    3. Launch a [Redshift Cluster](https://docs.aws.amazon.com/redshift/latest/gsg/rs-gsg-launch-sample-cluster.html) and enable public access


3. Start the **docker container**. [Just for PMI Member running on your local]
    ```
    docker-compose up -d
    ```

4. After a few moments the Airflow webserver will start, connect to it at http://13.212.89.106:8080/ [http://localhost:8080/admin/] [Just for PMI Member running on your local]

    Use Airflow UI to set up connections to AWS Account and AWS Redshift

    1. Go to Airflow UI Admin/Connections and navigate to the Create tab.
    ![AirFlow Admin Panel](./airflow-UI.PNG)

    2. Set up connection to AWS Account:
      * **Conn Id**: Enter `aws_credentials`.
      * **Conn Type**: Select `Amazon Web Services`.
      * **Login**: Enter your **Access key ID** from the IAM User credentials you downloaded. (AKIAIFQGGJINGVFZR6SA)
      * **Password**: Enter your **Secret access key** from the IAM User credentials you downloaded. (O73pgJIkG1AqVav5wlpBaeHZ8U2QPk82Is19g00t)


    3. Set up connection to AWS Redshift:
      * **Conn Id**: Enter `redshift`.
      * **Conn Type**: Enter `Postgres`.
      * **Host**: Enter your AWS Redshift endpoint.
      * **Schema**: Enter `dev`.
      * **Login**: Enter your AWS Redshift master user name. (pmi)
      * **Password**: Enter your AWS Redshift master user password. (Training123)
      * **Port**: Enter `5439`

### Run the DAG
1. Navigate to DAGs and switch on the sparkify_pipeline DAG
