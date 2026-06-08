---
name: Marine Taxonomy System
colors:
  surface: '#fff8f6'
  surface-dim: '#ebd6cf'
  surface-bright: '#fff8f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff1ec'
  surface-container: '#ffe9e3'
  surface-container-high: '#fae4dd'
  surface-container-highest: '#f4ded7'
  on-surface: '#241915'
  on-surface-variant: '#57423b'
  inverse-surface: '#3a2e29'
  inverse-on-surface: '#ffede8'
  outline: '#8b7169'
  outline-variant: '#dec0b6'
  surface-tint: '#a43c12'
  primary: '#a43c12'
  on-primary: '#ffffff'
  primary-container: '#ff7f50'
  on-primary-container: '#6c2000'
  inverse-primary: '#ffb59c'
  secondary: '#006a65'
  on-secondary: '#ffffff'
  secondary-container: '#76f3ea'
  on-secondary-container: '#006f69'
  tertiary: '#00658e'
  on-tertiary: '#ffffff'
  tertiary-container: '#61acda'
  on-tertiary-container: '#003e5a'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbcf'
  primary-fixed-dim: '#ffb59c'
  on-primary-fixed: '#380c00'
  on-primary-fixed-variant: '#822800'
  secondary-fixed: '#79f6ed'
  secondary-fixed-dim: '#59dad1'
  on-secondary-fixed: '#00201e'
  on-secondary-fixed-variant: '#00504c'
  tertiary-fixed: '#c7e7ff'
  tertiary-fixed-dim: '#85cfff'
  on-tertiary-fixed: '#001e2e'
  on-tertiary-fixed-variant: '#004c6c'
  background: '#fff8f6'
  on-background: '#241915'
  surface-variant: '#f4ded7'
typography:
  display-lg:
    fontFamily: Manrope
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.4'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 64px
---

## Brand & Style

The design system is engineered for scientific precision blended with the organic vibrancy of marine life. It targets marine biologists, conservationists, and citizen scientists who require a tool that is both analytically rigorous and visually refreshing.

The aesthetic follows a **Minimalist-Professional** direction with subtle **Glassmorphic** accents. High-quality whitespace and thin structural lines reflect a laboratory-grade environment, while soft, translucent layers mimic the clarity of tropical waters. The emotional response should be one of "Informed Wonder"—clear, focused, and intellectually stimulating.

## Colors

The palette is derived from the reef ecosystem, balanced for accessibility and scientific clarity:
- **Coral Pink (#FF7F50):** Used as the primary action color for identification triggers and primary CTA buttons.
- **Seafoam Green (#20B2AA):** Utilized for success states, taxonomy confirmations, and growth indicators.
- **Deep Ocean Blue (#006994):** The foundational color for navigation, headers, and serious data visualizations.
- **Sandy White (#F4A460):** Used sparingly as an accent for highlights, tooltips, or special metadata tags.
- **Neutral Backgrounds:** A very light, cool-grey base (#F8FAFB) ensures that coral photographs remain the focal point without color contamination.

## Typography

This design system utilizes a tiered typographic approach to separate biological data from instructional UI:
- **Headlines (Manrope):** Chosen for its modern, balanced proportions. It provides a clean, authoritative look for species names and section headers.
- **Body (Inter):** A systematic sans-serif that ensures high legibility for long-form morphological descriptions and habitat reports.
- **Data Labels (JetBrains Mono):** A monospaced font used specifically for specimen IDs, GPS coordinates, and taxonomic classifications, providing a technical, "lab-result" feel.

## Layout & Spacing

The design system employs a **12-column fluid grid** for desktop and a **4-column grid** for mobile. 

- **The "Oxygen" Principle:** Generous margins (64px on desktop) are used to prevent the UI from feeling cluttered, mimicking the vastness of the ocean.
- **Rhythm:** An 8px base grid governs all component dimensions.
- **Density:** High-density layouts are permitted only within "Data Sheets" where technical specs are compared. Otherwise, standard layouts favor a 24px vertical rhythm between blocks.

## Elevation & Depth

To maintain a sleek, modern feel, this design system avoids heavy shadows. Instead, it uses **Tonal Layers** and **Backdrop Blurs**:

1.  **Base Layer:** Solid neutral light grey.
2.  **Surface Layer (Cards/Containers):** Pure white with a 1px border in a very light Deep Ocean Blue tint (5% opacity).
3.  **Floating Elements (Modals/Dropdowns):** Uses a glassmorphic effect—`backdrop-filter: blur(12px)` with a semi-transparent white background.
4.  **Shadows:** When used for primary interactions, shadows are highly diffused and tinted with Ocean Blue (e.g., `0 8px 30px rgba(0, 105, 148, 0.08)`).

## Shapes

The shape language reflects the organic but structured nature of coral. 
- **Standard UI elements** (Buttons, Inputs) use a 0.5rem (8px) radius.
- **Cards and Image Containers** use 1rem (16px) to appear soft and modern.
- **Interactive Tags/Chips** are fully rounded (Pill-shaped) to distinguish them from functional buttons.

## Components

- **Primary Buttons:** Solid Coral Pink with white Manrope text. No gradients. On hover, the color shifts to a slightly deeper coral tone.
- **Secondary Buttons:** Ghost style with a 1.5px Seafoam Green border and Seafoam Green text.
- **Identification Chips:** Pill-shaped backgrounds using 10% opacity versions of the brand colors (e.g., a Light Pink chip for "Endangered" status).
- **Taxonomy Lists:** Clean, border-bottom only separation using 8% Deep Ocean Blue. High contrast on the species name (Manrope) vs. the family name (Inter Italic).
- **Observation Cards:** Large-format image containers with a white footer. The footer contains the species name in Headline-MD and technical metadata in the JetBrains Mono label style.
- **Input Fields:** Minimalist style; only a bottom border that transforms into a Seafoam Green 2px border on focus.
- **Specimen Map Pins:** Minimalist circular pips using Deep Ocean Blue with a Coral Pink center dot for the active selection.