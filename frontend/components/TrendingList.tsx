import type { NewsItem } from "@/types";
import { timeAgo } from "@/lib/format";

export default function TrendingList({ news }: { news: NewsItem[] }) {
  return (
    <div className="overflow-hidden rounded-sm border border-bills-navy/10 bg-white shadow-card">
      <div className="flex items-center justify-between border-b border-bills-navy/10 px-5 py-3">
        <h2 className="font-display text-sm font-bold uppercase tracking-wide text-bills-red">
          Trending
        </h2>
      </div>
      <ul className="divide-y divide-bills-navy/5">
        {news.map((item) => (
          <li key={item.id}>
            <a
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              className="block px-5 py-3 transition-colors hover:bg-bills-silver"
            >
              <p className="text-sm font-semibold leading-snug text-bills-navy">
                {item.title}
              </p>
              <div className="mt-1 flex items-center gap-2 text-xs text-bills-steel">
                <span>{item.publisher}</span>
                <span>·</span>
                <span>{timeAgo(item.published_at)}</span>
              </div>
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
