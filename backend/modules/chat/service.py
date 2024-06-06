import os

from langchain import hub
from pypdf import PdfReader
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import PyPDFLoader
from modules.appointment_setting.dto import APPOINTMENTSETTINGDTO
from langchain.document_loaders import DirectoryLoader
from modules.appointment_setting.entity import ConversationHistory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import MessagesPlaceholder, SystemMessagePromptTemplate
from modules.appointment_setting.service import get_appointment_setting_by_phone_number, update_appointment_setting

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_pdf_loaders():
    diretorio_atual = os.getcwd()
    print("Diretório atual:", diretorio_atual)
    pdf_files = []
    for root, dirs, files in os.walk("./docs"):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))

    print(pdf_files)
    loaders = []
    for pdf in pdf_files:
        print(pdf)
        if "barema-avaliacao-01.pdf" not in pdf:
            continue
        loader = PyPDFLoader(pdf)
        loaders.extend(loader.load())
    return loaders

def load_conversation_history(conversation_history, previous_conversation):
    for message in previous_conversation:
        if message.message_type == 'HumanMessage':
            conversation_history.append(HumanMessage(content = message.message))
        else:
            conversation_history.append(AIMessage(content = message.message))

def create_agent(user_data):
    loaders = get_pdf_loaders()
    print(loaders)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(loaders)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_type="similarity_score_threshold",search_kwargs={"k":10, "score_threshold": 0.6})

    llm = ChatOpenAI(temperature=0.2,model_name='gpt-4')

    tool = create_retriever_tool(
        retriever,
        "barema_apresentacao",
        "Use esta ferramenta para cessar o modelo/barema em que a resposta deve ser fornecida.",
    )
    tools = [tool]
    prompt = hub.pull("hwchase17/openai-tools-agent")
    prompt.messages[0] = SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[],
    template=f"""Você é um assistente que fornece informações sobre vários métodos de aprendizado de máquina utilizando um barema específico fornecido.
        Seja educado e amigável e tenha uma conversa com o usuário para fornecer informações sobre a os métodos de aprendizado de máquina.
        Seja sempre educado e amigável e converse como uma pessoa. Não seja um robô.
        Suas respostas sobre um determinado método de aprendizado de máquina devem ser baseadas no barema fornecido.
        As informações do usuário são: Nome: {user_data['name']}, Email: {user_data['email']}, Telefone: {user_data['phone_number']}
    """))
    # template=f"""Você é um assistente da Anna Pegova Paris Estética para responder perguntas sobre a Anna Pegova Paris.
    #     Seja educado e amigável e tenha uma conversa com o usuário para fornecer informações sobre a Anna Pegova Paris.
    #     Seja sempre educado e amigável e converse como uma pessoa. Não seja um robô.
    #     As informações do usuário são: Nome: {user_data['name']}, Email: {user_data['email']}, Telefone: {user_data['phone_number']}
    #     Caso o usuario peça para agendar uma sessão, informe o link do calendly e oriente o usuario a acessar o link:
    #     https://calendly.com/ygorbalves222/30min
    # """))
    prompt.messages[1] = MessagesPlaceholder(variable_name='chat_history', optional=False)
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    qa = agent_executor

    return qa

def get_response_from_llm(params):
    appointment_setting = APPOINTMENTSETTINGDTO.from_entity_to_DTO(get_appointment_setting_by_phone_number(params.phone_number))

    qa = create_agent({'name': appointment_setting.name, 'email': appointment_setting.email, 'phone_number': appointment_setting.phone_number})

    chat_history = []
    load_conversation_history(chat_history, appointment_setting.conversation_history)

    result = qa.invoke({"input": params.message, "chat_history": chat_history})

    appointment_setting.conversation_history.append(ConversationHistory(message_type='HumanMessage', message=params.message.replace('"', "")))
    appointment_setting.conversation_history.append(ConversationHistory(message_type='AIMessage', message=result['output'].replace('"', "")))

    updated_appointment_setting = update_appointment_setting(appointment_setting)
    
    return {'content': result['output'].replace('"', "")}