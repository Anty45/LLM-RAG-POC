from typing import Optional

from llama_index import ServiceContext
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import completion_to_prompt, messages_to_prompt


def instantiate_llm(model_config: dict, model_pth: Optional):
    conf_key = [
        "llm_type",
        "llm_llama_model_url",
        "model_temperature",
        "max_new_tokens",
        "n_gpu_layers",
        "verbose",
    ]
    for k in conf_key:
        if k not in model_config:
            raise KeyError(
                f"{k} is a required key for llm instantiation. Please upload configuration"
            )

    if "llamacpp" != model_config["llm_type"]:
        raise ValueError("We only support llamacpp as backend for the moment")

    else:
        llm = LlamaCPP(
            model_url=model_config["llm_llama_model_url"],
            model_path=str(model_pth),
            temperature=model_config["model_temperature"],
            max_new_tokens=model_config["max_new_tokens"],
            model_kwargs={
                "n_gpu_layers": model_config["n_gpu_layers"],
            },
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=model_config["verbose"],
        )

    return llm


def create_service_context(llm, embedding, model_conf):
    service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embedding,
        chunk_size=model_conf["chunk_size"],
    )
    return service_context
