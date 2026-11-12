# Tests

    tests/
    ├── conftest.py        # shared fixtures
    ├── unit/              # fast, no network
    ├── integration/       # multiple components together
    ├── external_api/      # real API smoke tests (marked `external`)
    ├── fixtures/          # saved sample responses / data
    └── helpers/           # shared test utilities

## Run

    pytest                      # everything
    pytest -m "not external"    # offline only
    pytest -m external          # only real API tests
    pytest tests/unit           # one folder

API keys go in `.env` (see `.env.example`). Tests skip if a key is missing.
