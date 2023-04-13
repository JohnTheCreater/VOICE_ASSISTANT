import speech_recognition as sr
import math
import time
from datetime import datetime
import serial
import boto3
import sys
import openai
import pygame
from pygame import mixer


mixer.init()

# model_to_use = "text-davinc3"  # most capable
# model_to_use = "text-curie-001"
# model_to_use = "text-babbage-001"
model_to_use = "text-curie-001"  # lowest token cost

r = sr.Recognizer()
openai.api_key = ("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")

# Initialize AWS Polly client
client = boto3.client('polly', region_name='us-west-2')


def chatGPT(query, num_responses=1):

    response_text = ''
    usage = 0
    for i in range(num_responses):
        response = openai.Completion.create(
            model=model_to_use,
            prompt=query,
            temperature=0,
            max_tokens=1000 - usage)
        text = str.strip(response['choices'][0]['text'])
        response_text += text + ' '
        usage += response['usage']['total_tokens']
        if 'stop' in text.lower() or 'end' in text.lower():
            break
    return response_text, usage


def main():
    print('LED is ON while button is pressed(Ctrl-C for exit).')
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            print("Recognizing Now....")
        try:
            output_direct = 'D:\\download\\voice\\'
            command = str(r.recognize_google(audio))
            print(f"you said: {command}")
            query = command
            response_text, usage = chatGPT(query)
            print(response_text)
            response = client.synthesize_speech(
                OutputFormat='mp3',
                Text=response_text,
                VoiceId='Joanna')
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"out_{current_time}.mp3"
            with open(filename, 'wb') as f:

                f.write(response['AudioStream'].read())

            mixer.music.load(filename)
            mixer.music.play()

    # wait for audio to finish playing

    # cleanup

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))


if __name__ == '__main__':
    main()
