#!/usr/bin/env python3

import argparse
import os
import requests
import sys
from typing import List, Tuple
from bs4 import BeautifulSoup
import openai
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def fetch_steam_libraries(username: str) -> List[Tuple[str, str]]:
    """
    Fetches a Steam user's library of games and playtimes.

    Parameters:
    username (str): The Steam username to fetch games for.

    Returns:
    List[Tuple[str, str]]: A list of games and their playtimes.
    """
    try:
        url = f"https://steamcommunity.com/id/{username}/games/?xml=1"
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, "xml")
    games = [
        (game.find("name").text, game.find("hoursOnRecord").text)
        for game in soup.find_all("game")
        if game.find("hoursOnRecord")
    ]

    games.sort(key=lambda game: float(game[1].replace(",", "")), reverse=True)

    token_limit = 1024
    pruned_games = games[:token_limit]

    logging.info("Pruned Games: %s", pruned_games)

    return pruned_games


def get_gpt4_response(prompt: str, gpt_api_key: str) -> str:
    """
    Fetches a GPT-4 response to a given prompt.

    Parameters:
    prompt (str): The prompt to get a response to.
    gpt_api_key (str): The OpenAI GPT-4 API key.

    Returns:
    str: The GPT-4 response.
    """
    openai.api_key = gpt_api_key

    try:
        messages = [{"role": "user", "content": prompt}]

        response = openai.ChatCompletion.create(
            model="gpt-4", max_tokens=650, n=1, temperature=0.7, messages=messages
        )

    except Exception as e:
        print(f"Something went wrong with the GPT-4 API: {e}")
        sys.exit(1)

    return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description='Compare Steam libraries and get game recommendations.')
    parser.add_argument('user', type=str, help='Your Steam username')
    parser.add_argument('friend', type=str, help="Your friend's Steam username")
    parser.add_argument('--key', type=str, default=os.getenv('GPT4_API_KEY'), help='OpenAI GPT-4 API Key')

    args = parser.parse_args()

    print("Fetching.. this may take a while..")
    user_library = fetch_steam_libraries(args.user)
    friend_library = fetch_steam_libraries(args.friend)

    print(f"\n\n---\n\n {args.user} ({user_library}) \n\n---\n\n {args.friend} ({friend_library}).")

    print(f"\n\nDone fetching! Amount of your games taken into consideration ({len(user_library)}). Your friend's games ({len(friend_library)})")

    print("\n\nPrompting GPT-4.. this may take a while..")
    prompt = f"Act as a gaming recommendation expert. Compare the Steam libraries of two users:\n\n---\n\n {args.user} ({user_library}) \n\n---\n\n {args.friend} ({friend_library}). \n\nSuggest what they might enjoy playing together (co-op/multiplayer). Recommend new games too, if possible. Let's work this out in a step by step way to be sure we have the right answer."

    gpt4_response = get_gpt4_response(prompt, args.key)
    print(gpt4_response)


if __name__ == "__main__":
    main()
