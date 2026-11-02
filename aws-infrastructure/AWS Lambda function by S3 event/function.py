
import csv
import io
import json
import boto3
from decimal import Decimal, InvalidOperation
from urllib.parse import unquote_plus

# AWS configuration
REGION = "us-east-1"
TABLE_NAME = "custometable"

s3_client = boto3.client("s3", region_name=REGION)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION
)

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    try:
        # 1. Get S3 event information
        record = event["Records"][0]

        bucket_name = record["s3"]["bucket"]["name"]
        file_name = unquote_plus(record["s3"]["object"]["key"])

        print(f"Processing file: s3://{bucket_name}/{file_name}")
        print(f"DynamoDB region: {REGION}")
        print(f"DynamoDB table: {TABLE_NAME}")

        # 2. Verify DynamoDB table exists and is active
        table_info = dynamodb.meta.client.describe_table(
            TableName=TABLE_NAME
        )

        print(
            "DynamoDB table status:",
            table_info["Table"]["TableStatus"]
        )

        # 3. Read CSV file from S3
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=file_name
        )

        content = response["Body"].read().decode("utf-8-sig")

        # 4. Read CSV records
        csv_reader = csv.DictReader(io.StringIO(content))

        required_columns = [
            "username",
            "full_name",
            "gender",
            "institution_name",
            "exam_topic_name",
            "year",
            "total_score",
            "is_disqualified",
            "is_absent",
            "supervisor_report",
            "status"
        ]

        if not csv_reader.fieldnames:
            raise ValueError("CSV file has no header row.")

        missing_columns = [
            column for column in required_columns
            if column not in csv_reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(
                f"Missing CSV columns: {missing_columns}"
            )

        # 5. Get the last data row
        last_row = None

        for row in csv_reader:
            last_row = row

        if last_row is None:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    "CSV file contains no data rows."
                )
            }

        # 6. Prepare DynamoDB item
        item = {
            "username": last_row["username"],
            "full_name": last_row["full_name"],
            "gender": last_row["gender"],
            "institution_name": last_row["institution_name"],
            "exam_topic_name": last_row["exam_topic_name"],
            "year": last_row["year"],
            "total_score": Decimal(
                last_row["total_score"] or "0"
            ),
            "is_disqualified": int(
                last_row["is_disqualified"] or "0"
            ),
            "is_absent": int(
                last_row["is_absent"] or "0"
            ),
            "supervisor_report": int(
                last_row["supervisor_report"] or "0"
            ),
            "status": last_row["status"]
        }

        # 7. Write item to DynamoDB
        table.put_item(Item=item)

        print(
            f"Successfully saved username: {item['username']}"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Successfully processed the last record.",
                "username": item["username"]
            })
        }

    except (ValueError, InvalidOperation, KeyError) as e:
        print(f"Data validation error: {str(e)}")
        raise

    except Exception as e:
        print(f"Error processing CSV: {str(e)}")
        raise
