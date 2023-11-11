from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms.openai import OpenAI
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.chroma import Chroma

from api.api_models.models import InformationSource, CoreModelAnswer, Answer, Query

URL_MOCK_FILE_PATH = 'data/file1.txt'


def mock_url_source_raw_content(url) -> str:
    try:
        return read_file(url)
    except FileNotFoundError:
        return "EMPTY_RESOURCE"


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()


def get_mapped_sources(sources) -> list[InformationSource]:
    mapped_sources = []
    for source in sources:
        if source.url is None:
            mapped_sources.append(source)
        else:
            mocked_source = InformationSource(raw_content=mock_url_source_raw_content(source.url), url=source.url,
                                              title=source.title)
            mapped_sources.append(mocked_source)
    return mapped_sources


def get_text_chunks_langchain(text: str) -> list[Document]:
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
    return docs


def get_mocked_answer(query: Query):
    return Answer(answer="42",
                  question=query.question,
                  confidence=0.42,
                  sources=[
                      InformationSource(url="https://www.google.com", title="Google",
                                        raw_content="Last year COVID-19 kept us apart. This year we are finally together again."),
                      InformationSource(url="https://www.wikipedia.org", title="Wikipedia",
                                        raw_content="With a duty to one another to the American people to the Constitution.  And with an unwavering resolve that freedom will always triumph over tyranny."),
                      InformationSource(url=None, title="custom text",
                                        raw_content="America is moving. Moving forward. And we can't stop now.")
                  ])


def get_answer(sources: list[InformationSource], query: Query) -> CoreModelAnswer:
    documents = []
    mapped_sources = get_mapped_sources(sources)
    for source in mapped_sources:
        docs = get_text_chunks_langchain(source.raw_content)
        docs = list(map(lambda d: Document(page_content=d.page_content, metadata={"source": source.title}), docs))
        documents.extend(docs)

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    llm = OpenAI(temperature=1.5, model_name='text-davinci-003')

    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)

    qa = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, retriever=docsearch.as_retriever(),
                                                     return_source_documents=True)

    result = qa({"question": query.question})

    return CoreModelAnswer(question=query.question, answer=result['answer'], sources=result['sources'].split(","))
