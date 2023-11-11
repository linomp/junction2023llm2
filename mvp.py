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

llm = OpenAI(model_name="curie", temperature=0)

loader = TextLoader("./data/state_of_the_union_full.txt", encoding="utf-8")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# TODO: serialize the embeddings and/or docsearch to disk, consider pickle
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)

prompt_template = """Answer in one sentence.

{context}

Question: {question}
"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

chain_type_kwargs = {"prompt": PROMPT}
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(),
                                 chain_type_kwargs=chain_type_kwargs)

query = "Who did Vladimir Putin meet?"

res = qa.run(query)

print(f"Q: {query}")
print(res)
