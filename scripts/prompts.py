def get_correction_and_summarization_prompt(characters_str=None, language="en"):
    flag = characters_str is not None
    
    return {
        "ru": "Ты хорошо пересказываешь транскрипты игр по Dungeon&Dragons. Это часть сессии игры группы героев. " + \
        "Твоя задача - пересказать этот транскрипт, исправив ошибки, которые могли возникнуть в процессе распознавания речи. Пересказывай используя только информацию в тексте. " + \
        "Сначала раздели текст на отдельные части: сцена считается отдельной частью, если она происходит в новой локации. Затем кратко (до 3 предложений) перескажи каждую часть. " + \
        "Если предпринималось несколько попыток решить проблему, используй только финальный результат. " + \
        "Добавляй только необходимую пунктуацию и капитализацию, кратко перескажи сессию, убрав лишние детали. Развитие персонажей считается важной деталью. Игнорируй диалоги, не относящиеся к игре. " + \
        "Пересказ не должен быть длиннее 5 предложений. " + \
        "Think step-by-step. " + \
        f"Убедись, что следующие названия персонажей правильно записаны: {characters_str}. " * flag,
        
        "en": "You are good at summarizing Dungeon&Dragons game transcripts. This is a part of game session of a group of heroes. " + \
        "Your task is to summarize this transcript, correcting any errors that may have occurred during the speech recognition process. Summarize only using information in the text. " + \
        "First, divide the text into separate parts: a scene is considered a separate part if it takes place in a new location. Then briefly (up to 3 sentences) summarize each part. " + \
        "If multiple attempts were made to solve the problem, use only the final result. " + \
        "Add only the necessary punctuation and capitalization, briefly summarize the session, removing unnecessary details. Character development is considered an important detail. Ignore dialogues that are not related to the game. " + \
        "The summary should not be longer than 5 sentences. " + \
        "Think step-by-step. " + \
        f"Make sure that the following character names are correctly transcripted: {characters_str}. " * flag
    }[language]