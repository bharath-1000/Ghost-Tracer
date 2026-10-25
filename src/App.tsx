import React, { useState, useEffect } from 'react';
import { Sidebar, NavTab } from './components/Sidebar';
import { Header } from './components/Header';
import { OverviewDashboard } from './components/OverviewDashboard';
import { AuditRequests } from './components/AuditRequests';
import { InvestigationWorkspace } from './components/InvestigationWorkspace';
import { IdentityGraphView } from './components/IdentityGraphView';
import { EvidenceExplorer } from './components/EvidenceExplorer';
import { LifecycleMap } from './components/LifecycleMap';
import { RemediationPlannerView } from './components/RemediationPlannerView';
import { AssuranceReportView } from './components/AssuranceReportView';
import { EvaluationLabView } from './components/EvaluationLabView';
import { SecurityAdminView } from './components/SecurityAdminView';
import { CaseRecord, EvidenceFile, OverviewMetrics, UserRole } from './types/audit';

export default function App() {
  const [activeTab, setActiveTab] = useState<NavTab>('overview');
  const [userRole, setUserRole] = useState<UserRole>('Auditor');
  const [cases, setCases] = useState<CaseRecord[]>([]);
  const [selectedCaseId, setSelectedCaseId] = useState<string>('case_017');
  const [evidenceFiles, setEvidenceFiles] = useState<EvidenceFile[]>([]);
  const [metrics, setMetrics] = useState<OverviewMetrics>({
    total_cases: 518,
    complete_count: 203,
    incomplete_count: 226,
    not_applicable_count: 89,
    false_complete_count: 0,
    status_accuracy: 1.0,
    total_findings: 312,
    total_lifecycle_risks: 84,
    audit_coverage: 100.0,
    avg_latency_ms: 1.2
  });
  const [loading, setLoading] = useState(true);
  const [isExporting, setIsExporting] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        // Fetch cases
        const reqRes = await fetch('/api/v1/requests?limit=518');
        if (reqRes.ok) {
          const reqData = await reqRes.json();
          if (reqData.cases && reqData.cases.length > 0) {
            setCases(reqData.cases);
          }
        }

        // Fetch metrics
        const mRes = await fetch('/api/v1/metrics/overview');
        if (mRes.ok) {
          const mData = await mRes.json();
          setMetrics(mData);
        }

        // Fetch evidence
        const evRes = await fetch('/api/v1/evidence');
        if (evRes.ok) {
          const evData = await evRes.json();
          if (evData.files) {
            setEvidenceFiles(evData.files);
          }
        }
      } catch (err) {
        console.error('Failed to load API data:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const currentCase = cases.find(c => c.case_id === selectedCaseId) || cases[0] || {
    case_id: 'case_017',
    email: 'alice.wong@example.com',
    requested_at: '2026-09-03T08:00:00Z',
    reported_status: 'COMPLETE',
    reported_at: '2026-09-03T08:30:00Z',
    audit_at: '2026-09-03T12:00:00Z',
    request_text: 'Please delete my account and all personal details.',
    deletion_status: 'INCOMPLETE',
    steps_json: '[]',
    steps: []
  };

  const handleExportCsv = async () => {
    setIsExporting(true);
    try {
      const response = await fetch('/api/v1/export/output-csv');
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'output.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (err) {
      console.error('Failed to download output.csv:', err);
    } finally {
      setIsExporting(false);
    }
  };

  const handleSelectCase = (caseId: string) => {
    setSelectedCaseId(caseId);
    setActiveTab('workspace');
  };

  return (
    <div className="flex h-screen overflow-hidden bg-slate-950 font-sans text-slate-100">
      {/* Persistent Left Sidebar */}
      <Sidebar
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        caseCount={cases.length || 518}
      />

      {/* Main Viewport */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Bar Header */}
        <Header
          currentTab={activeTab}
          selectedCaseId={activeTab === 'workspace' || activeTab === 'identity' || activeTab === 'remediation' ? selectedCaseId : undefined}
          userRole={userRole}
          onChangeRole={setUserRole}
          onExportCsv={handleExportCsv}
          isExporting={isExporting}
        />

        {/* Scrollable Workspace Content */}
        <main className="flex-1 overflow-y-auto">
          {activeTab === 'overview' && (
            <OverviewDashboard
              metrics={metrics}
              recentCases={cases}
              onSelectCase={handleSelectCase}
              onNavigateToRequests={() => setActiveTab('requests')}
            />
          )}

          {activeTab === 'requests' && (
            <AuditRequests
              cases={cases}
              onSelectCase={handleSelectCase}
            />
          )}

          {activeTab === 'workspace' && (
            <InvestigationWorkspace
              currentCase={currentCase}
              allCases={cases}
              onSelectCase={setSelectedCaseId}
              onNavigateToIdentity={() => setActiveTab('identity')}
              onNavigateToRemediation={() => setActiveTab('remediation')}
            />
          )}

          {activeTab === 'identity' && (
            <IdentityGraphView
              currentCase={currentCase}
            />
          )}

          {activeTab === 'evidence' && (
            <EvidenceExplorer
              evidenceFiles={evidenceFiles}
              userRole={userRole}
            />
          )}

          {activeTab === 'lifecycle' && (
            <LifecycleMap />
          )}

          {activeTab === 'remediation' && (
            <RemediationPlannerView
              currentCase={currentCase}
            />
          )}

          {activeTab === 'reports' && (
            <AssuranceReportView
              currentCase={currentCase}
            />
          )}

          {activeTab === 'evaluation' && (
            <EvaluationLabView />
          )}

          {activeTab === 'admin' && (
            <SecurityAdminView
              userRole={userRole}
              onChangeRole={setUserRole}
            />
          )}
        </main>
      </div>
    </div>
  );
}
