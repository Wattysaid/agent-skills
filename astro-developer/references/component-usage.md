# Component Usage (Production)

These components are designed as drop-in templates that use Tailwind classes and the existing `src/styles/global.css` setup. They are intended to be copied into your project and customized.

## Global Styles

- Ensure `src/styles/global.css` is imported in your main layout.
- Components rely on Tailwind utilities and shared global styles defined there.

## Vue Islands

Interactive components import Vue islands from `@components/vue`. Copy the Vue templates from `assets/vue` into `src/components/vue` and use the Astro components as-is.

## Pattern

- Copy Astro component from `assets/components` into `src/components/ui` (or a domain folder).
- Copy Vue island from `assets/vue` into `src/components/vue` if required.
- Keep naming PascalCase for all components.

## Helpful Scripts

- `scripts/copy_component_library.sh` - Copy all Astro components and Vue islands into the project (use `--overwrite` to replace).
- `scripts/list_component_library.sh` - List all available component templates.
- `scripts/validate_component_library.sh` - Validate naming and required compound components.

## Visual Preview

- `assets/component-preview.astro` - Copy into a project page (e.g., `src/pages/component-preview.astro`) to see a live component showcase.
