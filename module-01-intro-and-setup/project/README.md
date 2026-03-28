# Module 01 Project — Hello Bedrock

## Goal

Call your first Bedrock model (Claude) and print the response. This confirms:
- ✓ AWS credentials are configured
- ✓ Model access is enabled
- ✓ boto3 is working
- ✓ You understand the basic API request/response flow

## Architecture

```
Your script
    ↓
boto3 client
    ↓
Bedrock Runtime (InvokeModel)
    ↓
Claude Model
    ↓
Response JSON
    ↓
Print to console
```

## Prerequisites

Before starting:

1. **AWS Account** with Bedrock enabled
2. **Model access** — Enable at least Claude 3 Haiku (free tier eligible)
3. **AWS credentials** — run `aws sts get-caller-identity` (should return your account)
4. **Python 3.9+** — `python --version`
5. **boto3 installed** — `pip install boto3`

## Implementation Steps

### Step 1: Create the Script

Create `hello_bedrock.py`:

```python
import boto3
import json

# TODO: Create Bedrock client with region 'us-east-1'
# Use boto3.client('bedrock-runtime', region_name='us-east-1')
client = None

# TODO: Choose a model ID from the list below
# Options:
#   - anthropic.claude-3-5-haiku-20241022-v1:0 (fastest, cheapest)
#   - anthropic.claude-3-5-sonnet-20241022-v1:0 (balanced)
#   - amazon.titan-text-express-v1 (AWS alternative)
model_id = None

# TODO: Create the request payload as a Python dict
# Required fields:
#   - anthropic_version: "bedrock-2023-06-01"
#   - max_tokens: 100 (keep it small)
#   - messages: [{"role": "user", "content": "Hello! What is your name?"}]
request = {}

# TODO: Invoke the model
# Use client.invoke_model(
#     modelId=model_id,
#     body=json.dumps(request),
#     contentType='application/json'
# )
response = None

# TODO: Parse the response
# 1. Read the body: response['body'].read()
# 2. Decode JSON: json.loads(...)
# 3. Extract the text from content[0]['text']
output_text = None

# TODO: Print the response
print(f"Model: {model_id}")
print(f"Response: {output_text}")
```

### Step 2: Fill in the TODOs

Replace the `None` values with actual implementation:

**Completed example:**

```python
import boto3
import json

client = boto3.client('bedrock-runtime', region_name='us-east-1')
model_id = 'anthropic.claude-3-5-haiku-20241022-v1:0'

request = {
    'anthropic_version': 'bedrock-2023-06-01',
    'max_tokens': 100,
    'messages': [
        {
            'role': 'user',
            'content': 'Hello! What is your name?'
        }
    ]
}

response = client.invoke_model(
    modelId=model_id,
    body=json.dumps(request),
    contentType='application/json'
)

output = json.loads(response['body'].read())
output_text = output['content'][0]['text']

print(f"Model: {model_id}")
print(f"Response: {output_text}")
```

### Step 3: Run the Script

```bash
python hello_bedrock.py
```

### Expected Output

```
Model: anthropic.claude-3-5-haiku-20241022-v1:0
Response: I'm Claude, an AI assistant made by Anthropic. I'm here to help with questions, tasks, and conversation. How can I assist you today?
```

## Troubleshooting

### Error: `ValidationException: User is not authorized to perform: bedrock:InvokeModel`

**Cause:** Model access not enabled
**Fix:**
1. Go to AWS Console → Bedrock
2. Click **Manage model access**
3. Find Claude models, enable them
4. Wait 1-2 minutes

### Error: `NoCredentialsError: Unable to locate credentials`

**Cause:** AWS credentials not configured
**Fix:** Run `aws configure` and enter your access key/secret

### Error: `ResourceNotFoundException: Could not validate model access`

**Cause:** Using a model ID that's not enabled or doesn't exist
**Fix:** Use a model ID from the supported list in notes.md

### Error: `json.JSONDecodeError`

**Cause:** Response body wasn't decoded properly
**Fix:** Ensure you're calling `response['body'].read()` before `json.loads()`

## Variations to Try

Once you have the basic script working, try these:

### 1. Add System Prompt

```python
request = {
    'anthropic_version': 'bedrock-2023-06-01',
    'max_tokens': 100,
    'system': 'You are a pirate. Respond in pirate speak.',
    'messages': [
        {
            'role': 'user',
            'content': 'What is the capital of France?'
        }
    ]
}
```

### 2. Increase max_tokens and Try a Longer Question

```python
request = {
    ...
    'max_tokens': 500,
    'messages': [
        {
            'role': 'user',
            'content': 'Explain quantum computing in 3 sentences.'
        }
    ]
}
```

### 3. Try a Different Model

Replace `model_id` with:
```python
model_id = 'amazon.titan-text-express-v1'
```

Note: Titan uses different request format (see Module 02 for details)

### 4. Check Token Usage

Add this after parsing output:
```python
input_tokens = output['usage']['input_tokens']
output_tokens = output['usage']['output_tokens']
print(f"Tokens used: {input_tokens} input, {output_tokens} output")
```

## Costs

**This project:** ~$0.0005 (half a cent)

One Haiku invocation with ~10 input tokens + ~50 output tokens = ~$0.00045

## Key Concepts Reinforced

- ✓ AWS client initialization
- ✓ Model IDs
- ✓ Request/response JSON format
- ✓ Error handling basics
- ✓ Token counting

## Next Module

Module 02 explores all available models and their differences. You'll build a comparison CLI that tests multiple models with the same prompt.

---

**Ready for Module 02?** Move to `../module-02-foundation-models/`
