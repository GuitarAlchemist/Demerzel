import json
from datetime import datetime

def load_events(filepath):
    events = []
    with open(filepath, 'r') as f:
        for line in f:
            events.append(json.loads(line))
    return events

def compute_kpis(events):
    kpis = {
        "avg_issue_to_pr_latency": 0,
        "avg_pr_to_merge_latency": 0,
        "total_cost": 0,
        "merged_prs": 0,
        "ci_pass_rate": 0
    }

    issue_created = {}
    pr_created = {}
    ci_runs = 0
    ci_success = 0
    total_latency_issue_pr = 0
    total_latency_pr_merge = 0

    for e in events:
        ts = datetime.fromisoformat(e['timestamp'].replace('Z', ''))

        if e['event'] == 'issue_opened':
            issue_created[e['issue_id']] = ts

        elif e['event'] == 'pr_opened':
            pr_created[e['pr_id']] = ts
            issue_id = e.get('issue_id')
            if issue_id in issue_created:
                latency = (ts - issue_created[issue_id]).total_seconds() / 60
                total_latency_issue_pr += latency
                kpis['merged_prs'] += 1 # Rough count for now

        elif e['event'] == 'pr_merged':
            pr_id = e['pr_id']
            if pr_id in pr_created:
                latency = (ts - pr_created[pr_id]).total_seconds() / 60
                total_latency_pr_merge += latency
            kpis['total_cost'] += e.get('cost_usd', 0)

        elif e['event'] == 'ci_run':
            ci_runs += 1
            if e['status'] == 'success':
                ci_success += 1

    if kpis['merged_prs'] > 0:
        kpis['avg_issue_to_pr_latency'] = total_latency_issue_pr / kpis['merged_prs']
        kpis['avg_pr_to_merge_latency'] = total_latency_pr_merge / kpis['merged_prs']

    if ci_runs > 0:
        kpis['ci_pass_rate'] = ci_success / ci_runs

    return kpis

def generate_recommendation(events):
    # Mock logic: Jules is good at implementation
    return {
        "issue_or_pr": "ga#486",
        "required_capability": "implementation",
        "recommended_worker": "jules",
        "confidence": 0.95,
        "rationale": "Historical data shows Jules has a 100% success rate on implementation tasks with low latency.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def main():
    events = load_events('fixtures/streeling-events-sample.jsonl')
    kpis = compute_kpis(events)
    recommendation = generate_recommendation(events)

    print("=== Seldon Engineering Intelligence Summary ===")
    print(f"Avg Issue to PR Latency: {kpis['avg_issue_to_pr_latency']:.2f} minutes")
    print(f"Avg PR to Merge Latency: {kpis['avg_pr_to_merge_latency']:.2f} minutes")
    print(f"CI Pass Rate: {kpis['ci_pass_rate'] * 100:.1f}%")
    print(f"Total Cost: ${kpis['total_cost']:.2f}")
    print(f"Cost per Merged PR: ${kpis['total_cost'] / kpis['merged_prs']:.2f}" if kpis['merged_prs'] > 0 else "N/A")

    print("\n=== Advisory Routing Recommendation ===")
    print(json.dumps(recommendation, indent=2))

if __name__ == "__main__":
    main()
