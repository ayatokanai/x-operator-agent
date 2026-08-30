# ローカル・本番共通の基礎リソース

provider "aws" {
  region = "ap-northeast-1"
}

resource "aws_dynamodb_table" "x_operator_agent_table" {
  name         = "x-operator-agent-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "PK"
  range_key    = "SK"

  # -------------------------------------------------------------
  # キー属性定義
  # ※ DynamoDBでは PK, SK, GSIのキーとして使う属性のみ定義します
  # -------------------------------------------------------------
  attribute {
    name = "PK"
    type = "S" # String
  }

  attribute {
    name = "SK"
    type = "S" # String
  }

  attribute {
    name = "GSI1PK"
    type = "S" # String
  }

  attribute {
    name = "GSI1SK"
    type = "S" # String
  }

  # -------------------------------------------------------------
  # GSI1 定義（ステータス別の新着順一覧取得用）
  # -------------------------------------------------------------
  global_secondary_index {
    name            = "GSI1"
    hash_key        = "GSI1PK"
    range_key       = "GSI1SK"
    projection_type = "ALL" # 投稿本文やメタデータも含めて全属性を射影
  }

  # -------------------------------------------------------------
  # TTL（Time to Live）設定（90日後などの自動データ破棄用）
  # -------------------------------------------------------------
  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  # 削除保護（誤削除を防ぎたい場合は true に設定）
  deletion_protection_enabled = false

  tags = {
    Environment = "production"
    Application = "x-auto-poster"
  }
}

# -------------------------------------------------------------
# Lambda 等から参照するための Output 定義
# -------------------------------------------------------------
output "dynamodb_table_name" {
  description = "DynamoDB Table Name"
  value       = aws_dynamodb_table.x_operator_agent_table.name
}

output "dynamodb_table_arn" {
  description = "DynamoDB Table ARN"
  value       = aws_dynamodb_table.x_operator_agent_table.arn
}