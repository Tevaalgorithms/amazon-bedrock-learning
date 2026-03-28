# Module 10 — Fine-Tuning & Custom Models

## What is Fine-Tuning?

**Fine-tuning** adapts a pretrained model to your specific domain/task using your data.

```
Pretrained Claude (Knows everything)
    +
Your Data (20k support conversations)
    =
Fine-Tuned Claude (Expert in your domain)
```

## When to Fine-Tune

✅ **Fine-tune if:**
- You have 1000+ examples of correct behavior
- Domain-specific terminology (legal, medical, technical)
- Consistent output format needed
- Cost savings important (fine-tuned = faster = cheaper)

❌ **Don't fine-tune if:**
- <500 examples (not enough data)
- Task is simple (prompt engineering suffices)
- Data changes frequently (better to use RAG)

## Fine-Tuning Process

### Step 1: Prepare Data

JSONL format with prompt + completion:

```jsonl
{
  "prompt": "What is the refund policy?",
  "completion": "Refunds accepted within 30 days of purchase."
}
{
  "prompt": "How long for shipping?",
  "completion": "Standard shipping takes 5-7 business days."
}
```

**Data quality:**
- 1000+ examples minimum
- Consistent format
- Accurate completions
- No PII

### Step 2: Upload to S3

```bash
aws s3 cp training.jsonl s3://my-bucket/training.jsonl
```

### Step 3: Create Fine-Tuning Job

```python
bedrock = boto3.client('bedrock')

response = bedrock.create_model_customization_job(
    jobName='support-bot-tuning',
    customModelName='support-claude-v1',
    roleArn='arn:aws:iam::...:role/BedrockTuningRole',
    trainingDataConfig={
        's3Uri': 's3://my-bucket/training.jsonl'
    },
    outputDataConfig={
        's3Uri': 's3://my-bucket/output/'
    },
    customizationType='FINE_TUNING',
    foundationModelIdentifier='anthropic.claude-3-5-haiku-20241022-v1:0',
    hyperParameters={
        'batchSize': '4',
        'learningRate': '0.0002',
        'epochs': '5'
    }
)

job_id = response['jobIdentifier']
```

### Step 4: Monitor Progress

```python
response = bedrock.get_model_customization_job(
    jobIdentifier=job_id
)

print(f"Status: {response['status']}")  # InProgress, Completed, Failed
print(f"Progress: {response['outputModelDetails']}")
```

Takes 1-4 hours depending on data size.

### Step 5: Use Fine-Tuned Model

Once complete, invoke like any model:

```python
bedrock_runtime = boto3.client('bedrock-runtime')

response = bedrock_runtime.converse(
    modelId='arn:aws:bedrock:us-east-1:...:custom-model/support-claude-v1:0',
    messages=[
        {'role': 'user', 'content': 'What is your refund policy?'}
    ]
)
```

## Hyperparameters

| Parameter | Effect | Default |
|-----------|--------|---------|
| **batchSize** | Samples per gradient update | 4 |
| **learningRate** | Speed of adaptation | 0.0002 |
| **epochs** | Times through dataset | 5 |
| **warmupSteps** | Gradual learning ramp | 10% of total |

```python
hyperParameters={
    'batchSize': '8',  # Higher = faster but less stable
    'learningRate': '0.0001',  # Lower = slower but more stable
    'epochs': '3',  # More = better fit but risk overfitting
}
```

## Validation Data

Optional: test set to prevent overfitting

```python
trainingDataConfig={
    's3Uri': 's3://bucket/train.jsonl'
},
validationDataConfig={
    's3Uri': 's3://bucket/val.jsonl'
}
```

## Costs

### Training
- Claude 3.5 Haiku: $0.03 per 1M input tokens
- Claude 3.5 Sonnet: $0.15 per 1M input tokens
- Claude 3 Opus: $0.75 per 1M input tokens

Example:
- 10k training examples × 100 tokens = 1M tokens
- Haiku fine-tuning = $0.03

### Deployment (Provisioned Throughput)

```python
response = bedrock.create_provisioned_model_throughput(
    provisionedModelName='support-claude-deployment',
    foundationModelIdentifier='custom-model/support-claude-v1',
    modelUnits=1  # Each = 100k TPM (tokens per minute)
)
```

Cost: ~$100/month per model unit

## Evaluation: Before vs After

```python
prompt = "What is the refund policy?"

# Original model
original_response = bedrock_runtime.converse(
    modelId='anthropic.claude-3-5-haiku-20241022-v1:0',
    messages=[{'role': 'user', 'content': prompt}]
)

# Fine-tuned model
tuned_response = bedrock_runtime.converse(
    modelId='arn:aws:bedrock:...:custom-model/support-claude-v1:0',
    messages=[{'role': 'user', 'content': prompt}]
)

# Compare responses
print(f"Original: {original_response}")
print(f"Fine-tuned: {tuned_response}")
```

## Best Practices

1. **Balance data** — if 90% refund questions, add more policy questions
2. **Iterate** — start with 1k examples, evaluate, add more if needed
3. **Version control** — track which data version trained which model
4. **Test on held-out set** — evaluate on data NOT in training
5. **Monitor in production** — track quality metrics after deployment
6. **Budget for cleanup** — provisioned throughput is expensive, delete when unused

## Common Mistakes

### 1. Insufficient Data
<1000 examples = overfitting risk

### 2. Distribution Mismatch
Training on customer service, deploying on technical support = poor performance

### 3. Data Leakage
Training data in test set = inflated accuracy

### 4. Forgetting Old Tasks
Fine-tuning on specialized task can forget general knowledge

### 5. Not Cleaning Data
Typos, inconsistencies in training data → model learns them

## Continued Pre-training vs Fine-tuning

| Aspect | Fine-tuning | Continued Pre-training |
|--------|-------------|----------------------|
| Data Type | Task-specific | Large corpus (100k+ examples) |
| Time | Hours | Days |
| Cost | Cheap ($0.03-1) | Expensive ($10-100) |
| Quality | Good for tasks | Better general knowledge |

Use fine-tuning in most cases.

## Next Steps

Module 10 project: Train custom model on support data.

## Resources

- **Fine-tuning Docs:** https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model.html
- **Training Format:** https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-prepare.html
