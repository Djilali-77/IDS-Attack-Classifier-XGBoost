import { motion } from 'framer-motion';

const ScanResult = ({ result }) => {
  if (!result) return null; 

  const isDanger = result.status === 'danger';

  return (
    <motion.div 
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`mt-8 w-full max-w-3xl mx-auto p-6 rounded-lg border-2 text-center shadow-2xl ${
        isDanger 
          ? 'bg-red-900/20 border-red-500 text-red-400' 
          : 'bg-emerald-900/20 border-emerald-500 text-emerald-400'
      }`}
    >
      <div className="flex items-center justify-center space-x-3">
        <span className="text-3xl">
          {isDanger ? '⚠️' : '✅'}
        </span>
        <h3 className="text-2xl font-black uppercase tracking-widest">
          {result.message}
        </h3>
      </div>
      
      {isDanger && (
        <motion.p 
          initial={{ opacity: 0 }}
          animate={{ opacity: [0, 1, 0] }}
          transition={{ repeat: Infinity, duration: 1.5 }}
          className="mt-2 text-red-300 font-mono text-sm"
        >
          [ ACTION REQUIRED: BLOCKING SOURCE IP ]
        </motion.p>
      )}
    </motion.div>
  );
};

export default ScanResult;