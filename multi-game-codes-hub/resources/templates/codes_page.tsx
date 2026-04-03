import type { Metadata } from 'next';
import Link from 'next/link';
import { CopyButton } from '@/components/CopyButton';

export const metadata: Metadata = {
  title: '{{gameName}} Codes ({{currentMonth}} {{currentYear}}) | Active & Expired',
  description: 'All working {{gameName}} codes for {{currentMonth}} {{currentYear}}. Get free {{rewards}}. Updated daily with new codes!',
  keywords: [
    '{{gameName}} codes',
    'codes for {{gameSlug}}',
    '{{gameSlug}} codes {{currentYear}}',
    'roblox {{gameSlug}} codes',
    'free {{rewards}}',
  ],
  openGraph: {
    title: '{{gameName}} Codes - {{currentMonth}} {{currentYear}} (Verified Daily)',
    description: 'Free {{rewards}} for {{gameName}}. One-click copy, verified daily.',
    images: ['/og-{{gameSlug}}.webp'],
  },
  alternates: { canonical: 'https://jujutsucalc.com/{{gameSlug}}' },
};

interface CodeEntry {
  code: string;
  reward: string;
  expiryDate?: string;
  conditions?: string;
}

const activeCodes: CodeEntry[] = {{activeCodesData}};

const expiredCodes: CodeEntry[] = {{expiredCodesData}};

const faqItems = [
  {
    q: 'How do I redeem {{gameName}} codes?',
    a: 'Open {{gameName}}, click the Settings or Menu icon, find the "Codes" or "Redeem" button, enter the code exactly as shown (case-sensitive), and click Submit or Redeem.',
  },
  {
    q: 'Why isn\'t my {{gameName}} code working?',
    a: 'Codes are case-sensitive and may have expired. Double-check spelling, ensure no extra spaces, and verify the code is still active in our table above.',
  },
  {
    q: 'How often are new {{gameName}} codes released?',
    a: 'New codes typically drop with major updates, milestone celebrations (like subscriber/like goals), and seasonal events. Check back daily for updates!',
  },
  {
    q: 'Do {{gameName}} codes expire?',
    a: 'Yes, most codes expire after a few weeks or when the next update is released. We update this page daily to mark expired codes.',
  },
];

export default function {{gameSlug}}CodesPage() {
  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqItems.map(f => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a },
    })),
  };

  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://jujutsucalc.com' },
      { '@type': 'ListItem', position: 2, name: '{{gameName}} Codes', item: 'https://jujutsucalc.com/{{gameSlug}}' },
    ],
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }} />

      <main className="container mx-auto px-4 py-8 max-w-5xl">
        <div className="mb-8">
          <Link href="/" className="text-sm text-muted-foreground hover:text-primary mb-4 inline-block">&larr; Back to Home</Link>
          <h1 className="text-3xl font-bold mb-2">{{gameName}} Codes ({{currentMonth}} {{currentYear}})</h1>
          <p className="text-muted-foreground">
            All working codes for {{gameName}}. Get free {{rewards}}. Verified daily.
            Last updated: <time dateTime="{{lastUpdated}}">{{lastUpdated}}</time>.
          </p>
        </div>

        {/* Active Codes Section */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <span className="w-3 h-3 bg-green-500 rounded-full animate-pulse shadow-[0_0_10px_rgba(34,197,94,0.6)]"></span>
            Active Codes
          </h2>
          <div className="space-y-3">
            {activeCodes.map((item, idx) => (
              <div key={idx} className="p-4 bg-zinc-900/60 rounded-lg border border-white/5 hover:border-green-500/30 transition-colors">
                <div className="flex justify-between items-start mb-2">
                  <code className="text-xl font-mono font-bold text-green-400 drop-shadow-md">{item.code}</code>
                  <CopyButton code={item.code} />
                </div>
                <div className="text-sm font-medium text-white mb-1">Reward: {item.reward}</div>
                {item.conditions && (
                  <div className="text-xs text-muted-foreground bg-black/30 inline-block px-2 py-1 rounded">
                    {item.conditions}
                  </div>
                )}
                {item.expiryDate && (
                  <div className="text-xs text-yellow-400 mt-2">
                    Expires: {item.expiryDate}
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* How to Redeem Section */}
        <section className="mb-12 p-6 bg-gradient-to-br from-zinc-900 to-black border border-zinc-800 rounded-lg">
          <h2 className="text-2xl font-bold mb-4">How to Redeem {{gameName}} Codes</h2>
          <ol className="list-decimal list-inside space-y-3 text-sm text-zinc-400">
            <li>Launch <strong className="text-white">{{gameName}}</strong> on Roblox.</li>
            <li>Look for the <strong className="text-white">Settings</strong> or <strong className="text-white">Menu</strong> button (usually a gear icon).</li>
            <li>Find and click the <strong className="text-white">&quot;Codes&quot;</strong> or <strong className="text-white">&quot;Redeem Code&quot;</strong> button.</li>
            <li>Copy a code from the table above using the copy button.</li>
            <li>Paste the code into the text box (codes are case-sensitive!).</li>
            <li>Click <strong className="text-white">Submit</strong> or <strong className="text-white">Redeem</strong> to claim your rewards.</li>
          </ol>
          <div className="mt-4 p-4 bg-yellow-500/10 border-l-4 border-yellow-500 rounded-r">
            <h4 className="font-bold text-yellow-300 mb-2">⚠️ Code Not Working?</h4>
            <ul className="text-sm text-zinc-400 space-y-1">
              <li>• Codes are <strong className="text-white">case-sensitive</strong> — copy them exactly</li>
              <li>• Remove any extra spaces before or after the code</li>
              <li>• Check if the code has expired (see Expired Codes section)</li>
              <li>• Some codes may have already been redeemed on your account</li>
            </ul>
          </div>
        </section>

        {/* Related Content */}
        <section className="mb-12 p-6 border border-purple-500/30 rounded-xl bg-purple-500/5">
          <h2 className="text-xl font-bold mb-3 text-purple-300">More {{gameName}} Guides</h2>
          <p className="text-sm text-zinc-400 mb-4">
            Got your rewards? Check out our other guides to maximize your gameplay:
          </p>
          <div className="flex flex-wrap gap-3">
            <Link href="/tier-list" className="px-5 py-2 bg-purple-600/20 text-purple-300 border border-purple-500/30 rounded-lg hover:bg-purple-600/30 transition-colors text-sm font-medium">
              Tier List →
            </Link>
            <Link href="/wiki" className="px-5 py-2 bg-blue-600/20 text-blue-300 border border-blue-500/30 rounded-lg hover:bg-blue-600/30 transition-colors text-sm font-medium">
              Wiki & Guides →
            </Link>
            <Link href="/wiki/trading/value-list" className="px-5 py-2 bg-green-600/20 text-green-300 border border-green-500/30 rounded-lg hover:bg-green-600/30 transition-colors text-sm font-medium">
              Trading Values →
            </Link>
          </div>
        </section>

        {/* Expired Codes */}
        {expiredCodes.length > 0 && (
          <section className="mb-12">
            <h2 className="text-xl font-bold mb-4 text-zinc-500 border-b border-glass-border pb-2">
              Expired Codes (Reference)
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm text-muted-foreground">
                <thead>
                  <tr className="border-b border-glass-border">
                    <th className="py-2 px-4">Code</th>
                    <th className="py-2 px-4">Previous Reward</th>
                  </tr>
                </thead>
                <tbody>
                  {expiredCodes.map((item, idx) => (
                    <tr key={idx} className="border-b border-glass-border border-opacity-50 hover:bg-white/5 transition-colors">
                      <td className="py-2 px-4 font-mono line-through text-zinc-600">{item.code}</td>
                      <td className="py-2 px-4">{item.reward}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {/* FAQ Section */}
        <section className="mb-8">
          <h2 className="text-xl font-bold mb-4">Frequently Asked Questions</h2>
          <div className="space-y-4">
            {faqItems.map((f, i) => (
              <details key={i} className="group border border-glass-border rounded-lg bg-card/40">
                <summary className="cursor-pointer p-4 font-medium text-zinc-200 group-open:border-b group-open:border-glass-border">
                  {f.q}
                </summary>
                <div className="p-4 text-sm text-zinc-400">{f.a}</div>
              </details>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
