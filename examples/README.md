# Runnable examples

Each script in this directory is a consumer of the `design_patterns` library: it imports a pattern from the library and applies it to a realistic scenario. A test suite gate (`tests/test_examples.py`) checks that no example redefines a library class, that every script listed here exists, that every script is listed, and that every script runs to completion.

## Setup

```bash
uv sync --extra dev
```

## Running an example

```bash
uv run python examples/factory_logger.py
```

## Available examples

| Script | Pattern | Scenario |
|---|---|---|
| `factory_logger.py` | Factory | Creating console, file, and database log writers from a configuration value |
| `strategy_payment.py` | Strategy | Paying a shopping cart with interchangeable payment methods and sorting with interchangeable algorithms |
| `observer_event_system.py` | Observer | Email, analytics, database, and admin components reacting to user events |
| `decorator_middleware.py` | Decorator | Stacking logging, authentication, rate limiting, timing, and CORS middleware around an HTTP handler |
| `facade_order_system.py` | Facade | Placing an order through one call that coordinates inventory, payment, shipping, and notifications |

Each example prints the scenario as it runs and ends with the benefits the pattern provides in that setting.
