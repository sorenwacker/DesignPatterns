# Runnable Examples

This directory contains practical, runnable examples demonstrating design patterns in real-world scenarios.

## Setup

First, install the package in editable mode:

```bash
pixi run pip install -e .
```

Or with uv:

```bash
uv pip install -e .
```

## Running Examples

Once installed, run any example directly:

```bash
python examples/factory_logger.py
```

Or with pixi:

```bash
pixi run python examples/factory_logger.py
```

## Available Examples

### Creational Patterns

- **factory_logger.py** - Creating different logger types based on configuration
- **singleton_config.py** - Managing application configuration with Singleton
- **builder_http_request.py** - Building complex HTTP requests with Builder pattern
- **prototype_document.py** - Cloning expensive document objects

### Behavioral Patterns

- **strategy_payment.py** - Implementing multiple payment methods with Strategy
- **observer_event_system.py** - Building an event notification system
- **command_text_editor.py** - Implementing undo/redo with Command pattern
- **state_order_workflow.py** - Managing order states with State pattern

### Structural Patterns

- **decorator_middleware.py** - Stacking middleware with Decorator pattern
- **adapter_legacy_integration.py** - Integrating with legacy systems using Adapter
- **facade_order_system.py** - Simplifying complex order processing with Facade
- **proxy_lazy_loading.py** - Implementing lazy loading with Proxy pattern

## Learning Path

1. Start with simple patterns: Factory, Strategy, Decorator
2. Move to patterns with state: Observer, State, Memento
3. Tackle complex patterns: Visitor, Mediator, Interpreter

Each example includes:
- Real-world scenario description
- Complete working code
- Comments explaining key concepts
- Output showing the pattern in action
