# Vedic Atlas: analysis and coverage

Built on 2 November 2026 from the 30 PDFs supplied in `inputs/`. The corpus contains **7,984 physical PDF pages**. The graph contains **12,722 nodes and 25,501 directed relationships**.

## Open and navigate

Open [the interactive atlas](../output/vedic-atlas.html). The library runs in the browser and is also available as a complete local copy. Keep the output files together and preserve the relative `inputs` folder for original-PDF links.

- Library: browse text families, works, books, hymns, stories, chapters, and source editions.
- Connections: explore recurring figures, ideas, and narratives across the supplied sources.
- Passages: search every extracted or recognized source page. Spellings and diacritics vary.
- Coverage: inspect partial editions, overlaps, OCR, commentary, and known gaps.
- Click a node to focus its neighborhood. The map pages six children at a time; the library and detail list expose the rest. Drag to pan, scroll to zoom, or use Fit.
- Open source PDF links use one-based physical PDF pages, not printed page or verse numbering.
- Download the current view as SVG, or use the [complete GraphML graph](../output/atlas.graphml) and [JSON data](../output/atlas.json).

## What completeness means

Every input file and every physical PDF page has a graph record. The supplied Muktika catalog has all 108 entries mapped. All reliably extracted structural units are indexed, including the 1,028 Rigveda hymns and all observed main chapter starts in the two scanned Purana volumes.

This is **complete source coverage with a structured index and selected semantic analysis**. It is not an exhaustive scholarly annotation of every verse, embedded story, theological claim, or cross-text parallel. Some supplied files are summaries, partial editions, or drafts. Missing material has not been invented or imported. A heading labeled story is a navigation classification, not proof that every narrative unit has been separately interpreted.

## Main findings

The collection is best understood as several connected forms of literature rather than one uniform sequence of stories. The Veda files contain hymn, chant, and ritual-formula collections. The Upanishad compilation adds philosophical dialogues, contemplative instructions, renunciant teaching, and texts centered on named deities. The Purana files organize narratives alongside cosmology, genealogy, ritual, devotion, and pilgrimage. The practical guides form a separate modern layer.

Names such as Agni, Indra, Rudra, Vishnu, Yama, and Narada provide useful navigation across families, but their roles and meanings depend on the passage. Shared names and words alone do not establish one doctrine or direct literary borrowing. Brahma and Brahman are kept separate. The name Rama is flagged as potentially ambiguous.

The Rig/Sama comparison identifies **472 English phrase-overlap links** with source evidence from both supplied PDFs. These are translation-level observations, not verified Sanskrit verse equivalences or proof of historical dependence.

The Nachiketa reading path compares the Katha dialogue with the Varaha retelling. Other curated recurring cycles include Daksha and Sati, ocean churning, Matsya and the deluge, Dhruva, Prahlada and Narasimha, Vamana and Bali, Ganga, Krishna, and Rama. These remain parallel-account or theme links unless the source explicitly describes a different relationship.

## Indexed content

| Collection | Supplied coverage and indexed units |
|---|---|
| Vedas | 6 PDFs; 1,028 Rigveda hymns; 433 Whitney Atharva hymns in Books I–VII; 32 selected later-book Bloomfield hymns; 460 supplied Sama song groups; 650 observed Keith numbered passages; 40 Tulsi Ram Yajur chapters. |
| Upanishads | 1 compiled PDF; all 108 catalog texts; 31 selected story/dialogue entries; the ten Nirmalananda Giri commentaries separated; Gaudapada Karika separately identified. |
| Puranas | 20 PDFs representing 18 named works; source headings, 35 Skanda chapters, all 128 main Matsya chapters plus appendix chapters 271–273, and 31 Brahmanda continuation chapters. |
| Practical guides | 3 PDFs; 25 Ayurveda ingredient topics, 44 Vastu page topics, and all 51 supplied yoga PDF pages. |

Counts refer to observed supplied units and may use edition-specific numbering; they are not claims about canonical totals.

## Relation meanings

| Relation | Meaning and limit |
|---|---|
| contains | Navigation hierarchy, not a historical or theological derivation. |
| source | The indexed entry starts on this PDF-page witness. |
| mentions | Literal term match on the listed PDF pages. Front matter, translation notes, and commentary can be included. |
| theme | An editorial tag connecting an indexed unit to a concept. |
| shared narrative / parallel account | A source-attested comparison of accounts; differences are retained. |
| shared wording | Exact English phrase overlap in the supplied translations. |
| traditional affiliation | Veda affiliation stated in the supplied Upanishad compilation; not containment in an independent Samhita PDF. |
| commentary-on | A separately identified commentary on a primary text. |

## Source audit

| File | Pages | Text method | Low-text pages |
|---|---:|---|---:|
| inputs/Bonus/Ayurvedic-Home-RemediesEnglishEbook.pdf | 30 | Embedded PDF text | 1 |
| inputs/Bonus/Common Yoga Aasana Englishebook.pdf | 51 | Local OCR | 2 |
| inputs/Bonus/Practical_Vastu_Professional_Guide (1).pdf | 44 | Embedded PDF text | 0 |
| inputs/Puranas/Agni Puranas.pdf | 34 | Embedded PDF text | 0 |
| inputs/Puranas/Bhavisya Puranas.pdf | 13 | Embedded PDF text | 0 |
| inputs/Puranas/Brahma Puran.pdf | 5 | Embedded PDF text | 0 |
| inputs/Puranas/Brahma Vaivart Puran.pdf | 34 | Embedded PDF text | 0 |
| inputs/Puranas/Garuda Purana.pdf | 30 | Embedded PDF text | 0 |
| inputs/Puranas/Kurma Puran.pdf | 35 | Embedded PDF text | 0 |
| inputs/Puranas/Linga Purana.pdf | 27 | Embedded PDF text | 0 |
| inputs/Puranas/Markandeya Puran.pdf | 62 | Embedded PDF text | 0 |
| inputs/Puranas/Matsyapurana English .pdf | 488 | Local OCR | 13 |
| inputs/Puranas/Narad Puran.pdf | 21 | Embedded PDF text | 0 |
| inputs/Puranas/Padma puran.pdf | 32 | Embedded PDF text | 1 |
| inputs/Puranas/Shrimad Bhagwat puran.pdf | 76 | Embedded PDF text | 0 |
| inputs/Puranas/The-Skanda-Purana.pdf | 325 | Embedded PDF text | 0 |
| inputs/Puranas/Vamana puran.pdf | 47 | Embedded PDF text | 0 |
| inputs/Puranas/Varaha Purana.pdf | 37 | Embedded PDF text | 0 |
| inputs/Puranas/Vishnu puran-1.pdf | 39 | Embedded PDF text | 0 |
| inputs/Puranas/Vishnu puran-2.pdf | 40 | Embedded PDF text | 0 |
| inputs/Puranas/brahmaand purana.pdf | 248 | Local OCR | 11 |
| inputs/Puranas/shiv maha Purana-1.pdf | 47 | Embedded PDF text | 0 |
| inputs/Puranas/shiv maha Purana-2.pdf | 48 | Embedded PDF text | 0 |
| inputs/Upanishads /108upanishads compiled.pdf | 908 | Embedded PDF text | 0 |
| inputs/Vedas/Four-Vedas-English-Translation.pdf | 1446 | Embedded PDF text | 1 |
| inputs/Vedas/RigVeda.pdf | 750 | Embedded PDF text | 0 |
| inputs/Vedas/The-Sama-Veda.pdf | 214 | Embedded PDF text | 0 |
| inputs/Vedas/atharvaveda.pdf | 648 | Embedded PDF text | 18 |
| inputs/Vedas/the-4-vedas_in_1.pdf | 1109 | Embedded PDF text | 0 |
| inputs/Vedas/yajurveda.pdf | 1096 | Embedded PDF text | 0 |

A low-text page has fewer than 40 extracted characters. Many are blank leaves, plates, or tables; the original PDF is the authority. All 787 scanned PDF pages were processed locally.

## Material limits and editorial distinctions

- All 30 supplied PDFs and all 7,984 physical PDF pages are represented. All 108 catalogued Upanishads and the machine-indexed Vedic and Purana headings are navigable. Curated narrative summaries and semantic links are selective, not an exhaustive scholarly annotation of every embedded story or verse.
- Contains means an organizational parent. Source points to a PDF page. Mentions means a literal term match, including front matter or modern commentary where present. Theme and comparison links are editorial. Traditional affiliation follows the supplied compilation; none of these relations proves historical derivation.
- Every reference uses one-based PDF page numbers, not printed page or verse numbers. A section and its following commentary can begin or end on the same physical page.
- Matsya, Brahmanda, and the yoga guide required local OCR. OCR can misread names, numbers, accents, and columns. Open the original scan to check any quotation.
- Scope is the supplied PDFs, not all recensions, manuscripts, Brahmanas, Aranyakas, Sutras, or all Hindu literature.
- Rigveda: all 1,028 observed HYMN headings indexed in 10 books. Machine numbering follows heading order within each book because several Roman numerals are mistyped.
- Samaveda: 460 actual song groups from the draft compilation body, plus 51 structural nodes. The source’s inconsistent mantra totals are not treated as established counts. Stevenson’s separate OCR translation remains available through source pages.
- Yajurveda: 40 Tulsi Ram chapters indexed. Keith numbered passage headings indexed separately without assuming a one-to-one match to the 40-chapter edition. Some source references are malformed (e.g. iii.6.8 between iii.5.7 and iii.5.9; iv.8.4 between iv.3.3 and iv.3.5; vii.6.16 between vii.5.15 and vii.5.17); labels are retained with source pages.
- Atharvaveda: Whitney/Lanman volume I supplies Books I–VII only. Its Berlin numbering has 35,36,31,40,31,142,118 hymns respectively, totaling 433. Book VII includes different parenthesized Bombay numbering; no automatic equivalence is asserted.
- Bloomfield anthology introduction (Four Vedas p1313) explicitly calls itself about one third of the entire material. Later-book selections are indexed; this does not make later books complete.
- the-4-vedas-in-1 is Issue 1, Draft 2 and has many literal “Sukta text here” placeholders in the Atharva portion. These placeholders are excluded as hymn content. Its editorial merger of recensions and speculative totals are not endorsed.
- 472 Sama–Rig reading links were generated from exact 12-word English matches, with evidence on both sides. These links show translation wording overlap, not a verified philological stemma or complete identity.
- The first ten Rigveda key-summary examples and other curated summaries are editorial reading aids grounded in their cited passages. Other heading-only summaries do not claim a full interpretive analysis of each hymn.
- All 108 numbered Muktika catalog entries were found in the supplied compilation. Catalog numbers are navigation identifiers, not composition dates.
- PDF page numbers are one-based physical pages, not printed page numbers. Ten modern commentaries sometimes begin on the same PDF page as the end of the translation; both nodes therefore legitimately share a boundary page.
- The Mandukya translation proper occupies pages 181–182; Gaudapada’s separately titled Karika occupies pages 182–193, followed by Nirmalananda Giri’s modern commentary on pages 193–197.
- Nrisimhatapini is catalog item 27; the compilation supplies separate Poorva and Uttara translations and explicitly notes the alternate counting. They are child sections, not two extra entries in the 108.
- Rama Tapaniya also contains Poorva and Uttara sections; both remain children of the one catalog entry.
- Kshurika explicitly marks verses 2–9 unavailable; Yoga Chudamani marks verses 2–29 unavailable. These gaps belong to the supplied edition and are not silently filled.
- Avyakta as supplied presents transliterated Nasadiya, Hiranyagarbha and Purusha Suktas with a compiler-style introduction; it is indexed as supplied, without asserting textual-critical completeness.
- All summaries and episodes refer to the supplied translations. Extra anecdotes and interpretations inside modern commentaries are not labeled as original Upanishadic stories.
- Vedic affiliations, where recorded, follow the compilation’s traditional colophons and Muktika grouping; affiliation is not proof that the supplied independent Samhita PDF contains that Upanishad.
- Thematic comparisons are editorial navigation links. They do not establish chronology, textual derivation or uniform doctrine. Sectarian differences are retained.
- Tags record terms attested in the primary translation, including recurring invocations; they are discovery aids rather than proof of an episode-level or doctrinal relationship. Curated edges carry their own passage evidence.
- The supplied library contains 20 Purana PDFs representing 18 named Purana works. Shiva and Vishnu are each split over two overlapping files.
- Most text-readable Purana PDFs are short English overviews or retellings with modern editorial comments. A file bearing a Purana name is not evidence that the whole Sanskrit work is present.
- Skanda is explicitly Part I: Book I, Maheshvarakhanda, Section I, Kedarakhanda, chapters 1–35. PDF page = printed page + 4. Chapter 6 is corrected to PDF 46 (actual printed 42); the contents list incorrectly says 41.
- Brahma Vaivarta supplied file: introductory description and numbered narrative body differ in emphasis. Retain supplied identification and avoid certifying canonical completeness.
- Narada supplied file begins with Linga Purana carryover on PDF page 1; Narada section 18.1 begins on PDF page 2.
- Shiva volume 1 pages 47 and volume 2 page 1 overlap at sections 5.2.126–5.2.129; Vishnu volume 1 page 39 and volume 2 page 1 overlap at section 3.4.4. Keep these witnesses separate, not additional stories.
- Bhavishya prediction and historical assertions are the supplied edition’s claims. No external chronology or historical authentication was performed.
- Heading extraction gives navigable source units, not verified Sanskrit verse/chapter numbering. Numbering such as 16.10.20 belongs to the supplied retelling.
- Section summaries labeled extracted heading with passage opening are shortened source openings; curated readings are explicitly marked. Shared-narrative edges are title-attested comparison links, not historical derivation or proof of theological agreement.
- Matsya and Brahmanda initially had no extractable text; OCR-generated headings, if added by the main analysis, must retain their OCR status. Visual title evidence identifies the Matsya scan as Matsya Puranam Part I (1916), rather than a complete Purana.
- Matsya supplied scan identifies itself as Volume XVII, Part I, chapters 1–128 (title page PDF3). Its translated body occupies PDF19–380. It is not the complete canonical Matsya Purana.
- Matsya Appendix III additionally translates chapters 271–273 (PDF407–428). The remaining appendices are largely modern editorial discussions and genealogical tables, indexed separately from scripture.
- Brahmanda supplied scan identifies itself as PART III (PDF6) and Section III continuation. It contains chapters 44–74 (PDF10–248), not the whole Brahmanda Purana.
- Both PDFs are image scans. These navigation nodes use locally generated OCR, whose spelling, diacritics and Roman chapter numerals can contain recognition errors. Display titles normalize obvious heading errors; evidence excerpts preserve the OCR wording.
- Matsya chapter 13 begins on PDF57 after the chapter12 colophon without a recognizable chapter13 heading in the OCR. The boundary was identified from the following dialogue and chapter13 colophon atPDF61.
- Chapter ranges are inclusive navigation spans to the next heading page, so adjoining chapters may legitimately share one PDF page. They are not verse-level critical segmentation.
- All128 Matsya main-body chapters, its three translated appendix chapters, and all31 Brahmanda chapters are represented, totaling162 chapter nodes.
- Matsya pages429–432 have very little OCR text and appear to contain diagram or table material. They remain accessible through page navigation and are not assigned invented appendix titles.
- Editorial dates and historical identifications in the early20th-century appendices are presented as claims of that edition, not accepted current scholarship.
- Curated episode summaries are reading aids anchored to the supplied translations; the complete page text remains the place to inspect the wording.
- Visual checks: Matsya PDF19 confirms the chapterI body start; Brahmanda PDF8 confirms the chapter44–67 contents in the supplied PartIII continuation.
- Work-summary patch nodes retain the original work IDs, parent category and full PDF endpoints so the merged graph replaces pre-OCR placeholder summaries. Brahmanda PartIII is based on rendered PDF6 andPDF8, overriding an OCR error reading PartII.
- The three Bonus PDFs are practical guides, cataloged separately from the Veda, Upanishad and Purana collections.
- Ayurvedic Home Remedies has 25 ingredient entries on PDF pages 5–29, preceded by four index/instruction pages. The map does not reproduce dosing instructions or assess efficacy.
- Vastu is a modern 44-page advisory guide, not a supplied ancient Vastu scripture. Headings and topic labels describe this particular file.
- The scanned Yoga PDF contains 51 pages and ends at the Dhyana section. Sankalpa, Shantih Patha, references, Yoga Geet and expert committee items appear in its contents, but those later sections are not included as body pages in the supplied file.
- Yoga title normalization is based on OCR and the supplied contents. PDF page numbers are used throughout. Blank or illustration-dominated pages remain navigable.

## Validation and reproducibility

All node IDs, parent links, edge endpoints, and cited PDF page ranges are validated during the build. Family, work, source edition, and page are separate identities, so duplicated translations and overlapping volumes do not silently become extra canonical works. Original files are identified by SHA-256 in the source manifest.

See [the validation record](validation.json) for final checks and [browser verification](browser-validation.json) for tested interactions.

The analysis data remains editable under `analysis/`. `scripts/extract_corpus.py` preserves physical PDF page boundaries; `scripts/run_ocr.py` processes scan-only files locally; the collection analyzers generate index records; `scripts/build_atlas.py` produces JSON, GraphML, and offline browser data. Regenerating the extracted corpus alone overwrites OCR text, so run OCR again or preserve the final corpus when rebuilding.

Detailed collection notes: [Vedas](vedas-notes.md), [Upanishads](upanishads-notes.md), [Puranas](puranas-notes.md).

The companion [editable overview board](https://www.tldraw.com/f/dqkvNcwdrQ3GX4MkrPqRB) provides four overview pages. The detailed local atlas contains the complete graph and source-page index.
