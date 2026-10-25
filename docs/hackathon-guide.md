# AKS vs ACA decision guide

This app is intentionally designed to run as the same containerized image locally and in Azure. The platform story is the comparison between AKS and Azure Container Apps for the same product.

## Shared architecture

- One Streamlit app
- One deterministic analytics engine for the seven questions
- One optional Azure AI model explanation layer
- Same container image across local, AKS, and ACA
- Platform differences exist only in deployment configuration

## AKS

Use AKS when the story is about operational control, cluster-level configuration, scaling policy, and rollout/rollback patterns.

## ACA

Use ACA when the story is about simpler app-centric operations, lower operational burden, and faster deployment of a stateless app.

## Recommendation

For the session, keep the same app and same analytics logic on both platforms. The comparison becomes clearer when the business logic is identical and the deployment choices are the only variation.

## Guardrails

- Keep the dataset local or in private storage.
- Do not commit secrets.
- Keep the public repo shareable and free of generated artifacts.
