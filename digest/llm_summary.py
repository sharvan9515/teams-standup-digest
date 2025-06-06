def summarize_with_llm(weekly_data):
    if len(weekly_data) <= 1:
        return "No data available for summarization."

    header, *rows = weekly_data
    grouped = {}

    for row in rows:
        if len(row) < 4:
            continue
        user, yest, today, block = row[:4]
        if user not in grouped:
            grouped[user] = []
        grouped[user].append((yest, today, block))

    summary = ""
    for user, updates in grouped.items():
        summary += f"\n👤 {user}:\n"
        for i, (y, t, b) in enumerate(updates):
            summary += f"  Day {i+1} → Yesterday: {y} | Today: {t} | Blockers: {b}\n"

    return summary.strip()
