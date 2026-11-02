import csv
import io
import json
import boto3

s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# Make sure this matches your actual DynamoDB table name
TABLE_NAME = "Students" 
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    # 1. Get bucket and file name from the S3 trigger event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    
    print(f"Processing CSV file: {file_name} from bucket: {bucket_name}")
    
    try:
        # 2. Read file content from S3
        resp = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        content = resp['Body'].read().decode('utf-8')
        
        # 3. Parse CSV safely using Python's csv module
        csv_reader = csv.DictReader(io.StringIO(content))
        
        success_count = 0
        error_count = 0
        
        # 4. Iterate over each row and convert types before saving to DynamoDB
        for row in csv_reader:
            try:
                item = {
                    "username": row["username"],  # Partition Key (Primary Key)
                    "full_name": row["full_name"],
                    "gender": row["gender"],
                    "institution_name": row["institution_name"],
                    "exam_topic_name": row["exam_topic_name"],
                    "year": row["year"],
                    "total_score": float(row["total_score"]) if row["total_score"] else 0.0,
                    "is_disqualified": int(row["is_disqualified"]),
                    "is_absent": int(row["is_absent"]),
                    "supervisor_report": int(row["supervisor_report"]),
                    "status": row["status"]
                }
                
                # Write item into DynamoDB
                table.put_item(Item=item)
                success_count += 1
                
            except Exception as e:
                error_count += 1
                print(f"Error processing row for {row.get('username')}: {str(e)}")
                
        print(f"Finished processing CSV. Success: {success_count}, Errors: {error_count}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"Successfully processed {success_count} records from {file_name}.")
        }
        
    except Exception as e:
        print(f"Failed to read object from S3: {str(e)}")
        raise e
