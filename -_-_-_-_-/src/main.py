"""
Main entry point for Pulse AI Assistant.
"""
import logging
from src.core.config import config
from src.bot.telegram_bot import PulseBot

def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info("Pulse AI Assistant starting...")

def main() -> None:
    """Main application entry point."""
    try:
        # Validate configuration
        config.validate()
        
        # Setup logging
        setup_logging()
        
        # Initialize and run the bot
        bot = PulseBot(config.TELEGRAM_BOT_TOKEN)
        bot.run()
        
    except Exception as e:
        logging.error(f"Failed to start Pulse AI Assistant: {e}")
        raise

if __name__ == "__main__":
    main()
