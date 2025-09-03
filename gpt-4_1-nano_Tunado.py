import os
import json
import time
from openai import OpenAI

# --- CONFIGURAÇÃO OBRIGATÓRIA ---
# 1. Cole sua chave de API da OpenAI aqui.
API_KEY = ""

# 2. Cole o ID completo do seu modelo fine-tuned.
# Exemplo: "ft:gpt-3.5-turbo-0125:your-org:custom-name:id"
FINE_TUNED_MODEL_ID = "ft:gpt-4.1-nano-2025-04-14:ita:leonardo-valle-102087-ga-ita-br:CBiDAYf5"

# 3. Defina o nome do seu arquivo de dataset de teste.
TEST_DATASET_FILE = 'dataset_unido.jsonl'
# ---------------------------------

def read_test_dataset(filepath):
    """Lê o arquivo de dataset .jsonl e extrai os requisitos e as respostas corretas."""
    test_data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    requirement = data['messages'][1]['content']
                    correct_answer = data['messages'][2]['content']
                    test_data.append({"requirement": requirement, "answer": correct_answer})
                except (json.JSONDecodeError, IndexError, KeyError):
                    print(f"Aviso: Linha malformada no dataset ignorada: {line.strip()}")
    except FileNotFoundError:
        print(f"Erro: O arquivo de teste '{filepath}' não foi encontrado.")
        return None
    return test_data

def get_model_prediction(client, model_id, requirement_text):
    """Envia um requisito para a API e retorna a predição do modelo."""
    max_retries = 3
    retry_delay = 5  # segundos

    system_prompt = "You are a Software Engineer and need to categorize requirements into 'functional' or 'non-functional'. Your answer must be 'functional' or 'non-functional' only."

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": requirement_text}
                ],
                max_tokens=5,
                temperature=0.0 # Usamos 0 para respostas mais determinísticas
            )
            # Extrai o conteúdo da resposta e remove espaços extras ou quebras de linha
            return response.choices[0].message.content.strip().lower()
        except Exception as e:
            print(f"Erro na chamada da API (tentativa {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                print(f"Aguardando {retry_delay} segundos antes de tentar novamente...")
                time.sleep(retry_delay)
            else:
                print("Número máximo de tentativas atingido. Falha ao obter predição.")
                return None

def main():
    """Função principal para executar a verificação de acurácia."""
    print("--- Verificador de Acurácia para Modelo Fine-Tuned ---")

    # Validação inicial
    if API_KEY == "SUA_CHAVE_DE_API_VAI_AQUI" or FINE_TUNED_MODEL_ID == "SEU_MODELO_CUSTOMIZADO_AQUI":
        print("\nErro: Por favor, preencha sua API_KEY e seu FINE_TUNED_MODEL_ID no início do script.")
        return

    # Obtém o caminho absoluto para o arquivo de teste
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_filepath = os.path.join(script_dir, TEST_DATASET_FILE)

    # Carrega o dataset de teste
    dataset = read_test_dataset(test_filepath)
    if not dataset:
        return

    # Inicializa o cliente da OpenAI
    try:
        client = OpenAI(api_key=API_KEY)
    except Exception as e:
        print(f"Erro ao inicializar o cliente da OpenAI: {e}")
        return

    correct_predictions = 0
    total_predictions = len(dataset)
    
    print(f"\nIniciando a avaliação de {total_predictions} requisitos com o modelo: {FINE_TUNED_MODEL_ID}")
    print("-" * 50)

    # Itera sobre o dataset, obtém predições e compara com o gabarito
    for i, item in enumerate(dataset):
        requirement = item['requirement']
        correct_answer = item['answer']
        
        print(f"Processando requisito {i + 1}/{total_predictions}...")
        
        prediction = get_model_prediction(client, FINE_TUNED_MODEL_ID, requirement)
        
        if prediction is None:
            print("  -> Falha ao obter predição. Abortando a avaliação.")
            return

        # Verifica se a predição está correta
        if prediction == correct_answer:
            correct_predictions += 1
            print("  -> Predição: '" + prediction + "' (Correta!)")
        else:
            print("  -> Predição: '" + prediction + "' (Incorreta! Esperado: '" + correct_answer + "')")
        
        # Pausa para evitar exceder os limites de taxa da API (rate limits)
        time.sleep(1) 

    # Calcula e exibe os resultados finais
    accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
    
    print("-" * 50)
    print("\n--- Resultado Final da Avaliação ---")
    print(f"Modelo Testado: {FINE_TUNED_MODEL_ID}")
    print(f"Total de Requisitos Analisados: {total_predictions}")
    print(f"Classificações Corretas: {correct_predictions}")
    print(f"Acurácia do Modelo: {accuracy:.2f}%")
    print("-" * 50)


if __name__ == '__main__':
    main()
