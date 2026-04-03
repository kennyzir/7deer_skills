import { CopyButton } from './CopyButton';

interface Code {
  code: string;
  reward: string;
  expiryDate?: string;
  conditions?: string;
}

export function CodeTable({ 
  codes, 
  status 
}: { 
  codes: Code[]; 
  status: 'active' | 'expired' 
}) {
  return (
    <div className="code-table overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b border-glass-border">
            <th className="py-3 px-4 font-bold">Code</th>
            <th className="py-3 px-4 font-bold">Reward</th>
            {status === 'active' && <th className="py-3 px-4 font-bold">Expires</th>}
            {status === 'active' && <th className="py-3 px-4 font-bold">Action</th>}
          </tr>
        </thead>
        <tbody>
          {codes.map((code) => (
            <tr 
              key={code.code} 
              className={`border-b border-glass-border hover:bg-white/5 transition-colors ${
                status === 'expired' ? 'opacity-50' : ''
              }`}
            >
              <td className="py-3 px-4">
                <code className={`font-mono font-bold ${
                  status === 'active' ? 'text-green-400' : 'text-zinc-600 line-through'
                }`}>
                  {code.code}
                </code>
                {status === 'active' && (
                  <span className="ml-2 px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded">
                    Active
                  </span>
                )}
              </td>
              <td className="py-3 px-4 text-white">{code.reward}</td>
              {status === 'active' && (
                <td className="py-3 px-4 text-yellow-400">
                  {code.expiryDate || 'Unknown'}
                </td>
              )}
              {status === 'active' && (
                <td className="py-3 px-4">
                  <CopyButton code={code.code} />
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
      {code.conditions && (
        <div className="mt-2 text-xs text-muted-foreground">
          * {code.conditions}
        </div>
      )}
    </div>
  );
}
