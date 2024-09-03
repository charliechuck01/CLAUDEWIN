# CLAUDEWIN

CLAUDEWIN is a versatile AI assistant that combines natural language processing, file operations, and AWS service integration to provide a powerful and flexible tool for various tasks.

## Features

- Natural language processing using OpenAI's GPT-4
- File operations with AWS S3 integration
- Text analysis using AWS Comprehend
- Document indexing and searching with Elasticsearch
- Background task processing with AWS Lambda
- User-friendly GUI built with tkinter

## Prerequisites

- Python 3.7+
- AWS account with appropriate permissions
- OpenAI API key
- Elasticsearch cloud account (optional)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/CLAUDEWIN.git
   cd CLAUDEWIN
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   AWS_REGION=your_aws_region
   S3_BUCKET_NAME=your_s3_bucket_name
   ELASTIC_CLOUD_ENDPOINT=your_elasticsearch_endpoint
   ELASTIC_CLOUD_USERNAME=your_elasticsearch_username
   ELASTIC_CLOUD_PASSWORD=your_elasticsearch_password
   AWS_ACCOUNT_ID=your_aws_account_id
   ```

## Usage

Run the main application:

```
python main.py
```

This will start the CLAUDEWIN GUI, allowing you to interact with the assistant, process files, generate reports, and perform other tasks.

## Project Structure

- `main.py`: Entry point of the application
- `unified_assistant.py`: Core CLAUDEWIN functionality
- `gui_components.py`: GUI implementation
- `lambda_operations.py`: AWS Lambda integration
- `file_operations.py`: File handling operations
- `nlp_processor.py`: Natural language processing functions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT-4 API
- Amazon Web Services for cloud infrastructure and services
- Elastic for Elasticsearch functionality
