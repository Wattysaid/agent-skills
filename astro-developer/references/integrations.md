# Integrations and UI Frameworks

Astro can integrate with popular UI frameworks (React, Svelte, Vue, SolidJS, Alpine.js, and more) and CSS libraries. To add a framework, run:

```bash
npm run astro add react
```

Replace `react` with `svelte`, `vue`, or another integration as needed. Astro will modify configuration files and install dependencies. Then you can import React components into `.astro` files using the `client:load` or `client:only` directives to control hydration.
