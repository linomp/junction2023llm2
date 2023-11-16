# Experiments Directory

Here we summarize what experiments we performed and what we learned from them.

## [mvp](./mvp)

### TL;DR

It demonstrates how to use the OpenAI API and LangChain to create embeddings from a set of
files, make questions and get the names of the specific files where the LLM found the answers.

## [mvp-local-llama](./mvp-local-llama)

// todo @Martin

## [mvp-localai](./mvp-localai)

### TL;DR

It demonstrates how to use local models hosted with [LocalAI](https://localai.io), to create embeddings from a
file and make
questions, using the same LangChain python classes that we would use when calling the real OpenAI
API: `Chroma`, `OpenAIEmbeddings` and `ChatOpenAI`.

### Setup

1. Clone LocalAI in another directory:

    ```bash
    git clone https://github.com/mudler/LocalAI/tree/master
    cd LocalAI/examples/langchain-chroma
    ```
1. Create the model descriptor files inside the folder `LocalAI/examples/langchain-chroma/models`:

   ```yaml
   # File name: text-embedding-ada-002.yaml
   backend: bert-embeddings
   name: text-embedding-ada-002
   parameters:
   model: ggml-model-q4_0.bin
   embeddings: true
   ```

    ```yaml
    # File name: gpt-3.5-turbo.yaml
    backend: gpt4all-j
    context_size: 1024
    name: gpt-3.5-turbo
    parameters:
      model: ggml-gpt4all-j.bin
      temperature: 0.2
      top_k: 80
      top_p: 0.7
    template:
      chat: gpt4all-chat
      completion: gpt4all-completion
    ```

1. Download the models:
    - For chat: [ggml-gpt4all-j.bin](https://gpt4all.io/models/ggml-gpt4all-j.bin)
    - For
      embeddings: [ggml-model-q4_0.bin](https://huggingface.co/mudler/all-MiniLM-L6-v2/resolve/main/ggml-model-q4_0.bin)

1. Create an `.env` file based on the `.env.example` file and set `DEBUG=true`
1. Start LocalAI with docker (make sure you are in `LocalAI/examples/langchain-chroma`):
    ```bash
    docker-compose up
    ```

1. Test the API:

   ```bash
   curl --location --request GET 'http://localhost:8080/v1/models'
   ```

   ```bash
   curl --location --request POST 'http://localhost:8080/v1/chat/completions' \
   --header 'Content-Type: application/json' \
   --data-raw '{
       "model":"gpt-3.5-turbo",
       "messages": [{"role": "user", "content": "Hello who are you"}],
       "temperature": 0.5
   }'
   ```
1. If all is working, then you can run the `mvp-localai` script.