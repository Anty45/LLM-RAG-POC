from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from llama_index import set_global_service_context, load_index_from_storage, StorageContext
from pathlib import Path
import sys


src_path = Path(__file__.split("src")[0])  # change that to serving
sys.path.append(src_path.as_posix())

from src.scripts.llm_core.llm import instantiate_llm, create_service_context
from src.scripts.llm_core.embbedings import create_embbeding
from src.scripts.llm_core.indexing import get_query_engine
from src.serving.global_config import CLIENT_ORIGINS
from src.scripts.utils.io import load_conf
from qa.routers import qa_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # load confs and neccessary elements from predictions
    model_conf = load_conf(src_path / "conf/model.yaml")
    data_conf = load_conf(src_path / "conf/paths.yaml")

    llm = instantiate_llm(model_conf, src_path)
    embbeding = create_embbeding(model_conf)
    service_context = create_service_context(llm, embbeding, model_conf)
    set_global_service_context(service_context)

    pth_vector_store = Path(src_path / data_conf["vector_store"])
    storage_context = StorageContext.from_defaults(persist_dir=str(pth_vector_store))
    vector_index = load_index_from_storage(storage_context)
    query_engine = get_query_engine(vector_index, service_context, model_conf)

    yield {"query_engine": query_engine, }


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CLIENT_ORIGINS,
    allow_credentials=True,
    allow_headers=["*"],
)

app.include_router(qa_router)


@app.get("/")
def entrypoint():
    return {"s": "hello"}
