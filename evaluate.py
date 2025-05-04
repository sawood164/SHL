# evaluate.py

def recall_at_k(recommended, relevant, k=3):
    recommended_at_k = recommended[:k]
    relevant_set = set(relevant)
    return len([item for item in recommended_at_k if item in relevant_set]) / len(relevant_set) if relevant_set else 0

def average_precision_at_k(recommended, relevant, k=3):
    relevant_set = set(relevant)
    if not relevant_set:
        return 0
    score = 0.0
    num_hits = 0
    for i, item in enumerate(recommended[:k]):
        if item in relevant_set:
            num_hits += 1
            score += num_hits / (i + 1)
    return score / min(len(relevant_set), k)

def evaluate_all(queries_results, k=3):
    recalls = []
    map_scores = []
    for query in queries_results:
        recommended = query['recommended']
        relevant = query['relevant']
        recalls.append(recall_at_k(recommended, relevant, k))
        map_scores.append(average_precision_at_k(recommended, relevant, k))
    mean_recall = sum(recalls) / len(recalls) if recalls else 0
    mean_ap = sum(map_scores) / len(map_scores) if map_scores else 0
    return mean_recall, mean_ap


# Sample test data
if __name__ == "__main__":
    test_queries = [
        {
            "query": "Hiring Java devs under 45 mins",
            "recommended": ["Java Basics", "SQL Intermediate", "Python Fundamentals"],
            "relevant": ["Java Basics", "SQL Intermediate"]
        },
        {
            "query": "Analyst cognitive & personality test",
            "recommended": ["Cognitive Aptitude", "Personality Fit", "Excel Skills"],
            "relevant": ["Cognitive Aptitude", "Personality Fit"]
        },
        {
            "query": "Mid-level Python, JS, SQL",
            "recommended": ["Python Intermediate", "SQL Advanced", "JS Fundamentals"],
            "relevant": ["Python Intermediate", "SQL Advanced", "JS Fundamentals"]
        }
    ]

    mean_recall, mean_ap = evaluate_all(test_queries, k=3)
    print("🎯 Mean Recall@3:", round(mean_recall, 3))
    print("📊 MAP@3:", round(mean_ap, 3))
