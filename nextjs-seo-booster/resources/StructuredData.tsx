import { WithContext, Thing } from 'schema-dts';

// Decoupled from lib/constants to ensure portability
const DEFAULT_SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://example.com';

interface StructuredDataProps<T extends Thing> {
    data: WithContext<T>;
    id?: string;
}

export default function StructuredData<T extends Thing>({ data, id }: StructuredDataProps<T>) {
    return (
        <script
            id={id}
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
        />
    );
}
