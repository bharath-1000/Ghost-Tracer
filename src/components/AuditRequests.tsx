import React, { useState } from 'react';
import { Search, Filter, CheckCircle2, AlertTriangle, HelpCircle, ArrowRight } from 'lucide-react';
import { CaseRecord, DeletionStatus } from '../types/audit';

interface AuditRequestsProps {
  cases: CaseRecord[];
  onSelectCase: (caseId: string) => void;
}

export const AuditRequests: React.FC<AuditRequestsProps> = ({ cases, onSelectCase }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'ALL' | DeletionStatus>('ALL');
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 20;

  // Filter cases
  const filteredCases = cases.filter(c => {
    const matchesStatus = statusFilter === 'ALL' || c.deletion_status === statusFilter;
    const matchesSearch = !searchTerm || 
      c.case_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.request_text.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  const totalPages = Math.ceil(filteredCases.length / pageSize) || 1;
  const paginatedCases = filteredCases.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  const getStatusBadge = (status: DeletionStatus) => {
    switch (status) {
      case 'COMPLETE':
        return (
          <span className="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-400">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>COMPLETE</span>
          </span>
        );
      case 'INCOMPLETE':
        return (
          <span className="inline-flex items-center gap-1.5 text-xs font-medium text-amber-400">
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>INCOMPLETE</span>
          </span>
        );
      case 'NOT_APPLICABLE':
        return (
          <span className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-400">
            <HelpCircle className="w-3.5 h-3.5" />
            <span>NOT_APPLICABLE</span>
          </span>
        );
    }
  };

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto">
      {/* Header & Filter Bar */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tight">Audit Requests</h1>
          <p className="text-xs text-slate-400 mt-1">
            Browse and filter through all 518 cases with verified ground truth up to audit_at timestamp.
          </p>
        </div>

        {/* Filter Controls (buttons with active state) */}
        <div className="flex items-center gap-2">
          {(['ALL', 'COMPLETE', 'INCOMPLETE', 'NOT_APPLICABLE'] as const).map(tab => (
            <button
              key={tab}
              onClick={() => { setStatusFilter(tab); setCurrentPage(1); }}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
                statusFilter === tab
                  ? 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              {tab === 'ALL' ? 'All Cases' : tab.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Search Input Bar */}
      <div className="relative">
        <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => { setSearchTerm(e.target.value); setCurrentPage(1); }}
          placeholder="Search by Case ID, email address, or request keywords..."
          className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50"
        />
      </div>

      {/* Table Container */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 bg-slate-950/40">
                <th className="py-3 px-4 font-medium">Case ID</th>
                <th className="py-3 px-4 font-medium">Subject Email</th>
                <th className="py-3 px-4 font-medium">Requested At</th>
                <th className="py-3 px-4 font-medium">Audit Cutoff (audit_at)</th>
                <th className="py-3 px-4 font-medium">Reported Claim</th>
                <th className="py-3 px-4 font-medium">Audited Verdict</th>
                <th className="py-3 px-4 font-medium">Remediation Steps</th>
                <th className="py-3 px-4 font-medium text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono text-slate-300">
              {paginatedCases.length > 0 ? (
                paginatedCases.map((c) => (
                  <tr key={c.case_id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4 text-cyan-400 font-medium">{c.case_id}</td>
                    <td className="py-3 px-4 font-sans text-slate-200">{c.email}</td>
                    <td className="py-3 px-4 text-slate-400 tabular-nums">
                      {c.requested_at.replace('T', ' ').replace('Z', '')}
                    </td>
                    <td className="py-3 px-4 text-slate-400 tabular-nums">
                      {c.audit_at.replace('T', ' ').replace('Z', '')}
                    </td>
                    <td className="py-3 px-4 font-sans text-slate-400">
                      {c.reported_status}
                    </td>
                    <td className="py-3 px-4 font-sans">
                      {getStatusBadge(c.deletion_status)}
                    </td>
                    <td className="py-3 px-4 text-slate-400 tabular-nums">
                      {c.steps.length > 0 ? `${c.steps.length} step${c.steps.length > 1 ? 's' : ''}` : '0 steps ([])'}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => onSelectCase(c.case_id)}
                        className="px-3 py-1 text-xs font-sans font-medium text-cyan-300 bg-cyan-950/60 border border-cyan-500/30 rounded-md hover:bg-cyan-900/50 transition-colors inline-flex items-center gap-1.5"
                      >
                        <span>Investigate</span>
                        <ArrowRight className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-500 font-sans">
                    No audit requests match the specified query and filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        <div className="px-4 py-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <div className="font-mono tabular-nums">
            Showing {(currentPage - 1) * pageSize + 1} to {Math.min(currentPage * pageSize, filteredCases.length)} of {filteredCases.length} cases
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 disabled:opacity-40 hover:bg-slate-700 transition-colors"
            >
              Previous
            </button>
            <span className="font-mono tabular-nums px-2">
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              className="px-2.5 py-1 rounded bg-slate-800 text-slate-300 disabled:opacity-40 hover:bg-slate-700 transition-colors"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
