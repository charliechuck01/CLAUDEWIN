import tkinter as tk
from gui_components import CLAUDEWIN_GUI
from unified_assistant import UnifiedAssistant
import os
from dotenv import load_dotenv

def main():
    load_dotenv()  # Load environment variables from .env file

    # Ensure all required environment variables are set
    required_vars = ['OPENAI_API_KEY', 'AWS_REGION', 'S3_BUCKET_NAME', 
                     'ELASTIC_CLOUD_ENDPOINT', 'ELASTIC_CLOUD_USERNAME', 
                     'ELASTIC_CLOUD_PASSWORD', 'AWS_ACCOUNT_ID']
    
    for var in required_vars:
        if os.environ.get(var) is None:
            raise EnvironmentError(f"Missing required environment variable: {var}")

    root = tk.Tk()
    assistant = UnifiedAssistant()
    app = CLAUDEWIN_GUI(root, assistant)
    root.mainloop()

if __name__ == "__main__":
    main()
