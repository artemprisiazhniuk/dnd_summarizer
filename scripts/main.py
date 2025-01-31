import dotenv
import os
import httpx
import argparse
from collections import defaultdict

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
from openai import OpenAI
from tqdm import tqdm

import prompts


def transcribe_audio(client, audio_file_path, language="en"):
    response = None
    
    try:
        with open(audio_file_path, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True, 
            language=language,
            punctuate=True
        )

        response = client.listen.rest.v("1").transcribe_file(payload, options, timeout=httpx.Timeout(300.0, connect=10.0))

    except Exception as e:
        print(f"Exception: {e}")
        
    return response


def generate_completion(client, system_prompt, transcribed_text, temperature=0, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": transcribed_text
            }
        ]
    )
    return response


def summarize_transcript(client, transcript, characters, temperature=0, language="en", model="gpt-4o"):
    if characters:
        characters_str = ", ".join(characters)
        
        system_prompt = prompts.get_correction_and_summarization_prompt_w_characters(
            characters_str,
            language=language
        )
    else:
        system_prompt = prompts.get_correction_and_summarization_prompt(
            language=language
        )
    
    response = generate_completion(
        client, system_prompt, transcript, 
        temperature=temperature, model=model
    )
    if not response:
        raise ValueError("Failed to transcribe audio")
    result = response.choices[0].message.content

    return result


def summarize_summaries(client, summaries, characters, temperature=0, language="en", model="gpt-4o"):
    if characters:
        characters_str = ", ".join(characters)
        
        system_prompt = prompts.get_correction_and_summarization_prompt_w_characters(
            characters_str,
            language=language
        )
    else:
        system_prompt = prompts.get_correction_and_summarization_prompt(
            language=language
        )
    
    summary = "\n".join(summaries)
    
    response = generate_completion(
        client, system_prompt, summary, 
        temperature=temperature, model=model
    )
    if not response:
        raise ValueError("Failed to transcribe audio")
    result = response.choices[0].message.content

    return result


def main(args):
    openai_client = OpenAI()
    deepgram_client = DeepgramClient()
    
    if args.audio_file:
        filenames = [args.audio_file]
    else:
        filenames = os.listdir(args.audio_path)
        
    parts_dict = defaultdict(list)
      
    if not parts_dict:  
        for filename in tqdm(filenames):
            if filename.startswith("."):
                continue
            
            response = transcribe_audio(deepgram_client, os.path.join(args.audio_path, filename), language=args.language)
            if not response:
                raise ValueError("Failed to transcribe audio")
            result = response.results.channels[0].alternatives[0].transcript
            
            filename = os.path.basename(filename).split(".")[0]
            
            with open(os.path.join(args.transcription_path, f"{filename}.txt"), "w") as file:
                file.write(result)
            
            summary = summarize_transcript(openai_client, result, args.characters, temperature=args.temperature, language=args.language, model=args.model)
            
            with open(os.path.join(args.summary_path, f"{filename}.txt"), "w") as file:
                file.write(summary)
                
            if "_part_" in filename:
                general_filename = filename.split("_part_")[0]
                parts_dict[general_filename].append(os.path.join(args.summary_path, f"{filename}.txt"))
            
    if parts_dict:
        for general_filename, parts in tqdm(parts_dict.items()):
            texts = []
            
            for part in sorted(parts):
                with open(part, "r") as part_file:
                    summary_ = part_file.read()
                texts.append(summary_)
                os.remove(part)
                
            summary = summarize_summaries(openai_client, texts, args.characters, temperature=args.temperature, language=args.language, model=args.model)
            
            with open(os.path.join(args.summary_path, f"{general_filename}.txt"), "w") as file:
                file.write(summary)
                    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ap", "--audio-path", type=str, default="data/recordings/")
    parser.add_argument("-a", "--audio-file", type=str, default=None, help="(Optional) Path to specific file to transcribe")
    parser.add_argument("-tp", "--transcription-path", type=str, default="data/transcriptions/")
    parser.add_argument("-sp", "--summary_path", type=str, default="data/summaries/")
    parser.add_argument("-c", "--characters", type=str, nargs="+", help="(Optional) List of characters")
    parser.add_argument("-m", "--model", type=str, default="gpt-4o")
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--language", type=str, default="ru", help="Language code for the audio file, used in DeepGram")
    args = parser.parse_args()
    
    dotenv.load_dotenv()
    
    main(args)
    
