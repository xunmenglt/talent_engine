import os, sys
sys.path.append(os.getcwd())
import argparse
from server.api import run_api
from configs import logger,settings

def main():
    logger.info("=========================Starting Service=========================")

    try:
        run_api(host=settings.server.api_server_host,
                port=settings.server.api_server_port,
                ssl_keyfile=None,
                ssl_certfile=None)
    except Exception as e:
        logger.error("Api Server 启动失败：", e)
        sys.stderr.write("Fail to start application")


if __name__ == "__main__":
    main()