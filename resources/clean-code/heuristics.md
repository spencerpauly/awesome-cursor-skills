# Clean Code — smells & heuristics (Ch. 17 quick reference)

Use ids when reviewing (“G5 duplication”, “F3 flag args”). Fix the smell; don’t argue the label.

## Comments

| Id | Smell |
| --- | --- |
| C1 | Inappropriate information (in VCS/tracker, not source) |
| C2 | Obsolete comment |
| C3 | Redundant comment |
| C4 | Poorly written comment |
| C5 | Commented-out code |

## Environment

| Id | Smell |
| --- | --- |
| E1 | Build requires more than one step |
| E2 | Tests require more than one step |

## Functions

| Id | Smell |
| --- | --- |
| F1 | Too many arguments |
| F2 | Output arguments |
| F3 | Flag arguments |
| F4 | Dead function |

## General

| Id | Smell |
| --- | --- |
| G1 | Multiple languages in one source file |
| G2 | Obvious behavior is unimplemented |
| G3 | Incorrect behavior at the boundaries |
| G4 | Overridden safeties |
| G5 | Duplication |
| G6 | Code at wrong level of abstraction |
| G7 | Base classes depending on their derivatives |
| G8 | Too much information (poor encapsulation) |
| G9 | Dead code |
| G10 | Vertical separation (related code far apart) |
| G11 | Inconsistency |
| G12 | Clutter |
| G13 | Artificial coupling |
| G14 | Feature envy |
| G15 | Selector arguments |
| G16 | Obscured intent |
| G17 | Misplaced responsibility |
| G18 | Inappropriate static |
| G19 | Use explanatory variables |
| G20 | Function names should say what they do |
| G21 | Understand the algorithm |
| G22 | Make logical dependencies physical |
| G23 | Prefer polymorphism to if/else or switch/case |
| G24 | Follow standard conventions |
| G25 | Replace magic numbers with named constants |
| G26 | Be precise |
| G27 | Structure over convention |
| G28 | Encapsulate conditionals |
| G29 | Avoid negative conditionals |
| G30 | Functions should do one thing |
| G31 | Hidden temporal couplings |
| G32 | Don’t be arbitrary |
| G33 | Encapsulate boundary conditions |
| G34 | Functions should descend only one level of abstraction |
| G35 | Keep configurable data at high levels |
| G36 | Avoid transitive navigation (train wrecks) |

## Java-specific (map to your language)

| Id | Smell |
| --- | --- |
| J1 | Avoid long import lists / wildcards where harmful |
| J2 | Don’t inherit constants |
| J3 | Prefer enums (or union types) over loose constants |

## Names

| Id | Smell |
| --- | --- |
| N1 | Choose descriptive names |
| N2 | Names at the appropriate abstraction level |
| N3 | Use standard nomenclature where possible |
| N4 | Unambiguous names |
| N5 | Long names for long scopes |
| N6 | Avoid encodings |
| N7 | Names should describe side effects |

## Tests

| Id | Smell |
| --- | --- |
| T1 | Insufficient tests |
| T2 | Use a coverage tool |
| T3 | Don’t skip trivial tests |
| T4 | Ignored test = unresolved ambiguity |
| T5 | Test boundary conditions |
| T6 | Exhaustively test near bugs |
| T7 | Patterns of failure are revealing |
| T8 | Coverage patterns can be revealing |
| T9 | Tests should be fast |
