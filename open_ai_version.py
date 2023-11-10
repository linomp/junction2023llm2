import os

from langchain.llms.openai import OpenAI

os.environ["OPENAI_API_KEY"] = "..."
# os.environ["OPENAI_PROXY"] = "http://localhost:8080"

llm = OpenAI(openai_api_base="http://localhost:8080")
llm("hello who are you")
#
# loader = TextLoader("./data/state_of_the_union.txt", encoding="utf-8")
# documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# texts = text_splitter.split_documents(documents)
#
# embeddings = OpenAIEmbeddings()
# docsearch = Chroma.from_documents(texts, embeddings)
#
# qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())
