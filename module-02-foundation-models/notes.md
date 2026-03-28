# Module 02 — Foundation Models Deep Dive

## Overview

Bedrock provides access to multiple foundation models from different providers. Each has different strengths, speeds, and costs. Choosing the right model is critical for your application.

## Model Families

### Claude (Anthropic)

**Latest:** Claude 3.5 Haiku, Sonnet, and Claude 3 Opus

| Model | Speed | Cost | Best For | Context |
|-------|-------|------|----------|---------|
| **Claude 3.5 Haiku** | Fastest ⚡ | Cheapest | Simple tasks, real-time | 200k tokens |
| **Claude 3.5 Sonnet** | Medium ⚡⚡ | Medium | General purpose, balance | 200k tokens |
| **Claude 3 Opus** | Slower ⚡⚡⚡ | Most expensive | Complex reasoning, analysis | 200k tokens |

**Strengths:**
- Best reasoning and coding
- Long context window (200k tokens = ~150 pages)
- Excellent at following instructions
- Low hallucination rate

**Pricing (approximate, per 1M tokens):**
- Haiku: $0.80 input / $4 output
- Sonnet: $3 input / $15 output
- Opus: $15 input / $75 output

### Titan (AWS)

**Latest:** Titan Text Express, Titan Text Premier

| Model | Speed | Cost | Best For | Context |
|-------|-------|------|----------|---------|
| **Titan Text Express** | Medium ⚡⚡ | Low | Summarization, search | 8k tokens |
| **Titan Text Premier** | Slow ⚡⚡⚡ | Medium | Complex queries, semantic search | 8k tokens |

**Strengths:**
- AWS-native, good cost/performance
- Good for multilingual tasks
- Integrated monitoring in CloudWatch

### Llama 3 (Meta)

**Latest:** Llama 3.1 70B, 8B

| Model | Speed | Cost | Best For | Context |
|-------|-------|------|----------|---------|
| **Llama 3.1 70B** | Medium ⚡⚡ | Low-Medium | Code, reasoning, general | 128k tokens |
| **Llama 3.1 8B** | Fastest ⚡ | Cheapest | Lightweight tasks | 128k tokens |

**Strengths:**
- Open-source, fully transparent
- Good for coding tasks
- Lower cost than Claude
- Acceptable reasoning

### Mistral (Mistral AI)

**Latest:** Mistral Large, Mistral 7B

| Model | Speed | Cost | Best For | Context |
|-------|-------|------|----------|---------|
| **Mistral Large** | Medium ⚡⚡ | Medium | General purpose, reasoning | 128k tokens |
| **Mistral 7B** | Fast ⚡⚡ | Very cheap | Lightweight tasks, edge | 32k tokens |

**Strengths:**
- Efficient, low latency
- Good for European customers (data residency)
- Excellent cost/performance

### Cohere (Cohere)

**Latest:** Command, Command R+

| Model | Speed | Cost | Best For | Context |
|-------|-------|------|----------|---------|
| **Command R+** | Medium ⚡⚡ | Medium | Long document analysis | 128k tokens |

**Strengths:**
- Strong on long documents
- Fine-tuning friendly
- Good multilingual support

### Image Models

**Stable Diffusion:**
- Image generation from text prompts
- Fast, low-cost image creation
- Fine-tuning support

**Titan Image:**
- AWS-native image generation
- Competitive with Stable Diffusion
- Integrated with AWS services

## Capability Matrix

| Capability | Claude | Titan | Llama | Mistral | Cohere |
|------------|--------|-------|-------|---------|--------|
| Reasoning | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Code generation | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Speed | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Cost | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Long context | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Multilingual | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Hallucination | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

## How to Choose

### Use Claude if:
- You need best reasoning and coding
- You have complex instructions to follow
- Accuracy is critical (legal, financial, medical)
- You can afford higher costs

### Use Llama or Mistral if:
- Cost is a priority
- You need a fast, open-source alternative
- You're fine-tuning on your own data
- Latency is critical

### Use Titan if:
- You want AWS-native integration
- You need cost-effective general purpose
- You prefer managed by AWS

### Use Cohere if:
- You're analyzing long documents (128k context)
- You're fine-tuning frequently
- You need multilingual support

## API Format Differences

### Claude (Messages API)

```python
request = {
    'anthropic_version': 'bedrock-2023-06-01',
    'max_tokens': 1024,
    'messages': [
        {'role': 'user', 'content': 'Hello'}
    ]
}
```

### Titan

```python
request = {
    'inputText': 'Hello',
    'textGenerationConfig': {
        'maxTokenCount': 1024,
        'temperature': 0.7
    }
}
```

### Llama

```python
request = {
    'prompt': 'Hello',
    'max_gen_len': 1024,
    'temperature': 0.7
}
```

### Mistral

```python
request = {
    'prompt': 'Hello',
    'max_tokens': 1024,
    'temperature': 0.7
}
```

Each model has a slightly different JSON format — see project for normalization helper.

## Context Windows

| Model | Context | Equivalent |
|-------|---------|-----------|
| Claude 3.x | 200,000 tokens | ~150,000 words / 500 pages |
| Llama 3.1 | 128,000 tokens | ~100,000 words / 300 pages |
| Mistral Large | 128,000 tokens | ~100,000 words / 300 pages |
| Titan | 8,000 tokens | ~6,000 words / 20 pages |
| Cohere | 128,000 tokens | ~100,000 words / 300 pages |

Longer context = better for document analysis, RAG, few-shot learning.

## Pricing Comparison

For a typical request: 500 input tokens + 500 output tokens

| Model | Cost |
|-------|------|
| **Llama 3.1 8B** | $0.00025 |
| **Mistral 7B** | $0.00015 |
| **Titan Express** | $0.00025 |
| **Claude Haiku** | $0.00135 |
| **Llama 3.1 70B** | $0.00265 |
| **Mistral Large** | $0.00270 |
| **Claude Sonnet** | $0.01800 |
| **Cohere Command R+** | $0.02000 |
| **Claude Opus** | $0.04500 |

**Rule of thumb:** Cheapest isn't always best. Claude costs 10-100x more but often gets the answer right first try (saving retries).

## Model IDs

Get latest from: https://docs.aws.amazon.com/bedrock/latest/userguide/models-support.html

### Claude
- `anthropic.claude-3-5-haiku-20241022-v1:0`
- `anthropic.claude-3-5-sonnet-20241022-v1:0`
- `anthropic.claude-opus-4-1-20250805-v1:0`

### Titan
- `amazon.titan-text-express-v1`
- `amazon.titan-text-premier-v1:0`

### Llama
- `meta.llama3-1-405b-instruct-v1:0` (405B)
- `meta.llama3-1-70b-instruct-v1:0`
- `meta.llama3-70b-instruct-v1:0`

### Mistral
- `mistral.mistral-large-2402-v1:0`
- `mistral.mixtral-8x7b-instruct-v0:1`
- `mistral.mistral-7b-instruct-v0:2`

### Cohere
- `cohere.command-r-plus-v1:0`
- `cohere.command-r-v1:0`

## Streaming vs Non-Streaming

### Non-Streaming (Default)
- Model generates entire response
- Wait for full response before displaying
- Better for short responses

### Streaming
- Response comes in chunks
- Display text as it arrives
- Better UX for long responses
- Slight latency increase

See Module 04 for streaming examples.

## Advanced: Model-Specific Parameters

### Claude: Temperature
```python
'temperature': 0.0  # Deterministic (always same answer)
'temperature': 1.0  # Creative (varied answers)
```

### Claude: Top-P
```python
'top_p': 0.9  # Nucleus sampling (restrict to top 90% of probability)
```

### All Models: Max Tokens
```python
'max_tokens': 100  # Hard limit on output length
```

## Common Mistakes

### 1. Assuming Same API Format
Each model has different request/response format. Need wrapper functions.

### 2. Over-Estimating Context
200k tokens ≠ 200k characters. Tokens are subwords, ratio is ~1:4.

### 3. Ignoring Costs
Claude can cost 100x more per token. Budget accordingly.

### 4. Not Testing Trade-offs
Spend 5 minutes testing Haiku vs Sonnet on your use case. Might save 90% on costs.

## Next Steps

1. Complete the Module 02 project
2. Build a model comparison CLI
3. Test different models on your use case
4. Choose your default model for future modules

## Resources

- **Model Docs:** https://docs.aws.amazon.com/bedrock/latest/userguide/models-support.html
- **Pricing:** https://aws.amazon.com/bedrock/pricing/
- **Anthropic Docs:** https://docs.anthropic.com/
- **Llama Docs:** https://www.llama.com/docs/
- **Mistral Docs:** https://docs.mistral.ai/
