#!/usr/bin/env python3.8

from bs4 import BeautifulSoup
from glob import glob
import json
import unicodedata


def clean(txt):
    # Found this online, NYTimes includes '\xa0' which is raw ascii ' '
    # character,
    # this gets rid of that
    return unicodedata.normalize("NFKD", txt.strip())


# types of variables are not explicit in python, but they are enforced,
# - lists: a list of strings
# - title: a string
def ul(lists, title, count=2):
    # f-strings allow you to insert variables inside of strings
    # when you write out = ... this creates a variable called out
    # it can then be used anywhere inside this function (def<name>())
    # python figures out this is a String, so it will only allow you to
    # do things strings can do.
    hashes = '#' * count
    out = f"{hashes} {title}\n\n"
    for item in lists:
        out += f"- {item}\n"
    return out

# types of variables are not explicit in python, but they are enforced,
# - lists: a list of strings
# - title: a string


def ul_dict(lists, title, count=2):
    # f-strings allow you to insert variables inside of strings
    # when you write out = ... this creates a variable called out
    # it can then be used anywhere inside this function (def<name>())
    # python figures out this is a String, so it will only allow you to
    # do things strings can do.
    hashes = '#' * count
    out = f"{hashes} {title}\n\n"
    for item in lists:
        out += f"- {item}: {lists[item]}\n"
    return out


# types of variables are not explicit in python, but they are enforced,
# - lists: a list of strings
# - title: a string
def ol(lists, title, count=2):
    hashes = '#' * count
    out = f"{hashes} {title}\n\n"
    # enumerate gives us every item in a list and it's index
    for idx, item in enumerate(lists):
        out += f"{idx+1}. {item}\n"
    return out


with open("captured.txt", "a") as c:
    for path in glob("/Users/dustinknopoff/Documents/1-Areas/Recipes/nytcooking-scraper/raw_html/*.html"):
        with open(path, 'r') as f:
            contents = BeautifulSoup(f.read(), 'html.parser')
            ctx = contents.find(
                "script", {"type": "application/ld+json"}).get_text()
            link = contents.find("link", {"rel": "canonical"})["href"]
            ctx = clean(ctx)
            ctx = json.loads(ctx)
            name = ctx["name"]
            print(name)
            description = ctx["description"]
            author = ctx["author"]["name"]
            image = ctx["image"]
            totalTime = ctx.get("totalTime")
            totalTimeStr = ""
            if totalTime:
                totalTime = totalTime.replace("PT", "").replace(
                    "H", "h ").replace("M", "m")
                totalTimeStr = f'in {totalTime}'
            recipeYield = ctx["recipeYield"]
            recipeCuisine = ctx["recipeCuisine"].strip().replace(" ", "_")
            recipeCategory = " ".join(
                [f"#{x.replace(' ', '_').replace('#', '')}" for x in ctx["recipeCategory"]
                 .split(", ")])
            nutrition = ctx.get("nutrition")
            if nutrition:
                nutrition.pop("@context", None)
                nutrition.pop("@type", None)
            ingredients = ctx["recipeIngredient"]
            instructions = map(lambda x: x["text"], ctx["recipeInstructions"])
            as_markdown = f"""# {name}

By: {author}

![]({image})

{description}

Yields: {recipeYield} {totalTimeStr}

#{recipeCuisine} {recipeCategory}

{ul(ingredients, "Ingredients")}

{ol(instructions, "Instructions")}

{ul_dict(nutrition, "Nutrition", count=3) if nutrition else ""}

Source: [{name}]({link})
"""
            path_name = name.replace(" ", "-")
            with open(f"./md/{path_name}.md", "w") as out:
                out.write(as_markdown)
            c.write(f"{link}\n")
