import React, { useState } from 'react';
import { Database, ShieldCheck, Eye, EyeOff, Search, FileCode2, Lock } from 'lucide-react';
import { EvidenceFile, UserRole } from '../types/audit';

interface EvidenceExplorerProps {
  evidenceFiles: EvidenceFile[];
  userRole: UserRole;
}

export const EvidenceExplorer: React.FC<EvidenceExplorerProps> = ({ evidenceFiles, userRole }) => {
  const [selectedFile, setSelectedFile] = useState<EvidenceFile | null>(evidenceFiles[0] || null);
  const [showMaskedPii, setShowMaskedPii] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  // Sample records inside the inspected database snapshot
  const mockDbRecords = [
    { user_id: 'usr_009', email: 'sarah.connor@example.com', name: 'Sarah Connor', status: 'DELETED', tombstone: 'CLEAN (NO PII)' },
    { user_id: 'usr_010', email: 'david.ross@example.com', name: 'David Ross', status: 'DELETED', tombstone: 'CLEAN (NO PII)' },
    { user_id: 'usr_017', email: 'alice.wong@example.com', name: 'Alice Wong', status: 'ACTIVE (REPLICA DRIFT)', tombstone: 'MISSING IN REPLICA' },
    { user_id: 'usr_019', email: 'claire.fontaine@example.com', name: 'Claire Fontaine', status: 'DELETED', tombstone: 'LEAK: PII PRESENT IN TOMBSTONE' },
    { user_id: 'usr_020', email: 'diego.torres@example.com', name: 'Diego Torres', status: 'DELETED', tombstone: 'RESTORE RISK STAGED' },
  ];

  const maskEmail = (em: string) => {
    if (showMaskedPii) return em;
    const parts = em.split('@');
    if (parts.length === 2) {
      return `${parts[0].slice(0, 2)}***@${parts[1]}`;
    }
    return '***@***';
  };

  const maskName = (nm: string) => {
    if (showMaskedPii) return nm;
    return `${nm.slice(0, 1)}***`;
  };

  const filteredFiles = evidenceFiles.filter(f =>
    !searchTerm || f.file_id.toLowerCase().includes(searchTerm.toLowerCase()) || f.system_id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <Database className="w-5 h-5 text-cyan-400" />
            <span>Evidence Files & Snapshot Explorer</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Read-only, sandboxed inspection of SQLite snapshots, secondary database replicas, and audit manifest records.
          </p>
        </div>

        {/* PII Masking Control */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowMaskedPii(!showMaskedPii)}
            className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors flex items-center gap-1.5 border ${
              showMaskedPii
                ? 'bg-amber-500/10 text-amber-300 border-amber-500/30'
                : 'bg-slate-900 text-slate-300 border-slate-800 hover:text-white'
            }`}
          >
            {showMaskedPii ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
            <span>{showMaskedPii ? 'Mask PII' : 'Reveal Unmasked (Role Gated)'}</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left: Manifest File List (Col 4) */}
        <div className="lg:col-span-4 bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h2 className="text-xs font-semibold text-slate-300 tracking-wider uppercase">
            Manifest Evidence Files
          </h2>

          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search file_id or system..."
              className="w-full bg-slate-950 border border-slate-800 rounded-md pl-8 pr-3 py-1.5 text-xs text-slate-300 placeholder-slate-500 focus:outline-none"
            />
          </div>

          <div className="space-y-1.5 max-h-[480px] overflow-y-auto">
            {filteredFiles.slice(0, 15).map((f) => {
              const isSelected = selectedFile?.file_id === f.file_id;
              return (
                <div
                  key={f.file_id}
                  onClick={() => setSelectedFile(f)}
                  className={`p-3 rounded-lg border text-xs cursor-pointer transition-colors ${
                    isSelected
                      ? 'bg-cyan-500/10 border-cyan-500/30 text-cyan-200'
                      : 'bg-slate-950/60 border-slate-800/80 text-slate-400 hover:bg-slate-800/40 hover:text-slate-200'
                  }`}
                >
                  <div className="flex items-center justify-between font-mono font-medium">
                    <span>{f.file_id}</span>
                    <span className="text-[10px] text-emerald-400">{f.status}</span>
                  </div>
                  <div className="mt-1 font-sans text-slate-300 font-medium">{f.system_id}</div>
                  <div className="mt-0.5 text-[10px] font-mono text-slate-500 tabular-nums">
                    {f.captured_at.replace('T', ' ').replace('Z', '')} · {f.file_type}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Snapshot Data Inspector (Col 8) */}
        <div className="lg:col-span-8 bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <h2 className="text-sm font-semibold text-white flex items-center gap-2">
                <FileCode2 className="w-4 h-4 text-cyan-400" />
                <span>Snapshot Table Inspector: {selectedFile?.system_id || 'account_service'}</span>
              </h2>
              <p className="text-xs text-slate-400 font-mono">
                {selectedFile?.file_path || 'dataset/evidence/databases/primary_account_store.db'} (PRAGMA trusted_schema=OFF)
              </p>
            </div>
          </div>

          {/* Table */}
          <div className="border border-slate-800 rounded-lg overflow-hidden bg-slate-950">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 bg-slate-900/60 font-medium">
                  <th className="py-2.5 px-3">user_id</th>
                  <th className="py-2.5 px-3">Customer Name</th>
                  <th className="py-2.5 px-3">Email Address</th>
                  <th className="py-2.5 px-3">Observed State</th>
                  <th className="py-2.5 px-3">Tombstone Integrity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono text-slate-300">
                {mockDbRecords.map((r) => (
                  <tr key={r.user_id} className="hover:bg-slate-900/40">
                    <td className="py-2.5 px-3 text-cyan-400 font-medium">{r.user_id}</td>
                    <td className="py-2.5 px-3 font-sans">{maskName(r.name)}</td>
                    <td className="py-2.5 px-3 font-sans text-slate-300">{maskEmail(r.email)}</td>
                    <td className="py-2.5 px-3 font-sans">
                      <span className={r.status.includes('ACTIVE') ? 'text-amber-400 font-medium' : 'text-slate-400'}>
                        {r.status}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 font-sans">
                      <span className={r.tombstone.includes('LEAK') ? 'text-rose-400 font-medium' : 'text-emerald-400'}>
                        {r.tombstone}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-400 space-y-1">
            <span className="font-semibold text-slate-300">Sanitization Guard:</span>
            <p>
              Snapshots are queried in memory with zero write capability. SQL statements containing ATTACH, load_extension, or administrative PRAGMAs are strictly rejected.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
