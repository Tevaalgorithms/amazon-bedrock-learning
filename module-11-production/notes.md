# Module 11 — Production & Observability

## Production Readiness Checklist

- ✓ Monitoring (CloudWatch)
- ✓ Error handling & retries
- ✓ Cost tracking
- ✓ Logging & debugging
- ✓ Failover strategy
- ✓ Rate limiting
- ✓ Security (encryption, access control)

## CloudWatch Monitoring

### Enable Bedrock Logging

```python
bedrock = boto3.client('bedrock')

bedrock.put_model_invocation_logging_configuration(
    loggingConfig={
        'cloudWatchConfig': {
            'logGroupName': '/aws/bedrock/invocations',
            'roleArn': 'arn:aws:iam::...:role/BedrockLoggingRole'
        },
        's3Config': {
            'bucketName': 'my-logging-bucket',
            'keyPrefix': 'bedrock-logs/'
        }
    }
)
```

### CloudWatch Metrics

View in CloudWatch → Metrics → Bedrock:

- `InvokeModel.Latency` — response time (ms)
- `InvokeModel.UserErrors` — bad requests
- `InvokeModel.SystemErrors` — server errors
- `InputTokens` — tokens sent to model
- `OutputTokens` — tokens from model

### Create Alarms

```python
cloudwatch = boto3.client('cloudwatch')

cloudwatch.put_metric_alarm(
    AlarmName='bedrock-error-spike',
    MetricName='InvokeModel.SystemErrors',
    Namespace='AWS/Bedrock',
    Statistic='Sum',
    Period=300,  # 5 minutes
    EvaluationPeriods=1,
    Threshold=10,  # Alert if >10 errors in 5 mins
    AlarmActions=['arn:aws:sns:us-east-1:...:alert-topic']
)
```

## Cost Optimization

### Track Costs

```python
logs = boto3.client('logs')

# Query logs for token usage
query = '''
fields @message, @timestamp
| stats sum(inputTokens) as total_input, sum(outputTokens) as total_output by modelId
| sort total_input desc
'''

response = logs.start_query(
    logGroupName='/aws/bedrock/invocations',
    startTime=int((datetime.now() - timedelta(days=7)).timestamp()),
    endTime=int(datetime.now().timestamp()),
    queryString=query
)
```

### Cost Control Strategies

1. **Use cheaper models** — Haiku costs 10x less than Opus
2. **Limit max_tokens** — set reasonable upper bound
3. **Cache results** — don't re-invoke for same query
4. **Batch requests** — process multiple queries together
5. **Monitor per-user costs** — identify power users

### Provisioned Throughput

For predictable, high-volume:

```python
bedrock.create_provisioned_model_throughput(
    provisionedModelName='production-capacity',
    foundationModelIdentifier='anthropic.claude-3-5-sonnet-20241022-v1:0',
    modelUnits=10  # ~1M tokens/minute
)
```

Cost: ~$100/month per unit, but ~30% cheaper per token at volume.

## Error Handling & Retries

```python
import time
from botocore.exceptions import ClientError

def invoke_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.converse(
                modelId='anthropic.claude-3-5-sonnet-20241022-v1:0',
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response

        except ClientError as e:
            if e.response['Error']['Code'] == 'ThrottlingException':
                # Exponential backoff
                wait_time = 2 ** attempt
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            elif e.response['Error']['Code'] == 'ValidationException':
                print(f"Bad request: {e}")
                return None
            else:
                print(f"Unexpected error: {e}")
                raise

        except Exception as e:
            print(f"Connection error: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                raise

    raise Exception("Max retries exceeded")
```

## Logging & Debugging

### Request/Response Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)

response = client.converse(
    modelId='...',
    messages=[...]
)

# boto3 logs request/response details at DEBUG level
```

### Structured Logging

```python
import json
from datetime import datetime

def log_invocation(model_id, prompt, response, error=None):
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'model_id': model_id,
        'input_tokens': response.get('usage', {}).get('inputTokens'),
        'output_tokens': response.get('usage', {}).get('outputTokens'),
        'latency_ms': response.get('latency'),
        'error': str(error) if error else None
    }
    print(json.dumps(log_entry))
```

## Failover Strategy

### Multi-Model Failover

```python
MODELS = [
    'anthropic.claude-3-5-sonnet-20241022-v1:0',  # Primary
    'anthropic.claude-3-5-haiku-20241022-v1:0',   # Fallback
    'meta.llama3-1-70b-instruct-v1:0'              # Last resort
]

def invoke_with_fallback(prompt):
    for model_id in MODELS:
        try:
            response = client.converse(
                modelId=model_id,
                messages=[{'role': 'user', 'content': prompt}],
                inferenceConfig={'maxTokens': 100}
            )
            return response, model_id
        except Exception as e:
            print(f"Model {model_id} failed: {e}")
            continue

    raise Exception("All models unavailable")
```

### Multi-Region Failover

```python
REGIONS = ['us-east-1', 'us-west-2', 'eu-west-1']

def invoke_with_region_failover(prompt):
    for region in REGIONS:
        try:
            client = boto3.client('bedrock-runtime', region_name=region)
            response = client.converse(...)
            return response, region
        except Exception as e:
            print(f"Region {region} failed: {e}")
            continue

    raise Exception("All regions unavailable")
```

## Security

### Encryption

Bedrock automatically encrypts data at rest and in transit.

### Access Control

```python
# IAM policy for Bedrock access
{
    "Effect": "Allow",
    "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
    ],
    "Resource": "arn:aws:bedrock:us-east-1::model/anthropic.claude-3-5-sonnet-*"
}
```

### Data Privacy

- Data does NOT go to Anthropic
- Data stored in AWS account only
- Encrypted at rest in your regions
- Comply with HIPAA, PCI-DSS, SOC2

## Rate Limiting

Bedrock has quotas:

```python
# Check quota
bedrock = boto3.client('bedrock')

response = bedrock.get_foundation_model(
    modelIdentifier='anthropic.claude-3-5-sonnet-20241022-v1:0'
)

quota = response['modelDetails']['modelDimensions']['throughput']
print(f"Quota: {quota} tokens per minute")
```

Implement client-side throttling:

```python
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, tpm=100000):
        self.tpm = tpm
        self.tokens_used = 0
        self.window_start = datetime.now()

    def check_rate(self, tokens_needed):
        now = datetime.now()
        if (now - self.window_start).total_seconds() > 60:
            self.tokens_used = 0
            self.window_start = now

        if self.tokens_used + tokens_needed > self.tpm:
            wait = 60 - (now - self.window_start).total_seconds()
            print(f"Rate limited, wait {wait}s")
            return False
        return True
```

## Next Steps

Module 11 project: Production stack with CDK, CloudWatch dashboard.

## Resources

- **CloudWatch:** https://docs.aws.amazon.com/cloudwatch/
- **Bedrock Logging:** https://docs.aws.amazon.com/bedrock/latest/userguide/logging-monitoring.html
- **AWS CDK:** https://docs.aws.amazon.com/cdk/
