# Styling and CSS

You can style Astro sites using plain CSS, classless stylesheets, or frameworks like Tailwind or UnoCSS. For rapid prototyping, download a classless CSS file (for example, Sakura) and place it in `public/css/style.css`. Link it in your layout's `<head>` section:

```html
<link rel="stylesheet" href="/css/style.css" type="text/css" />
```

For utility-first styling, install Tailwind CSS:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Then configure Tailwind in `tailwind.config.js` and import the generated stylesheet in your layout.
