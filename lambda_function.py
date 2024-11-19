import json
import boto3
import uuid
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")
table_name = "ExpensesTable"  # Replace with your DynamoDB table name
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Parse the request body
        body = json.loads(event.get("body", "{}"))
        action = body.get("action", "").lower()

        if action == "add":
            return add_expense(body)
        elif action == "get":
            return get_expenses()
        elif action == "delete":
            return delete_expense(body)
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid action. Use 'add', 'get', or 'delete'."})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


def add_expense(data):
    try:
        expense_id = str(uuid.uuid4())
        item = {
            "expense_id": expense_id,
            "name": data.get("name", "Unnamed Expense"),
            "amount": float(data.get("amount", 0)),
            "category": data.get("category", "Miscellaneous"),
            "date": data.get("date", datetime.utcnow().isoformat())
        }
        table.put_item(Item=item)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Expense added successfully.", "expense_id": expense_id})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


def get_expenses():
    try:
        response = table.scan()
        items = response.get("Items", [])
        return {
            "statusCode": 200,
            "body": json.dumps(items)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


def delete_expense(data):
    try:
        expense_id = data.get("expense_id")
        if not expense_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Please provide an 'expense_id' to delete."})
            }

        table.delete_item(Key={"expense_id": expense_id})
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Expense deleted successfully."})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
