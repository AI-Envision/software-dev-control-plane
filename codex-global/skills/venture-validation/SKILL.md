---
name: venture-validation
description: Use for a material commercial product decision, market hypothesis, customer segment, pricing, product positioning, or continue/pivot/stop review. Compare evidence with synthetic consumer scenarios and a minimum real-world test; do not invoke for routine code fixes.
---

# Evidence-gated commercial venture validation

**Trigger:** The user is considering investing in a product, changing target customer/offer/pricing, entering a market, or relying on claimed demand. Do not run this as a standing background service or for unrelated engineering work.

1. **Read current state.** Verify the actual product, current repo/test state, decisions in the project's authorized context, existing customer data, competitor features and primary-source dates. Label SHIPPED, TESTED_LOCAL, PROPOSED and UNKNOWN. Do not copy project/customer details to a public shared repo.
2. **Define controls.** Identify 2–4 specific customer segments and falsifiable value propositions. Include the current do-nothing/manual/general-purpose-AI baseline and at least one material existing competitor where relevant. Decide what would make the user *change the plan*.
3. **Screen cheaply with synthetic scenarios.** Use realistic skeptical personas and free-text responses, randomized presentation, fixed offers and recorded prompts/models/seeds/costs. Treat multiple variations of one persona as dependent simulations. Separately classify objections, evidence gaps and potential willingness to try; no invented testimonials.
4. **Use scientific claims precisely.** Maier et al. (2025; https://arxiv.org/abs/2510.08338) compared 57 personal-care surveys / 9,300 human responses; their SSR method used text + semantic anchor similarity to Likert distributions and reached ~90% of a human survey-consistency benchmark **for that task**. This is not a 90% success or purchase prediction. If no verified semantic-anchor/embedding conversion exists, call the result "qualitative synthetic screening" rather than SSR.
5. **Separate quantities.** Product/offer ranking, rating distributions, real willingness to pay, observed conversion, unit economics, and commercial-success probability are distinct. Never report numeric WTP, expected revenue or "likelihood of success" from uncalibrated model personas. Two agreeing models may share errors. Small apparent score gaps are not a validated winner.
6. **Prioritize human evidence.** Start with founder dogfooding, 3–6 observed external users for feasibility, real payment/choice/action tests, then sufficient segment-specific independent outcomes for calibration. Keep genuine sales, declines, retention, and support costs separate from mock results; precommit continue/pivot/stop thresholds.
7. **Measure economically relevant outcomes.** Time/interruptions removed, mistakes, approval/completion, real payments/sales, acquisition/support and inference costs. Construct scenarios with assumptions and uncertainty ranges only after baseline measurement; update based on held-out real observations.
8. **Persist at the narrowest owner.** Project Notion/issue/decision log for specifics; Git doc for reproducible experiment and evidence ledger; cross-project notes only for transferable method. Date sources and record what was actually run. Seek permission for outreach, paid APIs, private uploads, public publication, deployment and remote pushes.

**Useful sources:** [Original SSR paper](https://arxiv.org/abs/2510.08338) and [Alex Krol's Nov 22 2026 Elsa synthetic example](https://alexeykrol.com/blog/2026/11/22/research/) (12 persona seeds, 96 variants, 1,344 model answers; not observed purchases).

**Existing tools:** Reuse authorized market/consumer/pricing/competitor research plugins or skills if available, but verify their actual callable capabilities. Having an instruction-only plugin does not mean independent agents, SSR scoring, web/API execution, auto-synchronization, or scheduled monitoring occurred. If the tool is absent, a manual preregistered study plan is still useful.
