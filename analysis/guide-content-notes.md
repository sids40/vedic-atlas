# Source-guide reading paths

The starter paths in `output/guide-topics.js` are editorial reading recommendations through existing indexed entries. They add no new source text or historical chronology. All topic IDs and step IDs resolve to the current atlas.

## Curated paths

| Path | Scope | Reading distinction |
|---|---|---|
| How does the world begin? | Rigveda 10.129 and 10.90; Aitareya; supplied Vishnu overview | The questioning hymn, cosmic Person, creation-and-entry account, and Purana section remain separate presentations. |
| Self, consciousness, and Brahman | Chandogya dialogue; Brihadaranyaka dialogue; Mandukya; Agni overview | Brahman is distinct from the creator Brahma. Mandukya's primary translation, Gaudapada's Karika, and modern commentary remain separate. |
| Nachiketa, death, and the self | Katha dialogue; Varaha retelling; Rigveda 10.14 | Yama is a shared figure; the sources differ in genre, setting, and focus. |
| Sacrifice, fire, and inward ritual | Rigveda 1.1 and 10.90; Pranagnihotra; Skanda chapter 2 | Opening praise, cosmological sacrifice, inward interpretation, and a narrative gathering are comparison points. Skanda is supplied Part I only. |
| Devotion through three stories | Linga Dhruva; Vishnu Prahlada; Bhagavata Gajendra | These are passages from supplied English retellings, not claims of complete canonical editions. |
| Shiva, Sati, and Daksha's sacrifice | Shiva volume 1; Padma; Kurma; Skanda chapter 2 | Parallel accounts should not be merged into one presumed original version. The Kurma summary itself flags version differences. |
| Divine speech and the Goddess | Rigveda 10.125; Devi Upanishad; Markandeya and Vamana narratives | Similar names and themes do not establish identical theology or historical derivation. |
| Yoga, attention, and meditation | Katha chariot image; Yoga Tattva; Shiva meditation; Common Yoga Protocol p51 | The modern practical guide is a distinct layer. The supplied yoga scan ends at Dhyana; later contents-listed sections are not present. |

## Answer-writing requirements

- Cite physical PDF page numbers and label the specific supplied source, not just a generic text title.
- Use the source entry's reviewed summary or the curated step note. Do not turn a heading or a table-of-contents record into a detailed invented summary.
- Keep quoted evidence separate from brief editorial explanation. Excerpts must be exact substrings of the cited page after whitespace normalization.
- Name the connection: shared figure, theme, parallel account, traditional affiliation, or English phrase match. None alone establishes composition dates or borrowing.
- Do not quote or summarize a modern commentary as if it were the primary Upanishad translation.
- Do not present practical medical or physical-practice claims as independently established advice; the guide can identify and refer to the supplied material.
- For vague requests, offer a small set of distinct starting topics. For follow-ups, retain the prior topic instead of treating "tell me more" as a literal search.
- Unknown or unsupported topics should produce an honest no-match response with relevant available alternatives, rather than invented references.

## High-value behavioral checks

1. "Where should I begin?" should offer topics or short paths with original-source links.
2. "Nachiketa" should surface the Katha dialogue and Varaha retelling and distinguish them.
3. "Connect creation across Vedas and Upanishads" should show more than one work and avoid asserting one uniform account.
4. "Brahman" should not primarily return Brahma, Brahmanaspati, or an unrelated Brahmana social designation.
5. "Sati" should not retrieve Samaveda "Dasati" groups merely by substring matching.
6. "Rama" should keep Ramachandra and Parashurama distinguishable and note ambiguous source usage.
7. "Tell me more" after a topic should remain on that topic, with additional references or a path.
8. "Show me the original page" should open the cited PDF page rather than the first page of the source file.
9. "What is in the yoga PDF after Dhyana?" should preserve the known supplied-file gap.
10. No answer should imply a live model, training process, or independent verification when the feature uses local indexed retrieval and editorial summaries.

Validation: all eight topic nodes and all 30 step nodes exist in `output/atlas.json`; the script passes `node --check`.
