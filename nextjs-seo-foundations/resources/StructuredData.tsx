import { WithContext, Thing } from 'schema-dts';

export default function StructuredData<T extends Thing>({ data }: { data: WithContext<T> }) {
    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
        />
    );
}

/* Example Usage:
   <StructuredData<FAQPage>
      data={{
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        mainEntity: [...]
      }}
   />
*/
