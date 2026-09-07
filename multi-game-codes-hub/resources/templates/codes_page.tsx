import type { Metadata } from 'next';
import Link from 'next/link';
import { CopyButton } from '@/components/CopyButton';

const gameName = {{gameNameJson}};
const gameSlug = {{gameSlugJson}};
const baseUrl = {{baseUrlJson}};
const rewards = {{rewardsJson}};
const generatedDate = {{generatedDateJson}};
const currentMonth = {{currentMonthJson}};
const currentYear = {{currentYearJson}};

export const metadata: Metadata = {
  title: `${gameName} Codes (${currentMonth} ${currentYear}) | Active & Expired`,
  description: `Codes supplied for ${gameName}. Verify each code before use. Generated on ${generatedDate}.`,
  keywords: [
    `${gameName} codes`,
    `codes for ${gameSlug}`,
    `${gameSlug} codes ${currentYear}`,
    `roblox ${gameSlug} codes`,
    `free ${rewards}`,
  ],
  openGraph: {
    title: `${gameName} Codes - ${currentMonth} ${currentYear}`,
    description: `Codes supplied for ${gameName}. Verify each code before use.`,
    images: [`/og-${gameSlug}.webp`],
  },
  alternates: { canonical: `${baseUrl}/${gameSlug}` },
};

interface CodeEntry {
  code: string;
  reward: string;
  expiryDate?: string;
  conditions?: string;
}

interface FAQEntry {
  question: string;
  answer: string;
}

const activeCodes: CodeEntry[] = {{activeCodesData}};
const expiredCodes: CodeEntry[] = {{expiredCodesData}};
const redemptionSteps: string[] = {{redemptionStepsData}};
const faqItems: FAQEntry[] = {{faqItemsData}};

export default function CodesPage() {
{{faqSchemaDefinition}}
  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: baseUrl },
      { '@type': 'ListItem', position: 2, name: `${gameName} Codes`, item: `${baseUrl}/${gameSlug}` },
    ],
  };
  const breadcrumbSchemaMarkup = { __html: JSON.stringify(breadcrumbSchema) };

  return (
    <div className="min-h-screen bg-background text-foreground">
{{faqSchemaScript}}
      <script type="application/ld+json" dangerouslySetInnerHTML={breadcrumbSchemaMarkup} />

      <main className="container mx-auto px-4 py-8 max-w-5xl">
        <div className="mb-8">
          <Link href="/" className="text-sm text-muted-foreground hover:text-primary mb-4 inline-block">&larr; Back to Home</Link>
          <h1 className="text-3xl font-bold mb-2">{gameName} Codes ({currentMonth} {currentYear})</h1>
          <p className="text-muted-foreground">
            Codes on this page are supplied input and must be independently verified.
            Generated on <time dateTime={generatedDate}>{generatedDate}</time>.
          </p>
        </div>

        <section className="mb-12">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <span className="w-3 h-3 bg-green-500 rounded-full"></span>
            Active Codes
          </h2>
          <div className="space-y-3">
            {activeCodes.map((item, index) => (
              <div key={index} className="p-4 bg-zinc-900/60 rounded-lg border border-white/5 hover:border-green-500/30 transition-colors">
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

{{redemptionSection}}

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
                  {expiredCodes.map((item, index) => (
                    <tr key={index} className="border-b border-glass-border border-opacity-50 hover:bg-white/5 transition-colors">
                      <td className="py-2 px-4 font-mono line-through text-zinc-600">{item.code}</td>
                      <td className="py-2 px-4">{item.reward}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}

{{faqSection}}
      </main>
    </div>
  );
}
