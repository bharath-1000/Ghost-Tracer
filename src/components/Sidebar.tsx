import React from 'react';
import { 
  ShieldCheck, 
  LayoutDashboard, 
  FolderCheck, 
  SearchCode, 
  Network, 
  Database, 
  Workflow, 
  ListOrdered, 
  FileCheck2, 
  Activity, 
  ShieldAlert
} from 'lucide-react';

export type NavTab = 
  | 'overview' 
  | 'requests' 
  | 'workspace' 
  | 'identity' 
  | 'evidence' 
  | 'lifecycle' 
  | 'remediation' 
  | 'reports' 
  | 'evaluation' 
  | 'admin';

interface SidebarProps {
  activeTab: NavTab;
  onSelectTab: (tab: NavTab) => void;
  caseCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, onSelectTab, caseCount }) => {
  const navItems = [
    { id: 'overview' as NavTab, label: 'Overview', icon: LayoutDashboard },
    { id: 'requests' as NavTab, label: 'Audit Requests', icon: FolderCheck, count: caseCount },
    { id: 'workspace' as NavTab, label: 'Investigation Room', icon: SearchCode },
    { id: 'identity' as NavTab, label: 'Identity Graph', icon: Network },
    { id: 'evidence' as NavTab, label: 'Evidence Explorer', icon: Database },
    { id: 'lifecycle' as NavTab, label: 'Lifecycle & Sync', icon: Workflow },
    { id: 'remediation' as NavTab, label: 'Remediation Plan', icon: ListOrdered },
    { id: 'reports' as NavTab, label: 'Assurance Certificate', icon: FileCheck2 },
    { id: 'evaluation' as NavTab, label: 'Evaluation Lab', icon: Activity },
    { id: 'admin' as NavTab, label: 'Security & Integrity', icon: ShieldAlert },
  ];

  return (
    <aside className="w-64 shrink-0 bg-slate-900 border-r border-slate-800 flex flex-col min-h-screen text-slate-300">
      {/* Brand Zone */}
      <div className="h-16 flex items-center px-6 border-b border-slate-800 gap-3">
        <div className="w-9 h-9 rounded-lg bg-cyan-950 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
          <ShieldCheck className="w-5 h-5" />
        </div>
        <div className="flex flex-col">
          <span className="font-semibold text-sm tracking-tight text-white flex items-center gap-1.5">
            GHOST TRACER
          </span>
          <span className="text-[11px] text-slate-400 font-mono tracking-wider">AUDIT ENGINE</span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onSelectTab(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2 text-xs font-medium rounded-md transition-colors text-left ${
                isActive
                  ? 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/20'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.count !== undefined && item.count > 0 && (
                <span className="text-[11px] font-mono tabular-nums text-slate-400 bg-slate-800 px-1.5 py-0.5 rounded">
                  {item.count}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Audit-Only Boundary Notice */}
      <div className="p-3 m-3 rounded-lg bg-slate-950/70 border border-slate-800/80 text-[11px] text-slate-400 leading-relaxed">
        <p className="font-medium text-slate-300 mb-1">Audit-Only System</p>
        <p className="text-[10px] text-slate-400">
          All remediation steps are recommendations. GHOST TRACER never mutates production data.
        </p>
      </div>

      {/* Engine & Dataset Status */}
      <div className="px-4 py-3 border-t border-slate-800 text-[11px] font-mono text-slate-400 flex items-center justify-between">
        <span>Engine v1.0.0</span>
        <span className="text-cyan-400">Deterministic</span>
      </div>
    </aside>
  );
};
