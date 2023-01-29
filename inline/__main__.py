from inline.logger import error_logger, logger
import inline
import os
from inline.bot import inline


def main():
    case_id = os.getenv("CASE_ID")
    accident_date = os.getenv("ACDT_DATE") # accident date
    final_screen_path = os.getenv("FINAL_SCREEN_PATH")
    line_token = os.getenv("LINE_TOKEN")

    logger.info(f'case id:       {case_id}')
    logger.info(f'accident date: {accident_date}')
    # logger.info(f'commit hash: {inline.__commit_hash__}')

    bot = inline()
    try:
        bot.run(case_id, accident_date, final_screen_path)
        bot.notify_line(line_token)
    except Exception as e:
        error_logger.error(f"Failed to run bot: {e}")
        # raise e
    finally:
        pass
        # bot.teardown()
    
if __name__ == "__main__":    
    main()
