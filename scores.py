SCORES_FILE = "scores.txt"

def save_score(score):
        try:
            with open(SCORES_FILE, "a") as f:
                f.write(str(score) + "\n")
        except OSError:
            pass

def load_score():
    scores = []
    try:
        with open(SCORES_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line.isdigit():
                    scores.append(int(line))
    except FileNotFoundError:
        return []
    return scores

def get_top_scores(scores):
    scores = load_score()
    unique = sorted(set(scores), reverse=True)
    return unique[:5]