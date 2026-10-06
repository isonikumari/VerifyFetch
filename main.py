from concurrent.futures import ThreadPoolExecutor

from agents import planner_chain, writer_chain, critic_chain, reviser_chain
from tools import web_search


MAX_ROUNDS = 3
PASS_SCORE = 8


def run_fact_check(claim: str, review: bool = False) -> dict:
    state = {}

    with ThreadPoolExecutor(max_workers=2) as executor:
        planner_future = executor.submit(planner_chain.invoke, {"claim": claim})
        search_future = executor.submit(web_search.invoke, {"query": claim})
        state["sub_claims"] = planner_future.result()
        state["evidence"] = search_future.result()

    state["report"] = writer_chain.invoke({
        "claim": claim,
        "evidence": state["evidence"],
    })
    state["feedback"] = "Review skipped for a faster result."

    if review:
        for _ in range(MAX_ROUNDS):
            feedback = critic_chain.invoke({
                "evidence": state["evidence"],
                "report": state["report"],
            })
            if extract_score(feedback) >= PASS_SCORE:
                break

            state["report"] = reviser_chain.invoke({
                "report": state["report"],
                "feedback": feedback,
                "evidence": state["evidence"],
            })

        state["feedback"] = feedback
    return state

def extract_score(feedback: str) -> int:
    try:
        line = [l for l in feedback.splitlines() if "Score" in l][0]
        return int(line.split(":")[1].split("/")[0].strip())
    except Exception:
        return 0

if __name__ == "__main__":
    claim = input("\nEnter a claim to fact-check: ")
    result = run_fact_check(claim)
    print("\n" + "="*50)
    print("FINAL REPORT")
    print("="*50)
    print(result["report"])