import { useState } from 'react';
import axios from 'axios';

const TrafficForm = ({ setScanResult }) => {
  const [formData, setFormData] = useState({
    "Bwd Packet Length Std": 0.0,
    "Init_Win_bytes_forward": 29200,
    "Flow IAT Mean": 0.0,
    "Fwd Packets/s": 0.0,
    "Average Packet Size": 0.0,
    "Packet Length Variance": 0.0
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: Number(value) });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setScanResult(null);

    try {
      const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
      const response = await axios.post(`${API_URL}/predict`, {
        features: formData
      });
      
      setScanResult(response.data);
      
    } catch (error) {
      const detail = error.response?.data?.detail || "Connection Error to Backend";
      setScanResult({ status: 'danger', message: String(detail) });
    }
  };

  const inputStyle = "bg-gray-900 text-gray-100 border border-gray-700 rounded px-3 h-11 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 w-full font-mono text-sm";
  const labelStyle = "text-emerald-400 text-xs font-semibold mb-1 uppercase";

  return (
    <form onSubmit={handleSubmit} className="bg-gray-900/50 p-6 rounded-lg shadow-2xl border border-gray-800 w-full">
      <h2 className="text-xl font-bold text-gray-100 mb-6 border-b border-gray-700 pb-2">
        [ Manual Flow Injector ]
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {Object.keys(formData).map((key) => (
          <div className="flex flex-col" key={key}>
            <label className={labelStyle}>{key}</label>
            <input 
              type="number" 
              name={key} 
              value={formData[key]} 
              onChange={handleChange} 
              step="any"
              className={inputStyle} 
            />
          </div>
        ))}
      </div>

      <button type="submit" className="mt-8 w-full bg-emerald-600 hover:bg-emerald-500 text-gray-950 font-bold py-3 px-4 rounded transition-colors duration-200 uppercase tracking-widest">
        Analyze Flow
      </button>
    </form>
  );
};

export default TrafficForm;