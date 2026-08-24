FROM python:3.12-slim

# 基本ツールのインストール
RUN apt-get update && apt-get install -y \
    curl \
    git \
    zip \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# AWS CLI v2 のインストール
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip ./aws

# Terraform CLI のインストール
RUN curl -fsSL https://releases.hashicorp.com/terraform/1.8.0/terraform_1.8.0_linux_amd64.zip -o terraform.zip \
    && unzip terraform.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform.zip

WORKDIR /workspace

COPY src/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["bash"]