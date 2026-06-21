# Design Review Checklist

LinkedIn: https://www.linkedin.com/in/levkantorovich

## Checklist

- Problem framing: Is the task clearly stated, with explicit requirements, non-goals, and boundaries?
- Scope control: Does the proposal avoid widening scope beyond what the task requires?
- Architecture simplicity: Is this the simplest design that can satisfy the requirement?
- Overengineering check: Has the design avoided unnecessary frameworks, services, plugin systems, daemons, or abstraction layers?
- Data model / data structures: Are the main data structures intentional, and are tradeoffs explained where relevant?
- Algorithmic complexity: Are expected time and space complexity stated for non-trivial logic?
- Error handling: Are failure modes clear, with fail-closed behavior where safety matters and reviewable error messages?
- Test strategy: Can core logic be tested deterministically without network, credentials, or external services?
- Dependency strategy: Are dependencies minimized and justified, with preference for the standard library where practical?
- Security/privacy boundaries: Are secrets, credential logging, hidden network calls, public-disclosure risks, and protected-repository dependencies explicitly ruled out or justified?
- Claims/non-claims: Does the design say what it will validate and what it is not claiming?
