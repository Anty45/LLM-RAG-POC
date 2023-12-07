from contextlib import nullcontext as does_not_raise
import pytest

import sys
from pathlib import Path

root_path = Path(__file__.split('tests')[0])
sys.path.append(root_path.as_posix())

from src.llm_core.llm import instantiate_llm
from src.utils.io import load_conf

mdl_conf = load_conf(root_path / "tests/ressources/model.yaml")

@pytest.mark.parametrize(
    "model_config, model_pth,expected",
    [
        ({}, mdl_conf["llm_llama_path"], pytest.raises(KeyError)),
        ({"eza": "qdsd"}, mdl_conf["llm_llama_path"], pytest.raises(KeyError)),
        ({"llm_type": "qdsd"}, mdl_conf["llm_llama_path"], pytest.raises(KeyError)),
        (
                {
                    "llm_type": "llamacpp",
                    "llm_llama_model_url": "https://huggingface.co/TheBloke/Vigogne-2-7B-Chat-GGUF/resolve/main/vigogne-2-7b-chat.Q5_K_M.gguf",
                    "model_temperature": 0.1,
                    "max_new_tokens": 250,
                    "n_gpu_layers": 2,
                    "verbose": 1
                }, mdl_conf["llm_llama_path"], pytest.raises(ValueError)),
    ]
)
def test_instantiate_llm_raise(model_config, model_pth, expected):
    with expected:
        assert instantiate_llm(model_config, model_pth) is not None
