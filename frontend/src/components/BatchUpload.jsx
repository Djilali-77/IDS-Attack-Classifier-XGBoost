import { useState } from 'react';
import axios from 'axios';

const BatchUpload = ({ setScanResult }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a CSV file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:8000/predict-batch", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setScanResult(response.data);
    } catch (error) {
      console.error("Error uploading file: ", error);
      setScanResult({ status: 'danger', message: 'Error processing the CSV file.' });
    }
  };

  return (
    <div className="bg-slate-800 p-6 rounded-lg shadow-xl border border-slate-700 w-full max-w-3xl mx-auto mt-6">
      <h2 className="text-xl font-bold text-slate-100 mb-4 border-b border-slate-600 pb-2">
        Batch Analysis (CSV File)
      </h2>
      <form onSubmit={handleUpload} className="flex items-center gap-4">
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="block w-full text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-500 cursor-pointer"
        />
        <button
          type="submit"
          className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 px-6 rounded transition-colors duration-200 whitespace-nowrap"
        >
          Analyze File
        </button>
      </form>
    </div>
  );
};

export default BatchUpload;