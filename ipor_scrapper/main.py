from scrapper_service import Scrapper
from loggers import configure_logging
from configuration.properties.config import ProductionConfig


configure_logging()

configuration = ProductionConfig().import_configuration()

scrapper_service = Scrapper(configuration)
scrapper_service.scrape_reserve_data()
