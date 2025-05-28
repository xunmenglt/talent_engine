import os
import logging
import logging.config
import nltk

from logging.config import fileConfig

from configs.configuration import settings as _settings

logging.config.fileConfig(os.path.join(
    os.getcwd(),
    "configs/log.cfg"
))

__all__ = ["settings","logger","nltk"]

settings = _settings

log_save_dir=os.path.join(os.getcwd(),"logs")
if not os.path.exists(log_save_dir):
    os.makedirs(log_save_dir,exist_ok=True)
logger = logging.getLogger()


nltk_data_path=os.path.join(
    os.getcwd(),
    "data/nltk_data"
)
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path,exist_ok=True)

nltk.data.path = nltk_data_path


