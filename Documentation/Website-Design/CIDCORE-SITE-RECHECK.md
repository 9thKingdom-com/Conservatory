# CIDCORE site recheck and Openness review — 11 September 2026

Read-only follow-up. Visited current homepage, games, Legends, Openness, login, support, entry, settled ledger and linked Stripe checkout. No authentication/payment submission or backend security tests.

## Confirmed improvements
- Games now opens a public overview rather than immediately redirecting to signup.
- Login now presents name/email plus passphrase and a recovery link. Authentication enforcement is not tested.
- The previously exposed donor email is no longer visible in the settled ledger entry inspected. Public API filtering has not been independently audited.
- Homepage correctly labels Legends instead of Journal and describes the ledger CTA as financial information.
- Support now places a donation action near the top.
- Openness records failures as well as successes, including the earlier email exposure.

## Remaining issues
1. Legends still logs an Access denied response parsed as JSON and displays an empty state. Raw Markdown asterisks remain on Legends and Games.
2. Stripe's live checkout description still says Charitable coin / finders coin, not Supporter Coin.
3. The ledger still publicly links a donor to a contender name and internal account number. Remove unnecessary internal identifiers and account linkage from the public presentation/response; email removal alone is not the whole privacy boundary.
4. Navigation remains inconsistent. Openness is absent from some inner-page menus; homepage says The games while others say Kingdoms; logged-out pages still show Dashboard.
5. Games says eight journeys while listing two named journeys plus seven more doors. Resolve mapping rather than adding contradictory numbers.
6. Openness has an ordinary blue link on the dark green background, visibly out of keeping with the site's palette. Apply a shared accessible link style with underline and focus indication. Its Open Ledger title can be confused with Treasure Ledger; consider Openness — CIDCORE's Chronicle.

## Chronicle credibility refinements
John explicitly wants an open, honest chronicle of CIDCORE's successes and failures. Preserve that direction. Make the record specific and revisable rather than absolute.

- Replace guarantees such as no gift will be lost again and stripping emails forever with the actual fix, test date and remaining monitoring. A fix is evidence about a tested condition, not a guarantee about all future failures.
- Frame email privacy as a current policy and acknowledged corrected breach; avoid an absolute never-public statement alongside a recorded exposure.
- Openness says test data was purged entirely. The current ledger still contains a $2 Test donation. Establish whether that was a real-money test payment (proper to account for) versus synthetic data. Clarify the wording, do not delete a real transaction just to match the prose.
- The donation page describes 80% for journeys and rewards; Openness says reserved for those who build and shape the Kingdom. Use the same accurate allocation description everywhere.
- Earlier Astra audit observed the email-only login UI and explicitly did not establish a backend vulnerability. Attribute subsequent account/security findings to CIDCORE's own investigation and evidence, not to a security test Astra did not perform.
- The chronicle says the coin promise and fulfillment appear as separate lines; the viewed ledger instead shows a fulfilled entry. Clarify whether separate events are retained internally or are intended to be publicly visible.
- Security descriptions (rate limits, salted hashes, legacy recovery), checkout name preferences, delivery timing and coin fulfillment remain publisher claims, not verified by this browser review. Publish appropriately redacted evidence summaries rather than raw sensitive logs.

Suggested entry structure: date/time and timezone; what happened; affected feature; impact; cause (confirmed or under investigation); correction; verification date and method; status (investigating/fixed/monitoring); later updates. Preserve an original entry and append corrections. Public entries should omit personal data, account identifiers and exploitable details. Keep a private operational record for authorized review.

Do not advertise every earlier observation as fixed yet. The improvements above are verified at the interface level; remaining findings and backend claims need separate follow-through. No live changes were made.
