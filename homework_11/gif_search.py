import questionary
from send_request import send_request
from send_request import return_urls

MIN_NUM, MAX_NUM = 1, 50

ENG_TEXT: dict = {
    "question": "What gif you want to find?",
    "limit": "How many do you want to see?",
    "instructions": f"Input a number in range {MIN_NUM}-{MAX_NUM}.",
    "query_error": "Input is empty! Please try again!",
    "num_error": "WRONG number. Please try again!",
    "query": "eng",
}

UKR_TEXT: dict = {
    "question": "Яку гіфку ти шукаєш?",
    "limit": "Скільки ти хочеш побачити?",
    "instructions": f"Введіть число в діапазоні {MIN_NUM}-{MAX_NUM}.",
    "query_error": "Ви нічого не ввели! Спробуйте ще раз!",
    "num_error": "НЕПРАВИЛЬНИЙ номер. Спробуйте ще раз!",
    "query": "uk",
}


def choose_lang() -> dict:
    languages = {
        "English": ENG_TEXT,
        "Українська": UKR_TEXT,
    }

    lang = questionary.select(
        "Choose language/Обери мову", choices=[*languages.keys()]
    ).ask()

    return languages[lang]


def get_user_input() -> tuple[str, str, str]:
    query: str = ""
    number: str = ""
    choice: dict = choose_lang()
    lang: str = choice["query"]

    while True:
        try:
            query = questionary.text(choice["question"]).ask()
            if query.strip() == "":
                raise Exception()
        except Exception:
            questionary.print(choice["query_error"], style="bold italic fg:darkred")
            continue
        break

    while True:
        try:
            number = questionary.text(
                choice["limit"], instruction=choice["instructions"]
            ).ask()

            if (
                not number.isdigit()
                or (int(number) < MIN_NUM)
                or (int(number) > MAX_NUM)
            ):
                raise Exception()
        except Exception:
            questionary.print(choice["num_error"], style="bold italic fg:darkred")
            continue
        break

    return (lang, query, number)


def print_search_results(data_list: list) -> None:
    for i, img in enumerate(data_list, start=1):
        url, title = img
        questionary.print(f"{i}: {title}:", style="bold fg:orange")
        questionary.print(f"    {url}\n", style="italic fg:#3366CC")


if __name__ == "__main__":
    input = get_user_input()
    request = send_request(*input)
    data = return_urls(request)
    print_search_results(data)
