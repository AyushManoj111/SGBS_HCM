# Importa módulos necessários
import os  # Para acessar variáveis de ambiente (ex: chave da API)
import google.generativeai as genai  # Biblioteca para usar os modelos generativos da Google
from dotenv import load_dotenv  # Para carregar variáveis de ambiente do arquivo .env

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura a chave da API do Gemini, usando o valor da variável de ambiente GEMINI_API_KEY
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configurações da geração de texto
generation_config = {
    "temperature": 0,  # Geração determinística (respostas sempre iguais para a mesma pergunta)
    "top_p": 0.95,  # Probabilidade acumulada para amostragem (controle de criatividade)
    "top_k": 64,  # Considera os 64 tokens mais prováveis ao gerar o próximo
    "max_output_tokens": 8192,  # Número máximo de tokens (palavras/pedaços) na resposta
    "response_mime_type": "text/plain",  # Formato da resposta (texto simples)
}

# Configurações de segurança (para controle de conteúdo sensível ou impróprio)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},  # Não bloqueia por assédio
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},  # Bloqueia discurso de ódio moderado ou grave
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},  # Bloqueia conteúdo sexual explícito moderado ou grave
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},  # Bloqueia conteúdo perigoso moderado ou grave
]

# Cria o modelo generativo com as configurações acima
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  # Nome do modelo escolhido (rápido e eficiente)
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=(
        # Instrução do sistema que define o comportamento do assistente
        "És um assistente que ajuda a responder qualquer questão sobre doações de sangue na área da saúde. "
        "Formule a resposta em parágrafo nao muito longo e seja direto. "
        "Não podes responder questões fora do contexto de saúde humana, caso recebas uma pergunta fora disso, "
        "deves dizer que não podes fornecer essa informação."
    ),
)

# Inicia uma sessão de chat (memória de histórico vazia no começo)
chat_session = model.start_chat(history=[])

# Função que envia uma pergunta ao modelo e retorna a resposta em texto
def answer_question(question: str) -> str:
    response = chat_session.send_message(question)  # Envia a pergunta para o modelo
    return response.text  # Retorna apenas o texto da resposta
