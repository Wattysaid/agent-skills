# Deployment

Astro builds static files into `dist/` by running `npm run build`. To preview the output locally, run `npm run preview`. Deploy your site using an adapter. Popular options include:

- Netlify: `npm run astro add netlify` then deploy via Netlify CLI or the Git integration.
- Vercel: `npm run astro add vercel` and deploy using the Vercel CLI or dashboard.
- Cloudflare/Node/Static: Install the relevant adapter and configure `astro.config.mjs` accordingly.

CI/CD pipelines should set appropriate environment variables and run `astro build` before deployment.
