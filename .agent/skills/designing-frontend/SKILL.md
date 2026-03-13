---
name: designing-frontend
description: Generates frontend components and layouts adhering to the Delphi brand guidelines. Use when the user requests UI designs, new pages, or component implementations.
---

# Frontend Design Generator (Delphi Brand)

## When to use this skill
- When creating new React components.
- When styling pages with Tailwind CSS.
- When the user asks for "Delphi" branded UI.
- When specific brand colors or typography need to be applied.

## Brand Source of Truth
These guidelines define color codes, spacing, and typography pairings.
[brand_guidelines.json](resources/brand_guidelines.json)

## Design Tokens (Quick Reference)
| Token | Value | Notes |
| :--- | :--- | :--- |
| **Primary Color** | `#3E2407` | Deep Brown - Use for primary buttons, important headings. |
| **Accent Color** | `#3E2407` | Same as primary for this brand. |
| **Background** | `#FDF6EE` | Cream/Off-white - Default page background. |
| **Text Primary** | `#0000EE` | Bright Blue - Used for text on light backgrounds and button text. |
| **Link Color** | `#F7F0E8` | Very light beige. |
| **Font Heading** | "Martina Plantijn Light" | Use for H1, H2, Hero text. Fallback: sans-serif. |
| **Font Body** | "Inter" | Use for paragraphs, buttons, inputs. Fallback: sans-serif. |
| **Border Radius** | `12px` | Standard for buttons, cards, inputs. |

## Component Rules

### Buttons
- **Primary Button**:
    - **Background**: `#3E2407` (Deep Brown)
    - **Text Color**: `#0000EE` (Bright Blue)
    - **Border Radius**: `12px`
    - **Box Shadow**: `0px 0px 8px 0px rgba(255, 92, 0, 0.25)` (Orange glow)
    - **Tailwind Example**: `bg-[#3E2407] text-[#0000EE] rounded-[12px] shadow-[0px_0px_8px_0px_rgba(255,92,0,0.25)] font-inter`

- **Secondary Button**:
    - **Background**: `#FFFFFF` (White)
    - **Text Color**: `#0000EE` (Bright Blue)
    - **Border Radius**: `12px`
    - **Box Shadow**: None
    - **Tailwind Example**: `bg-white text-[#0000EE] rounded-[12px] font-inter`

### Typography
- **Headings (H1/H2)**: Use "Martina Plantijn Light". If custom font is not loaded, ensure fallback is clean. Sizes: H1 ~64px, H2 ~56px.
- **Body**: Use "Inter". Size ~15px.

## Workflow
1.  **Context**: Determine if this is a new page, a standalone component, or a modification.
2.  **Tokens**: Pull specific values from the `brand_guidelines.json` or the Quick Reference above. Do not guess colors.
3.  **Generate**: Write the React/Tailwind code.
    - If `tailwind.config.js` is not configured with these specific colors, useful specific arbitrary values (e.g., `text-[#0000EE]`) to ensure brand accuracy.
    - Ensure fonts are applied via class names or inline styles if necessary (e.g., `font-['Martina_Plantijn_Light']` or similar if configured).
4.  **Verify**: Check contrast (Blue text on Brown background for buttons, Blue text on Cream background for page).

## Instructions
- **Always** use the specific hex codes provided.
- **Micro-interactions**: Add hover states that slightly lighten/darken the primary color or add scale effects, but keep the core brand colors intact.
- **Spacing**: Use multiples of 4px (Tailwind base unit) but align with the 12px border radius aesthetic.
