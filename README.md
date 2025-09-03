# PE_serv_estaduais_etl

### Ambiente

Baixar (ou usar venv) da versão do Python 3.12.5. Ao baixar instalar o gereciador de pacotes pip caso não esteja instalado

```bash
python -m ensurepip --default-pip
```

Baixar o projeto: https://github.com/abner-valente/Automacao-de-Coleta-de-Dados-Governamentais---PE

Assim que estiver com o pip instalado, executar os seguintes comandos para instalação das bibliotecas necessárias:

```bash
pip install pandas==2.2.2 requests==2.32.3
```

### Processo

Executar o arquivo `getPeApi.py` colocando o input de Mês e Ano requerido. Ao terminar o processo de download os dados são unificados e colocados em um .csv na propria pasta.

Ao ter posse do arquivo, verificar a estrutura do mesmo que deve estar organizado com as seguintes colunas:

```
r_instituicao;r_cpf;r_matricula;r_nome;r_categoria;r_cargo;r_vencimento_cargo;r_funcao;r_gratificacao_funcao;r_remuneracao;r_ferias;r_natalina;r_outras_vantagens;r_total_vantagens;r_desconto_excedente;r_descontos_faltas;r_descontos_previdencia;r_imposto_renda;r_descontos_compulsorios;r_valor_liquido;r_link
```

Verificada a estrutura do arquivo passar para o **Processo de importação de arq. para a tabela**.
