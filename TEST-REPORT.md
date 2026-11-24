# Flow diagram skill: test and performance report

## Summary

The test measures the cost of a single diagram page and the cost of adding a second diagram to that page, using the installed 1.5.0 skill and a bare task prompt. The final workflow builds a one-diagram page in 69.3 s with 41,897 context and 369,280 total tokens, averaged over two runs, with both pages passing the validator. Adding a second diagram to the same page costs 64.4 s, 43,185 context and 268,705 total tokens, with the 25 KB shell untouched.

Each gain below was built on the previous workflow, but each row compares a different pair, so the percentages do not add.

| Change | Comparison | Reduction |
|---|---|---|
| Validator out of the payload | new input and wall, paired trial | 40.5% input, 38.1% time |
| Checker script removed | A, final against the old clean A | 46.8% total, 27.2% time |
| Read-only step 7 plus full checklist | pair, against the clean pair | 37.8% total, 19.9% time |
| Second diagram on the same page | against a fresh one-diagram page | 27.2% total, 7.1% time |
| Two-diagram page | against two separate pages | 13.6% total, 3.5% time |

The validator removal is the largest single gain: 40.5% fewer new input and 38.1% less wall time, with the same pass rate. The 1.5.0 no-render workflow and the index shell are part of the baseline; their cost was not isolated in this test.

## Method

The prompt was identical for every run except the destination path:

> Use the simple-flow-diagram-skill to build a DNS lookup flow diagram and save it at <path>. Use Windows browsers only, never WSL.

For the second-diagram case the prompt asked to add a TLS handshake section to an existing page and keep the DNS section. Each case used two agents in separate folders. No prompt asked for a report, a list of checks or a defect hunt. The installed skill was read from the OpenCode skills folder.

Measurements come from the session store. Wall time is idle time minus creation time. Context is the last turn's input plus the cached prefix, the number the agent UI shows. Total tokens is new input plus output plus reasoning plus cache reads across the session; it is a cumulative billing figure, not the context of one turn.

A maintainer ran the page validator after each run:

```sh
python testing-tools/validate.py <page>.html agent-skill/template.html
```

The validator is a maintainer tool outside the skill payload.

## Changes under test

- 1.3.7 moved the page validator out of the skill payload to `testing-tools/validate.py`. The agent no longer reads the 14.6 KB source or runs the tool, and the payload no longer needs Python.
- 1.5.0 removed the per-page browser pass. The shell is checked once in the repository, the written part is checked by reading and the page is opened once for the reader.
- Step 7 now names the check method: read the page against the manual section 12 checklist, and do not write a checker script or run a separate check tool.
- The section 12 checklist was expanded after a comparison with the validator. It now covers page structure, shell parity, line endings, corners, side heights, text indents, budgets, accent classes, loop shape, marker prefixes, assets and storage.

## Validator removal

The validator left the skill payload in 1.3.7. The table below compares the paired runs that read the validator source with the runs that did not. All four pages passed the validator on the first attempt.

| Arm | New input, run 1 | New input, run 2 | Mean new input | Wall s, run 1 | Wall s, run 2 | Mean wall s | Pages |
|---|---:|---:|---:|---:|---:|---:|---|
| With validator read | 55,686 | 54,480 | 55,083 | 275.2 | 267.9 | 271.6 | 2/2 |
| Without | 34,527 | 30,966 | 32,747 | 189.7 | 146.6 | 168.2 | 2/2 |
| Change | | | -22,336 (-40.5%) | | | -103.4 (-38.1%) | same |

The trial used paired runs on the order topic. The mean is the average of the two runs. The gain is in the fixed read and the tool work, not in page quality.

## Step 7 iterations

The clean pair is the 1.5.0 baseline before step 7 changed. In that pair the check method was open: one agent wrote a private checker script and the other read the page. The v1 pair used the read-only step 7. v1 A missed the first arrow and its caption because the checklist had no connector item. The connector item was added for v2, and the full checklist for v3.

| Pair | Step 7 | Wall s | Turns | Context | New input | Total | Pages |
|---|---|---:|---:|---:|---:|---:|---|
| clean | free method, checker allowed | 86.5 | 14.5 | 47,785 | 38,558 | 593,449 | 2/2 |
| v1 | read-only, no connector item | 78.3 | 11.5 | 44,936 | 35,252 | 398,827 | 1/2 |
| v2 | plus connector item | 104.4 | 13 | 47,767 | 38,212 | 498,147 | 2/2 |
| v3 | plus full checklist | 69.3 | 11 | 41,897 | 32,191 | 369,280 | 2/2 |

The v1 A page failed two checks, both the same missing arrow and its caption. The v2 and v3 pages pass. The v3 pair is the final one-diagram result.

## Final one-diagram runs

| Run | Wall s | Turns | Tools | Context | New input | Output | Reasoning | Cache read | Total | Checks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A | 78.4 | 13 | 14 | 42,990 | 33,411 | 4,210 | 9,120 | 410,752 | 457,493 | pass 275 |
| B | 60.2 | 9 | 12 | 40,803 | 30,971 | 2,826 | 7,525 | 239,744 | 281,066 | pass 216 |
| Mean | 69.3 | 11 | 13 | 41,897 | 32,191 | 3,518 | 8,323 | 325,248 | 369,280 | 2/2 |

The A/B spread is 1.30x in wall time. The two pages are different DNS flows and both pass the contract.

## Second diagram on the same page

The base page was a seven-row DNS diagram of 25,163 bytes, validated at 275 checks. Two agents added a TLS 1.3 section to separate copies of that page and kept the DNS section.

| Case | Diagrams | Wall s | Turns | Context | New input | Total | Result |
|---|---:|---:|---:|---:|---:|---:|---|
| Fresh one-diagram page | 1 | 69.3 | 11 | 41,897 | 32,191 | 369,280 | 2/2 pass |
| Add a second diagram | +1 | 64.4 | 8 | 43,185 | 33,282 | 268,705 | 2/2 pass |
| Two-diagram page, total | 2 | 133.7 | 19 | - | 65,473 | 637,985 | 2/2 pass |
| Two separate pages, total | 2 | 138.6 | 22 | - | 64,382 | 738,560 | 4/4 pass |

The added section grows the page to 29,685 and 29,880 bytes, an increase of 4.5 to 4.7 KB. The shell, theme table, bar script and print rules are unchanged.

The add run reads the existing page instead of the template, so its context is 3.1% higher and its new input 3.4% higher than a fresh one-diagram run. The saving is in turns, output and cache reads. The TLS flow is a familiar protocol, so part of the lower turn count is topic familiarity rather than shell reuse. The result supports the file claim: the added diagram writes about 4.6 KB and leaves the 25 KB shell alone. It does not make a second diagram free.

## Checklist scan

The scan compared `testing-tools/validate.py` with manual section 12. It found ten rules that the checklist did not name and three manual ambiguities. All are now in the manual, and the static check count is 360.

| Area | Rule added |
|---|---|
| File endings | LF, not only ASCII |
| Page structure | one main, at least one section, head, note, one SVG, role and aria-label |
| Card geometry | rx 3, side height 70/90/100, side box on a row or 20 lower |
| Text geometry | x+18 or x+16, one title per card, third line at +74 on side cards only |
| Text budgets | 65/28/26, title 24 on every card, caption 42/18, tag 78 |
| Connector classes | `arrow-a` for accents, matching muted and accent markers |
| Loop shape | four segments, upward, 12-character label |
| Marker ids | prefixed by section and defined for every arrowhead |
| Shell and assets | shell parity, two inline scripts, no external assets, URLs or storage |
| Manual ambiguities | split one-branch, 90/100 mid mark, 10 px input and 4 px output stubs |

## Final state

- Skill payload: five files, no executable, no runtime.
- Static checks: 360, zero failures.
- Bar harness: ok.
- Demo validator: 245 checks, zero failures.
- Two-section test pages: 490 checks each, zero failures.
- Tested skill state: commit 94e4f6f, pushed; Pages built at that commit.
- Installed skill: synced with the repository.
- No per-page render pass: the shell is checked in the repository, the written part is read against the checklist and the page is opened once for the reader.
- The test pages were deleted after the figures were recorded. This report is the record.

## Limits

- Two runs per case; the A/B spread remains 1.30x on the final one-diagram pair and 1.10x on the add pair.
- The add case uses a known TLS flow; the lower cost is partly topic familiarity.
- Context and total tokens measure different things; the report keeps them separate.
- The validator remains a maintainer tool; the skill no longer reads or runs it.
- The 360 px bar and the head-script theme application remain separate shell findings. The text contrast shortfalls remain separate from the accepted mark deviations.
