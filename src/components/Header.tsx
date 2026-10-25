import React from 'react';
import { Download, UserCheck, Shield } from 'lucide-react';
import { UserRole } from '../types/audit';

interface HeaderProps {
  currentTab: string;
  selectedCaseId?: string;
  userRole: UserRole;
  onChangeRole: (role: UserRole) => void;
  onExportCsv: () => void;
  isExporting: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  currentTab,
  selectedCaseId,
  userRole,
  onChangeRole,
  onExportCsv,
  isExporting
}) => {
  const formatTabName = (tab: string) => {
    switch (tab) {
      case 'overview': return 'Overview Dashboard';
      case 'requests': return 'Audit Requests';
      case 'workspace': return 'Investigation Room';
      case 'identity': return 'Identity Resolution Graph';
      case 'evidence': return 'Evidence Explorer';
      case 'lifecycle': return 'Lifecycle & Recreation Risks';
      case 'remediation': return 'Remediation Planner';
      case 'reports': return 'Compliance Assurance Certificate';
      case 'evaluation': return 'Benchmark Evaluation Lab';
      case 'admin': return 'Security & Immutability Ledger';
      default: return tab;
    }
  };

  return (
    <header className="h-16 px-6 bg-slate-900 border-b border-slate-800 flex items-center justify-between gap-8 shrink-0">
      {/* Zone 1: Breadcrumb context */}
      <div className="flex items-center gap-3 text-xs font-medium text-slate-400 whitespace-nowrap shrink-0">
        <span className="text-slate-200">Northstar Shop Audit</span>
        <span aria-hidden="true" className="text-slate-600">/</span>
        <span className="text-cyan-400">{formatTabName(currentTab)}</span>
        {selectedCaseId && (
          <>
            <span aria-hidden="true" className="text-slate-600">/</span>
            <span className="font-mono text-cyan-300">{selectedCaseId}</span>
          </>
        )}
      </div>

      {/* Zone 2: Informational trust badges */}
      <div className="hidden md:flex items-center gap-4 text-xs text-slate-400 whitespace-nowrap">
        <span className="flex items-center gap-1.5">
          <Shield className="w-3.5 h-3.5 text-cyan-400" />
          <span>Audit-At Cutoff Enforced</span>
        </span>
        <span aria-hidden="true" className="text-slate-700">·</span>
        <span className="font-mono tabular-nums text-slate-400">518 Cases Indexed</span>
        <span aria-hidden="true" className="text-slate-700">·</span>
        <span className="text-emerald-400 font-mono">0 False-COMPLETE Errors</span>
      </div>

      {/* Zone 3: Actions & Role switcher */}
      <div className="flex items-center gap-3 shrink-0">
        {/* Role Switcher */}
        <div className="flex items-center gap-1.5 bg-slate-950 border border-slate-800 px-2.5 py-1.5 rounded-md text-xs text-slate-300">
          <UserCheck className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
          <span className="text-[11px] text-slate-400">Role:</span>
          <select 
            value={userRole} 
            onChange={(e) => onChangeRole(e.target.value as UserRole)}
            className="bg-transparent text-xs text-cyan-300 font-medium focus:outline-none cursor-pointer"
          >
            <option value="Administrator" className="bg-slate-900 text-slate-100">Administrator</option>
            <option value="Auditor" className="bg-slate-900 text-slate-100">Auditor</option>
            <option value="Analyst" className="bg-slate-900 text-slate-100">Analyst</option>
            <option value="Reviewer" className="bg-slate-900 text-slate-100">Reviewer (Read-Only)</option>
          </select>
        </div>

        {/* Export output.csv button */}
        <button
          onClick={onExportCsv}
          disabled={isExporting}
          className="px-3.5 py-2 text-xs font-medium text-slate-950 bg-cyan-400 hover:bg-cyan-300 transition-colors rounded-md flex items-center gap-2 whitespace-nowrap shrink-0 disabled:opacity-50"
        >
          <Download className="w-3.5 h-3.5" />
          <span>{isExporting ? 'Generating...' : 'Export output.csv'}</span>
        </button>
      </div>
    </header>
  );
};
