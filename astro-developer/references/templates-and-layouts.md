# Templates, Layouts, and Components

## Choosing Templates and Themes

Astro offers an extensive catalog of starter templates and themes for blogs, e-commerce, landing pages, portfolios, and documentation. Themes are filtered by category, technology (for example, React, Svelte, Tailwind), and price. Visit https://astro.build/themes/ and browse categories such as Blog, Docs, E-commerce, and Portfolio. Selecting a theme provides a ready-made structure and styling; you can then customize content and components.

To start from a template without using the CLI wizard, you can scaffold directly via `npx degit` or by cloning the template repository. For example:

```bash
npx degit withastro/astro-starter-blog my-blog
cd my-blog && npm install && npm run dev
```

## Layouts and Components

Astro encourages the use of layouts, reusable page structures containing `<html>`, `<head>`, and shared navigation. You create a layout component (for example, `src/layouts/Base.astro`), then wrap pages with it. Use a `<slot />` element inside the layout to specify where page-specific content will be injected.

Steps to create a layout:

1. Create a `layouts` directory under `src` and add `Base.astro`.
2. Move common HTML from `src/pages/index.astro` into `Base.astro`, replacing page-specific content with `<slot />`.
3. In your page (for example, `index.astro`), import the layout and wrap your content:

   ```astro
   ---
   import Base from "@/layouts/Base.astro";
   ---
   <Base>
     <h1>My Site</h1>
     <p>Welcome to my Astro site!</p>
   </Base>
   ```

Components in Astro use the `.astro` file extension and combine frontmatter scripts (between `---` fences) with JSX-like markup. You can import and reuse components across pages. Astro also supports islands architecture, where interactive components are hydrated on the client as needed.
