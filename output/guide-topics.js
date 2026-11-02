/* Curated reading paths through the supplied sources. Steps are comparisons,
   not claims of chronology, borrowing, identical doctrine, or complete editions. */
window.GUIDE_TOPICS = [
  {
    id: 'concept-creation',
    title: 'How does the world begin?',
    description: 'Compare a Vedic question about origins, the cosmic Person, and two other presentations of creation.',
    prompt: 'Help me explore creation across the Vedas, Upanishads, and Puranas',
    aliases: ['creation', 'origin', 'origins', 'cosmology', 'universe', 'nasadiya', 'purusha', 'hiranyagarbha'],
    steps: [
      {id: 'rv-10-129', note: 'Begin with the hymn that asks about existence before creation and who can know its origin.'},
      {id: 'rv-10-90', note: 'Compare the cosmic Person and primordial sacrifice with the questioning approach of RV 10.129.'},
      {id: 'u-aitareya-upanishad', note: 'Read the account of the Self creating and entering embodied life; notice its turn toward consciousness.'},
      {id: 'p-vishnu-puran-1-3-1-1', note: 'Compare the origins section in the supplied Vishnu retelling. Its headings and numbering belong to this edition.'}
    ]
  },
  {
    id: 'concept-atman',
    title: 'Self, consciousness, and Brahman',
    description: 'Follow teaching dialogues and a Purana passage on the self. Keep Brahman distinct from the creator figure Brahma.',
    prompt: 'Help me understand Atman and Brahman with a short reading path and references',
    aliases: ['self', 'atman', 'atma', 'brahman', 'consciousness', 'tat tvam asi', 'maitreyi', 'svetaketu', 'shvetaketu'],
    steps: [
      {id: 'u-story-uddalaka-teaches-svetaketu', note: 'Start with Uddalaka’s ordinary examples and the repeated teaching “That Thou Art.”'},
      {id: 'u-story-yajnavalkya-and-maitreyi', note: 'Compare Maitreyi’s question about wealth and immortality with Yajnavalkya’s instruction to hear, reflect on, and realize the self.'},
      {id: 'u-mandukya-upanishad', note: 'Read the short primary translation on Om and states of experience. Gaudapada’s Karika and the modern commentary are separate entries.'},
      {id: 'p-agni-puranas-10-9-4', note: 'Follow the explicit discussion of atman and Brahman into the supplied Agni Purana overview; compare its own formulation.'}
    ]
  },
  {
    id: 'concept-death',
    title: 'Nachiketa, death, and the self',
    description: 'Compare Nachiketa’s philosophical dialogue with a Purana afterlife retelling, then read a Vedic funeral hymn.',
    prompt: 'Show me Nachiketa, death, and afterlife references across the books',
    aliases: ['nachiketa', 'nachiketas', 'naciketas', 'death', 'afterlife', 'yama', 'immortality', 'katha'],
    steps: [
      {id: 'u-story-nachiketas-and-death', note: 'Read why Nachiketas rejects transient rewards and asks Death what remains after a person dies.'},
      {id: 'p-varaha-purana-8-10-1', note: 'Compare the Varaha retelling’s account of Yama’s realm and conduct. It is not the same presentation as the Katha dialogue.'},
      {id: 'rv-10-14', note: 'Read the funeral hymn addressing Yama and the ancestors as another distinct setting for the theme.'}
    ]
  },
  {
    id: 'concept-sacrifice',
    title: 'Sacrifice, fire, and inward ritual',
    description: 'Move from Vedic hymns to an inward interpretation of sacrifice and a Purana narrative about a sacrificial gathering.',
    prompt: 'Connect Agni, sacrifice, and inward ritual across the PDFs',
    aliases: ['sacrifice', 'ritual', 'yajna', 'yagya', 'fire', 'agni', 'offering', 'pranagnihotra'],
    steps: [
      {id: 'rv-1-1', note: 'Begin with the opening Rigveda hymn addressed to Agni.'},
      {id: 'rv-10-90', note: 'Compare the primordial sacrifice in the Purusha hymn; it serves a cosmological setting here.'},
      {id: 'u-pranagnihotra-upanishad', note: 'Read how eating, life-breaths, and the body are interpreted as an inward sacrifice.'},
      {id: 'p-skanda-ch-2', note: 'Compare Sati’s arrival at Daksha’s sacrifice in the supplied Skanda Part I, Kedarakhanda; the available PDF is a partial edition.'}
    ]
  },
  {
    id: 'concept-devotion',
    title: 'Devotion through three stories',
    description: 'Explore Dhruva, Prahlada, and Gajendra in different supplied Purana retellings.',
    prompt: 'Recommend stories about devotion: Dhruva, Prahlada, and Gajendra',
    aliases: ['devotion', 'bhakti', 'dhruva', 'prahlada', 'prahlad', 'gajendra', 'surrender'],
    steps: [
      {id: 'p-linga-purana-17-4-1', note: 'Start with the Linga retelling’s question about Dhruva’s attainment and status among the stars.'},
      {id: 'p-vishnu-puran-1-3-1-11', note: 'Read the Prahlada and Narasimha account in the supplied Vishnu retelling, then follow its neighboring episodes.'},
      {id: 'p-shrimad-bhagwat-puran-16-8-2', note: 'Compare Gajendra’s appeal for refuge and deliverance in the supplied Bhagavata retelling.'}
    ]
  },
  {
    id: 'motif-daksha-sacrifice',
    title: 'Shiva, Sati, and Daksha’s sacrifice',
    description: 'Read parallel accounts side by side while keeping the versions’ details separate.',
    prompt: 'Compare the Shiva and Sati story at Daksha’s sacrifice across the Puranas',
    aliases: ['shiva', 'siva', 'sati', 'daksha', 'daksa', 'virabhadra', 'veerbhadra', 'daksha sacrifice'],
    steps: [
      {id: 'p-shiv-maha-purana-1-5-2-52', note: 'Begin with Sati’s death and the following Virabhadra episodes in the supplied Shiva volume 1.'},
      {id: 'p-padma-puran-2-1-5', note: 'Compare the Padma retelling’s explanation of why Sati gives up her life.'},
      {id: 'p-kurma-puran-12-12', note: 'Read Daksha’s story in the Kurma overview, which explicitly comments on differences between Purana versions.'},
      {id: 'p-skanda-ch-2', note: 'Compare Sati’s arrival in the supplied Skanda Part I, Kedarakhanda. Do not combine all versions into one presumed original account.'}
    ]
  },
  {
    id: 'concept-devi',
    title: 'Divine speech and the Goddess',
    description: 'Compare a Vedic speaking voice, an Upanishadic declaration, and Goddess narratives in the Puranas.',
    prompt: 'Help me explore Devi, divine speech, and Goddess stories across the texts',
    aliases: ['devi', 'goddess', 'shakti', 'sakti', 'durga', 'vak', 'speech', 'mahishasura'],
    steps: [
      {id: 'rv-10-125', note: 'Begin with Vak’s first-person declaration of her activity and pervasiveness.'},
      {id: 'u-devi-upanishad', note: 'Compare the Goddess’s answer to the gods, including the text’s own descriptions of Brahman, nature, and consciousness.'},
      {id: 'p-markandeya-puran-7-9-8-2', note: 'Read the gods’ radiance and weapons in the supplied Markandeya account of the Goddess fighting Mahishasura’s forces.'},
      {id: 'p-vamana-puran-6-6-3', note: 'Compare the Mahishasura episode in the Vamana retelling. A shared figure does not imply identical details or doctrine.'}
    ]
  },
  {
    id: 'concept-yoga',
    title: 'Yoga, attention, and meditation',
    description: 'Compare disciplines in Upanishadic and Purana passages, then see how a modern illustrated guide presents meditation.',
    prompt: 'Build a reading path on yoga and meditation across the Upanishads, Puranas, and yoga PDF',
    aliases: ['yoga', 'meditation', 'dhyana', 'attention', 'discipline', 'chariot', 'practice', 'yogatattva'],
    steps: [
      {id: 'u-story-the-chariot-of-the-self', note: 'Start with the chariot image: self, body, intellect, mind, and senses have distinct roles in the passage.'},
      {id: 'u-yoga-tattva-upanishad', note: 'Read the discussion of yoga, knowledge, and disciplines leading to liberation.'},
      {id: 'p-shiv-maha-purana-2-5-7-5', note: 'Compare the supplied Shiva retelling’s account of concentrating the restless mind during meditation.'},
      {id: 'b-yoga-page-51', note: 'Read the modern Common Yoga Protocol’s Dhyana page as a separate practical-guide layer. This supplied scan ends here; later contents-listed sections are absent.'}
    ]
  }
];
