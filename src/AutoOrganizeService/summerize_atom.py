from .. import AIService
from .. import index

model = AIService.LLM.model_api_map["lwai"]


def log(*args, **kwargs):
    print("[AOS]", *args, **kwargs)

def summerize(aid):
    atom = index.ATOMS[aid]

    # atom.info = {"occupied": True}
    log("Summerizing", f"<{atom.title}> ... ", end="")

    retry_times = 3
    res = 0
    while retry_times > 0:
        try:
            res = AIService.logic.summerize_atom(atom, model)
        except BaseException as e:
            print(e)
            retry_times -= 1
            log("Failed to get response, retrying...", retry_times)
            continue

        break

    if retry_times == 0:
        # Failed to get response
        log("Failed to get response after 3 attempts!")
        # atom.info = {}
        return {}

    # atom.info = res
    # atom.tags += res["tags"]
    # atom.title = res["title"] if atom.title == "New Atom" else atom.title
    log("Done.", atom.title)

    return res
