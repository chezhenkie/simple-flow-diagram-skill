# Colour vision audit of the nine themes

The nine themes keep every structural signal under protanopia, deuteranopia, tritanopia and achromatopsia. No step, branch or return is named by hue alone: text, position, arrowheads, stroke pattern (solid, dashed, dotted) and stroke width carry the diagram, and the focus card keeps a 2 px border against 1.2 px for the other cards. Contrast survives the simulation with small losses. The lowest text pair is 3.96:1, tokyonight card ink under tritanopia, against 4.5:1 for normal text; the weakest element is the accent in vercel and cursor, 1.59-2.12:1 against the page, which affects the title outline, the focus border and the accent connectors. No colour is changed by this review.

## Method

The tokens are the six values per theme from `THEMES` in `template.html`: page background, card, ink, muted, line and accent. The print palette is black on white and is achromatic by construction.

Simulation uses the Machado, Oliveira and Fernandes (2009) severity 1.0 matrices on linear RGB for protanopia, deuteranopia and tritanopia. Achromatopsia keeps the relative luminance and drops the hue. Normal vision is the identity.

Contrast is the WCAG 2.2 ratio `(L1 + 0.05) / (L2 + 0.05)` on relative luminance. The pairs and floors:

- Text at 4.5:1: ink on page, ink on card, muted on page, muted on card.
- Marks at 3:1: accent on page, accent on card, line on card, line on page.
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

The normal-vision minimum is cursor's muted text at 4.44:1, 0.06 under the floor. Under full-severity simulation the largest loss is 0.79:1 on vercel ink, from 4.99 to 4.20. No text pair falls below 3.9:1.

Github and solarized move by up to 0.14 in either direction; those themes stay above the floor in every case.

## Mark contrast

Normal vision. Card on page is the fill separation, given for context and not held to the 3:1 mark floor.

| Theme | Card on page | Line on card | Accent on page | Accent on card |
|---|---:|---:|---:|---:|
| github | 1.09 | 1.68 | 4.09 | 4.44 |
| harbor | 1.08 | 1.60 | 9.36 | 8.63 |
| solarized | 1.15 | 1.00 | 3.17 | 2.74 |
| oledblack | 1.21 | 1.06 | 14.17 | 11.74 |
| ayu | 1.04 | 3.90 | 10.13 | 9.76 |
| vercel | 1.29 | 12.63 | 1.71 | 2.22 |
| tokyonight | 1.12 | 2.96 | 3.69 | 3.29 |
| cursor | 1.17 | 2.79 | 2.00 | 2.33 |
| orng | 1.22 | 3.29 | 3.55 | 4.34 |

The accent on page moves under simulation: vercel falls to 1.59 (deuteranopia), cursor to 1.83 (protanopia), solarized to 2.39 (protanopia). Every other theme stays at or above 3.09. Achromatopsia leaves these ratios unchanged.

Two themes have a line that equals or nearly equals the card: solarized `line` and `card` are both `#073642`, ratio 1.00, and oledblack is 1.06. Their cards separate by fill at 1.15:1 and 1.21:1. The light themes use a dark line and separate strongly.

The accent marks are thin: a 2 px outline, a 2 px focus border and a 1.6 px connector. Below 3:1 they are faint for every reader, not only for readers with a colour vision deficiency.

## Checked menu row

The checked row is an accent fill with the ink chosen by `inkOn`. Normal vision passes in all nine themes, 4.59-14.17:1. Five theme and simulation cases miss 4.5:1:

| Theme | Simulation | Ink | Ratio |
|---|---|---|---:|
| github | protanopia | white | 4.04 |
| github | tritanopia | white | 3.99 |
| solarized | deuteranopia | white | 4.16 |
| tokyonight | deuteranopia | white | 4.31 |
| orng | deuteranopia | white | 4.00 |

The ink is neutral; the loss comes from the simulated accent luminance. The fill against the menu background is 2.22:1 in vercel, 2.33:1 in cursor and 2.74:1 in solarized, so the row is marked by a light tint as well as by its text.

## Conclusions

1. No information is carried by hue. Every simulated reader keeps the row order, the arrowheads, the dash and dot patterns, the 1.2 and 2 px widths and the labels. A colour vision deficiency cannot remove a step, a split or a return from these pages.
2. Text remains legible under full-severity simulation. The worst pair is 3.96:1, 0.54 under the normal-text floor; the five themes that stay above 4.5 in every simulation are github, harbor, solarized, oledblack and ayu. The affected light themes sit between 3.96 and 4.48.
3. The text shortfall is not specific to colour vision deficiency. Cursor's muted text is 4.44:1 in normal vision, and the simulations move the other themes by at most 0.79.
4. The accent is the weak mark. Vercel and cursor are under 3:1 against the page in normal vision (1.71 and 2.00), and solarized falls to 2.39 under protanopia. The title outline, the focus border and the accent connectors are emphasis; the structure survives without them, and the focus card still reads by width.
5. The checked row keeps its label at 3.99-4.31 in five simulated cases, with a visible fill in all nine themes. The row remains identifiable, at reduced contrast.
6. Solarized's card border does not draw, because its line and card are the same value; the fill separates the card. This is a palette property, unaffected by vision type.
7. The palettes stay as frozen at 1.3.5. If accent visibility is raised later, the lever is luminance in the light themes and in solarized, not hue; the text floors need no change.

## Limits

The matrices model the extreme form, not a particular reader, and anomalous trichromacy is milder. The test computes token ratios, not rendered pixels: anti-aliasing, 1.2 px strokes and 11.5 px side text are harder to read than the ratios suggest. No user test was run. Deuteranopia and protanopia are the common forms; tritanopia and achromatopsia are rare, so their shortfalls weigh less.

## Reproduction

Tokens are in `template.html`: the `:root` block, the dark block and the `THEMES` table. Convert sRGB to linear, apply the matrix, then take the WCAG relative luminance. The three matrices, severity 1.0, linear RGB:

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
