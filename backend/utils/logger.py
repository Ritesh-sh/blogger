"""
Logging utility for the application.
Provides colored console logging with proper formatting.
"""
import logging
import colorlog


def setup_logger(name):
    """
    Set up a colored logger with the given name.
    
    Args:
        name (str): Name of the logger (usually __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create console handler with colored output
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # Create colored formatter
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger
