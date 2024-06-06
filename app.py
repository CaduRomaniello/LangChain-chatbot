import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import time
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.retriever import create_retriever_tool
from dotenv import load_dotenv


from langchain_core.messages import HumanMessage, AIMessage

def main():   
    # Configure Streamlit page
    st.set_page_config(
        page_title="Chatbot Elite Top Estética",
    )
    st.title("Chatbot Elite Top Estética 👩")

    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    load_dotenv()
     
    if "qa" not in st.session_state:
        loader = PyPDFLoader("./EliteTop.pdf")
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
        retriever = vectorstore.as_retriever(search_type="similarity_score_threshold",search_kwargs={"k":10, "score_threshold": 0.6})
        llm = ChatOpenAI(temperature=0.2,model_name='gpt-4')

        tool = create_retriever_tool(
            retriever,
            "pesquisar_elite_top",
            "Use esta ferramenta para obter informações sobre a Elite Top Estética Med Spa. Sobre serviços, perguntas frequentes e mais.",
        )
        tools = [tool]
        prompt = hub.pull("hwchase17/openai-tools-agent")
        prompt.messages[0] = SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[],
           template="""Você é um assistente da Elite Top Estética para responder perguntas sobre a Elite Top Estética, a melhor clínica de estética do sul da Flórida.
Seja educado e amigável e tenha uma conversa com o usuário para fornecer informações sobre a Elite Top Estética Med Spa.
Alguns serviços que a clínica oferece e sobre os quais você pode falar: anti-envelhecimento, esteticista, depilação a laser, terapia de reposição hormonal e serviços de perda de peso médica.
Além disso, é a clínica de estética número 1 em Port St Lucie. Veronica Hexter, uma Enfermeira Especialista Avançada Registrada e certificada, traz mais de 20 anos de experiência na área da saúde para a Elite Top Estética.
Seja sempre educado e amigável e converse como uma pessoa. Não seja um robô.
Colete o e-mail e o nome do usuário no in[icio da conversa sem ser de forma direta.
Caso o usuario peça para agendar uma sessão, informe o link do calendly e oriente o usuario a acessar o link:
 https://calendly.com/ygorbalves222/30min
"""))
        prompt.messages[1] = MessagesPlaceholder(variable_name='chat_history', optional=False)
        agent = create_openai_tools_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools)
        qa = agent_executor
        st.session_state["qa"] = qa
    else:
        qa = st.session_state["qa"]

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role": "assistant", 
                                    "content": "Bem-vindo à Elite Top Estética! Como posso ajudá-lo hoje?"}]
        
    for message in st.session_state['messages']:
        with st.chat_message(message["role"], avatar='👩' if message["role"] == 'assistant' else None):
            st.markdown(message["content"])


    # Chat logic
    query = st.chat_input("Ask me anything")
    if query:
        # Add user message to chat history        
        user_message = {"role": "user", "content": query}
        st.session_state['messages'].append(user_message)
        st.session_state['chat_history'].append(HumanMessage(content=query))

        # st.session_state['messages'].append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
            
        # Prepare for response
        with st.chat_message("assistant", avatar='👩'):
            message_placeholder = st.empty()
            # Simulate assistant typing
            result = qa.invoke({"input": query, "chat_history": st.session_state['chat_history']})      
            print('\n' + '-'*100)
            print(f'Result message:\n{result}')
            response = result['output']
            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.02)  # Delay to simulate typing
                message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)        
            message_placeholder.markdown(full_response)
        # Add assistant message to chat history
        st.session_state['chat_history'].append(AIMessage(content=response))
        assistant_message = {"role": "assistant", "content": response}
        st.session_state['messages'].append(assistant_message)
        
if __name__ == "__main__":
    main()