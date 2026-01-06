# Component Library Templates

This skill ships a component template library under `assets/`. All templates are Astro components and use a consistent PascalCase naming convention. Vue island templates live under `assets/vue` for interactive components. See `references/component-index.md` for a curated pick list and `references/component-usage.md` for production usage notes.

## Component Patterns

### Compound Components

Some components are split into multiple pieces for cleaner composition (e.g., Accordion, Banner, Sidebar menu). Use the parent wrapper and nest the child parts inside it.

### Slot-First API

All components accept a `class` prop for overrides and expose slots for content. Default props (`title`, `description`, `items`) are provided for quick drop-in use.

## Example Usage

```astro
---
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@components/ui/Accordion.astro";
import {
  Banner,
  BannerContent,
  BannerTitle,
  BannerDescription,
} from "@components/ui/Banner.astro";
import {
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
} from "@components/ui/SidebarMenu.astro";
import { Icon } from "astro-icon/components";
---

<Accordion>
  <AccordionItem open>
    <AccordionTrigger>Product Information</AccordionTrigger>
    <AccordionContent class="flex flex-col gap-4 text-balance">
      <p>Our flagship product combines cutting-edge technology with sleek design.</p>
      <p>Key features include advanced processing capabilities.</p>
    </AccordionContent>
  </AccordionItem>
</Accordion>

<Banner>
  <BannerContent>
    <BannerTitle>Banner Title</BannerTitle>
    <BannerDescription>Banner Description</BannerDescription>
  </BannerContent>
</Banner>

<SidebarMenu class="w-64">
  <SidebarMenuItem>
    <SidebarMenuButton href="/">
      <Icon name="tabler:home" />
      <span>Home</span>
    </SidebarMenuButton>
  </SidebarMenuItem>
</SidebarMenu>
```

## Notes

- Keep icons as `tabler:` names and validate before dev or build.
- Use `.astro` for static components and reserve Vue for interactive UI.
- For interactivity, prefer Vue islands and keep behavior in small, focused components.
- Vue island templates: `Accordion.vue`, `Dialog.vue`, `Tabs.vue`, `Carousel.vue`, `DropdownMenu.vue`, `Popover.vue`, `Tooltip.vue`, `Select.vue`, `Toast.vue`, `Sheet.vue`.
- Tabler icon lists (`references/tabler-icons.txt`, `references/tabler-icons-curated.txt`) may be empty until the validator runs.
