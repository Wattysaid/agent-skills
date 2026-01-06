# Examples and Usage Scenarios

## Build a Personal Blog

1. Scaffold a new project:
   ```bash
   npm create astro@latest
   # choose the blog template when prompted or use an empty template
   ```
2. Add a base layout and configure site metadata.
3. Create a `src/pages/blog` directory and add Markdown posts (for example, `my-first-post.md`) with frontmatter.
4. Implement a dynamic route `[slug].astro` to display individual posts.
5. Style the site with Tailwind or your preferred CSS framework.

## Launch a Marketing Landing Page

1. Browse the Astro themes gallery and pick a Landing page or Portfolio template.
2. Clone or scaffold the template and customize hero sections, testimonials, and call-to-action blocks.
3. Optimize for SEO using meta tags and the `@astrojs/seo` integration.
4. Deploy using a static adapter for fast load times.

## Create a Multi-Page Web Application

1. Start with an empty Astro project and add integrations (for example, React or Vue) for client-side interactivity.
2. Structure pages under `src/pages` and use dynamic routes for user-specific views.
3. Implement server endpoints for API communication.
4. Use content collections for structured data and global state management via islands or framework state libraries.

## Snippets

- Command to scaffold a project: `npm create astro@latest`.
- Link to import a classless CSS: `<link rel="stylesheet" href="/css/style.css" type="text/css" />`.
- Layout with slot: Move content from `index.astro` into `Base.astro` and include `<slot />` to inject page content.
