from typing import Optional

from llama_index.llms import OpenAI, LlamaCPP
from llama_index import ServiceContext
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt


def instantiate_llm(model_config: dict, model_pth: Optional):
    if model_config["llm_type"] == "llamacpp":
        llm = LlamaCPP(
            model_url=model_config["llm_llama_model_url"],
            model_path=str(src_path / model_config["llm_llama_path"]),
            temperature=model_config["model_temperature"],
            max_new_tokens=model_config["max_new_tokens"],
            model_kwargs={
                #"low_cpu_mem_usage": model_config["low_cpu_mem_usage"],
                "n_gpu_layers": model_config["n_gpu_layers"],
            },
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=model_config["verbose"],
        )
    # TODO: take care of the case where llm_type does not correspond to anything
    return llm


def create_service_context(llm, embedding, model_conf):
    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embedding,
        chunk_size=model_conf["chunk_size"],
    )
    return service_context
