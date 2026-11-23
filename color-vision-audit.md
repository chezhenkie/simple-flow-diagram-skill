# Colour vision audit of the nine themes

The nine themes keep every structural signal under protanopia, deuteranopia, tritanopia and achromatopsia. No step, branch or return is named by hue alone: text, position, arrowheads, stroke pattern (solid, dashed, dotted) and stroke width carry the diagram, and the focus card keeps a 2 px border against 1.2 px for the other cards. The lowest text pair is 3.96:1, tokyonight card ink under tritanopia, against 4.5:1 for normal text. The line marks clear 3:1 in every theme; four accent and label cases remain under a floor in deuteranopia and are accepted deviations. The palettes are fixed at 1.4.0.

## Method

The tokens are the six values per theme from `THEMES` in `template.html`: page background, card, ink, muted, line and accent. The print palette is black on white and is achromatic by construction.

Simulation uses the Machado, Oliveira and Fernandes (2009) severity 1.0 matrices on linear RGB for protanopia, deuteranopia and tritanopia. The matrix output is clamped to the range 0 to 1 before the luminance is taken; without the clamp the ratios move by up to 0.59. Achromatopsia keeps the relative luminance and drops the hue. Normal vision is the identity.

Contrast is the WCAG 2.2 ratio `(L1 + 0.05) / (L2 + 0.05)` on relative luminance. The pairs and floors:

- Text at 4.5:1: ink on page, ink on card, muted on page, muted on card.
- Marks at 3:1: accent on page, accent on card, line on card (the card border) and line on page (the bar borders and the footer divider).
- Menu label at 4.5:1: the checked row's ink on the accent, using the page's own `inkOn` rule.

The accent carries emphasis, not meaning. The focus card is also 2 px wide against 1.2 px, and the checked menu row keeps `aria-checked` for assistive technology.

## Text contrast

Lowest of the four text pairs, per theme and simulation. The pair is the same in all five columns unless named.

| Theme | Normal | Protanopia | Deuteranopia | Tritanopia | Achromatopsia |
|---|---:|---:|---:|---:|---:|
| github | 6.15 | 6.22 | 6.11 | 6.16 | 6.15 |
| harbor | 5.65 | 5.65 | 5.65 | 5.65 | 5.65 |
| solarized | 5.03 | 4.92 | 5.11 | 4.89 | 5.03 |
| oledblack | 7.32 | 7.32 | 7.32 | 7.32 | 7.32 |
| ayu | 9.38 | 10.32 | 8.77 | 9.88 | 9.38 |
| vercel | 4.99 | 6.97 | 4.20 | 4.56 | 4.99 |
| tokyonight | 4.58 | 3.99 | 4.70 | 3.96 | 4.58 |
| cursor | 4.44 | 4.34 | 4.51 | 4.44 | 4.44 |
| orng | 4.91 | 6.21 | 4.32 | 4.95 | 4.91 |

Pairs under 4.5:1, by theme and simulation:

| Theme | Simulation | Pair | Ratio |
|---|---|---|---:|
| vercel | deuteranopia | ink on page | 4.20 |
| tokyonight | protanopia | ink on card | 3.99 |
| tokyonight | protanopia | ink on page | 4.48 |
| tokyonight | tritanopia | ink on card | 3.96 |
| tokyonight | tritanopia | ink on page | 4.45 |
| cursor | normal, protanopia, tritanopia, achromatopsia | muted on page | 4.34-4.44 |
| orng | deuteranopia | ink on page | 4.32 |

The normal-vision minimum is cursor's muted text at 4.44:1, 0.06 under the floor. Among the lowest pairs the largest loss is 0.79:1 on vercel ink on page, from 4.99 to 4.20. Across all four pairs the largest loss is 1.01:1, vercel ink on card from 6.45 to 5.44 under deuteranopia. No text pair falls below 3.9:1.

Github and solarized move by up to 0.14 on their minima and up to 0.19 on any pair; those themes stay above the floor in every case.

## Mark contrast

Normal vision. Card on page is the fill separation, given for context and not held to the 3:1 mark floor. Line on card is the 1.2 px card border; line on page draws the bar borders and the footer divider.

| Theme | Card on page | Line on card | Line on page | Accent on page | Accent on card |
|---|---:|---:|---:|---:|---:|
| github | 1.09 | 4.47 | 4.12 | 5.15 | 5.58 |
| harbor | 1.08 | 3.40 | 3.68 | 9.36 | 8.63 |
| solarized | 1.15 | 4.86 | 5.61 | 4.50 | 3.89 |
| oledblack | 1.21 | 3.41 | 4.12 | 14.17 | 11.74 |
| ayu | 1.04 | 3.90 | 4.05 | 10.13 | 9.76 |
| vercel | 1.29 | 12.63 | 9.77 | 3.13 | 4.05 |
| tokyonight | 1.12 | 3.33 | 3.74 | 3.69 | 3.29 |
| cursor | 1.17 | 3.96 | 3.39 | 4.34 | 5.05 |
| orng | 1.22 | 4.40 | 3.60 | 3.55 | 4.34 |

The accent on page moves under simulation: vercel falls to 2.91 (deuteranopia), tokyonight to 3.33 (deuteranopia), solarized to 3.55 (protanopia) and cursor to 4.07 (protanopia). Vercel's 2.91 is the only accent on page under 3:1 and is an accepted deviation; every other theme stays at or above 3.09. Achromatopsia leaves these ratios unchanged.

Every line clears 3:1 on card and on page in all simulations. The lowest are tokyonight 3.29 on card, cursor 3.31 on page, orng 3.33 on page, harbor 3.40 on card and oledblack 3.41 on card. Solarized's line is now `#93A1A1`, so its card border draws; the fill separation remains 1.15:1.

The accent marks are thin: a 2 px outline, a 2 px focus border and a 1.6 px connector. Below 3:1 they are faint for every reader, not only for readers with a colour vision deficiency.

## Checked menu row

The checked row is an accent fill with the ink chosen by `inkOn`. Normal vision passes in all nine themes, 4.59-14.17:1. Two theme and simulation cases miss 4.5:1:

| Theme | Simulation | Ink | Ratio |
|---|---|---|---:|
| tokyonight | deuteranopia | white | 4.31 |
| orng | deuteranopia | white | 4.00 |

The ink is neutral; the loss comes from the simulated accent luminance. The fill against the menu background is 3.13:1 in vercel, 4.34:1 in cursor and 4.50:1 in solarized, so the row is marked by a tint as well as by its text.

## Accepted deviations

The 1.4.0 palette pass raised the weak line and accent values. Four mark pairs remain under a floor in one simulation:

| Theme | Mark | Worst | Floor | Simulation |
|---|---|---:|---:|---|
| vercel | accent on page | 2.91 | 3 | deuteranopia |
| tokyonight | accent on card | 2.97 | 3 | deuteranopia |
| tokyonight | checked label | 4.31 | 4.5 | deuteranopia |
| orng | checked label | 4.00 | 4.5 | deuteranopia |

These are accepted. The shortfalls are small and affect emphasis and a menu label, not the diagram structure: the focus card still reads by 2 px width, the line marks clear the floor, and the labels are text. Solarized and vercel accents sit between their original and fully passing values; tokyonight and orng accents are unchanged. Github accent and line, harbor line, solarized accent and line, oledblack line, vercel accent, tokyonight line, cursor accent and line, and orng line changed in the pass. The palettes are otherwise fixed at 1.4.0.

## Conclusions

1. No information is carried by hue. Every simulated reader keeps the row order, the arrowheads, the dash and dot patterns, the 1.2 and 2 px widths and the labels. A colour vision deficiency cannot remove a step, a split or a return from these pages.
2. Text remains legible under full-severity simulation. The worst pair is 3.96:1, 0.54 under the normal-text floor; the five themes that stay above 4.5 in every simulation are github, harbor, solarized, oledblack and ayu. The affected light themes sit between 3.96 and 4.48.
3. The text shortfall is not specific to colour vision deficiency. Cursor's muted text is 4.44:1 in normal vision; the simulations move the other themes' minima by at most 0.79 and any text pair by at most 1.01.
4. The accent is the weakest emphasis mark. Vercel's accent on page is 2.91 under deuteranopia and tokyonight's accent on card is 2.97; both are accepted deviations. The title outline, the focus border and the accent connectors are emphasis; the structure survives without them, and the focus card still reads by width.
5. The checked row keeps its label at 4.00-4.31 in two simulated cases, both accepted deviations. The row remains identifiable, at reduced contrast.
6. Every line clears 3:1 in all simulations. The palette pass raised the weak borders; solarized's line is `#93A1A1` and its card border draws. No line shortfall is accepted.
7. The palettes are fixed at 1.4.0. The accepted deviations are listed above; no further colour change is proposed.

## Limits

The matrices model the extreme form, not a particular reader, and anomalous trichromacy is milder. The test computes token ratios, not rendered pixels: anti-aliasing, 1.2 px strokes and 11.5 px side text are harder to read than the ratios suggest. No user test was run. Deuteranopia and protanopia are the common forms; tritanopia and achromatopsia are rare, so their shortfalls weigh less.

## Reproduction

Tokens are in `template.html`: the `:root` block, the dark block and the `THEMES` table. Convert sRGB to linear, apply the matrix, clamp each channel to the range 0 to 1, then take the WCAG relative luminance. The three matrices, severity 1.0, linear RGB:

```
protanopia     0.152286  1.052583 -0.204868
               0.114503  0.786281  0.099216
              -0.003882 -0.048116  1.051998

deuteranopia   0.367322  0.860646 -0.227968
               0.280085  0.672501  0.047413
              -0.011820  0.042940  0.968881

tritanopia     1.255528 -0.076749 -0.178779
              -0.078411  0.930809  0.147602
               0.004733  0.691367  0.303900
```
