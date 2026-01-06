# Stack and Conventions

This repository uses Astro as the framework with a Vue integration and a Tailwind CSS setup. Follow these conventions to avoid conflicts.

## Tech Stack

- Astro 5.x
- Vue 3 integration
- Tailwind CSS (v4)
- Zod for validation
- Astro loaders for external content sources

## Conventions

- Use `.astro` components by default.
- Use Vue components only when you need client-side interactivity.
- Use `@/` path aliases for imports.
- Use `tabler:` icon names for icons.
- Keep content in `src/data` and load through `src/lib` where possible.
- Keep validation rules in `src/validation` and shared types in `src/types`.

## Data Sources

- Content loaders live in `src/lib/loaders`.
- External data sources include Notion, Airtable, Google Sheets.

## Styling

- Use Tailwind utility classes for layout and spacing.
- Use `src/styles/global.css` for shared styles.

## Testing and Validation

- Available scripts include `npm run lint:lessons` and `npm run test:lessons`.
- Prefer adding validation to `src/validation` for data-driven features.

