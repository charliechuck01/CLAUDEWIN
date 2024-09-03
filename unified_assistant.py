import openai
import boto3
from botocore.exceptions import ClientError
from elasticsearch import Elasticsearch
from lambda_operations import LambdaOperations
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(filename='claudewin.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UnifiedAssistant:
    def __init__(self):
        load_dotenv()
        
        try:
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.region_name = os.getenv('AWS_REGION', 'us-east-1')
            self.s3 = boto3.client('s3', region_name=self.region_name)
            self.comprehend = boto3.client('comprehend', region_name=self.region_name)
            self.bucket_name = os.getenv('S3_BUCKET_NAME')

            elastic_cloud_endpoint = os.getenv('ELASTIC_CLOUD_ENDPOINT')
            elastic_cloud_username = os.getenv('ELASTIC_CLOUD_USERNAME')
            elastic_cloud_password = os.getenv('ELASTIC_CLOUD_PASSWORD')

            self.es = Elasticsearch(
                f"https://{elastic_cloud_endpoint}:443",
                basic_auth=(elastic_cloud_username, elastic_cloud_password),
                verify_certs=True
            )

            self.lambda_ops = LambdaOperations(self.region_name)
            self.chat_history = []

            logger.info("UnifiedAssistant initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing UnifiedAssistant: {str(e)}")
            raise

    def generate_response(self, user_input):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are CLAUDEWIN, a helpful AI assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            ai_response = response.choices[0].message['content']
            self.chat_history.append({"role": "user", "content": user_input})
            self.chat_history.append({"role": "assistant", "content": ai_response})
            logger.info(f"Generated response for input: {user_input[:50]}...")
            return ai_response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"An error occurred: {str(e)}"

    def upload_file_to_s3(self, file_path, file_name):
        try:
            self.s3.upload_file(file_path, self.bucket_name, file_name)
            logger.info(f"File {file_name} uploaded successfully to S3.")
            return f"File {file_name} uploaded successfully to S3."
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {str(e)}")
            return f"Error uploading file to S3: {str(e)}"

    def analyze_text_with_comprehend(self, text):
        try:
            sentiment = self.comprehend.detect_sentiment(Text=text, LanguageCode='en')
            entities = self.comprehend.detect_entities(Text=text, LanguageCode='en')
            logger.info(f"Analyzed text with Comprehend: sentiment={sentiment['Sentiment']}")
            return {
                "sentiment": sentiment['Sentiment'],
                "entities": [e['Text'] for e in entities['Entities']]
            }
        except ClientError as e:
            logger.error(f"Error analyzing text with Comprehend: {str(e)}")
            return f"Error analyzing text with Comprehend: {str(e)}"

    def index_document(self, doc_id, content):
        try:
            self.es.index(index="claudewin_docs", id=doc_id, body=content)
            logger.info(f"Document {doc_id} indexed successfully.")
            return f"Document {doc_id} indexed successfully."
        except Exception as e:
            logger.error(f"Error indexing document: {str(e)}")
            return f"Error indexing document: {str(e)}"

    def search_documents(self, query):
        try:
            result = self.es.search(index="claudewin_docs", body={"query": {"match": {"content": query}}})
            logger.info(f"Searched documents with query: {query}")
            return [hit['_source'] for hit in result['hits']['hits']]
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return f"Error searching documents: {str(e)}"

    def process_large_file(self, file_name):
        payload = {
            "operation": "process_large_file",
            "file_name": file_name,
            "bucket_name": self.bucket_name
        }
        logger.info(f"Invoking background processor for file: {file_name}")
        return self.lambda_ops.invoke_background_processor(payload)

    def generate_report(self, report_type, parameters):
        payload = {
            "operation": "generate_report",
            "report_type": report_type,
            "parameters": parameters
        }
        logger.info(f"Generating report: {report_type}")
        return self.lambda_ops.invoke_background_processor(payload)

    def update_data(self, data_source):
        payload = {
            "operation": "update_data",
            "data_source": data_source
        }
        logger.info(f"Updating data from: {data_source}")
        return self.lambda_ops.invoke_background_processor(payload)

    def get_background_task_result(self, task_id):
        logger.info(f"Retrieving result for task: {task_id}")
        return self.lambda_ops.get_task_result(task_id)

    def test_elastic_connection(self):
        try:
            info = self.es.info()
            logger.info(f"Successfully connected to Elasticsearch. Cluster name: {info['cluster_name']}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Elasticsearch: {str(e)}")
            return False
