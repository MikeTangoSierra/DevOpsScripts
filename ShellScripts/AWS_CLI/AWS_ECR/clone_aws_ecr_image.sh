#!/bin/bash
# This script copies a Container Images from a source AWS ECR repository in one AWS account, to a destination AWS ECR repository in another AWS account.
# Whilst we can use AWS ECR replication rules to copy these Container Images from our source AWS account to our destination AWS account, it doesn't do this for Container Images that already in our source AWS account's AWS ECR repository/AWS ECR repositories.

# Pre-requisites include;
  # Having the AWS CLI installed to the machine you are running this script from.
  # Having your AWS CLI configured and two profiles setup, one for your source AWS account and one for your destination AWS account.
  # Having the AWS ECR repository created in source AWS account and destination AWS account.
  # Having the Container Image/Container Images in your source AWS account's AWS ECR repository.

# Future Improvements for this script include;
  # Doing the same process as this, but for Helm Charts as well as Container Images.

set -euo pipefail

# Config.
SOURCE_PROFILE="source-profile"
DEST_PROFILE="destination-profile"

SOURCE_REGION="us-west-2"
DEST_REGION="us-east-1"

SOURCE_ACCOUNT_ID="111111111111"
DEST_ACCOUNT_ID="222222222222"

REPOSITORIES=("my-repo-1" "my-repo-2")

# Login to both AWS Account's AWS ECRs.
echo "Logging into source ECR..."
aws ecr get-login-password --region "$SOURCE_REGION" --profile "$SOURCE_PROFILE" \
  | docker login --username AWS --password-stdin "${SOURCE_ACCOUNT_ID}.dkr.ecr.${SOURCE_REGION}.amazonaws.com"

echo "Logging into destination ECR..."
aws ecr get-login-password --region "$DEST_REGION" --profile "$DEST_PROFILE" \
  | docker login --username AWS --password-stdin "${DEST_ACCOUNT_ID}.dkr.ecr.${DEST_REGION}.amazonaws.com"

# Loop through repositories,
for repo in "${REPOSITORIES[@]}"; do
  echo -e "\nProcessing repository: $repo"

  # List image tags in source repo.
  TAGS=$(aws ecr list-images \
    --repository-name "$repo" \
    --region "$SOURCE_REGION" \
    --profile "$SOURCE_PROFILE" \
    --query 'imageIds[*].imageTag' \
    --output text)

  for tag in $TAGS; do
    echo "Copying tag: $tag"

    SRC_IMAGE="${SOURCE_ACCOUNT_ID}.dkr.ecr.${SOURCE_REGION}.amazonaws.com/${repo}:${tag}"
    DEST_IMAGE="${DEST_ACCOUNT_ID}.dkr.ecr.${DEST_REGION}.amazonaws.com/${repo}:${tag}"

    echo "Pulling $SRC_IMAGE"
    docker pull "$SRC_IMAGE"

    echo "Tagging as $DEST_IMAGE"
    docker tag "$SRC_IMAGE" "$DEST_IMAGE"

    echo "Pushing $DEST_IMAGE"
    docker push "$DEST_IMAGE"
  done
done

echo -e "\nDone copying images!"