# Module 01 — Introduction & Setup

## What is Amazon Bedrock?

**Amazon Bedrock** is a managed service that provides **foundation models** (large language models and other AI models) through an API. Instead of deploying and managing your own models, you access pre-trained models from leading AI companies via simple APIs.

### Key Points

- **Fully managed** — no servers to manage, no model deployment
- **Foundation models** — Claude, Titan, Llama, Mistral, Cohere, Stable Diffusion
- **Serverless** — pay per API call (InvokeModel)
- **Secure** — no data leaves your AWS environment, no model training on your data
- **Customizable** — fine-tune models on your own data, manage access via IAM
- **Multi-modal** — text, image understanding, embedding models

## Why Use Bedrock?

| Feature | Benefit |
|---------|---------|
| **No model training** | Focus on your application, not ML ops |
| **Fast deployment** | Minutes to production, not months |
| **Cost-efficient** | Pay only for what you use |
| **Security** | Data stays in your AWS account |
| **Multiple models** | Switch models without rewriting code |
| **Integration** | Works natively with Lambda, S3, CloudWatch, etc. |

## Bedrock vs Alternatives

| Aspect | Bedrock | OpenAI API | Self-hosted |
|--------|---------|-----------|------------|
| Setup time | Minutes | Minutes | Hours/days |
| Data privacy | High ✓ | Medium | Highest |
| Cost control | Per-call | Per-token | Upfront infrastructure |
| Model selection | 10+ | 5 | Unlimited |
| Compliance | AWS native | Third-party | Your responsibility |

## Available Models

### Large Language Models (Text)

- **Claude** (Anthropic) — Best for complex reasoning, long context (200k tokens)
- **Titan Text** (AWS) — Cost-effective, multilingual
- **Llama 3** (Meta) — Open-source alternative, good performance/cost
- **Mistral** — Efficient, multilingual
- **Cohere Command** — Fine-tuning friendly

### Image Models

- **Stable Diffusion** — Image generation from text
- **Titan Image** (AWS) — Image generation, low-latency

### Embedding Models

- **Titan Embeddings** (AWS) — Text embeddings for RAG, clustering
- **Cohere Embeddings** — Multilingual, dense embeddings

## Pricing Model

### Pay-Per-Request

```
Cost = (Input tokens × Input price) + (Output tokens × Output price)
```

**Example Claude pricing:**
- Input: $0.003 per 1k tokens
- Output: $0.015 per 1k tokens

**A 1000-token response costs:**
```
(500 input tokens × $0.003/1k) + (500 output tokens × $0.015/1k)
= $0.0015 + $0.0075 = $0.009 (~1 cent)
```

### Provisioned Throughput (Optional)

- Reserve model capacity for predictable workloads
- Pay upfront monthly cost (~$100-1000/month depending on throughput)
- Good for high-volume production applications
- Modules 10-12 explore this further

## Setting Up Your AWS Environment

### Prerequisites

- AWS Account (free tier eligible)
- AWS CLI installed (`aws --version`)
- Python 3.9+ installed (`python --version`)

### Step 1: Enable Bedrock Models

1. Go to **AWS Console** → Bedrock
2. Click **Manage model access** (bottom-left)
3. Select models you want access to:
   - ✓ Claude 3 Haiku, Sonnet, Opus (Anthropic)
   - ✓ Titan Text Express (AWS)
4. **Request model access**
5. Wait 1-2 minutes for approval (usually immediate)

### Step 2: Create IAM User (Optional but Recommended)

For development, create a dedicated user:

```bash
# Create user
aws iam create-user --user-name bedrock-dev

# Attach policy
aws iam attach-user-policy \
  --user-name bedrock-dev \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

# Create access key
aws iam create-access-key --user-name bedrock-dev
```

Save the `Access Key ID` and `Secret Access Key`.

### Step 3: Configure AWS Credentials

Option A: AWS CLI (simplest)
```bash
aws configure
# Enter Access Key ID
# Enter Secret Access Key
# Enter region (e.g., us-east-1)
# Enter output format (json)
```

Option B: Environment variables
```bash
export AWS_ACCESS_KEY_ID=your_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

Option C: `~/.aws/credentials` file
```ini
[default]
aws_access_key_id = your_key_id
aws_secret_access_key = your_secret_key
```

### Step 4: Install boto3

```bash
pip install boto3
```

That's it! You're ready to call Bedrock.

## Bedrock API Basics

### The InvokeModel API

The core Bedrock API for getting responses from models.

```python
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

response = client.invoke_model(
    modelId='anthropic.claude-3-haiku-20240307-v1:0',
    body='{"prompt": "Hello, world!"}',  # JSON serialized
    contentType='application/json'
)

output = json.loads(response['body'].read())
print(output['content'][0]['text'])
```

### Model IDs

Each model has a unique `modelId`:

- `anthropic.claude-3-5-haiku-20241022-v1:0` — Claude 3.5 Haiku (fastest, cheapest)
- `anthropic.claude-3-5-sonnet-20241022-v1:0` — Claude 3.5 Sonnet (balanced)
- `anthropic.claude-opus-4-1-20250805-v1:0` — Claude 3 Opus (most capable)
- `amazon.titan-text-express-v1` — Titan (AWS)
- `meta.llama3-70b-instruct-v1:0` — Llama 3

Get the latest model IDs: https://docs.aws.amazon.com/bedrock/latest/userguide/models-support.html

### Request Format (Claude)

```json
{
  "anthropic_version": "bedrock-2023-06-01",
  "max_tokens": 1024,
  "system": "You are a helpful assistant.",
  "messages": [
    {
      "role": "user",
      "content": "What is 2+2?"
    }
  ]
}
```

### Response Format (Claude)

```json
{
  "id": "msg_...",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "2+2 equals 4."
    }
  ],
  "model": "claude-3-haiku-...",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 10,
    "output_tokens": 5
  }
}
```

## Common Gotchas

### 1. Model Access Not Enabled

**Error:** `ResourceNotFoundException: Could not validate model access`

**Fix:** Enable model access in Bedrock Console → Manage model access

### 2. Region Mismatch

**Error:** `ValidationException: User is not authorized to perform: bedrock:InvokeModel`

**Fix:** Ensure your `region_name` matches where you enabled model access

### 3. IAM Permissions

**Error:** `AccessDenied`

**Fix:** User/role needs `bedrock:InvokeModel` permission:
```json
{
  "Effect": "Allow",
  "Action": "bedrock:InvokeModel",
  "Resource": "arn:aws:bedrock:us-east-1::model/*"
}
```

### 4. Cost Surprises

**Gotcha:** Long responses = expensive. Set `max_tokens` limit.

### 5. JSON Serialization

**Gotcha:** `body` must be a JSON string (not a dict), and must be bytes when sent:

```python
# Correct
body = json.dumps({"prompt": "Hello"})
response = client.invoke_model(modelId=..., body=body)

# Wrong
response = client.invoke_model(modelId=..., body={"prompt": "Hello"})
```

## Architecture Overview

```
Your Application
    ↓
boto3 (AWS SDK)
    ↓
Bedrock Runtime API (us-east-1, etc.)
    ↓
Foundation Model (Claude, Titan, etc.)
    ↓
Response (streamed or in full)
    ↓
Your Application (processes output)
```

All data stays within AWS.

## Next Steps

- Complete the Module 01 project: `hello_bedrock.py`
- Move to Module 02 for deeper model understanding
- Enable additional models as needed

## Additional Resources

- **AWS Bedrock Docs:** https://docs.aws.amazon.com/bedrock/
- **Anthropic Claude Docs:** https://docs.anthropic.com/
- **boto3 Reference:** https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html
- **Pricing Calculator:** https://calculator.aws/
