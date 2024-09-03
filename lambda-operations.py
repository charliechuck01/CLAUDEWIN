import boto3
import json
import logging

logger = logging.getLogger(__name__)

class LambdaOperations:
    def __init__(self, region_name):
        self.lambda_client = boto3.client('lambda', region_name=region_name)
        self.function_name = "ClaudeWinBackgroundProcessor"

    def invoke_background_processor(self, payload):
        try:
            response = self.lambda_client.invoke(
                FunctionName=self.function_name,
                InvocationType='Event',  # Asynchronous invocation
                Payload=json.dumps(payload)
            )
            logger.info(f"Background process initiated. RequestId: {response['ResponseMetadata']['RequestId']}")
            return f"Background process initiated. RequestId: {response['ResponseMetadata']['RequestId']}"
        except Exception as e:
            logger.error(f"Error invoking Lambda function: {str(e)}")
            return f"Error invoking Lambda function: {str(e)}"

    def get_task_result(self, task_id):
        try:
            response = self.lambda_client.invoke(
                FunctionName=self.function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps({"operation": "get_task_result", "task_id": task_id})
            )
            result = json.loads(response['Payload'].read().decode())
            logger.info(f"Retrieved result for task: {task_id}")
            return result
        except Exception as e:
            logger.error(f"Error retrieving task result: {str(e)}")
            return f"Error retrieving task result: {str(e)}"

    def schedule_task(self, task_name, task_data, schedule_expression):
        # This method would be used to set up CloudWatch Events to trigger the Lambda function
        # Implementation depends on specific scheduling needs
        pass
