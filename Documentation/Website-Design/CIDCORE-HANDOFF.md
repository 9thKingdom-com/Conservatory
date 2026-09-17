# 9th Kingdom website — design and implementation handoff

Prepared for John and CIDCORE, 11 September 2026. Proposed design, not approved publication copy. No live website, database, account or payment changes have been made. CIDCORE owns implementation and must map this design onto the existing backend.

## Creative direction

**A beautiful world worth preserving. A larger mystery worth following.**

Lead with the playable experience and an invitation. Introduce integrity through the choices a journey presents, without opening with a lecture or describing a hidden scoring system. On the Edge of Extinction is the first featured journey; the wider brand supports independently playable games of different genres. Do not publicly reveal how choices unlock the room of doors, or spoil the Chapter 2 survivor reveal.

The public site should feel like a premium independent adventure game: botanical realism, ivory glasshouse architecture, warm brass, forest shadow and humane typography. Hope and curiosity should be stronger than apocalypse imagery. The visual concept is an aspirational design mockup, not evidence of finished Unreal graphics. Keep an explicit Concept art label anywhere that imagery is published.

## Why change the entrance

The [live homepage reviewed on 11 September 2026](https://9thkingdom.com/) foregrounds integrity economics, treasure journeys, tokens and treasury funding. That is a different first impression from the new linked-game direction. This proposal leads with On the Edge of Extinction and keeps existing account, ledger and treasury information discoverable. It does not authorize replacing the financial purpose of existing contributions or removing existing terms.

Conversion hypothesis: visitors are more likely to explore and follow when they first understand the experience and see tangible progress. This is a hypothesis to measure, not a promised uplift.

## Visual specification

| Token | Value | Use |
|---|---|---|
| Forest | #142C27 | Header, dark sections, primary text on ivory |
| Ivory | #F3EFE4 | Main page surface and light text |
| Brass | #B99A5B | Rules, ornament, filled CTA with forest text |
| Muted ink | #53645D | Secondary text on ivory; verify final contrast |
| Stone | #D7D1C4 | Dividers and quiet panels |
| Display | Georgia, serif fallback; optional licensed editorial serif later | Headlines, short quotations |
| Interface | system-ui, sans-serif | Body, forms, navigation |

Use brass as an accent, not small body text on ivory. Desktop: 1200 px max content width; 32 px gutters; 12-column layout; 88–112 px section spacing. Mobile: 20 px gutters and 48–64 px spacing. Body 18 px/1.6, mobile at least 16 px. Hero heading clamp(42px, 5.5vw, 80px), short line lengths. Buttons at least 48 px high, 4 px corner radius. Keep ornament to thin rules and one restrained existing brand mark; do not invent a final logo in this mockup.

Hero media has a dark gradient behind text. Use a selected mobile crop with the glasshouse still visible. Alternate dark photographic sections and generous ivory editorial sections. Avoid glossy dashboard cards, neon effects, spinning emblems, auto-playing sound, fake system terminals and dense icon grids. Motion is optional: subtle 150–250 ms transitions; respect reduced-motion settings.

## Homepage structure and draft copy

### 1. Header
Wordmark: **9TH KINGDOM**. Navigation: The games · Journal · CIDCORE. Actions: Sign in (quiet), Support (outlined). On mobile use a labelled menu button and keep the wordmark visible. Existing authenticated users should retain an obvious route back to their account.

### 2. Hero — make the premise understandable immediately
Eyebrow: **ON THE EDGE OF EXTINCTION · IN DEVELOPMENT**

Headline: **What will you preserve?**

Copy: **An independent survival adventure inside a living sanctuary. Explore the world beyond the glass through robots, and discover what it takes to keep life flourishing.**

Primary button: **Discover the game** → game detail page. Secondary: **Follow development** → signup section. Do not use Play now, Download or Wishlist until an actual matching destination exists. Put the development label near the title, not in a distant footer.

For the actual launch use a compelling real in-engine image or clearly labelled concept art. Add a Watch development footage action only when genuine footage is ready; no pretend trailer player.

### 3. The first journey
Eyebrow: **THE FIRST JOURNEY**
Heading: **Survival is only the beginning.**
Intro: **A scientist's five-year study becomes an uncertain fight for the future when a catastrophe changes the world outside. Your sanctuary is alive. Keeping it that way is the challenge.**

Three columns, stacking on mobile:
- **Protect your sanctuary.** A conservatory at the heart of the journey. Use current verified footage; do not imply all survival systems are finished.
- **Explore through robots.** Venture beyond the glass through machines you control. Link to a verified demonstration.
- **Find another way.** The design asks what ingenuity and coexistence can make possible when resources become scarce. Label this as a design goal until the animal/survival systems are implemented.

Use small explicit labels such as Prototype footage or Planned system alongside the media/copy they qualify. Never mix concept images into a gameplay gallery without labelling each one.

### 4. Wider world, without spoilers
Heading: **Different journeys. Choices that stay with you.**
Copy: **9th Kingdom is being developed as a connected collection of playable journeys. From intimate puzzles to open landscapes, each offers a different challenge—and a reason to look beyond the obvious answer.**

Feature one substantial On the Edge of Extinction card with In development status. Use a simple text teaser for future journeys rather than eight fake game covers. No invented titles, release calendar or chapter-to-door numbering. Do not expose the secret discovery route in marketing, page source, public API responses or analytics event labels.

### 5. Meet CIDCORE
Heading: **Meet the keeper of knowledge.**
Copy: **CIDCORE is the intelligence connecting the 9th Kingdom journeys. Discover the ideas behind the world and the role your choices will play in it.**
Action: **Meet CIDCORE** → explanatory page with the existing conversation route clearly linked.

Avoid claims that CIDCORE sees every action, knows motives, is conscious, or has implemented future cross-game observation. Explain actual account memory and data use in plain language near the conversation/account experience; narrative mystery is not a substitute for that explanation. Never use a logged-in player's private history as public social proof.

### 6. Development journal — establish trust with evidence
Heading: **See the world take shape.**
Three most recent real posts: date, image, descriptive title and short summary. Suggested subjects based on existing project work: the five-dome habitat, exploring through robots, the Landscape paint experiment. Confirm media and factual claims before posting. Empty state: show one genuine progress note, not fabricated activity.

### 7. Support — give people a concrete reason
Heading: **Help bring the first journey to life.**
Copy: **9th Kingdom is John's passion project. Follow its progress, or help support the work behind the next step.**
Actions: **See support options** and **Read the latest progress**.

On the support destination, show the actual purpose, current milestone and applicable contribution terms before payment. The mockup's Support development wording is conditional on a separately accurate development-support route. Until John and CIDCORE resolve the existing treasury allocation, use See support options pointing to the existing explanation. Do not relabel treasury contributions as development donations. No invented totals, countdowns, funding targets or reward benefits; a contribution cannot buy integrity or the title of 9th King.

### 8. Follow development and footer
Heading: **Be here as the world grows.**
One email field with visible label and button **Keep me updated**. Copy: **Development news from 9th Kingdom. Unsubscribe whenever you wish.** Publish only if a working subscription/unsubscribe flow exists. No account requirement to read public progress. Show clear success, invalid-address, duplicate and service-error states without exposing subscriber records.

Footer links: Games · Journal · About John · CIDCORE · Support · existing Treasury/Ledger · Account · Privacy · Terms · Contact. Reuse existing destinations; URLs below are proposals, not current route assumptions.

## Proposed information architecture

| Page | Purpose |
|---|---|
| / | Introduce the world; direct visitors to the featured game and updates |
| /games/edge-of-extinction | Premise, honest availability, verified media, working/planned feature distinction, FAQ |
| /journal and article pages | Dated development evidence and shareable stories |
| /cidcore | Character context, actual capabilities, memory explanation, existing conversation entry |
| /support | Accurate support purposes, terms and existing payment integration |
| Existing account and treasury routes | Preserve functionality, history and established links |

CIDCORE should first inventory actual routes, authentication/session contracts and integrations. Reuse rather than recreate them. Preserve old URLs or add deliberate redirects; do not change user identifiers, database schema, payment destinations or authorization behavior merely to implement a visual redesign.

## Build contract for CIDCORE

- Build a private preview with this copy and design system first. Keep public deployment separate from design implementation.
- Implement text, buttons and layouts as real HTML/CSS, not as one image of a website. The generated mockup guides composition; this document controls exact copy and behavior.
- Use the existing site stack and authentication. Do not infer backend changes from a static visual concept.
- Content fields: title, summary, media, media classification (in-engine/concept), development status, date and destination. Reuse the existing content mechanism; no schema migration is mandated.
- Use responsive image sizes and modern formats where supported, explicit dimensions, lazy loading below the hero and a static poster before optional video. No third-party tracker or embedded video loading automatically just to decorate the page.
- Keyboard navigation, visible focus, semantic headings, skip link, labelled fields, meaningful alt text, accessible errors, touch targets and contrast checks are required. Test at 390 px and 1440 px plus 200% zoom; no horizontal overflow.
- Keep headings/copy in DOM for search. Proposed page title: **9th Kingdom — On the Edge of Extinction & Connected Game Journeys**. Meta description: **Discover On the Edge of Extinction, an independent survival adventure in development. Explore the world of 9th Kingdom and follow its creation.** Share cards must also label concept art when used.
- Proposed measurement, using the site's approved privacy approach: game-detail clicks, development-follow completions and support-route visits. Do not send private CIDCORE conversations or inferred moral profiles into marketing analytics. Establish a baseline before claiming conversion improvement.

## Acceptance and unresolved decisions

The preview should communicate what this is, what is available now and how to follow within the first screen. All navigation/actions must have real destinations or clear preview-only annotations. Check mobile, keyboard and form states. Confirm existing sign-in, CIDCORE and treasury links survive the redesign. Verify every gameplay claim and media label.

John's visual approval, final production hero selection and the support-funding wording remain open. Future journey numbering, release dates and download platforms remain undecided. Nothing in this brief promises finished animal systems, live adaptive journeys, a game copy for a donation, or a particular release date.

Delivery request for CIDCORE: produce desktop/mobile previews and a short list of integration decisions needed from John. Retain the mystery in the fiction, make the public proposition clear, and keep progress claims specific.


Title update, 11 September 2026: John explicitly approves On the Edge of Extinction as the Chapter One title. Earlier generated mockups retain historical lettering; use this updated brief for current text. Existing URLs and asset filenames are not renamed by this copy update.
