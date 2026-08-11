# Gate Patterns

**Category:** Gate Pattern

## Overview

A gate is an automated check that makes a rule the build's problem instead of a reviewer's. A rule that exists only as prose erodes silently: nobody reverts it, it just stops being true one reasonable-looking change at a time, and the erosion is invisible until something breaks for the reason the rule was written to prevent.

Gates differ from ordinary tests in what they assert. A test asserts that code produces the right result; a gate asserts that a structural rule still holds — that a name stays deleted, that a layer stays ignorant of another, that a substitute still matches what it substitutes for. The failure a gate prevents is not a wrong answer but a decision quietly undone.

## Choosing a Gate

| The rule says | Gate |
|---|---|
| This must not come back | [Absence](absence.md) |
| There must be only one | [Population](population.md), detected by shape |
| This must match that | [Contract](contract.md), on signatures, or delete the substitute |
| This limit applies from now on | [Grandfathered debt](grandfathered_debt.md), with a staleness check |
| This layer must not know that one | [Boundary](boundary.md), plus a vocabulary check |
| The outside world behaves thus | [Live contract](live_contract.md), asserting what you found |
| A write must actually land | [Read-after-write](read_after_write.md) at runtime |

## What Makes a Gate Worth Having

### It must have failed once

A gate written green proves nothing: it may be checking a condition that cannot occur, or checking it incorrectly. Write the gate against the violation, watch it fail, then fix the violation. Gates written this way regularly fail on further violations nobody knew were there.

### The message must say what to do

`assert not offenders` is worthless alone. A message naming the offending file and line, the rule, and the sanctioned alternative is a fix instruction. The person who hits the failure is usually not the person who wrote the gate.

### The docstring carries the cost

Six months on, the assertion says what is checked; only the docstring says why, and why is the only thing that stops someone deleting the gate as an obstacle. Write the failure it prevents in the past tense, with numbers. "382 data files were attached to an assay holding none of them" survives rereading in a way that "ensures correct linking" does not.

### Detect by shape where you can

Names are chosen by people, and people choose differently. A search for `class _Fake` finds the doubles named that way and misses the one called `MockClient`. Structure is harder to evade by accident.

### Separate principle from debt

An exemption because something is genuinely allowed and an exemption because nobody has got to it yet are different things and belong in different lists. One shrinks over time; the other does not. Merged, the whole list becomes noise and stops being maintained.

## Usage Guidelines

**Use when:**

- A rule has already been broken once, and the breach was found late
- The rule is structural and cannot be expressed as a unit test on behaviour
- Enforcement currently depends on reviewers remembering the rule

**Avoid when:**

- The rule is enforced by the language, the packaging, or an existing linter
- The rule is provisional and likely to change before it can erode
- No violation has occurred and none is plausible, so the gate cannot be proven red

## Related Patterns

- [Fixture](../testing/fixture.md) provides the baseline state that gate tests run against
- [Proxy](../structural/proxy.md) and [Decorator](../structural/decorator.md) describe the wrapping used by the read-after-write gate
