---
name: designing-delphi-creative
description: Generates high-end, "Creative" UI components matching the Delphi Digital Twin aesthetic. Focuses on glassmorphism, floating animations, and strict cream/brown typography.
---

# Designing Delphi Creative UI

## When to use this skill
- When the user asks for "Creative" or "High-end" UI components for the Delphi project.
- When creating new sections that need to match the **Hero**, **Bento Grid**, or **Demo** styles.
- When the user asks for "animations", "glassmorphism", or "interactive" designs.

## Core Design System

### 1. Color Palette
- **Background**: `bg-delphi-cream` (Use `#FDF6EE` or `#FAF7F2` if variable not available).
- **Text Primary**: `text-delphi-brown` (Deep Brown `#3E2407`).
- **Text Secondary**: `text-delphi-brown/60` or `/40`.
- **Accents**: 
    - **Orange**: `text-orange-500` / `bg-orange-500` (for highlights, buttons).
    - **Blue/Purple**: Used sparingly for "Digital/Tech" elements (`bg-blue-50`, `text-blue-500`).

### 2. Typography
- **Headings**: **Serif** (`font-serif`). Large, bold, often with italicized keywords.
    - Example: `<h2 className="text-6xl font-serif text-delphi-brown">Title <span className="italic text-orange-500">Accent</span></h2>`
- **Body**: **Sans-serif** (`font-sans`). Clean, readable, high tracking for "eyebrows" (`tracking-wider uppercase`).

### 3. Key Visual Patterns

#### A. Glassmorphism (The Console Look)
Used for main interactive elements (like the Chat Demo).
```jsx
<div className="bg-white/40 backdrop-blur-2xl rounded-[2.5rem] border border-white/50 shadow-2xl ring-1 ring-delphi-brown/5">
  {/* Content */}
</div>
```

#### B. Floating Elements
Used to make the interface feel "alive".
- **Float**: `animate-float` (Up/down gentle motion).
- **Delayed Float**: `animate-float-delayed` (Offset timing).
- **Reverse Float**: `animate-float-reverse` (Opposite direction).

#### C. Bento Grids
Used for feature layouts.
- **Cards**: `bg-[#FAF7F2]` (slightly darker cream), Rounded `rounded-[2.5rem]`, Border `border-delphi-brown/5`.
- **Hover**: Scale up or shadow increase.

### 4. Background Atmosphere
- **Grain**: subtle noise overlay (`mix-blend-multiply opacity-[0.4]`).
- **Orbs**: Large, blurred colored orbs (`blur-[100px]`) in the background (Orange/Blue) to add depth.
- **Grid**: Subtle tech grid (`opacity-[0.03]`).

## Component Template (Start here)

```tsx
import { motion } from 'framer-motion';

const CreativeComponent = () => {
  return (
    <section className="relative py-24 bg-delphi-cream overflow-hidden">
      {/* Background Atmosphere */}
      <div className="absolute inset-0 pointer-events-none">
         <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-orange-200/20 rounded-full blur-[100px]" />
      </div>

      <div className="max-w-7xl mx-auto px-4 relative z-10">
         {/* Serif Header */}
         <h2 className="text-5xl font-serif text-delphi-brown mb-12 text-center">
            Your Creative <span className="italic text-orange-500">Title</span>
         </h2>

         {/* Glass Content */}
         <div className="bg-white/60 backdrop-blur-xl rounded-[2rem] p-8 border border-delphi-brown/5 shadow-xl">
            {/* Inner Content */}
         </div>
      </div>
    </section>
  )
}
```

## Checklist for Creativity
- [ ] Is the background **Cream**?
- [ ] Are headings **Serif**?
- [ ] Are key elements **Floating** or **Animated**?
- [ ] Is there a **Glass** effect on containers?
- [ ] Are we using **Delphi Brown** for text (not black)?
