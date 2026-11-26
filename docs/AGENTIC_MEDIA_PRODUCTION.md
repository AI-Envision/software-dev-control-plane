# Agentic media production — reusable capability candidate

Status: research / optional capability, not implemented or a commitment to a new product. 2026-11-26.

## Contract

For an authorized media task, use a bounded pipeline: source inventory and rights register → factual chronology and shot plan → optional spatial reconstruction → render → edit/audio → independent review → export. Preserve original assets separately from generated derivatives. Label scenes as original evidence, attributed recollection, evidence-based reconstruction, or creative interpretation; never present synthetic scenes as documented events.

Candidate adapters: Blender Python/headless rendering, FFmpeg, photogrammetry or Gaussian splatting when adequate evidence exists, optional image generation and composition tooling, licensed sound and narration. Verify current interfaces, licenses and costs before adoption. Use the smallest suitable existing tool; avoid building a generic media platform.

## Governance and quality gates

Follow [governance](GOVERNANCE.md) and [provider routing implementation](https://github.com/AI-Envision/software-dev-control-plane/issues/3). Default paid API budget zero. Private sources remain local unless external processing is explicitly authorized. Protect likeness and voice consent, media rights, credentials and metadata. Do not commit personal assets or private project information. Keep artifact paths, checksums, versions, render settings and source references in a local manifest.

Proposed evaluation: one 60–90 second consented or synthetic example, conventional montage versus spatial reconstruction. Compare factual fidelity, perceived presence (human review), manual effort, rendering time, cost per verified outcome and cost per finished minute. Validate duration, playable export, source provenance and disclosure. Use offline tests and fixtures; avoid paid calls or publication without approval.

When a project actually requires this capability, inspect this contract and existing skills, then scope a minimal pilot with acceptance criteria. Do not add mandatory media dependencies to unrelated projects. No implementation or rendering is claimed by this document.
