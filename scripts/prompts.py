def get_correction_and_summarization_prompt_w_characters(characters_str, language="en"):
    return {
        "ru": f"""
    Ты хорошо пересказываешь транскрипты игр по Dungeon&Dragons. Это сессия игры в группы героев, состоящей из {characters_str}.
    Твоя задача - пересказать этот транскрипт, исправив ошибки, которые могли возникнуть в процессе распознавания речи. Убедись, что следующие названия персонажей правильно записаны: {characters_str}.
    Добавляй только необходимую пунктуацию и капитализацию, кратко перескажи сессию, убрав лишние детали. Игнорируй диалоги, не относящиеся к игре.
        """,
        "en": f"""
    You are good at summarizing Dungeon&Dragons game transcripts. This is a game session of a group of heroes consisting of {characters_str}.
    Your task is to summarize this transcript, correcting any errors that may have occurred during the speech recognition process. Make sure that the following character names are correctly transcripted: {characters_str}.
    Add only the necessary punctuation and capitalization, briefly summarize the session, removing unnecessary details. Ignore dialogues that are not related to the game.
        """
    }[language]
    
def get_correction_and_summarization_prompt(language="en"):
    return {
        "ru": f"""
    Ты хорошо пересказываешь транскрипты игр по Dungeon&Dragons. Это сессия игры группы героев.
    Твоя задача - пересказать этот транскрипт, исправив ошибки, которые могли возникнуть в процессе распознавания речи.
    Добавляй только необходимую пунктуацию и капитализацию, кратко перескажи сессию, убрав лишние детали. Игнорируй диалоги, не относящиеся к игре.
        """,
        "en": f"""
    You are good at summarizing Dungeon&Dragons game transcripts. This is a game session of a group of heroes.
    Your task is to summarize this transcript, correcting any errors that may have occurred during the speech recognition process.
    Add only the necessary punctuation and capitalization, briefly summarize the session, removing unnecessary details. Ignore dialogues that are not related to the game.
        """
    }[language]