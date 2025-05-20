import io
import logging
import pytest
from lamd.log import Logger


@pytest.fixture
def test_logger():
    """Create a test logger instance with a StringIO handler at DEBUG level."""
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(asctime)s:%(message)s"))
    handler.setLevel(logging.DEBUG)

    logger = Logger(name="test_logger", level=logging.DEBUG)
    logger.logger.setLevel(logging.DEBUG)
    logger.logger.handlers = [handler]
    logger.log_stream = log_stream
    return logger


def test_logger_initialization(test_logger):
    """Test that Logger can be initialized with custom parameters."""
    assert test_logger.name == "test_logger"
    assert test_logger.level == logging.DEBUG
    assert test_logger.logger is not None


def test_logger_debug(test_logger):
    """Test debug logging."""
    test_logger.debug("Test debug message")
    log_content = test_logger.log_stream.getvalue()
    assert "DEBUG" in log_content
    assert "Test debug message" in log_content


def test_logger_info(test_logger):
    """Test info logging."""
    test_logger.info("Test info message")
    log_content = test_logger.log_stream.getvalue()
    assert "INFO" in log_content
    assert "Test info message" in log_content


def test_logger_warning(test_logger):
    """Test warning logging."""
    test_logger.warning("Test warning message")
    log_content = test_logger.log_stream.getvalue()
    assert "WARNING" in log_content
    assert "Test warning message" in log_content


def test_logger_error(test_logger):
    """Test error logging."""
    test_logger.error("Test error message")
    log_content = test_logger.log_stream.getvalue()
    assert "ERROR" in log_content
    assert "Test error message" in log_content


def test_logger_critical(test_logger):
    """Test critical logging."""
    test_logger.critical("Test critical message")
    log_content = test_logger.log_stream.getvalue()
    assert "CRITICAL" in log_content
    assert "Test critical message" in log_content
