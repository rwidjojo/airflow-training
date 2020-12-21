# Package apache-airflow-providers-amazon

**Table of contents**

- [Provider package](#provider-package)
- [Installation](#installation)
- [PIP requirements](#pip-requirements)
- [Cross provider package dependencies](#cross-provider-package-dependencies)
- [Provider class summary](#provider-classes-summary)
    - [Operators](#operators)
        - [New operators](#new-operators)
        - [Moved operators](#moved-operators)
    - [Transfer operators](#transfer-operators)
        - [New transfer operators](#new-transfer-operators)
        - [Moved transfer operators](#moved-transfer-operators)
    - [Sensors](#sensors)
        - [New sensors](#new-sensors)
        - [Moved sensors](#moved-sensors)
    - [Hooks](#hooks)
        - [New hooks](#new-hooks)
        - [Moved hooks](#moved-hooks)
    - [Secrets](#secrets)
        - [Moved secrets](#moved-secrets)

## Provider package

This is a provider package for `amazon` provider. All classes for this provider package
are in `airflow.providers.amazon` python package.



## Installation

NOTE!

In order to install Airflow you need to either downgrade pip to version 20.2.4
`pip upgrade --pip==20.2.4` or, in case you use Pip 20.3, you need to add option
`--use-deprecated legacy-resolver` to your pip install command.

You can install this package on top of an existing airflow 2.* installation via
`pip install apache-airflow-providers-amazon`

## PIP requirements

| PIP package   | Version required   |
|:--------------|:-------------------|
| boto3         | &gt;=1.15.0,&lt;1.16.0   |
| botocore      | &gt;=1.18.0,&lt;1.19.0   |
| watchtower    | ~=0.7.3            |

## Cross provider package dependencies

Those are dependencies that might be needed in order to use all the features of the package.
You need to install the specified backport providers package in order to use them.

You can install such cross-provider dependencies when installing from PyPI. For example:

```bash
pip install apache-airflow-providers-amazon[apache.hive]
```

| Dependent package                                                                                     | Extra       |
|:------------------------------------------------------------------------------------------------------|:------------|
| [apache-airflow-providers-apache-hive](https://pypi.org/project/apache-airflow-providers-apache-hive) | apache.hive |
| [apache-airflow-providers-google](https://pypi.org/project/apache-airflow-providers-google)           | google      |
| [apache-airflow-providers-imap](https://pypi.org/project/apache-airflow-providers-imap)               | imap        |
| [apache-airflow-providers-mongo](https://pypi.org/project/apache-airflow-providers-mongo)             | mongo       |
| [apache-airflow-providers-mysql](https://pypi.org/project/apache-airflow-providers-mysql)             | mysql       |
| [apache-airflow-providers-postgres](https://pypi.org/project/apache-airflow-providers-postgres)       | postgres    |
| [apache-airflow-providers-ssh](https://pypi.org/project/apache-airflow-providers-ssh)                 | ssh         |

# Provider classes summary

In Airflow 2.0, all operators, transfers, hooks, sensors, secrets for the `amazon` provider
are in the `airflow.providers.amazon` package. You can read more about the naming conventions used
in [Naming conventions for provider packages](https://github.com/apache/airflow/blob/master/CONTRIBUTING.rst#naming-conventions-for-provider-packages)


## Operators


### New operators

| New Airflow 2.0 operators: `airflow.providers.amazon` package                                                                                                                                                         |
|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [aws.operators.cloud_formation.CloudFormationCreateStackOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/cloud_formation.py)                                            |
| [aws.operators.cloud_formation.CloudFormationDeleteStackOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/cloud_formation.py)                                            |
| [aws.operators.datasync.AWSDataSyncOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/datasync.py)                                                                        |
| [aws.operators.ec2_start_instance.EC2StartInstanceOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/ec2_start_instance.py)                                               |
| [aws.operators.ec2_stop_instance.EC2StopInstanceOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/ec2_stop_instance.py)                                                  |
| [aws.operators.emr_modify_cluster.EmrModifyClusterOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/emr_modify_cluster.py)                                               |
| [aws.operators.glacier.GlacierCreateJobOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/glacier.py)                                                                     |
| [aws.operators.glue.AwsGlueJobOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/glue.py)                                                                                 |
| [aws.operators.s3_bucket.S3CreateBucketOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/s3_bucket.py)                                                                   |
| [aws.operators.s3_bucket.S3DeleteBucketOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/s3_bucket.py)                                                                   |
| [aws.operators.s3_file_transform.S3FileTransformOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/s3_file_transform.py)                                                  |
| [aws.operators.sagemaker_processing.SageMakerProcessingOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/sagemaker_processing.py)                                        |
| [aws.operators.step_function_get_execution_output.StepFunctionGetExecutionOutputOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/step_function_get_execution_output.py) |
| [aws.operators.step_function_start_execution.StepFunctionStartExecutionOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/step_function_start_execution.py)               |


### Moved operators

| Airflow 2.0 operators: `airflow.providers.amazon` package                                                                                                                                    | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                                                                                                                |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [aws.operators.athena.AWSAthenaOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/athena.py)                                                     | [contrib.operators.aws_athena_operator.AWSAthenaOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/aws_athena_operator.py)                                             |
| [aws.operators.batch.AwsBatchOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/batch.py)                                                        | [contrib.operators.awsbatch_operator.AWSBatchOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/awsbatch_operator.py)                                                  |
| [aws.operators.ecs.ECSOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/ecs.py)                                                                 | [contrib.operators.ecs_operator.ECSOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/ecs_operator.py)                                                                 |
| [aws.operators.emr_add_steps.EmrAddStepsOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/emr_add_steps.py)                                     | [contrib.operators.emr_add_steps_operator.EmrAddStepsOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/emr_add_steps_operator.py)                                     |
| [aws.operators.emr_create_job_flow.EmrCreateJobFlowOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/emr_create_job_flow.py)                    | [contrib.operators.emr_create_job_flow_operator.EmrCreateJobFlowOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/emr_create_job_flow_operator.py)                    |
| [aws.operators.emr_terminate_job_flow.EmrTerminateJobFlowOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/emr_terminate_job_flow.py)           | [contrib.operators.emr_terminate_job_flow_operator.EmrTerminateJobFlowOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/emr_terminate_job_flow_operator.py)           |
| [aws.operators.s3_copy_object.S3CopyObjectOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/s3_copy_object.py)                                  | [contrib.operators.s3_copy_object_operator.S3CopyObjectOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/s3_copy_object_operator.py)                                  |
| [aws.operators.s3_delete_objects.S3DeleteObjectsOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/s3_delete_objects.py)                         | [contrib.operators.s3_delete_objects_operator.S3DeleteObjectsOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/s3_delete_objects_operator.py)                         |
| [aws.operators.s3_list.S3ListOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/s3_list.py)                                                      | [contrib.operators.s3_list_operator.S3ListOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/s3_list_operator.py)                                                      |
| [aws.operators.sagemaker_base.SageMakerBaseOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/sagemaker_base.py)                                 | [contrib.operators.sagemaker_base_operator.SageMakerBaseOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/sagemaker_base_operator.py)                                 |
| [aws.operators.sagemaker_endpoint.SageMakerEndpointOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/sagemaker_endpoint.py)                     | [contrib.operators.sagemaker_endpoint_operator.SageMakerEndpointOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/sagemaker_endpoint_operator.py)                     |
| [aws.operators.sagemaker_endpoint_config.SageMakerEndpointConfigOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/sagemaker_endpoint_config.py) | [contrib.operators.sagemaker_endpoint_config_operator.SageMakerEndpointConfigOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/sagemaker_endpoint_config_operator.py) |
| [aws.operators.sagemaker_model.SageMakerModelOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/sagemaker_model.py)                              | [contrib.operators.sagemaker_model_operator.SageMakerModelOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/sagemaker_model_operator.py)                              |
| [aws.operators.sagemaker_training.SageMakerTrainingOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/sagemaker_training.py)                     | [contrib.operators.sagemaker_training_operator.SageMakerTrainingOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/sagemaker_training_operator.py)                     |
| [aws.operators.sagemaker_transform.SageMakerTransformOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/sagemaker_transform.py)                  | [contrib.operators.sagemaker_transform_operator.SageMakerTransformOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/sagemaker_transform_operator.py)                  |
| [aws.operators.sagemaker_tuning.SageMakerTuningOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/sagemaker_tuning.py)                           | [contrib.operators.sagemaker_tuning_operator.SageMakerTuningOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/sagemaker_tuning_operator.py)                           |
| [aws.operators.sns.SnsPublishOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/sns.py)                                                          | [contrib.operators.sns_publish_operator.SnsPublishOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/sns_publish_operator.py)                                          |
| [aws.operators.sqs.SQSPublishOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/operators/sqs.py)                                                          | [contrib.operators.aws_sqs_publish_operator.SQSPublishOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/aws_sqs_publish_operator.py)                                  |


## Transfer operators


### New transfer operators

| New Airflow 2.0 transfers: `airflow.providers.amazon` package                                                                                               |
|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [aws.transfers.glacier_to_gcs.GlacierToGCSOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/transfers/glacier_to_gcs.py) |
| [aws.transfers.mysql_to_s3.MySQLToS3Operator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/transfers/mysql_to_s3.py)          |


### Moved transfer operators

| Airflow 2.0 transfers: `airflow.providers.amazon` package                                                                                                                       | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                                                                                                   |
|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [aws.transfers.dynamodb_to_s3.DynamoDBToS3Operator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/transfers/dynamodb_to_s3.py)                     | [contrib.operators.dynamodb_to_s3.DynamoDBToS3Operator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/dynamodb_to_s3.py)                                       |
| [aws.transfers.gcs_to_s3.GCSToS3Operator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/transfers/gcs_to_s3.py)                                    | [operators.gcs_to_s3.GCSToS3Operator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/operators/gcs_to_s3.py)                                                                      |
| [aws.transfers.google_api_to_s3.GoogleApiToS3Operator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/transfers/google_api_to_s3.py)                | [operators.google_api_to_s3_transfer.GoogleApiToS3Transfer](https://github.com/apache/airflow/blob/v1-10-stable/airflow/operators/google_api_to_s3_transfer.py)                                |
| [aws.transfers.hive_to_dynamodb.HiveToDynamoDBOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/transfers/hive_to_dynamodb.py)               | [contrib.operators.hive_to_dynamodb.HiveToDynamoDBOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/hive_to_dynamodb.py)                                 |
| [aws.transfers.imap_attachment_to_s3.ImapAttachmentToS3Operator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/transfers/imap_attachment_to_s3.py) | [contrib.operators.imap_attachment_to_s3_operator.ImapAttachmentToS3Operator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/imap_attachment_to_s3_operator.py) |
| [aws.transfers.mongo_to_s3.MongoToS3Operator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/transfers/mongo_to_s3.py)                              | [contrib.operators.mongo_to_s3.MongoToS3Operator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/mongo_to_s3.py)                                                |
| [aws.transfers.redshift_to_s3.RedshiftToS3Operator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/transfers/redshift_to_s3.py)                     | [operators.redshift_to_s3_operator.RedshiftToS3Transfer](https://github.com/apache/airflow/blob/v1-10-stable/airflow/operators/redshift_to_s3_operator.py)                                     |
| [aws.transfers.s3_to_redshift.S3ToRedshiftOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/transfers/s3_to_redshift.py)                     | [operators.s3_to_redshift_operator.S3ToRedshiftTransfer](https://github.com/apache/airflow/blob/v1-10-stable/airflow/operators/s3_to_redshift_operator.py)                                     |
| [aws.transfers.s3_to_sftp.S3ToSFTPOperator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/transfers/s3_to_sftp.py)                                 | [contrib.operators.s3_to_sftp_operator.S3ToSFTPOperator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/s3_to_sftp_operator.py)                                 |
| [aws.transfers.sftp_to_s3.SFTPToS3Operator](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/transfers/sftp_to_s3.py)                                 | [contrib.operators.sftp_to_s3_operator.SFTPToS3Operator](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/operators/sftp_to_s3_operator.py)                                 |


## Sensors


### New sensors

| New Airflow 2.0 sensors: `airflow.providers.amazon` package                                                                                                                      |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [aws.sensors.cloud_formation.CloudFormationCreateStackSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/cloud_formation.py)             |
| [aws.sensors.cloud_formation.CloudFormationDeleteStackSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/cloud_formation.py)             |
| [aws.sensors.ec2_instance_state.EC2InstanceStateSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/ec2_instance_state.py)                |
| [aws.sensors.glacier.GlacierJobOperationSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/glacier.py)                                   |
| [aws.sensors.glue.AwsGlueJobSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/glue.py)                                                  |
| [aws.sensors.redshift.AwsRedshiftClusterSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/redshift.py)                                  |
| [aws.sensors.s3_keys_unchanged.S3KeysUnchangedSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/s3_keys_unchanged.py)                   |
| [aws.sensors.sagemaker_training.SageMakerTrainingSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/sagemaker_training.py)               |
| [aws.sensors.step_function_execution.StepFunctionExecutionSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/step_function_execution.py) |


### Moved sensors

| Airflow 2.0 sensors: `airflow.providers.amazon` package                                                                                                                          | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                                                                                                        |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [aws.sensors.athena.AthenaSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/athena.py)                                                  | [contrib.sensors.aws_athena_sensor.AthenaSensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/sensors/aws_athena_sensor.py)                                                  |
| [aws.sensors.emr_base.EmrBaseSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/emr_base.py)                                             | [contrib.sensors.emr_base_sensor.EmrBaseSensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/sensors/emr_base_sensor.py)                                                     |
| [aws.sensors.emr_job_flow.EmrJobFlowSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/emr_job_flow.py)                                  | [contrib.sensors.emr_job_flow_sensor.EmrJobFlowSensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/sensors/emr_job_flow_sensor.py)                                          |
| [aws.sensors.emr_step.EmrStepSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/emr_step.py)                                             | [contrib.sensors.emr_step_sensor.EmrStepSensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/sensors/emr_step_sensor.py)                                                     |
| [aws.sensors.glue_catalog_partition.AwsGlueCatalogPartitionSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/glue_catalog_partition.py) | [contrib.sensors.aws_glue_catalog_partition_sensor.AwsGlueCatalogPartitionSensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/sensors/aws_glue_catalog_partition_sensor.py) |
| [aws.sensors.s3_key.S3KeySensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/s3_key.py)                                                   | [sensors.s3_key_sensor.S3KeySensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/sensors/s3_key_sensor.py)                                                                           |
| [aws.sensors.s3_prefix.S3PrefixSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/s3_prefix.py)                                          | [sensors.s3_prefix_sensor.S3PrefixSensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/sensors/s3_prefix_sensor.py)                                                                  |
| [aws.sensors.sagemaker_base.SageMakerBaseSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/sagemaker_base.py)                           | [contrib.sensors.sagemaker_base_sensor.SageMakerBaseSensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/sensors/sagemaker_base_sensor.py)                                   |
| [aws.sensors.sagemaker_endpoint.SageMakerEndpointSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/sagemaker_endpoint.py)               | [contrib.sensors.sagemaker_endpoint_sensor.SageMakerEndpointSensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/sensors/sagemaker_endpoint_sensor.py)                       |
| [aws.sensors.sagemaker_transform.SageMakerTransformSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/sagemaker_transform.py)            | [contrib.sensors.sagemaker_transform_sensor.SageMakerTransformSensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/sensors/sagemaker_transform_sensor.py)                    |
| [aws.sensors.sagemaker_tuning.SageMakerTuningSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/sagemaker_tuning.py)                     | [contrib.sensors.sagemaker_tuning_sensor.SageMakerTuningSensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/sensors/sagemaker_tuning_sensor.py)                             |
| [aws.sensors.sqs.SQSSensor](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/sensors/sqs.py)                                                           | [contrib.sensors.aws_sqs_sensor.SQSSensor](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/sensors/aws_sqs_sensor.py)                                                           |


## Hooks


### New hooks

| New Airflow 2.0 hooks: `airflow.providers.amazon` package                                                                                                                                    |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [aws.hooks.batch_client.AwsBatchClientHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/batch_client.py)                                                |
| [aws.hooks.batch_waiters.AwsBatchWaitersHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/batch_waiters.py)                                             |
| [aws.hooks.cloud_formation.AWSCloudFormationHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/cloud_formation.py)                                       |
| [aws.hooks.ec2.EC2Hook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/ec2.py)                                                                             |
| [aws.hooks.elasticache_replication_group.ElastiCacheReplicationGroupHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/elasticache_replication_group.py) |
| [aws.hooks.glacier.GlacierHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/glacier.py)                                                                 |
| [aws.hooks.glue.AwsGlueJobHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/glue.py)                                                                    |
| [aws.hooks.kinesis.AwsFirehoseHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/kinesis.py)                                                             |
| [aws.hooks.redshift.RedshiftHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/redshift.py)                                                              |
| [aws.hooks.secrets_manager.SecretsManagerHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/secrets_manager.py)                                          |
| [aws.hooks.ses.SESHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/ses.py)                                                                             |
| [aws.hooks.step_function.StepFunctionHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/step_function.py)                                                |


### Moved hooks

| Airflow 2.0 hooks: `airflow.providers.amazon` package                                                                                          | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                                                                 |
|:-----------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [aws.hooks.athena.AWSAthenaHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/athena.py)                   | [contrib.hooks.aws_athena_hook.AWSAthenaHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/aws_athena_hook.py)                  |
| [aws.hooks.base_aws.AwsBaseHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/base_aws.py)                 | [contrib.hooks.aws_hook.AwsHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/aws_hook.py)                                      |
| [aws.hooks.datasync.AWSDataSyncHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/datasync.py)             | [contrib.hooks.aws_datasync_hook.AWSDataSyncHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/aws_datasync_hook.py)            |
| [aws.hooks.dynamodb.AwsDynamoDBHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/dynamodb.py)             | [contrib.hooks.aws_dynamodb_hook.AwsDynamoDBHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/aws_dynamodb_hook.py)            |
| [aws.hooks.emr.EmrHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/emr.py)                               | [contrib.hooks.emr_hook.EmrHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/emr_hook.py)                                      |
| [aws.hooks.glue_catalog.AwsGlueCatalogHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/glue_catalog.py)  | [contrib.hooks.aws_glue_catalog_hook.AwsGlueCatalogHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/aws_glue_catalog_hook.py) |
| [aws.hooks.lambda_function.AwsLambdaHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/lambda_function.py) | [contrib.hooks.aws_lambda_hook.AwsLambdaHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/aws_lambda_hook.py)                  |
| [aws.hooks.logs.AwsLogsHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/logs.py)                         | [contrib.hooks.aws_logs_hook.AwsLogsHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/aws_logs_hook.py)                        |
| [aws.hooks.s3.S3Hook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/s3.py)                                  | [hooks.S3_hook.S3Hook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/hooks/S3_hook.py)                                                         |
| [aws.hooks.sagemaker.SageMakerHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/sagemaker.py)             | [contrib.hooks.sagemaker_hook.SageMakerHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/sagemaker_hook.py)                    |
| [aws.hooks.sns.AwsSnsHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/sns.py)                            | [contrib.hooks.aws_sns_hook.AwsSnsHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/aws_sns_hook.py)                           |
| [aws.hooks.sqs.SQSHook](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/hooks/sqs.py)                               | [contrib.hooks.aws_sqs_hook.SQSHook](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/hooks/aws_sqs_hook.py)                              |


## Secrets



### Moved secrets

| Airflow 2.0 secrets: `airflow.providers.amazon` package                                                                                                                  | Airflow 1.10.* previous location (usually `airflow.contrib`)                                                                                                                  |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [aws.secrets.secrets_manager.SecretsManagerBackend](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/secrets/secrets_manager.py)               | [contrib.secrets.aws_secrets_manager.SecretsManagerBackend](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/secrets/aws_secrets_manager.py)               |
| [aws.secrets.systems_manager.SystemsManagerParameterStoreBackend](https://github.com/apache/airflow/blob/master/airflow/providers/amazon/aws/secrets/systems_manager.py) | [contrib.secrets.aws_systems_manager.SystemsManagerParameterStoreBackend](https://github.com/apache/airflow/blob/v1-10-stable/airflow/contrib/secrets/aws_systems_manager.py) |