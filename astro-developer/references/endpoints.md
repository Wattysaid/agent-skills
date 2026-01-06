# Server Endpoints and APIs

For dynamic server logic, create endpoint files under `src/pages/api` with `.ts` or `.js` extensions. Export a `GET`, `POST`, or `all` function to handle HTTP requests. Use endpoints to send form submissions, process data, or fetch external APIs.

Example endpoint (`src/pages/api/subscribe.ts`):

```ts
import type { APIRoute } from "astro";

export const POST: APIRoute = async ({ request }) => {
  const data = await request.json();
  // process subscription
  return new Response(JSON.stringify({ status: "ok" }), {
    headers: { "Content-Type": "application/json" },
  });
};
```
