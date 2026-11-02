import csv
import io
import json
import boto3

s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("Students")


def lambda_handler(event, context):
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    file_name = event["Records"][0]["s3"]["object"]["key"]

    try:
        # Read CSV file from S3
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=file_name
        )

        content = response["Body"].read().decode("utf-8")

        # Read only the last CSV data row
        csv_reader = csv.DictReader(io.StringIO(content))
        last_row = None

        for row in csv_reader:
            last_row = row

        if last_row is None:
            return {
                "statusCode": 400,
                "body": json.dumps("CSV file contains no data rows.")
            }

        # Prepare DynamoDB item
        item = {
            "username": last_row["username"],
            "full_name": last_row["full_name"],
            "gender": last_row["gender"],
            "institution_name": last_row["institution_name"],
            "exam_topic_name": last_row["exam_topic_name"],
            "year": last_row["year"],
            "total_score": float(last_row["total_score"] or 0),
            "is_disqualified": int(last_row["is_disqualified"]),
            "is_absent": int(last_row["is_absent"]),
            "supervisor_report": int(last_row["supervisor_report"]),
            "status": last_row["status"]
        }

        # Save only the last row
        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps(
                f"Successfully processed the last record: {item['username']}"
            )
        }

    except Exception as e:
        print(f"Error processing CSV: {str(e)}")
        raise
