# Module 09 — Model Evaluation

## Why Evaluate Models?

Before deploying, you need to:
- Measure accuracy on your use case
- Compare model versions
- Track quality over time
- Identify improvement areas

## Evaluation Types

### 1. Human Evaluation
Expert humans grade outputs

**Pros:** Most accurate
**Cons:** Slow, expensive, doesn't scale

### 2. Model-Based Evaluation
Use another model to grade

**Pros:** Fast, cheap, scalable
**Cons:** Only as good as grading model

### 3. Automated Metrics
BLEU, ROUGE, RAGAS, etc.

**Pros:** Instant, objective
**Cons:** Don't correlate with human judgment

## Bedrock Evaluation Jobs

AWS provides managed evaluation:

```python
bedrock = boto3.client('bedrock')

job = bedrock.create_evaluation_job(
    jobName='model-comparison-2024',
    jobDescription='Compare Claude vs Llama',
    roleArn='arn:aws:iam::...:role/BedrockEvalRole',
    datasetMetricConfigs=[
        {
            'dataset': {
                's3Uri': 's3://my-bucket/test-dataset.jsonl'
            },
            'metric': 'Accuracy'
        }
    ],
    modelEvaluationConfig=[
        {
            'modelIdentifier': 'anthropic.claude-3-5-sonnet-20241022-v1:0'
        },
        {
            'modelIdentifier': 'meta.llama3-1-70b-instruct-v1:0'
        }
    ]
)

job_id = job['jobIdentifier']
```

## Dataset Format

JSONL file with test cases:

```jsonl
{"input": "What is 2+2?", "expected": "4"}
{"input": "What is capital of France?", "expected": "Paris"}
{"input": "Explain quantum computing", "expected": "... (longer answer)"}
```

## Common Metrics

### BLEU (Bilingual Evaluation Understudy)
Measures n-gram overlap with reference

```
BLEU Score: 0-1 (higher is better)
0.9 = excellent match with reference
0.5 = moderate match
0.1 = poor match
```

**Good for:** Machine translation, paraphrasing

### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)
Measures overlap in summaries

```
ROUGE-1: Unigram overlap
ROUGE-2: Bigram overlap
ROUGE-L: Longest common subsequence
```

**Good for:** Summarization

### RAGAS (Retrieval-Augmented Generation Assessment Score)
Measures RAG quality

```
Faithfulness: Response consistent with context (0-1)
Answer Relevance: Response answers the question (0-1)
Context Precision: Context includes relevant info (0-1)
Context Recall: Context covers all relevant info (0-1)

Overall RAGAS = mean(Faithfulness, Relevance, Precision, Recall)
```

**Good for:** RAG systems

## Manual Scoring Rubric

For complex tasks, create a rubric:

```python
rubric = {
    'relevance': {
        'description': 'Does answer address the question?',
        'scale': [
            '1 - Not relevant at all',
            '2 - Slightly relevant',
            '3 - Mostly relevant',
            '4 - Completely relevant'
        ]
    },
    'accuracy': {
        'description': 'Is the information correct?',
        'scale': [
            '1 - Multiple errors',
            '2 - One significant error',
            '3 - Mostly accurate',
            '4 - Completely accurate'
        ]
    },
    'clarity': {
        'description': 'Is explanation clear?',
        'scale': [
            '1 - Confusing',
            '2 - Somewhat unclear',
            '3 - Clear',
            '4 - Excellent clarity'
        ]
    }
}

def score_response(response, rubric):
    # Have humans rate on each dimension
    # Calculate weighted average
    return (relevance_score + accuracy_score + clarity_score) / 3
```

## Evaluation Workflow

```
1. Create test dataset (50-100 examples)
2. Run evaluation job
3. Get scores for each model
4. Compare results
5. Choose winning model
6. Deploy to production
7. Monitor ongoing performance
```

## Continuous Evaluation

Monitor production models:

```python
# Weekly evaluation on new data
def evaluate_production_model():
    new_data = get_past_week_queries()  # User queries + feedback

    results = bedrock_runtime.converse(
        modelId='current-model',
        messages=format_as_conversation(new_data)
    )

    # Score results
    score = calculate_score(results)

    # Alert if degradation
    if score < previous_score * 0.95:  # >5% drop
        alert("Model quality degraded!")
```

## Cost of Evaluation

- Manual scoring: $50-500 per task (labor intensive)
- Model-based: Negligible (LLM calls cheap)
- Bedrock evaluation job: ~$0.01 per evaluation

Example: Evaluate 1000 responses with Claude = ~$10

## Best Practices

1. **Use real data** — evaluate on actual use case
2. **Sample randomly** — avoid cherry-picking
3. **Define metrics early** — before testing
4. **Include edge cases** — error-prone scenarios
5. **Version everything** — model version, test date, metric version
6. **Save results** — for comparison over time

## Gotchas

### 1. Gaming Metrics
Model can be optimized for metric that doesn't correlate with actual quality.

### 2. Data Leakage
If training data similar to test data, scores inflate.

### 3. Changing Test Sets
Must use same test set for comparisons.

### 4. Statistical Significance
Small improvements might be noise. Need enough samples.

## Next Steps

Module 09 project: Evaluation dashboard comparing 2 models.

## Resources

- **Bedrock Evaluation:** https://docs.aws.amazon.com/bedrock/latest/userguide/eval.html
- **RAGAS Framework:** https://github.com/explodinggradients/ragas
- **Metric Details:** https://en.wikipedia.org/wiki/BLEU
