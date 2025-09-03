
import requests
from typing import Optional
import pandas as pd
import json

class APISession:
    def __init__(self, base_url: str, headers: Optional[dict] = None, cookies: Optional[dict] = None, auth: Optional[tuple] = None):
        self.session = requests.Session()
        self.base_url = base_url

        # Configura headers padrão (se houver)
        if headers:
            self.session.headers.update(headers)
        
        # Configura cookies padrão (se houver)
        if cookies:
            self.session.cookies.update(cookies)

        # Configura autenticação básica (opcional)
        if auth:
            self.session.auth = auth

    def get(self, endpoint: str, params: Optional[dict] = None, timeout: int = 60):
        url = self.base_url + endpoint
        try:
            response = self.session.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"❌ Erro GET em {url}: {e}")
            return None

    def post(self, endpoint: str, data: Optional[dict] = None, json: Optional[dict] = None, timeout: int = 60):
        url = self.base_url + endpoint
        try:
            response = self.session.post(url, data=data, json=json, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"❌ Erro POST em {url}: {e}")
            return None

    def close(self):
        self.session.close()

# Entrada do usuário
while True:
    ano_in = input("Digite o ano da consulta (ex: 2024): ").strip()
    if ano_in.isdigit() and 2000 <= int(ano_in) <= 2100:
        break

while True:
    mes_in = input("Digite o mês da consulta (ex: 01 para Janeiro): ").strip()
    if mes_in.isdigit() and 1 <= int(mes_in) <= 12:
        mes_in = mes_in.zfill(2)
        break



# Configuração da sessão
url_base = "https://api.pentaho.transparencia.pe.gov.br"
endpoint = "/pentaho/plugin/cda/api/doQuery"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest"
}

cookies = {
    "JSESSIONID": "1DEF9A8FB6DD74199859FBC8F7B400DC"
}

parametros = {
    f"parampara_ano": {ano_in},
    f"parammes_": {mes_in},
    "paramsituacao": "%",
    "parampara_orgao_ano_mes": "%",
    "parampesquisa_": "",
    "paramoffset_": 0,
    "paramlimit_": 10000,
    "parammatricula_": "",
    "paramoutros": 3,
    "parampesquisa_cargo_": "",
    "path": "/public/OpenReports/Portal_Producao/Painel_Remuneracao/Painel_Remuneracao.cda",
    "dataAccessId": "sql_jndi",
    "outputIndexId": 1,
    "pageSize": 0,
    "pageStart": 0,
    "sortBy": "",
    "paramsearchBox": ""
}

# Cria a sessão com headers e cookies
api = APISession(base_url=url_base, headers=headers, cookies=cookies)

todos_dados = []
offset = 0

try:
    while True:
        print(f"🔄 Buscando registros página: {offset}...")

        parametros["paramoffset_"] = str(offset)

        #Se não tiver dados
        response = api.post(endpoint, data=parametros)
        
        # Faz a requisição POST usando a sessão criada
        if not response or response.status_code != 200:
            print(f"❌ Erro na requisição: {response.status_code if response else 'Sem resposta'}")
            break

        dados = response.json()
        resultset = dados.get("resultset", [])

        # Pega as colunas apenas na primeira requisição
        if offset == 0:
            colunas = [col["colName"] for col in dados.get("metadata", [])]

        # Condição de parada: se não houver mais registros para baixar
        if not resultset or not isinstance(resultset, list) or len(resultset) == 0:
            print("✅ Todos os registros foram baixados!")
            break
        

        todos_dados.extend(resultset)
        offset += int(parametros["paramlimit_"])

except Exception as e:
    print(f"❌ Ocorreu um erro: {e}")

finally:
    api.close()  # Encerra a sessão corretamente

# 🔽 Exporta o resultado
df = pd.DataFrame(todos_dados, columns=colunas)
df.to_csv(f"PE_{mes_in}{ano_in}.csv", index=False, encoding="utf-8", sep=";")

print(f"✅ Arquivo PE_{mes_in}{ano_in}.csv gerado com sucesso!")
