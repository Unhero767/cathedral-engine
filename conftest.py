def pytest_addoption(parser):
    parser.addoption("--gamma-target", action="store", default="0.5", help="Target resting entropy gamma")
    parser.addoption("--verify-tensor", action="store_true", default=False, help="Enable tensor invariant verification suite")
