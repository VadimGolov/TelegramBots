from random import choice
from pathlib import Path


def recipe_numbers(request_txt: str) -> list[int]:

    info_path: Path = Path('cookbook/info.txt')
    info_list: list[str] = info_path.read_text(encoding='utf-8').splitlines()

    request_list: list[str] = [item.strip().casefold() for item in request_txt.split(',')]
    request_nums: list[int] = []
    for line in info_list:
        if all([item in line for item in request_list]):
            dot_position: int = line.find('.')
            request_nums.append(int(line[:dot_position]))

    if len(request_nums) == 0:
        return [-1]

    return request_nums


def recipe_names(request_text: str) -> list[dict]:

    recipe_nums: list[int] = recipe_numbers(request_text)

    if recipe_nums[0] == -1:
        return [{'name': 'Error'}]

    recipe_path: Path = Path('cookbook/recipes_book.txt')
    recipe_list: list[str] = recipe_path.read_text(encoding='utf-8').splitlines()

    cook_recipes: list[dict] = []
    count: int = 0

    while True:

        cur_line: str = recipe_list[count]

        if cur_line == '+':
            count += 1
            cur_line: str = recipe_list[count]

            dot_position: int = cur_line.find('.')
            cur_num: int = int(cur_line[:dot_position])

        elif cur_line == '#':
            return cook_recipes

        else:
            count += 1
            continue

        if cur_num in recipe_nums:
            cook_name: str = cur_line[dot_position + 1:]
            cook_content: str = extract_recipe(count + 1, recipe_list)

            cur_dict: dict[str, str] = {'name': cook_name, 'content': cook_content}
            cook_recipes.append(cur_dict)

    return cook_recipes


def extract_recipe(first_line: int, cook_list: list[str]) -> str:

    recipe_text = ''

    for index in range(first_line, len(cook_list)):
        if cook_list[index] == '+' or cook_list[index] == '#':
            break
        else:
            recipe_text += cook_list[index]

    return recipe_text


def reduce_names(cook_list: list[dict]) -> list[dict]:

    upper_bound: int = 12
    short_list: list[dict] = []

    if len(cook_list) <= upper_bound:
        return cook_list

    for _ in range(upper_bound):

        short_list.append(choice(cook_list))
        short_index: int = len(short_list) - 1
        short_item: dict[str, str] = short_list[short_index]

        cook_list: list[dict] = [item for item in cook_list if item != short_item]

    return short_list