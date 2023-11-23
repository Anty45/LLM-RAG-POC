# RAG on French Law documents behind a FastAPI backend

---

[![Watch the video](./docs/illustration/llama.png)](./docs/illustration/rag-demo-short.mp4)
## RAG 
This project is an example of how to pratically create a [retrieval augmented generation](https://stackoverflow.blog/2023/10/18/retrieval-augmented-generation-keeping-llms-relevant-and-current/) (RAG) pipeline using an open-source LLM. We choose
[LlaMa 2 ](https://ai.meta.com/llama/) for the sake of the demonstration.
Please find the others [options here](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard) and update the [model configuration](https://github.com/Anty45/LLM-RAG-POC/blob/master/conf/model.yaml) file accordingly.


## FastAPI Backend 
On top of that you have an [example](https://github.com/Anty45/LLM-RAG-POC/tree/master/src/serving) of how to deploy the rag pipeline behind an endpoint.
There is only a question answering (QA) service right now, but it's an example that can be use to build other services

## Frontend 
**(coming)**
