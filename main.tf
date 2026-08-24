# ローカル・本番共通の基礎リソース

provider "aws" {
  region = "ap-northeast-1"
}

resource "aws_dynamodb_table" "x_operator_agent_table" {
  name           = "x-operator-agent-table"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id" # 主キーを汎用的な名前で定義

  attribute {
    name = "id"
    type = "S"
  }
}