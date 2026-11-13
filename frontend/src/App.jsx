import { useState } from 'react';
import TrafficForm from './components/TrafficForm';
import BatchUpload from './components/BatchUpload';
import ScanResult from './components/ScanResult';

function App() {
  const [scanResult, setScanResult] = useState(null);

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center py-12 px-4 font-mono text-gray-200">
      
      {/* --- (Header) --- */}
      <header className="mb-10 text-center">
        <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
          🛡️ Attack Profiler
        </h1>
        <p className="text-gray-400 mt-2 text-sm">Network Flow Classification with XGBoost</p>
        </header>

      {/* ---  (Main Content) --- */}
      <main className="w-full max-w-4xl space-y-8">
        
        <TrafficForm setScanResult={setScanResult} />
        <BatchUpload setScanResult={setScanResult} />
        <ScanResult result={scanResult} />
        
      </main>
    </div>
  );
}

export default App;