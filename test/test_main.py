import pytest
import sys
import logging
from unittest.mock import patch, MagicMock

import main

def test_setup_logging_non_verbose():
    with patch("logging.basicConfig") as mock_basic_config:
        main.setup_logging(False)
        mock_basic_config.assert_called_once_with(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

def test_setup_logging_verbose():
    with patch("logging.basicConfig") as mock_basic_config:
        main.setup_logging(True)
        mock_basic_config.assert_called_once_with(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

def test_run_demo(capsys):
    main.run_demo(difficulty=1)
    captured = capsys.readouterr()
    assert "BLOCKCHAIN LEDGER EXPORT" in captured.out
    assert "BLOCK 0" in captured.out
    assert "BLOCK 1" in captured.out
    assert "BLOCK 2" in captured.out

def test_run_demo_invalid_chain():
    with patch("main.Blockchain.is_chain_valid", return_value=False):
        with patch("logging.Logger.error") as mock_error:
            main.run_demo(difficulty=1)
            mock_error.assert_called_once_with("Validation failed: The blockchain data has been compromised.")

@patch("sys.argv", ["main.py", "--difficulty", "1"])
def test_main_success():
    with patch("main.run_demo") as mock_run_demo:
        with patch("main.setup_logging") as mock_setup_logging:
            main.main()
            mock_setup_logging.assert_called_once_with(False)
            mock_run_demo.assert_called_once_with(1)

@patch("sys.argv", ["main.py", "--difficulty", "1", "--verbose"])
def test_main_verbose():
    with patch("main.run_demo") as mock_run_demo:
        with patch("main.setup_logging") as mock_setup_logging:
            main.main()
            mock_setup_logging.assert_called_once_with(True)
            mock_run_demo.assert_called_once_with(1)

@patch("sys.argv", ["main.py"])
@patch("main.run_demo")
def test_main_keyboard_interrupt(mock_run_demo):
    mock_run_demo.side_effect = KeyboardInterrupt()
    with pytest.raises(SystemExit) as e:
        main.main()
    assert e.value.code == 1
