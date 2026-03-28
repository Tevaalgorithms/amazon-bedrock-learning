"""
Module 01 Project: Hello Bedrock
Call your first Bedrock model (Claude) and print the response.
"""

import boto3
import json


def main():
    # TODO: Create Bedrock client with region 'us-east-1'
    # Use: boto3.client('bedrock-runtime', region_name='us-east-1')
    client = None

    # TODO: Choose a model ID
    # Options:
    #   - anthropic.claude-3-5-haiku-20241022-v1:0 (fastest, cheapest)
    #   - anthropic.claude-3-5-sonnet-20241022-v1:0 (balanced)
    #   - anthropic.claude-opus-4-1-20250805-v1:0 (most capable)
    #   - amazon.titan-text-express-v1 (AWS alternative)
    model_id = None

    # TODO: Create the request payload
    # Required fields:
    #   - anthropic_version: "bedrock-2023-06-01"
    #   - max_tokens: 100
    #   - messages: [{"role": "user", "content": "Your message here"}]
    request = {}

    # TODO: Invoke the model
    # Use: client.invoke_model(modelId=model_id, body=json.dumps(request), contentType='application/json')
    response = None

    # TODO: Parse the response
    # 1. Read body: response['body'].read()
    # 2. Decode JSON: json.loads(...)
    # 3. Extract text: output['content'][0]['text']
    output_text = None

    # TODO: Print the response
    print(f"Model: {model_id}")
    print(f"Response: {output_text}")


if __name__ == '__main__':
    main()
