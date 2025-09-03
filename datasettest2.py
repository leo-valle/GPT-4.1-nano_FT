import pandas as pd
import json
import os

def convert_excel_to_jsonl(excel_filepath, jsonl_filepath):
    """
    Converte um arquivo Excel (.xlsx) para o formato JSON Lines (.jsonl)
    seguindo a estrutura de mensagens do assistente da OpenAI.

    Assume que o Excel tem as colunas 'requirement' e 'NF'.

    Args:
        excel_filepath (str): O caminho para o arquivo de entrada do Excel.
        jsonl_filepath (str): O caminho para o arquivo de saída JSONL.
    """
    # --- IMPORTANTE: Configure os nomes das suas colunas aqui ---
    REQUIREMENT_COLUMN = 'requirement'
    CATEGORY_COLUMN = 'NF'
    # -----------------------------------------------------------

    # Mensagem padrão do sistema para cada entrada no JSONL
    system_message_content = "You are a Software Engineer and need to categorize requirements into 'functional' or 'non-functional'. Your answer must be 'functional' or 'non-functional' only."

    try:
        # Lê o arquivo Excel para um DataFrame do pandas
        print(f"Lendo o arquivo Excel: '{excel_filepath}'...")
        df = pd.read_excel(excel_filepath)
        print("Arquivo lido com sucesso.")

        # Verifica se as colunas esperadas existem
        if REQUIREMENT_COLUMN not in df.columns or CATEGORY_COLUMN not in df.columns:
            print(f"Erro: O arquivo Excel deve conter as colunas '{REQUIREMENT_COLUMN}' e '{CATEGORY_COLUMN}'.")
            print(f"Colunas encontradas: {list(df.columns)}")
            return

        # Abre o arquivo de saída para escrita
        with open(jsonl_filepath, 'w', encoding='utf-8') as f:
            print(f"Iniciando a conversão para '{jsonl_filepath}'...")
            
            # Itera sobre cada linha do DataFrame
            for index, row in df.iterrows():
                # Extrai o conteúdo das colunas
                requirement = row[REQUIREMENT_COLUMN]
                category_value = row[CATEGORY_COLUMN]

                # Garante que os dados não sejam nulos/vazios
                if pd.isna(requirement) or pd.isna(category_value):
                    print(f"Aviso: Linha {index + 2} ignorada por conter dados vazios.")
                    continue

                # --- LÓGICA CORRIGIDA ---
                # Converte o valor numérico (0 ou 1) para o texto correspondente.
                # 1 agora corresponde a 'non-functional' e 0 a 'functional'.
                if category_value == 1:
                    category_text = 'non-functional'
                elif category_value == 0:
                    category_text = 'functional'
                else:
                    # Se o valor não for 0 ou 1, ignora a linha e avisa o usuário.
                    print(f"Aviso: Linha {index + 2} ignorada. O valor da categoria ('{category_value}') não é 0 ou 1.")
                    continue
                # ----------------------------------------

                # Monta a estrutura de dicionário do JSON
                json_structure = {
                    "messages": [
                        {"role": "system", "content": system_message_content},
                        {"role": "user", "content": str(requirement)},
                        {"role": "assistant", "content": category_text}
                    ]
                }

                # Converte o dicionário para uma string JSON e escreve no arquivo
                f.write(json.dumps(json_structure, ensure_ascii=False) + '\n')

        print("-" * 30)
        print("Conversão concluída com sucesso!")
        print(f"Total de {len(df)} linhas processadas.")
        print(f"O arquivo '{jsonl_filepath}' foi criado.")
        print("-" * 30)

    except FileNotFoundError:
        print(f"Erro: O arquivo '{excel_filepath}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == '__main__':
    # O script agora descobre automaticamente o seu próprio diretório
    # e procura os arquivos a partir dele.
    
    # Obtém o caminho absoluto do diretório onde o script está localizado
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Constrói o caminho completo para os arquivos de entrada e saída
    INPUT_EXCEL_FILE = os.path.join(script_dir, 'dataset-test2.xlsx')
    OUTPUT_JSONL_FILE = os.path.join(script_dir, 'dataset-convertido.jsonl')
    
    convert_excel_to_jsonl(INPUT_EXCEL_FILE, OUTPUT_JSONL_FILE)

