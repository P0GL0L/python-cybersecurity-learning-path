from app.main import main

def test_main_help_exit_code_zero(capsys):
    # main() returns 0 by default path
    assert main([]) == 0
