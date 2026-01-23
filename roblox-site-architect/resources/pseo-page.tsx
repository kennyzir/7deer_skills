import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { DATA_ITEMS } from "@/data/items"; // You need to implement this
import { CONFIG } from "@/lib/config"; // You need to implement this

// 1. Generate Static Params for SSG
export async function generateStaticParams() {
    return DATA_ITEMS.map((item) => ({
        slug: item.slug,
    }));
}

// 2. Dynamic Metadata
export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
    const item = DATA_ITEMS.find((p) => p.slug === params.slug);
    if (!item) return {};

    const title = CONFIG.seo.titleTemplate.replace('%s', item.name);
    const description = CONFIG.seo.descriptionTemplate.replace('%s', item.name);

    return {
        title,
        description,
        openGraph: {
            title,
            description,
            images: [{ url: item.image || '/images/og-default.jpg' }],
        },
    };
}

// 3. Page Component
export default function PSEOPage({ params }: { params: { slug: string } }) {
    const item = DATA_ITEMS.find((p) => p.slug === params.slug);
    if (!item) notFound();

    return (
        <main className="container mx-auto px-4 py-8">
            {/* Header Section */}
            <h1 className="text-4xl font-bold mb-4">
                {item.name} Stats & Location ({CONFIG.seo.version})
            </h1>

            {/* Quick Answer Box (Featured Snippet Optimization) */}
            <div className="bg-slate-800 border-l-4 border-yellow-500 p-6 mb-8">
                <h3 className="text-xl font-bold mb-2">Quick Summary</h3>
                <p>{item.quickAnswer || item.description}</p>
            </div>

            {/* Deep Link to Core Tool */}
            <div className="my-8">
                <a
                    href={`/build-planner?item=${item.slug}`}
                    className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition"
                >
                    Use {item.name} in Build Planner &rarr;
                </a>
            </div>

            {/* Stats Table */}
            <section className="mb-8">
                <h2 className="text-2xl font-bold mb-4">Stats breakdown</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {Object.entries(item.stats || {}).map(([key, value]) => (
                        <div key={key} className="bg-slate-900 p-4 rounded">
                            <div className="text-gray-400 text-sm uppercase">{key}</div>
                            <div className="text-2xl font-mono">{String(value)}</div>
                        </div>
                    ))}
                </div>
            </section>

            {/* Dynamic UGC Section (Comments) */}
            <section className="mt-12">
                <h2 className="text-2xl font-bold mb-4">Community Discussion</h2>
                <p className="text-gray-400">Is {item.name} currently meta in {CONFIG.seo.version}? Vote below.</p>
                {/* <Giscus /> component goes here */}
            </section>
        </main>
    );
}
