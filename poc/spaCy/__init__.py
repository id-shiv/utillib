import spacy
language_model = spacy.load('en')

document = "Hello!!, this is poc on how spacy works. lets explore natural language processing etc. in India here today"

loaded_doc = language_model(document)
print(loaded_doc)

cleaned_words = [word for word in loaded_doc if not word.is_stop and word.pos_ != 'PUNCT']
print(cleaned_words)

word_tags = [(word.lemma_, word.pos_, word.shape_, word.ent_type_, word.ent_iob_) for word in cleaned_words]
print(word_tags)

word_entities = [(word.text, word.label_) for word in loaded_doc.ents]
print(word_entities)

sentences = [(num, sentence) for num, sentence in enumerate(loaded_doc.sents)]
print(sentences)
