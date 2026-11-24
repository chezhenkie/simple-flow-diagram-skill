# Flow diagram skill: context and performance report

## Summary

Nine runs on the current skill, all with a bare task prompt and Windows Firefox: five build one DNS diagram on a page, four build three diagrams on one page. A one-diagram page takes 98.5 s, 9.4 turns, 41,642 end context and 309,065 total tokens, with 5 of 5 pages passing the validator. A three-diagram page takes 125.3 s, 11.5 turns, 48,732 end context and 434,066 total, 4 of 4 passing. Two extra diagrams add 26.8 s, 2.1 turns, 7,089 context and 124,992 total tokens, so end context grows 17 percent while wall time grows 27 percent and cost per diagram drops from 309k to 145k.

End context is the figure the agent interface shows in its footer: the input plus the cached prefix of the last request. It stays between 38 and 56k in every run, 4 to 6 percent of a million-token window. Total tokens is the cumulative billing figure and runs six to eight times larger, so the two are never compared as one number.

Earlier trials, kept as the record of how the workspace got here:

| Change | Comparison | Reduction |
|---|---|---|
| Validator out of the skill | new input and wall, paired trial | 40.5% input, 38.1% time |
| Checker script removed | A, final against the old clean A | 46.8% total, 27.2% time |
| Read-only step 7 plus full checklist | pair, against the clean pair | 37.8% total, 19.9% time |
| Second diagram on the same page | against a fresh one-diagram page | 27.2% total, 7.1% time |
| Two-diagram page | against two separate pages | 13.6% total, 3.5% time |

Each row compares a different pair, so the percentages do not add.

## Method

The one-diagram prompt: draw the DNS lookup flow as a simpleflow diagram, save it at the given path, open it once in the running Firefox. The three-diagram prompt names DNS lookup, TLS handshake and HTTP request on one page. No prompt asks for a report, a list of checks or a defect hunt, and no run is touched while it works.

Five agents ran the one-diagram task in separate folders and four ran the three-diagram task, all in parallel. Instructions, model and skill were identical within each set; only the destination path differed. A maintainer ran the validator after each run, since the validator is a tool outside the skill:

```sh
python testing-tools/validate.py <page>.html agent-skill/template.html
```

Wall time is the first request to idle. Turns are assistant messages. End context is the last request's input plus cache read plus cache write. Total is input, cache read, output and reasoning added over the session.

## One diagram

| Run | Wall s | Turns | End context | Total | Checks |
|---|---:|---:|---:|---:|---|
| f1 | 138.8 | 10 | 46,056 | 365,669 | pass 241 |
| f2 | 82.4 | 9 | 39,528 | 278,831 | pass 259 |
| f3 | 108.9 | 9 | 43,112 | 303,068 | pass 257 |
| f4 | 67.5 | 8 | 38,384 | 237,611 | pass 254 |
| f5 | 95.0 | 11 | 41,133 | 360,145 | pass 241 |
| Mean | 98.5 | 9.4 | 41,642 | 309,065 | 5/5 |

The spread is 2.06x in wall time and 1.20x in end context. f1 is the slow end at 138.8 s with 12,802 reasoning tokens against 4,741 to 9,117 in the others, while its seven tool calls sit at the low end, so the extra time is a long think about the flow and the checklist, not more reading or more edits.

## Three diagrams

| Run | Wall s | Turns | End context | Total | Checks |
|---|---:|---:|---:|---:|---|
| e1 | 106.2 | 11 | 44,773 | 384,129 | pass 576 |
| e2 | 114.2 | 10 | 45,098 | 337,723 | pass 512 |
| e3 | 152.2 | 15 | 56,064 | 635,956 | pass 553 |
| e4 | 128.5 | 10 | 48,993 | 378,456 | pass 586 |
| Mean | 125.3 | 11.5 | 48,732 | 434,066 | 4/4 |

Three diagrams per page lower the cost of a diagram to 108.6k total and 41.8 s, against 309.1k and 98.5 s for a page of one, because the manual and template read are paid once. End context rises by only 7,089 tokens, about a fifth, which is the section bodies and captions; the diagram bodies are small beside the 21 KB manual.

The 4 of 4 result follows the merge rule, the three-character budget margin and the one-repair cap. The round before them, on the same task, had four runs with two failures: a merge drawn as two arrows that the validator refused, and side-card lines one character over budget. Both are now contract, and the margin is what a read can see.

## Earlier trials

The validator left the skill in 1.3.7. The paired trial below read the validator source in one arm and not the other; all four pages passed on the first attempt.

| Arm | Mean new input | Mean wall s | Pages |
|---|---:|---:|---|
| With validator read | 55,083 | 271.6 | 2/2 |
| Without | 32,747 | 168.2 | 2/2 |
| Change | -40.5% | -38.1% | same |

The step 7 pairs, from the 1.5.0 baseline onward. The check method was open in the clean pair, read-only in v1, and grew the connector item and the full checklist for v2 and v3. v1 A missed the first arrow and its caption, which exposed the gap.

| Pair | Step 7 | Wall s | Turns | End context | Total | Pages |
|---|---|---:|---:|---:|---:|---|
| clean | free method | 86.5 | 14.5 | 47,785 | 593,449 | 2/2 |
| v1 | read-only | 78.3 | 11.5 | 44,936 | 398,827 | 1/2 |
| v2 | plus connectors | 104.4 | 13 | 47,767 | 498,147 | 2/2 |
| v3 | plus full checklist | 69.3 | 11 | 41,897 | 369,280 | 2/2 |

## Second diagram on the same page

A 1.5.0 record. Two agents added a TLS 1.3 section to separate copies of a seven-row DNS page and kept the DNS section.

| Case | Wall s | Turns | End context | Total | Result |
|---|---:|---:|---:|---:|---|
| Fresh one-diagram page | 69.3 | 11 | 41,897 | 369,280 | 2/2 |
| Add a second diagram | +64.4 | 8 | 43,185 | 268,705 | 2/2 |
| Two-diagram page | 133.7 | 19 | - | 637,985 | 2/2 |
| Two separate pages | 138.6 | 22 | - | 738,560 | 4/4 |

The added section grows the page by 4.5 to 4.7 KB and leaves the 25 KB template alone. Adding a diagram to a finished page costs 64.4 s, mostly the page read and a fresh look at the checklist; planning three at once, as the current rounds do, costs 13.4 s per extra diagram. The difference is that the three-diagram agent never re-reads a page it just wrote.

## Checklist scan

The scan compared `testing-tools/validate.py` with manual section 12 and found ten unnamed rules and three ambiguities. All are in the manual now, and the rule set has since gained the merge pair, the budget margin, the command ban, the two-edit order and the repair cap.

## Final state

- Skill: five files, no executable, no runtime, installed copy matching the repository.
- Static checks: 394, zero failures. Toolbar harness: ok. Demo validator: 245, zero failures.
- Nine test pages passed; the run before the merge and margin rules had two failures of four.
- No per-page browser pass. The template is checked in the repository, the written part is read once, the page is opened once.
- Test pages are kept in `test-runs/` until the user asks for their removal.

## Limits

- Five and four runs per case, on one model and one topic, so the means are indicative and the spreads are wide.
- The three-diagram arm has no fresh-page comparison inside this round; the marginal figures come from the two means.
- Context and total measure different things and are kept apart in every table.
- The validator is a maintainer tool; the skill neither reads nor runs it.
- The 360 px toolbar and the head-script theme application remain open template findings, as do the text contrast shortfalls against the accepted mark deviations.
