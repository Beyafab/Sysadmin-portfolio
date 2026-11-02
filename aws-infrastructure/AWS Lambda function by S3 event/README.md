# AWS Serverless CSV Processing Pipeline

## Project Overview

This project demonstrates an event-driven, serverless data processing pipeline built using **Amazon S3, AWS Lambda, and Amazon DynamoDB**.

Whenever a CSV file is uploaded to an Amazon S3 bucket, an S3 event notification automatically triggers an AWS Lambda function. The Lambda function reads the CSV file, extracts the last data record, processes its values using Python, and stores the record in an Amazon DynamoDB table.

The project demonstrates practical experience with AWS serverless architecture, event-driven automation, Python programming, IAM permissions, and cloud monitoring.

## Architecture

```text
        CSV File
            |
            v
      Amazon S3
   (File Upload Event)
            |
            v
      AWS Lambda
      (Python 3.10)
            |
            v
      Read CSV File
            |
            v
    Extract Last Record
            |
            v
    Process and Validate
            |
            v
     Amazon DynamoDB
       (custometable)
```

## AWS Services and Technologies

| Technology | Purpose |
|---|---|
| Amazon S3 | Stores uploaded CSV files |
| AWS Lambda | Executes the Python processing function |
| Amazon DynamoDB | Stores the processed CSV record |
| AWS IAM | Controls permissions between AWS services |
| Amazon CloudWatch | Monitors Lambda execution and troubleshooting |
| Python 3.10 | Implements the data processing logic |
| Boto3 | Python SDK for interacting with AWS services |

## Project Configuration

| Component | Configuration |
|---|---|
| AWS Region | `us-east-1` |
| S3 Bucket | `lambdadaynamos3` |
| Lambda Function | `s3trigerlambda` |
| Lambda Runtime | Python 3.10 |
| DynamoDB Table | `custometable` |
| Partition Key | `username` |
| Sort Key | `full_name` |

## How It Works

### 1. CSV Upload to Amazon S3

A CSV file named `sorted_output.csv` is uploaded to the S3 bucket.

The S3 bucket is configured with an event notification that invokes the Lambda function when a new object is created.

### 2. AWS Lambda Trigger

The S3 event automatically invokes the Lambda function.

The function retrieves:
- S3 bucket name
- Uploaded file name
- S3 object information

### 3. CSV Processing with Python

The Lambda function uses Python libraries to retrieve and process the CSV file.

Main libraries:

- `csv`: Reads CSV records.
- `io`: Processes CSV content in memory.
- `json`: Formats Lambda responses.
- `boto3`: Communicates with AWS services.
- `decimal`: Handles numeric values accurately.
- `urllib.parse`: Decodes S3 object filenames.

The function extracts the **last data row** from the uploaded CSV file.

### 4. DynamoDB Integration

After extracting the last record, Lambda prepares a DynamoDB item and writes it to the `custometable` table using the `put_item()` operation.

The table uses a composite primary key:

- Partition key: `username`
- Sort key: `full_name`

### 5. Monitoring with CloudWatch

Amazon CloudWatch captures Lambda execution logs.

The logs help monitor:
- S3 file processing.
- DynamoDB table availability.
- Successful record insertion.
- Errors during execution.
- Function execution duration.

## CSV Data Structure

The CSV file contains the following columns:

| Attribute | Description |
|---|---|
| `username` | Student username |
| `full_name` | Student full name |
| `gender` | Gender |
| `institution_name` | Educational institution |
| `exam_topic_name` | Examination topic |
| `year` | Examination year |
| `total_score` | Total examination score |
| `is_disqualified` | Disqualification flag |
| `is_absent` | Absence flag |
| `supervisor_report` | Supervisor report flag |
| `status` | Student examination status |

The `total_score` attribute is converted to Python `Decimal` before being stored in DynamoDB. The three flag attributes are converted to integers.

## IAM Permissions

The Lambda execution role requires permissions to access the S3 object and interact with DynamoDB.

### Amazon S3

Required action:

```json
"s3:GetObject"
```

Resource:

```text
arn:aws:s3:::lambdadaynamos3/*
```

### Amazon DynamoDB

Required actions:

```json
[
    "dynamodb:DescribeTable",
    "dynamodb:PutItem"
]
```

Resource:

```text
arn:aws:dynamodb:us-east-1:YOUR_ACCOUNT_ID:table/custometable
```

Replace `YOUR_ACCOUNT_ID` with your AWS account ID.

### CloudWatch Logs

The Lambda execution role also needs permissions to create log groups, log streams, and publish log events.

The AWS-managed `AWSLambdaBasicExecutionRole` policy provides these permissions.

## Implementation Steps

1. Create an Amazon S3 bucket.
2. Upload the CSV file to the bucket.
3. Create a DynamoDB table named `custometable`.
4. Configure `username` as the partition key and `full_name` as the sort key.
5. Create an AWS Lambda function using Python 3.10.
6. Configure the Lambda execution role with the required IAM permissions.
7. Configure an S3 event notification to trigger the Lambda function on object creation.
8. Deploy the Python Lambda code.
9. Upload a CSV file to S3 to initiate the processing workflow.
10. Verify the execution in CloudWatch and confirm the record in DynamoDB.

## Testing and Results

The project was successfully tested using the uploaded file:

`sorted_output.csv`

CloudWatch confirmed successful execution.

Example execution output:

```text
Processing file: s3://lambdadaynamos3/sorted_output.csv

DynamoDB region: us-east-1
DynamoDB table: custometable

DynamoDB table status: ACTIVE

Successfully saved username: euee00575516
```

The Lambda function successfully processed the CSV file and saved its last data record to DynamoDB.

**Observed execution duration:** Approximately 318–621 milliseconds across the two successful test executions.

## Challenges and Troubleshooting

During implementation, several issues were encountered and resolved.

| Challenge | Resolution |
|---|---|
| DynamoDB AccessDeniedException | Updated Lambda execution role permissions |
| ResourceNotFoundException | Corrected DynamoDB table name |
| Table configuration | Verified the AWS region and table status |
| CSV encoding | Used `utf-8-sig` to handle UTF-8 BOM |
| Numeric data conversion | Used `Decimal` for DynamoDB numeric compatibility |

This troubleshooting process helped reinforce the importance of IAM policies, correct resource names, AWS region configuration, and CloudWatch monitoring.

## Important Notes

- The current implementation processes only the last data row in each CSV file.
- DynamoDB `put_item()` replaces an existing item if both primary key attributes match.
- S3 event notifications can occasionally trigger duplicate Lambda executions.
- The current implementation does not process all CSV records.

## Future Improvements

Potential improvements include:

- Process all CSV records instead of only the last record.
- Add validation for malformed or incomplete CSV rows.
- Implement duplicate-event protection.
- Add structured error handling and reporting.
- Configure Amazon SNS notifications for processing failures.
- Implement automated testing.
- Improve scalability for large CSV files.

## Skills Demonstrated

- AWS Cloud Infrastructure
- Serverless Architecture
- Event-Driven Computing
- Python Programming
- AWS Lambda
- Amazon S3
- Amazon DynamoDB
- IAM Permissions and Security
- Boto3 and AWS SDK
- CloudWatch Monitoring
- Troubleshooting and Debugging

## Conclusion

This project demonstrates how AWS managed services can work together to automate data processing without requiring a continuously running server.

By integrating Amazon S3, AWS Lambda, and Amazon DynamoDB, I implemented a serverless workflow that automatically processes uploaded CSV data and stores the extracted record in a NoSQL database.

The project strengthened my practical understanding of AWS cloud services, serverless computing, and cloud infrastructure automation.

---

**Project Category:** AWS Cloud Infrastructure | Serverless Computing | Data Processing

**Author:** Beyene Bekele
