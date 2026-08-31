# Codebase review

Review date: 2026-08-31. Scope: every file under `src/`, `tests/`, `examples/`, and `docs/`, plus the project metadata (`pyproject.toml`, `Makefile`, `mkdocs.yml`, workflows, `README.md`, `CONTRIBUTING.md`). 39 source modules (6,981 lines), 34 test modules (4,360 lines), 5 example scripts (1,207 lines), and 40 documentation pages (3,224 lines) were read in full. Each finding marked "confirmed" was reproduced by running code, not only by reading it.

## Baseline gates

All of the project's own gates pass on the reviewed tree.

| Gate | Command | Result |
|---|---|---|
| Lint and format | `uv run ruff check .` and `ruff format --check .` | Pass |
| Type check | `uv run mypy src examples` | Pass, 44 files |
| Dead code | `uv run vulture` at 60% confidence | Pass |
| Tests | `uv run pytest` | 423 passed |
| Coverage | `--cov=design_patterns`, floor 97% | 97.28% |
| Module length | `tests/test_module_length_gate.py`, cap 1000 lines | Pass, longest module 393 lines |
| Documentation | `uv run mkdocs build --strict` | Pass |
| Lockfile | `uv lock --check` | In sync |

Passing gates say the code does what its tests expect. The findings that follow are about what the tests do not ask.

## Summary

| Severity | Count |
|---|---|
| High | 1 |
| Medium | 10 |
| Low | 14 |

Recurring themes:

- Documentation and metadata describe a project that differs from the one in the tree: a console script that points at a module that does not exist, an examples index listing seven files that are not there, a pattern count that is one too high, and code examples in two places that print the wrong result.
- Builder and Memento carry state across calls in ways their own documentation contradicts.
- The examples directory forks library classes instead of importing them, which the project's own rules prohibit and which nothing gates.
- The catalog mixes two conventions for abstract bases and two conventions for output (return a string versus `print`), and carries dead branches that the vulture gate cannot see because they are reachable by name but not by control flow.

## High

### H1. The declared console script imports a module that does not exist (confirmed)

`pyproject.toml:59` declares `main_script = "design_patterns.main:main"`. There is no `src/design_patterns/main.py`. Installing the package creates a `main_script` executable that fails on first use:

```
uv run main_script
ModuleNotFoundError: No module named 'design_patterns.main'
```

No gate catches this because nothing imports the entry point. Fix: delete the `[project.scripts]` table, or add a `main` module and a smoke test that runs the entry point. The user's release rule ("install the built artifact into a clean environment and smoke-test the entry points") would have caught this; that gate does not exist yet.

## Medium

### M1. `HouseBuilder` director methods carry state from the previous build (confirmed)

`src/design_patterns/creational/builder.py:299-333`. `build_simple_house` sets foundation, walls, roof, windows, and doors, then calls `build()`. It never clears `garage` or `garden`, and `HouseBuilder` has no `reset`. After `build_luxury_house()`, `build_simple_house()` returns a house with `garage=True` and `garden=True`, contradicting both the docstring ("basic features") and `tests/test_builder.py:96-106`, which passes only because it uses a fresh builder. Fix: have each director method start from a new `House`, and add a test that calls the two directors on one builder.

### M2. `build()` hands out the builder's live product (confirmed)

`builder.py:147-153` and `builder.py:291-297`. `build()` returns `self._computer` and keeps the reference, so a setter called after `build()` mutates the object the caller already holds: `c = b.set_cpu("i5").build(); b.set_cpu("i9")` leaves `c.cpu == "i9"`. `ComputerBuilder.reset()` exists but is opt-in; `HouseBuilder` has no reset at all. Fix: `build()` returns the product and replaces the builder's internal instance with a fresh one, which also removes the need for the separate `reset()`.

### M3. `Range` loops forever for a zero or negative step (confirmed)

`src/design_patterns/behavioral/iterator.py:316-333`. `__iter__` uses `while current < self.end`, so `Range(0, 10, -1)` never terminates, and `Range(0, 10, 0)` does not either. `__len__` for the same input returns a value that `__iter__` never produces. Fix: validate `step != 0` in `__init__` and mirror the built-in `range` semantics for negative steps, with tests for both.

### M4. The memento undo example is wrong in the module docstring and the docs page (confirmed)

`src/design_patterns/behavioral/memento.py:10-24` and `docs/patterns/behavioral/memento.md:92-110` both show `write`, `save`, `write`, `save`, `write`, then `undo`, and claim the first undo restores the last saved state. It does not: `History.undo` pops the most recent memento and restores the one before it, so the first undo skips a state. Running the documented steps gives `"Hello "` where the docs print `"Hello World"`. `tests/test_memento.py:45-64` passes only because it adds a third `save` the documentation does not show. A second defect on `memento.py:116-120`: when one memento remains, `undo` restores a hard-coded `Memento("")`, coupling the caretaker to `TextEditor`'s initial state. Fix: decide whether `save` records a checkpoint before or after a change, document that, and make the tests and both examples agree.

### M5. Examples fork library classes instead of importing them

`examples/strategy_payment.py:12-143` redefines `PaymentStrategy`, `CreditCardPayment`, `PayPalPayment`, `CryptocurrencyPayment`, and `ShoppingCart`, all of which exist in `design_patterns.behavioral.strategy`. `examples/observer_event_system.py:13-43` redefines `Observer` and `Subject` from `design_patterns.behavioral.observer`. The project's rule is "never fork library code into an application; a fork silently diverges", and these have already diverged (the example `ShoppingCart` raises on an empty cart; the library one returns a string). Nothing gates this even though the catalog ships a `PopulationGate` built for exactly this check. Fix: import from the library, or apply `PopulationGate` to `examples/` with the library classes as the sanctioned population.

### M6. `examples/README.md` lists seven scripts that do not exist and installs with pixi (confirmed)

`examples/README.md:33-51` names `singleton_config.py`, `builder_http_request.py`, `prototype_document.py`, `command_text_editor.py`, `state_order_workflow.py`, `adapter_legacy_integration.py`, and `proxy_lazy_loading.py`; none is in the tree. Lines 10 and 27-30 give `pixi` commands; the project uses uv. Fix: list the five scripts that exist, use `uv run python examples/<name>.py`, and add a test that every listed file is present.

### M7. `singleton_decorator` returns a function while claiming to return a class (confirmed)

`src/design_patterns/creational/singleton.py:84-111`. The docstring says "Returns: A wrapper class". It returns the closure `get_instance`, so `Logger` becomes a function: `type(Logger).__name__ == "function"` and `isinstance(Logger(), Logger)` raises `TypeError`. The `# type: ignore[return-value]` on line 111 is silencing mypy's report of this exact mismatch. The module docstring (lines 7-10) also promises a "Module-level Singleton (Pythonic approach)" that is not implemented; the third example is a class-attribute singleton. Fix: implement the decorator with `functools.wraps` and a class-based wrapper, or document that the decorated name is a factory function and drop the ignore; correct the module docstring.

### M8. The Factory docs page documents code that is not in the module

`docs/patterns/creational/factory.md` shows an `Animal(ABC)` hierarchy with an abstract `speak`; 14 of the 19 code lines in its Implementation block are absent from `src/design_patterns/creational/factory.py`, which instead imports `Animal`, `Dog`, `Cat` from `design_patterns.structural.inheritance` (`factory.py:10`), where `Animal` is a plain class raising `NotImplementedError`. The creational module also has a cross-category dependency on a structural example module. Fix: give the factory its own product hierarchy and make the docs page show that code.

### M9. The quick reference promises a `Command.undo()` that does not exist

`docs/quick_reference.md:22` says "`cmd.execute()` then `cmd.undo()`". `src/design_patterns/behavioral/command.py` has no `undo`, no receiver, and no state to undo; its commands `print`. `docs/patterns/behavioral/command.md:7` and `:15` also present undo as the pattern's use case. Fix: add a receiver and `undo` to the library command (the `examples/README.md` even advertises a `command_text_editor.py` with undo/redo that was never written), or stop claiming it.

### M10. Pattern counts and Python version are overstated (confirmed)

`README.md:7` says "the 23 Gang of Four design patterns"; the catalog implements 22 (Flyweight is absent, though four docs pages list it under Related Patterns). `docs/index.md:11` says "Structural (7)"; the nav has six structural pages. `README.md:4` shows a "Python 3.10+" badge; `pyproject.toml` requires `>=3.12`. Fix: state 22, or add Flyweight; count six; fix the badge.

## Low

### L1. Dead code the vulture gate cannot see

Vulture reports unused names; these are reachable by name but not by control flow, so they pass the gate while breaking the "remove dead code" rule.

- `if TYPE_CHECKING: pass` blocks with nothing in them: `behavioral/mediator.py:24-27`, `behavioral/state.py:26-29`, `behavioral/visitor.py:27-30`.
- `AirTrafficControl.request_landing` (`mediator.py:176-178`): the `isinstance` check is always true given the annotation, so "Permission denied" is unreachable. `Aircraft.request_landing` (`mediator.py:219-221`): every `Aircraft` is constructed with an `AirTrafficControl`, so "No ATC available" is unreachable.
- `CSVDataMiner.send_report` (`template_method.py:166-171`) overrides the base hook with an identical empty body.
- `SmartDevice.trigger_event` (`mediator.py:297-303`) only calls `self.send`.
- `chain_of_responsibility.py:105`: a trailing comment pointing at the docstring.
- `pyproject.toml:48-49`: `[tool.hatch.build.hooks.vcs] version-file = "_version.py"` writes a root-level `_version.py` (gitignored) that nothing imports; `__init__.py` reads the version through `importlib.metadata` instead.

### L2. Two conventions for abstract bases

`adapter.py:31-51`, `composite.py:24-34`, `inheritance.py:36-43`, and `interpreter.py:1-19` mark abstract methods by raising `NotImplementedError` on a plain class; the other 30 modules use `abc.ABC` and `@abstractmethod`. The `NotImplementedError` style lets `Animal("x")` and `Shape()` be instantiated, which `tests/test_inheritance.py:44-50` then tests as a feature. `interpreter.py` also has no module docstring, no `__init__` docstrings, and an `if __name__ == "__main__"` block inside a library module (`interpreter.py:57-62`, also `composition.py:56-58`). `composite.py:54-56` leaves `__init__` and `self.shapes` unannotated; `composite.py:40,47` and `inheritance.py:49,56` have no method docstrings.

### L3. Two conventions for output

`behavioral/command.py:37,45` and `structural/adapter.py:67` `print` their result; every other module returns a string. The tests for these two modules depend on `capsys`. Returning strings would make them consistent and testable without capturing stdout.

### L4. Function-local imports

`behavioral/visitor.py:170`, `:212`, `:238` each `import math` inside a method. Move to module level.

### L5. Naming that overstates what the code does

`structural/decorator.py:272-292`: `_encrypt` and `_decrypt` reverse a string, and `EncryptionDecorator` is documented as adding encryption. The user's rule is that names reflect what they implement. `decorator.py:336` slices with the magic number 12 instead of `len("[COMPRESSED]")`.

### L6. Substring ban list (confirmed)

`structural/proxy.py:165-167`: `if banned in url` blocks `https://unbanned.com` because it contains `banned.com`. `tests/test_proxy.py:167-175` documents the substring behaviour as intended, so this is a design choice to revisit rather than a regression.

### L7. Builder aliases the caller's list

`testing/fixture.py:202-212`: `with_items` stores the list it is given, so the built `Order` shares it with the caller and with any later `build()` from the same builder. Copy on the way in or on `build()`.

### L8. Skip reason names variables the gate never reads

`gates/live_contract.py:91-98`: `skip_reason` hard-codes `CONTRACT_URL` and `CONTRACT_TOKEN`, but the gate receives `url` and `token` as plain arguments and never reads the environment. A caller using other variable names gets a wrong instruction. Accept the variable names as constructor arguments.

### L9. Leftovers from the template and the pixi era

`pyproject.toml:146` has an empty `[tool.pixi.tasks]` table; `.gitattributes:2` refers to a `pixi.lock` that does not exist; `.copier-answers.yml` records `environment_manager: pixi` and `typing: no_typing` while the project uses uv and gates with mypy. `README.md:60-75` tells contributors to run `pytest` and `mkdocs serve` directly and to install with `uv pip install -e .`, while `CONTRIBUTING.md` and the `Makefile` say `uv sync --extra dev` and `make check`. `mkdocs.yml:3` sets `site_author: Design Patterns Library`.

### L10. Test hygiene

- `tests/test_singleton.py`: all three singletons are process-global and no fixture resets them, so every test observes the others' state. The suite passes in its current order.
- `tests/test_memento.py:76-91`: `test_history_multiple_undos` rebinds `editor` to a new `TextEditor` on every loop iteration, so the mementos come from three different editors; the test passes by accident of the last binding.
- `tests/test_facade.py:134-141`: `test_facade_simplifies_interface` asserts only a list length and carries the rest of its claim in comments.
- `tests/test_observer.py` asserts on `_observers` and `_temperature` privates rather than through `display()`.

### L11. Examples are not tested

The five scripts under `examples/` are gated by mypy only. `CONTRIBUTING.md` says pytest ensures "every pattern has passing tests"; the examples are excluded from coverage (`run.source = ["design_patterns"]`) and have no tests. The user's rule is that a feature is done when covered by tests. A parametrized test that runs each `main()` under `capsys` and asserts on a line of output would cover them cheaply.

### L12. Cosmetic drift between docs code blocks and modules

Twenty pattern pages contain at least one code line that is not in the module they document. Most differences are typing style (`Optional[...]` and `List[...]` in the docs, `X | None` and `list[...]` in the code: `chain_of_responsibility.md`, `command.md`, `proxy.md`, `fixture.md`). Two are structural: `composite.md` shows a `remove()` method the module does not have, and `iterator.md` shows `BookIterator` and `BookCollection` without the `Iterator` and `Aggregate` bases the module gives them. The API Reference block on each page pulls the real code, so readers see two versions.

### L13. Unused import in a docs snippet

`docs/practical_examples.md:10` imports `AnimalFactory` in a snippet that never uses it.

### L14. `docs/dataclasses.md` does not follow the pattern-page template

Added on 2026-08-31 as a Reference page. It has "Usage Guidelines", "Implementation", and "Pitfalls" but not the seven-section structure `CONTRIBUTING.md` prescribes, and no API Reference block for `design_patterns.structural.value_object`. Reference pages are not pattern pages, so this may be intended; noted for consistency.

## Remediation checklist

Grouped by theme so each item is one atomic change with its own gate.

1. Packaging and metadata: remove or implement the `main_script` entry point (H1); add a clean-install smoke test as a release gate; drop the hatch `version-file` hook, the pixi table, and the `pixi.lock` gitattribute (L1, L9); fix the README badge, pattern count, and dev instructions (M10, L9); fix `docs/index.md` counts (M10).
2. Builder semantics: make `build()` hand over the product and start fresh; make director methods independent of prior calls; add tests that reuse one builder (M1, M2).
3. Iterator and Memento correctness: validate `Range.step` and support negative steps (M3); settle the `History.undo` semantics and make the module docstring, the docs page, and the tests agree; remove the hard-coded `Memento("")` (M4).
4. Examples: import library classes instead of redefining them, or gate `examples/` with `PopulationGate` (M5); rewrite `examples/README.md` to list real files with uv commands and gate the list (M6); add a smoke test per example (L11).
5. Documentation accuracy: make `factory.md` show the real factory code and give the factory its own products (M8); remove or implement `Command.undo` (M9); modernise the typing in doc snippets and drop `composite.md`'s `remove()` (L12); remove the unused import (L13).
6. Consistency sweep: choose `ABC` everywhere (L2); return strings instead of printing (L3); move `import math` to module level (L4); rename `_encrypt`/`_decrypt` or implement a real cipher, and name the prefix length (L5); delete the dead branches and empty `TYPE_CHECKING` blocks (L1); fix `singleton_decorator`'s return type and the module docstring (M7).
7. Test hygiene: add a reset fixture for the singletons; fix `test_history_multiple_undos`; assert through public methods in `test_observer.py` (L10).
8. Design choices to confirm rather than fix: substring matching in `ProxyInternet` (L6); list aliasing in `OrderBuilder` (L7); environment variable names in `LiveContractGate.skip_reason` (L8); template structure for `docs/dataclasses.md` (L14).
