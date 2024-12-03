import requests

# Configurações
API_KEY = "Chave de API KEY new relic"
ACCOUNT_ID = "ID da conta new relic"
GRAPHQL_ENDPOINT = "https://api.newrelic.com/graphql"
# Adicione o webhook do Slack
SLACK_WEBHOOK_URL = "link webhook slack"

# Query GraphQL
query = """
{
  actor {
    account(id: ACCOUNT_ID) {
      nrql(query: "SELECT count(*) FROM SyntheticCheck WHERE monitorName = 'Site-academias-BR' AND result = 'SUCCESS' SINCE 1 hour ago") {
        results
      }
    }
  }
}
""".replace("ACCOUNT_ID", ACCOUNT_ID)

# Função para buscar dados no New Relic


def fetch_data():
    headers = {
        "Content-Type": "application/json",
        "API-Key": API_KEY
    }
    response = requests.post(GRAPHQL_ENDPOINT, json={
                             "query": query}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro: {response.status_code}, {response.text}")
        return None

# Função para enviar dados ao Slack


def send_to_slack(message):
    payload = {"text": message}  # Formata a mensagem no Slack
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        print("Mensagem enviada ao Slack com sucesso!")
    else:
        print(
            f"Erro ao enviar ao Slack: {response.status_code}, {response.text}")


# Executa a consulta e envia para o Slack
data = fetch_data()
if data:
    # Extrai os resultados
    results = data.get("data", {}).get("actor", {}).get(
        "account", {}).get("nrql", {}).get("results", [])
    if results:
        # Ajuste conforme os dados retornados
        count = results[0].get("count", 0)
        message = f"Relatório do New Relic:\nMonitores bem-sucedidos na última hora: {count}"
    else:
        message = "Não foi possível obter resultados da consulta NRQL."

    # Envia a mensagem ao Slack
    send_to_slack(message)
