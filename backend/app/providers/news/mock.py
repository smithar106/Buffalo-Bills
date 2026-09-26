"""Mock news provider — deterministic, clearly-labeled demo articles."""

from datetime import datetime, timezone

from app.models import NewsItem

ARTICLES = [
    NewsItem(
        id="n1",
        title="Allen leads Bills to 3-0 start with win over Patriots",
        publisher="Bills Mafia Wire (DEMO)",
        published_at=datetime(2026, 9, 22, 1, 30, tzinfo=timezone.utc),
        url="https://example.com/bills-patriots-recap",
        summary="Josh Allen threw for 240 yards and a score as Buffalo improved to 3-0 with a road win in Foxborough.",
    ),
    NewsItem(
        id="n2",
        title="Bills vs. Chargers set for Sunday showdown",
        publisher="Bills Mafia Wire (DEMO)",
        published_at=datetime(2026, 9, 23, 14, 0, tzinfo=timezone.utc),
        url="https://example.com/bills-chargers-preview",
        summary="Buffalo hosts San Diego in a marquee early-season AFC matchup.",
    ),
    NewsItem(
        id="n3",
        title="Injury report: Ed Oliver ruled out for Sunday",
        publisher="Bills Mafia Wire (DEMO)",
        published_at=datetime(2026, 9, 24, 14, 30, tzinfo=timezone.utc),
        url="https://example.com/bills-injury-report",
        summary="Defensive tackle Ed Oliver (ankle) is out; Curtis Samuel is questionable with a hamstring.",
    ),
    NewsItem(
        id="n4",
        title="Shakir emerging as Allen's go-to target",
        publisher="Bills Mafia Wire (DEMO)",
        published_at=datetime(2026, 9, 21, 18, 0, tzinfo=timezone.utc),
        url="https://example.com/shakir-emerging",
        summary="Khalil Shakir leads the team with 22 receptions through three games.",
    ),
    NewsItem(
        id="n5",
        title="Bills defense forcing turnovers at historic rate",
        publisher="Bills Mafia Wire (DEMO)",
        published_at=datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc),
        url="https://example.com/bills-defense",
        summary="Buffalo's defense has allowed just 17 points per game through three weeks.",
    ),
]


class MockNewsProvider:
    label = "mock"

    def search(self, query: str, limit: int = 5) -> list[NewsItem]:
        q = query.lower()
        results = [a for a in ARTICLES if q in a.title.lower() or q in a.summary.lower()]
        if not results:
            results = list(ARTICLES)
        return results[:limit]

    def recent(self, limit: int = 5) -> list[NewsItem]:
        return sorted(ARTICLES, key=lambda a: a.published_at, reverse=True)[:limit]
