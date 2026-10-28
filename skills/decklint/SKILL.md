---
name: decklint
description: After writing or editing any .pptx, run decklint as a quality gate before delivering. Use for slide QA, presentation review, Duarte/Zen rule checks.
---

# decklint skill

You generate or edit PowerPoint. **Done means the verifier passes**, not that you think it looks fine.

## When

- After creating a `.pptx`
- After applying design changes
- Before sending a file to the user

## How

```bash
decklint check PATH.pptx --preset stage|reading|keynote
```

- Live talk → `stage` or `keynote`
- Email / async document → `reading`
- Fix every `error`. Treat `warning` as should-fix unless the user waived it.
- Re-run until exit code 0 (or only waived warnings remain).

## Do not

- Skip the check because “the generator is good”
- Lower the preset to silence errors without asking the user
