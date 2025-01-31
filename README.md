# D&D Summarizer :dragon_face: :european_castle: :pencil2: :book:
Provided a recording of DnD game session, transcribes it (DeepGram) and corrects and summarizes (OpenAI) to provide brief in-game summary.

Steps to use:
1. Create *data/recordings/* folder, put audio recording in the folder.
2. Create *data/summaries/* folder for results.
2. Create *.env* with **OPENAI_API_KEY, DEEPGRAM_API_KEY**
2. *docker build -t dnd_summarizer .*
3. *docker run --rm -v "$(pwd)/data/summaries:/app/data/summaries" dnd_summarizer --language <required_language> -c <list_of_characters>*
4. Check the folder for results.