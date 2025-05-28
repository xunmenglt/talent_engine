# BSD 3- Clause License Copyright (c) 2023, Tecorigin Co., Ltd. All rights
# reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY,OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)  ARISING IN ANY
# WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.

from functools import lru_cache

from core.embedder.local_embedding import LocalEmbeddings

from langchain_core.embeddings import Embeddings
from configs import settings
from langchain_openai.embeddings import OpenAIEmbeddings


@lru_cache
def get_embedding_model(model_name_or_path, model_engine,base_url="",api_key="") -> Embeddings:
    """Create the embedding model."""

    if model_engine in ["huggingface"]:
        return LocalEmbeddings(model_name_or_path, model_engine)
    elif model_engine in ["openai"]:
        return OpenAIEmbeddings(model=model_name_or_path,base_url=base_url,api_key=api_key)
    else:
        raise RuntimeError("Unable to find any supported embedding model. Supported engine is huggingface.")


def get_default_embedding_model() -> Embeddings:
    embedding_model=get_embedding_model(
            settings.embeddings.model_name_or_path,
            settings.embeddings.model_engine,
            settings.embeddings.base_url,
            settings.embeddings.api_key
    )
    return embedding_model

# embedding_model = get_embedding_model(settings.embeddings.model_name_or_path,
#                                       settings.embeddings.model_engine)

