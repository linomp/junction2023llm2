from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.chroma import Chroma

# Settings for locally hosted OpenAI-compatible models
# os.environ["OPENAI_API_KEY"] = "KEY_DOESNT_MATTER_FOR_LOCALHOST"
# os.environ["OPENAI_API_BASE"] = "http://localhost:8080"

load_dotenv()

loader = TextLoader("data/state_of_the_union_full.txt", encoding="utf-8")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

llm = OpenAI(temperature= 0, model_name = 'text-davinci-003')

# TODO: serialize the embeddings and/or docsearch to disk, consider pickle
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)

prompt_template = """Answer in one sentence. If you do not know the answer, do not try to make one up. Say you do not know.

{context}

Question: {question}
"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

chain_type_kwargs = {"prompt": PROMPT}
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(),
                                 chain_type_kwargs=chain_type_kwargs, return_source_documents = True)

query = "What set us apart last year?"

result = qa({"query": query})

print(f"Q: {query}")
print(result['result'])
print(result['source_documents'])

