# Overview and Project Setup

Astro is a modern front-end framework and static site generator that emphasizes performance by shipping minimal JavaScript. It supports content-rich sites, blogs, portfolios, and complex web applications. You can start from an empty project or choose from hundreds of community-built templates. Astro uses a file-based routing system, supports Markdown/MDX content, and allows integrating UI libraries like React, Svelte, or Vue.

The instructions assume Node.js v18.17.1 or v20.3.0 and npm are installed.

## Installation and Project Setup

1. Create a new project. In a terminal, navigate to your working directory and run:

   ```bash
   npm create astro@latest
   ```

   The CLI prompts for the project folder, starter template, and TypeScript options. To build from scratch, choose the Empty template. The wizard can also initialize a Git repository and install dependencies.

2. Start the development server. Change into the project directory and run:

   ```bash
   cd my-astro-project
   npm run dev
   ```

   Open `http://localhost:4321` to view the default page. The development server live-reloads on file changes.

3. Configure TypeScript paths (optional). To simplify imports, update `tsconfig.json` with a base URL and alias:

   ```json
   {
     "compilerOptions": {
       "baseUrl": ".",
       "paths": {
         "@/*": ["./src/*"]
       }
     },
     "extends": "astro/tsconfigs/strict"
   }
   ```
