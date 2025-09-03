import json
import os
import time
from openai import OpenAI, APIConnectionError, RateLimitError

# --- CONFIGURAÇÃO ---
# O nome do modelo a ser usado. Troque para "gpt-4.1-nano" se estiver disponível.
MODEL_NAME = "gpt-4.1-nano"
# IMPORTANTE: Cole sua chave de API da OpenAI na linha abaixo.
# Lembre-se de não compartilhar este arquivo com a chave preenchida.
api_key = "SUA_CHAVE_DE_API_VAI_AQUI"

def get_model_prediction(client, requirement_text, retries=3, delay=5):
    """
    Obtém a classificação de um requisito usando a API da OpenAI.

    Args:
        client (OpenAI): O cliente da API OpenAI inicializado.
        requirement_text (str): O texto do requisito a ser classificado.
        retries (int): Número de tentativas em caso de falha de conexão.
        delay (int): Tempo de espera em segundos entre as tentativas.

    Returns:
        str: A classificação ('functional' ou 'non-functional') ou None se falhar.
    """
    system_prompt = "You are a Software Engineer. Categorize the requirement into 'functional' or 'non-functional'. Your answer must be ONLY 'functional' or 'non-functional'."
    
    for attempt in range(retries):
        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": requirement_text}
                ],
                temperature=0.0,  # Baixa temperatura para respostas mais consistentes
                max_tokens=5      # Limita a resposta a poucas palavras
            )
            prediction = completion.choices[0].message.content.strip().lower()
            # Limpa a resposta para garantir que seja apenas o esperado
            if 'non-functional' in prediction:
                return 'non-functional'
            if 'functional' in prediction:
                return 'functional'
            return None # Retorna None se a resposta for inesperada

        except (APIConnectionError, RateLimitError) as e:
            print(f"\nAviso: Erro na API ({e}). Tentativa {attempt + 1} de {retries}. Aguardando {delay}s...")
            time.sleep(delay)
        except Exception as e:
            print(f"\nOcorreu um erro inesperado na API: {e}")
            return None
    
    print(f"\nFalha ao obter predição para o requisito após {retries} tentativas.")
    return None

def check_model_accuracy(dataset_filepath):
    """
    Avalia a acurácia de um modelo na classificação de requisitos
    usando chamadas de API reais.
    """

    if api_key == "SUA_CHAVE_DE_API_VAI_AQUI" or not api_key:
        print("Erro: A chave de API não foi definida no script.")
        print("Por favor, edite o arquivo 'accuracy_checker.py' e insira sua chave na variável 'api_key'.")
        return

    client = OpenAI(api_key=api_key)

    # Tenta ler e processar o arquivo de dataset
    try:
        with open(dataset_filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Filtra linhas em branco
            lines = [line for line in lines if line.strip()]
    except FileNotFoundError:
        print(f"Erro: O arquivo '{dataset_filepath}' não foi encontrado.")
        return

    all_requirements = []
    ground_truth_labels = []

    for line in lines:
        try:
            data = json.loads(line)
            all_requirements.append(data['messages'][1]['content'])
            ground_truth_labels.append(data['messages'][2]['content'])
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            print(f"Aviso: Linha ignorada por erro de formato: {e}")

    if not ground_truth_labels:
        print("Nenhum dado válido foi extraído do arquivo. A análise foi interrompida.")
        return

    print(f"--- Iniciando Análise de Acurácia com o Modelo '{MODEL_NAME}' ---")
    print(f"Encontrados {len(all_requirements)} requisitos para classificar...")

    model_predictions = []
    for i, req in enumerate(all_requirements):
        # Mostra o progresso
        print(f"\rProcessando requisito {i + 1}/{len(all_requirements)}...", end="")
        prediction = get_model_prediction(client, req)
        if prediction:
            model_predictions.append(prediction)
        else:
            # Se a API falhar para um item, não podemos continuar a avaliação
            print(f"\nNão foi possível obter a predição para um requisito. A análise será interrompida.")
            return

    print("\nProcessamento concluído. Calculando resultados...")

    correct_predictions_count = 0
    total_items = len(ground_truth_labels)

    # Compara as predições com o gabarito
    for i in range(total_items):
        if ground_truth_labels[i].strip().lower() == model_predictions[i]:
            correct_predictions_count += 1

    accuracy = (correct_predictions_count / total_items) * 100 if total_items > 0 else 0

    print("\n--- Resultado da Análise de Acurácia ---")
    print(f"Modelo Utilizado: {MODEL_NAME}")
    print(f"Total de Requisitos Analisados: {total_items}")
    print(f"Classificações Corretas: {correct_predictions_count}")
    print(f"Acurácia do Modelo: {accuracy:.2f}%")


if __name__ == '__main__':
    DATASET_FILE = 'dataset.jsonl'
    check_model_accuracy(DATASET_FILE)


