# Module 10 Project — Fine-Tune Custom Model

## Goal

1. Prepare training data (support conversations)
2. Upload to S3
3. Launch fine-tuning job
4. Deploy fine-tuned model
5. Compare with base model

## Implementation Steps

### Step 1: Create JSONL Training Data

```python
training_data = [
    {"prompt": "What is your refund policy?", "completion": "Refunds accepted within 30 days."},
    {"prompt": "How long for shipping?", "completion": "5-7 business days standard."},
    # ... 1000+ more examples
]

with open('training.jsonl', 'w') as f:
    for item in training_data:
        f.write(json.dumps(item) + '\n')
```

### Step 2: Upload to S3

```bash
aws s3 cp training.jsonl s3://my-bucket/training.jsonl
```

### Step 3: Launch Fine-Tuning Job

```python
bedrock = boto3.client('bedrock')

response = bedrock.create_model_customization_job(
    jobName='support-bot-ft',
    customModelName='support-claude-v1',
    roleArn='arn:aws:iam::...:role/BedrockTuningRole',
    trainingDataConfig={'s3Uri': 's3://my-bucket/training.jsonl'},
    outputDataConfig={'s3Uri': 's3://my-bucket/output/'},
    foundationModelIdentifier='anthropic.claude-3-5-haiku-20241022-v1:0'
)

job_id = response['jobIdentifier']
```

### Step 4: Monitor Progress

```python
while True:
    response = bedrock.get_model_customization_job(jobIdentifier=job_id)
    print(f"Status: {response['status']}")
    if response['status'] != 'InProgress':
        break
    time.sleep(60)
```

### Step 5: Test Fine-Tuned Model

```python
response = bedrock_runtime.converse(
    modelId=f'arn:aws:bedrock:us-east-1:...:custom-model/support-claude-v1:0',
    messages=[{'role': 'user', 'content': 'What is your refund policy?'}]
)

print(f"Fine-tuned response: {response}")
```

## Key Learnings

- Data preparation importance
- Training job monitoring
- Before/after model comparison
- Cost of fine-tuning vs inference
