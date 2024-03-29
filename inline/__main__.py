# -*- coding: utf-8 -*-

import os
import json

from inline import __commit_hash__
from inline.logger import error_logger, logger
from inline.bot import inline
from inline.schema import OrderInfo


def main():
    final_screen_path = os.getenv("FINAL_SCREEN_PATH")
    line_token = os.getenv("LINE_TOKEN")
    config_path = os.getenv("INLINE_CONFIG_PATH")
    logger.info(f'commit hash: {__commit_hash__}')
    logger.info(f'config_path: {config_path}')
    logger.info(f'final_screen_path: {final_screen_path}')

    bot = inline()
    try:
        with open(config_path, 'r', encoding='utf-8') as jsonfile:
            j = json.load(jsonfile)
            order_info = OrderInfo(**j)
        
        logger.info(order_info)
        
        bot.run(order_info, final_screen_path)
        bot.notify_line(line_token)
    except Exception as e:
        error_logger.error(f"Failed to run bot: {e}")
        raise e
    finally:
        bot.teardown()
    
if __name__ == "__main__":    
    main()
