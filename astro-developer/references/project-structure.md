# Project Structure and Conventions

This repository uses a clear separation between pages, layouts, components, content, and data loaders. Follow these conventions when adding features.

## Core Directories

- `src/pages` - Route files. File-based routing; dynamic routes use brackets.
- `src/layouts` - Shared page layouts (BaseLayout, Listing, Landing, etc.).
- `src/components` - UI components grouped by domain (app, directory, listings, ui, etc.).
- `src/styles` - Global styles (Tailwind setup and global CSS).
- `src/config` - Site settings and theme configurations.
- `src/data` - Content data (blog, directory, tools, lessons).
- `src/lib` - Data loaders and core data access functions.
- `src/util` - Small helpers (formatting, theme config, OG images).
- `src/validation` - Data validation and schema checks.
- `src/types` - Shared types and interfaces.

## Theme and Icon Usage

- Theme configs live in `src/config/themes/*.toml`.
- Global settings live in `src/config/settings.toml`.
- Tabler icons are used via the `tabler:` prefix in markup.

## Pages and Layouts

- Add new routes in `src/pages`.
- Prefer using an existing layout from `src/layouts`.
- Keep layout changes centralized to avoid breaking multiple pages.

## Components

- Place reusable UI in `src/components/ui`.
- Place feature or domain-specific UI in `src/components/<domain>`.
- Prefer `.astro` for static components, and use framework components only when needed.

## Content Collections

- Content config is at `src/content.config.ts`.
- Content lives under `src/data`.

