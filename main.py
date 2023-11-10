from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings import LlamaCppEmbeddings
from langchain.llms import LlamaCpp
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

# model_path = "./models/WizardLM-7B-uncensored.ggmlv3.q2_K.bin"
# model_path = "./models/openorca-platypus2-13b.gguf.q2_K.bin"
model_path = "./models/WizardLM-7B-uncensored.gguf.q2_K.bin"

loader = TextLoader("./data/state_of_the_union.txt", encoding="utf-8")
# loader = TextLoader("./data/state_of_the_union-backup.txt", encoding="utf-8")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embeddings = LlamaCppEmbeddings(model_path=model_path)
docsearch = Chroma.from_documents(texts, embeddings)

llm = LlamaCpp(
    model_path=model_path,
    n_gpu_layers=1,
    n_batch=512,
    n_ctx=2048,
    f16_kv=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    verbose=True,
)

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())

# query = "What did the president say about Ketanji Brown Jackson"
query = "What kept us apart last year?"
qa.run(query)

# llm("Hi. Who are you?")