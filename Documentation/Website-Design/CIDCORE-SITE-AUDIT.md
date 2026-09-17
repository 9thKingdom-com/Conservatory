# 9th Kingdom — consistency and navigation audit

11 September 2026. Read-only review for John and CIDCORE. No site, account, payment or database changes made. Findings describe the public visitor experience observed during this session, not a backend audit.

## Scope and limits

Followed all unique same-site anchor destinations discovered on the homepage and the public pages reached from it, including account redirects. Inspected the two external service destinations linked directly from those pages: CIDCORE and Stripe checkout. Did not crawl those external domains further. Reviewed desktop screenshots of home, support, login and legends; mobile home/menu and support at a 390 px viewport. No forms submitted, payments made or accounts created. Private games/dashboard interiors, post-payment pages, all keyboard/form states and unlinked pages remain untested. This is not a full accessibility, security or legal audit.

## Fix first

### 1. Public ledger exposes a donor email and internal processing notes — urgent

On [Treasure Ledger](https://9thkingdom.com/treasure-ledger.html), a zero-value `coin_pending_claim` entry visibly includes a donor email and an account reconciliation message. The address is deliberately not copied here.

CIDCORE action: exclude internal reconciliation events and personal contact information from the public ledger response, not merely hide them with CSS. Publish only explicitly approved public fields; retain private operational records internally. Check public name preferences independently. Verify anonymously that neither rendered text nor public response contains email/internal notes, while legitimate totals and transactions remain accurate. Inspect similar historical entries for the same issue.

### 2. Registration and login do not offer a consistent identity path

[Signup](https://9thkingdom.com/signup.html) asks for a name and password and explicitly makes email optional. [Login](https://9thkingdom.com/login.html) presents only an email field. A visitor who followed the no-email route cannot see how to return. This is an observed UI contradiction; no login attempt or authentication vulnerability is claimed.

CIDCORE action: align login with the actual supported identity contract. Offer name/password if that is the registration contract, and a separate clearly explained recovery path. Preserve existing accounts and any legacy login routes. Add an obvious existing-account Sign in link on signup. Test accounts created both with and without an email in a controlled environment.

### 3. Games and progress navigation does not deliver what the label promises

- Homepage The games, See all journeys and the On the Edge of Extinction card all point to `/kingdoms.html`, which redirects an anonymous visitor to signup.
- Journal points to `/legends.html`, which is Stone of Legends, an honours page rather than development news.
- See the latest progress points to the financial ledger. The support page also promises milestones there; the inspected ledger showed transactions and patrons, not development updates.

CIDCORE action: provide a public game overview before requiring an account to play. Keep private play routes gated. Give Journal a real dated progress destination, or remove/rename the label until that exists. Keep Legends separate from Journal. Point progress CTAs to actual development evidence. These can be simple pages using the shared layout; no new CMS is required.

## Shared styling pass

### One header, footer and vocabulary

Homepage uses The games / Journal / CIDCORE / Login / Support. Inner pages variously use Kingdoms / Treasure Ledger / Collection / Legends / Enter / Dashboard. Logged-out login/signup pages even present Dashboard, which redirects back to signup. Support has no equivalent complete footer in the inspected page tree.

Build one reusable public header and footer using the homepage's approved typography, spacing, forest/ivory/brass palette and wordmark. Use the same destination names everywhere. Put Collection and Dashboard in account navigation; keep Sign in and Join visible to anonymous visitors. Suggested public menu: Games, Journal (when real), CIDCORE, Support, Sign in. Footer can retain Ledger and Legends. Add discoverable privacy, terms and contact destinations backed by actual pages; none were linked in the inspected public site navigation. Do not treat missing links as proof those documents do not exist elsewhere.

### Make inner pages feel like the same site

Support and login retain dark boxed panels, gold-toned body text and a different header scale. Legends has a large dark memorial graphic. Keep page-specific imagery but reuse a common page title, content width, typography and buttons. Use warm ivory content sections and dark readable body text, with forest headers; reserve brass for accents. Replace the login's bright crown emoji with the existing restrained brand mark or omit it.

On support mobile, the introduction becomes a very narrow, centred paragraph and pushes the donation action far down the page. Use left-aligned body copy, wider usable text space with roughly 20 px side gutters, and a short plain-language funding summary beside the action. Preserve full allocation details below. Suggested button wording: Support 9th Kingdom. Keep the primary action easy to find without concealing terms or funding purpose.

### Mobile menu semantics

The homepage hamburger opens its menu when clicked. Inspection shows the trigger is a LABEL with no accessible name, button role or tabindex. Replace with a real labelled button, expose expanded state and controlled menu, and test keyboard activation, Escape close and focus visibility. Reuse that mobile menu on inner pages; support currently hides major navigation links at narrow width without an equivalent visible menu. The viewport override was reset after testing.

## Copy and data consistency

1. **Stripe still uses the old coin name.** The [linked checkout](https://buy.stripe.com/7sY00d5M525AgHX1nE7AI02) loads, but its description calls the reward an exclusive finders coin / Charitable coin. Update the checkout description to Supporter Coin to match the donation page. Check receipts and follow-up templates too; those were not inspected. Do not change the payment link, pricing or allocation simply to fix copy.
2. **Journey count/position remains inconsistent.** Home calls On the Edge of Extinction the first journey but labels it II alongside I and seven more doors. Legends says eight journeys. Resolve chapter-versus-journey terminology with John; until then omit unsupported numbering rather than invent a new count. Keep the approved title On the Edge of Extinction.
3. **Availability should be explicit.** Keep an In development badge next to the featured title; Concept art — in development currently qualifies the image but can be mistaken for only the artwork's status. Distinguish joining the web experience from playing the Unreal journey.
4. **Benefit wording needs a single source.** Entry advertises lifetime access and 20 free CIDCORE chat credits weekly. CIDCORE should verify these against actual policy and implementation. No benefit fulfillment test was performed. Avoid interpreting entry as a promise that all future standalone games are available now.
5. **Support does not buy integrity.** Supporter Coin now correctly appears on donate. Home still says Nothing is for sale; narrower Support gives no gameplay advantage avoids an unnecessary conflict with future original-asset sales. Any change to commercial policy remains John's decision.
6. **Legends renders raw Markdown.** Its paragraph visibly includes `**Eight journeys. Eight stories.**`; render proper emphasis or remove the asterisks.
7. **Legends has a data error behind its empty state.** Browser console reported `Failed to load legends` with an Access denied response being parsed as JSON. Do not show an authoritative empty list when a load failed. Distinguish no records, loading and unavailable states; fix the endpoint/authorization response in the backend. The underlying cause is unverified.
8. **Ledger loading initially looks like zero funds.** It initially displayed $0.00 before settling at $22 total income, $17.60 Treasury and $4.40 reserve. Use placeholders until data loads, plus a last-updated indicator and an error state. These were public displayed values, not independently reconciled payments. Do not count the displayed $2 test donation as newly raised audience support.

## Destination inventory

| Requested route / link | Observed result | Recommendation |
|---|---|---|
| `/` | New homepage and hero render | Keep as visual baseline |
| `/index.html` | Same new homepage content | Use one canonical home destination consistently |
| `/kingdoms.html` | Redirect to signup | Public overview, gated play |
| `/legends.html` | Stone of Legends; data load error | Fix empty/error states; stop labelling this Journal |
| `/login.html` | Email-only login form | Align with signup |
| `/signup.html` | Name/password, optional email | Provide return-login path; backend test required |
| `/entry.html` | Free-entry information and entry button | Explain actual current access and benefits |
| `/challenge.html` | Redirect to signup | Label account requirement; private game not inspected |
| `/treasure-ledger.html` | Data eventually loads | Remove private operational content; improve loading |
| `/collection.html` | Sign-in-required explanation with login link | Useful explicit gate; apply common style |
| `/dashboard.html` | Redirect to signup | Returning-user login path instead of signup-only experience |
| `https://cidcore.com/` | Conversation UI loads with a return link | Preserve connection; conversation not submitted |
| Linked Stripe checkout | Amount/contact/payment form loads | Refresh old coin wording; transaction not tested |

No ordinary missing-page screen was encountered on these checked destinations. Several links are nevertheless misleading because they lead to a different purpose or an unexplained account gate. The entry page's action button and private/post-submit flows still require CIDCORE's end-to-end testing; anchor inventory alone is not that test.

## Economical implementation order for CIDCORE

1. Remove public email/internal events and resolve the login/signup mismatch.
2. Correct Journal/Games/progress routes and checkout coin wording.
3. Extract one shared header/footer, button style and content layout; apply across public/account pages.
4. Repair mobile navigation, support-page readability, data loading/error states and raw Markdown.
5. Preview anonymously and signed in on desktop/mobile. Check intended redirects, keyboard navigation, no-email account return, payment-description consistency and data privacy. Confirm changes in a preview before publishing; preserve working payment and account integrations.

This audit proposes fixes for CIDCORE to implement. No message was sent to CIDCORE and no changes were deployed.
