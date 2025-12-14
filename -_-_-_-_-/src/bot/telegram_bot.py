"""
Telegram bot for Pulse AI Assistant.
Based on the original giga_gen.py implementation.
"""
import telebot
import logging
from typing import Optional

from src.core.config import config
from src.core import constants
from src.llm.client import LLMClient
from src.database.connection import DatabaseConnection
from src.search.hybrid_searcher import HybridSearcher

logger = logging.getLogger(__name__)

class PulseBot:
    """Main Telegram bot class."""
    
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token)
        self.llm_client = LLMClient()
        self.db_connection = DatabaseConnection()
        self.searcher = HybridSearcher(self.db_connection)
        
        # Register handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register all message handlers."""
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            self._handle_welcome(message)
        
        @self.bot.message_handler(func=lambda message: True)
        def handle_query(message):
            self._handle_analytics_query(message)
    
    def _handle_welcome(self, message):
        """Send welcome message."""
        welcome_text = (
            "👋 Привет! Я Pulse — AI-аналитик вашей генетической сети.\n\n"
            "Я помогу найти информацию о генах, их функциях и связях. "
            "Задавайте вопросы на естественном языке, например:\n\n"
            + "\n".join(constants.EXAMPLE_QUERIES) + "\n\n"
            "Просто напишите название гена или ваш вопрос!"
        )
        self.bot.send_message(message.chat.id, welcome_text, parse_mode="HTML")
    
    def _handle_analytics_query(self, message):
        """Handle user query and generate response."""
        user_text = message.text
        chat_id = message.chat.id
        
        # Send "thinking" message
        wait_msg = self.bot.send_message(
            chat_id, 
            "🤖 <b>Анализирую запрос...</b>", 
            parse_mode="HTML"
        )
        
        try:
            # Step 1: Try hybrid search first (if implemented)
            if config.DEBUG:
                logger.info(f"User query: {user_text}")
            
            # For now, use the original SQL generation approach
            sql_query = self._generate_sql(user_text)
            
            if not sql_query:
                self.bot.edit_message_text(
                    "❌ Не удалось сгенерировать запрос к базе данных.",
                    chat_id,
                    wait_msg.message_id
                )
                return
            
            if config.DEBUG:
                logger.info(f"Generated SQL: {sql_query}")
            
            # Step 2: Execute SQL
            data_result = self._execute_sql(sql_query)
            
            if config.DEBUG:
                logger.info(f"DB Result: {data_result}")
            
            # Step 3: Format response
            final_answer = self._format_response(user_text, data_result)
            
            # Update message with final answer
            self.bot.edit_message_text(
                final_answer,
                chat_id,
                wait_msg.message_id
            )
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            self.bot.edit_message_text(
                f"❌ Произошла ошибка при обработке запроса: {str(e)}",
                chat_id,
                wait_msg.message_id
            )
    
    def _generate_sql(self, question: str) -> Optional[str]:
        """Generate SQL query from natural language question."""
        prompt = constants.SYSTEM_PROMPTS["sql_generator"].format(
            schema=constants.DB_SCHEMA,
            question=question
        )
        
        try:
            response = self.llm_client.generate(prompt)
            # Clean up response
            sql = response.strip().replace("```sql", "").replace("```", "").strip()
            return sql if sql.lower().startswith("select") else None
        except Exception as e:
            logger.error(f"Error generating SQL: {e}")
            return None
    
    def _execute_sql(self, sql_query: str) -> str:
        """Execute SQL query safely."""
        if not sql_query.lower().strip().startswith("select"):
            return "⚠️ Ошибка безопасности: Разрешены только запросы на чтение (SELECT)."
        
        try:
            result = self.db_connection.execute_query(sql_query)
            return str(result) if result else "Запрос выполнен, но данных не найдено."
        except Exception as e:
            return f"Ошибка SQL: {e}"
    
    def _format_response(self, question: str, data: str) -> str:
        """Format raw data into human-readable response."""
        prompt = constants.SYSTEM_PROMPTS["response_formatter"].format(
            question=question,
            result=data
        )
        
        try:
            response = self.llm_client.generate(prompt)
            return response
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return "Не удалось сформировать текстовый ответ."
    
    def run(self):
        """Start the bot."""
        logger.info("Starting Pulse Telegram bot...")
        self.bot.infinity_polling()

# For backward compatibility (original giga_gen.py style)
if __name__ == '__main__':
    from src.core.config import config
    config.validate()
    
    import logging
    logging.basicConfig(level=logging.INFO)
    
    bot = PulseBot(config.TELEGRAM_BOT_TOKEN)
    bot.run()
