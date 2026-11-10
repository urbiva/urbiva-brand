# Colour

## Brand palette

| Name | Hex | Notes |
| --- | --- | --- |
| Midnight Violet | `#241B42` | Primary dark surface |
| Volt Lime | `#D5FF66` | Signature accent; 13.9:1 on Midnight Violet |
| Porcelain White | `#F7F5F0` | Primary light surface |
| Digital Iris | `#7966EC` | White on Iris is 4.26:1, below AA for body text: graphics, selection and large text only |
| Muted Lavender | `#B9B1CE` | Secondary text on dark |
| Light Secondary | `#655A7D` | Secondary text on light |

## Semantic tokens

The product uses 35 semantic tokens with Dark and Light values (`tokens/tokens.json`, `tokens/tokens.css`): background, surface, text, border, accent, state, status, route and map groups. Primitives exist only as alias targets.

All 82 text and background token pairs pass WCAG 4.5:1 in both modes (checked at design freeze). Disabled states are exempt by WCAG 1.4.3.

## Change log

- v1.0 (10 Nov 2026): `surface/overlay` Light changed from Midnight Violet to White, because Midnight overlays failed contrast with Light text.
