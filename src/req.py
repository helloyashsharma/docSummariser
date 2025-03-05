import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# initialise environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
ASSISTANT_ID = os.getenv('LEGAL_ASSISTANT_ID')

# function to summarise the legal document
def summarize_pdf(pdf_path, max_retries=10, retry_interval=10):
    try:
        # upload the doc to vectore store
        with open(pdf_path, 'rb') as f:
            uploaded_file = client.files.create(
                file=f,
                purpose='assistants'
            )

        # create thread with reference to the uploaded doc
        thread = client.beta.threads.create(messages=[{
            'role': 'user',
            'content': 'Please go through the following document and extract 10 pivotal points in the case. \
                Provide arguments for and against these points.',
            'attachments': [{
                'file_id': uploaded_file.id,
                'tools': [{'type': 'file_search'}]
            }]
        }])

        # create run
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # polling for checking status
        for _ in range(max_retries):
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

            if run.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id,
                    order='asc'
                )
                return messages.data[-1].content[0].text.value
                
            elif run.status == 'failed':
                error = run.last_error.message if run.last_error else 'Unknown error'
                return f"Failed: {error}"
                
            time.sleep(retry_interval)

        return "Processing timed out"

    except Exception as e:
        return f"Error: {str(e)}"
    

pdf_path = ''
summary = summarize_pdf(pdf_path)