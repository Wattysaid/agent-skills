# Adding Content and Routing

Astro uses a file-based routing system:

- Pages: Files in `src/pages` become routes (for example, `src/pages/about.astro` -> `/about`).
- Dynamic routes: Bracket syntax defines parameters (for example, `src/pages/blog/[slug].astro` -> `/blog/:slug`). Use frontmatter to load dynamic data and display it within the page.
- Markdown and MDX: Create a `src/content` or `src/pages/blog` folder for posts written in `.md` or `.mdx`. Astro automatically renders Markdown to HTML.

Example dynamic blog page:

```astro
---
import Base from "@/layouts/Base.astro";
const { slug } = Astro.params;
const post = await Astro.fetchContent(`/posts/${slug}.md`);
---
<Base>
  <article>
    <h1>{post.frontmatter.title}</h1>
    <post.Content />
  </article>
</Base>
```

Content collections provide type-safe access to structured content. Define collections in `src/content/config.ts` and query them via `getCollection()`.
