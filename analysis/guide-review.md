# Reading guide review

The source-based conversational guide was reviewed independently against the requested topic discovery, short summaries, references, and cross-PDF navigation behavior.

## Verified behavior

- Eight starter paths and all their topic/step identifiers resolve in the atlas.
- Nachiketa queries surface the Katha dialogue and the Varaha retelling with separate source pages and an explicitly suggested comparison.
- Creation comparisons can span Vedas and Upanishads while respecting a requested collection or individual work.
- Brahma and Brahman remain distinct; an explicitly named Brahma Upanishad still resolves to that text.
- Modern commentary is identified separately from primary translations.
- Exact hymn references, direct work summaries, current-selection questions, and follow-up topic context work.
- Scoped page fallback respects the relevant section of a multi-work PDF instead of treating the entire compilation as one work.
- A fabricated title returns an honest no-match response and topic suggestions.
- Every returned source/page/quotation and relationship endpoint in the acceptance cases validates against the supplied data.

## Interface and data handling review

User questions, summaries, quotations, titles, and follow-up prompts are escaped before insertion into HTML. Source PDF links use encoded paths from the fixed manifest. The guide makes no external API calls and includes no API credentials. Source text and user questions remain data rather than executable instructions.

The native modal provides a labeled conversation log, keyboard submission, focus restoration, and explicit map/PDF actions. Browser interaction and responsive-layout checks are performed separately by the main task.

## Acceptance checks

Run `node scripts/check_guide.js` from the repository root. The checks cover 21 conversational cases, all eight topic paths, result identifiers, document/page bounds, exact source excerpt prefixes, commentary classification, and connection evidence.

The guide assembles reviewed summaries and source passages; it does not generate new doctrine or claim exhaustive scholarly interpretation. Text matching can still be affected by spelling, translation, and OCR. Responses preserve that limitation and direct readers back to the cited PDFs.
