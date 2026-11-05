# Optional specialist writer prototype

The private core remains the interpretation authority. The report generator
works without a writer, API key, provider connection or additional SDK.
No production report path or HTTP endpoint invokes this prototype.

## Authority and output contract

`mystic_rebels/report_writer.py` defines a replaceable Writer protocol. The
core-packet factory obtains the integrity-verified release, recomputes composition
from the trusted server chart, and validates it against the original chart,
question and owner. Candidate packets and caller-set approval flags are not
accepted as substitutes. Core sentences, exceptions, missing dependencies and
the incomplete-reading qualification remain authoritative. Core packets are
ineligible for external transmission in this prototype.

Arbitrary paraphrases cannot be mechanically certified with a keyword filter,
claim-ID citation or another language model. The safe initial contract therefore
lets the specialist select approved wording variants and reorder claims within
fixed sections. Every claim, including qualifications, must appear exactly once.
Only integer variant indexes are accepted; extra prose/keys, fabricated claims,
omissions and invalid selections are rejected. Rendering expands approved server
text, never raw model prose. Failure or timeout returns the canonical deterministic
template. Source correctness remains separate from writing style.

The only egress-eligible packets are three exact, immutable invented calibration
fixtures. They contain no astrology, birth records, names, locations, book text,
private rules, source locators or proprietary core output. Both the orchestrator
and direct provider transport enforce that allowlist. Changing a flag or adding
private text does not authorize a request. The API key goes only in the HTTPS
authorization header, never a prompt, browser bundle, output or repository file.
The transport requires no-data-collection, ZDR and supported-parameter routing;
those settings are not silently relaxed to get a response.

## Prototype benchmark

Use `python scripts/benchmark_report_writer.py` for the offline baseline.
Live runs require `--live` and either server-only NADIA_WRITER_API_KEY or
`--key-stdin` (non-echoing console input). Models are replaceable via `--models`.
Requests are limited to384output tokens and20seconds. No alternative model is
silently substituted after a failure. Provider exceptions are reduced to a safe
fallback reason; raw errors, credentials and provider bodies are not logged.

Saved receipt: `evidence/profile-report/writer-benchmark.json`. Twelve small
requests were made across two runs; all were invented calibration cases.
DeepSeek's verified model identifier was
`deepseek/deepseek-v4.1-flash-1017`:3/3selections passed the output contract,
with latency1.33–3.05seconds. Reported aggregate usage cost was0.000316924USD;
this is API-reported usage, not an independently audited billing statement.
Two of three accepted outputs differed from the canonical template by approved
wording/order selection. Unapproved rendered sentences remained zero by contract.

OpenAI gpt-4.1-mini and Gemini2.5Flash comparison requests did not produce usable
responses under the same settings (diagnostic rerun HTTP400/404). Every case
rendered the deterministic fallback. This is not evidence that their writing
quality is worse. Human evaluation of clarity, flow and emotional resonance is
still pending; a three-case constrained calibration is not a full-report quality
benchmark. No recommendation to enable production generation follows from it.

## Next gate before a real writer trial

The core must approve every interpretation claim and any alternative wording
before egress. A separately reviewed minimal projection must exclude personal
information, source materials and proprietary methodology; current core packets
remain blocked. Once suitable approved/public calibration wording exists, compare
templates and specialists on realistic synthetic report lengths, source fidelity,
coverage, readability, latency, failure rate and cost. Do not enable free prose,
personal-data transmission or full-reading approval through an environment flag.

This work changes no methodology, private release, consumer pin, deployment
protection, paid-reading readiness or production application configuration.
