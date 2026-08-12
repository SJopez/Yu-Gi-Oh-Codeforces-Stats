from collections import defaultdict
import json


async def unique_solved_problems(response_2):
    problems = dict()
    for sub in response_2:
        if sub.get('verdict') == 'OK':
            contesId = sub.get('contestId')
            problem_index = sub.get('problem').get('index')
            
            prog_lang = sub.get('programmingLanguage')
            tags = sub.get('problem').get('tags')
            rating = sub.get('problem').get('rating')

            #null rating == unrated contest

            problems.update({
                f'{contesId}_{problem_index}' : {
                    'prog_lang' : prog_lang,
                    'tags' : tags,
                    'rating' : rating
                } 
            })

    return problems

def normalize_lang(lang: str) -> str:
    if not lang:
        return "Otros"
    
    lang_lower = lang.lower()
    
    if "c++" in lang_lower or "g++" in lang_lower:
        return "C++"
    if "c#" in lang_lower or "mono c#" in lang_lower:
        return "C#"
    if "c11" in lang_lower or "gnu c" in lang_lower or lang_lower == "c":
        return "C"
    if "python" in lang_lower or "pypy" in lang_lower:
        return "Python"
    if "java" in lang_lower:
        return "Java"
    if "kotlin" in lang_lower:
        return "Kotlin"
    if "rust" in lang_lower:
        return "Rust"
    if "pascal" in lang_lower or "fpc" in lang_lower:
        return "Pascal"
    if "f#" in lang_lower:
        return "F#"
    
    mapping = {
        "go": "Go",
        "haskell": "Haskell",
        "javascript": "JavaScript",
        "node.js": "JavaScript",
        "scala": "Scala",
        "ruby": "Ruby",
        "php": "PHP",
        "perl": "Perl",
        "ocaml": "OCaml",
        "delphi": "Delphi",
        "d": "D",
        "tcl": "Tcl",
        "io": "Io",
        "pike": "Pike",
        "befunge": "Befunge",
        "cobol": "Cobol",
        "factor": "Factor",
        "roco": "Roco",
        "ada": "Ada",
        "false": "FALSE",
        "picat": "Picat",
        "j": "J"
    }
    
    return mapping.get(lang_lower, lang.split()[0] if lang else "Other")

async def get_pos(handle : str) -> tuple:
    
    with open('app/cache/top10_rated_cache.json', 'r') as file:
        rated_data = json.load(file)

    with open('app/cache/top10_contributors_cache.json', 'r') as file:
        contr_data = json.load(file)
    
    rate_pos = 1
    contr_pos = 1

    for user in rated_data:
        if user.get('handle') == handle:
            break
        rate_pos += 1
        
    for user in contr_data:
        if user.get('handle') == handle:
            break
        contr_pos += 1
    
    return (rate_pos if rate_pos != 11 else -1, 
            contr_pos if contr_pos != 11 else -1)
    
    
async def most_used_lang(problems) -> str:
    langs = defaultdict(int)

    for problem in problems.values():
        raw_lang = problem.get('prog_lang')
        if raw_lang:
            norm_lang = normalize_lang(raw_lang)
            langs[norm_lang] += 1
    
    if not langs:
        return ''

    best_lang = max(langs.items(), key=lambda x: x[1])
    return best_lang[0]


async def get_problems_tags(problems : dict):
    tag = defaultdict(int)

    for problem in problems.values():
        for tag_ in problem.get('tags'):
            tag[tag_] += 1

    tag = sorted(tag.items(),key = lambda x: x[1], reverse=True)
    return tag