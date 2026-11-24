# Flow diagram skill: context and performance report

## Summary

Nine runs on the current skill, all with a bare task prompt and Windows Firefox: five build one DNS diagram on a page, four build three diagrams on one page. A one-diagram page takes 98.5 s, 9.4 turns and 41,642 end context, with 5 of 5 pages passing the validator. A three-diagram page takes 125.3 s, 11.5 turns and 48,732 end context, 4 of 4 passing. Two extra diagrams add 26.8 s, 2.1 turns and 7,089 context, so end context grows 17 percent while wall time grows 27 percent and a diagram costs 41.8 s instead of 98.5 s.

End context is the figure the agent interface shows in its footer: the input plus the cached prefix of the last request. It stays between 38 and 56k in every run, 4 to 6 percent of a million-token window.

The trials that shaped the workflow, each against its own comparison, so the percentages do not add:

| Change | Reduction |
|---|---|
| Validator out of the skill | 40.5% input, 38.1% time |
| Checker script removed | 46.8% total, 27.2% time |
| Read-only step 7 plus full checklist | 37.8% total, 19.9% time |
| Second diagram on the same page | 27.2% total, 7.1% time |
| Two-diagram page against two pages | 13.6% total, 3.5% time |

## Method

The one-diagram prompt: draw the DNS lookup flow as a simpleflow diagram, save it at the given path, open it once in the running Firefox. The three-diagram prompt names DNS lookup, TLS handshake and HTTP request on one page. No prompt asks for a report, a list of checks or a defect hunt, and no run is touched while it works.

Five agents ran the one-diagram task in separate folders and four ran the three-diagram task, all in parallel. Instructions, model and skill were identical within each set; only the destination path differed. A maintainer ran the validator after each run, since the validator is a tool outside the skill:

```sh
python testing-tools/validate.py <page>.html agent-skill/template.html
```

Wall time is the first request to idle. Turns are assistant messages. End context is the last request's input plus cache read plus cache write.

## One diagram

| Run | Wall s | Turns | End context | Checks |
|---|---:|---:|---:|---|
| f1 | 138.8 | 10 | 46,056 | pass 241 |
| f2 | 82.4 | 9 | 39,528 | pass 259 |
| f3 | 108.9 | 9 | 43,112 | pass 257 |
| f4 | 67.5 | 8 | 38,384 | pass 254 |
| f5 | 95.0 | 11 | 41,133 | pass 241 |
| Mean | 98.5 | 9.4 | 41,642 | 5/5 |

The spread is 2.06x in wall time and 1.20x in end context. f1 is the slow end at 138.8 s with 12,802 reasoning tokens against 4,741 to 9,117 in the others, while its seven tool calls sit at the low end, so the extra time is a long think about the flow and the checklist, not more reading or more edits.

## Three diagrams

| Run | Wall s | Turns | End context | Checks |
|---|---:|---:|---:|---|
| e1 | 106.2 | 11 | 44,773 | pass 576 |
| e2 | 114.2 | 10 | 45,098 | pass 512 |
| e3 | 152.2 | 15 | 56,064 | pass 553 |
| e4 | 128.5 | 10 | 48,993 | pass 586 |
| Mean | 125.3 | 11.5 | 48,732 | 4/4 |

Three diagrams per page lower the cost of a diagram to 41.8 s, against 98.5 s for a page of one, because the manual and template read are paid once. End context rises by only 7,089 tokens, about a fifth, which is the section bodies and captions; the diagram bodies are small beside the 21 KB manual.

The 4 of 4 result follows the merge rule, the three-character budget margin and the one-repair cap. The round before them, on the same task, had four runs with two failures: a merge drawn as two arrows that the validator refused, and side-card lines one character over budget. Both are now contract, and the margin is what a read can see.

## Final state

- Skill: five files, no executable, no runtime, installed copy matching the repository.
- Static checks: 394, zero failures. Toolbar harness: ok. Demo validator: 245, zero failures.
- Nine test pages passed; the run before the merge and margin rules had two failures of four.
- No per-page browser pass. The template is checked in the repository, the written part is read once, the page is opened once.
- The test pages were removed after the figures were recorded; this report is the record.

## Limits

- Five and four runs per case, on one model and one topic, so the means are indicative and the spreads are wide.
- The three-diagram arm has no fresh-page comparison inside this round; the marginal figures come from the two means.
- End context is the last request's prompt, not the sum of every turn; the two are kept apart.
- The validator is a maintainer tool; the skill neither reads nor runs it.
- The 360 px toolbar and the head-script theme application remain open template findings, as do the text contrast shortfalls against the accepted mark deviations.

## One run

The prompt for the page below, with the destination shortened:

```text
Draw the DNS lookup flow as a simpleflow diagram. Save it as dns.html in the workspace. Then open it once as a new tab in the Firefox that is already running. No second browser, no screenshots, no validator, no report. Reply with the file path only.
```

The page the agent wrote is `sample-one-diagram.html`, embedded at the end of this document. It is the f4 run: 67.5 s, 8 turns, 38,384 end context, 254 checks.

