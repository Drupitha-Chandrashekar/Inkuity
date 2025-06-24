import React, { useState } from 'react';

function ArtTheftDetection() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    
    // Create preview URL
    if (selectedFile) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(selectedFile);
    } else {
      setPreview(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch("http://127.0.0.1:8000/detect-art-theft/", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error("Error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-blue-400">Art Theft Detection</h2>
      
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <form onSubmit={handleSubmit} className="mb-6">
          <div className="mb-4">
            <label className="block text-gray-300 mb-2">
              Upload your artwork to check for similarities:
            </label>
            <input 
              type="file" 
              onChange={handleFileChange}
              className="block w-full text-gray-300 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none p-2"
              accept="image/*"
            />
          </div>
          
          {preview && (
            <div className="mb-4">
              <h3 className="text-gray-300 mb-2">Your Artwork:</h3>
              <img 
                src={preview} 
                alt="Preview" 
                className="max-w-full h-auto max-h-64 rounded border border-gray-600"
              />
            </div>
          )}
          
          <button 
            type="submit" 
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
          >
            {loading ? 'Analyzing...' : 'Check for Similar Art'}
          </button>
        </form>

        {loading && (
          <div className="flex items-center justify-center p-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            <span className="ml-3 text-blue-400">Analyzing your artwork...</span>
          </div>
        )}

        {error && (
          <div className="bg-red-900 text-red-100 p-4 rounded mb-4">
            Error: {error}
          </div>
        )}

        {result && (
          <div className="mt-6">
            <h3 className="text-xl font-semibold mb-4 text-blue-300">Detection Results</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {result.matches && result.matches.map((match, index) => (
                <div key={index} className="bg-gray-700 p-4 rounded-lg">
                  <div className="font-medium text-gray-200 mb-2">
                    Match {index + 1} 
                    {result.distances && (
                      <span className="text-sm text-gray-400 ml-2">
                        (Distance: {result.distances[index]?.toFixed(4)})
                      </span>
                    )}
                    {result.cosine_similarities && (
                      <span className="text-sm text-gray-400 ml-2">
                        (Similarity: {(result.cosine_similarities[index] * 100).toFixed(2)}%)
                      </span>
                    )}
                  </div>
                  <img 
                    src={`http://127.0.0.1:8000/${match.replace(/\\/g, '/')}`} 
                    alt="Similar artwork" 
                    className="w-full h-auto rounded"
                    onError={(e) => {
                      e.target.src = 'https://via.placeholder.com/300x200?text=Image+Not+Found';
                    }}
                  />
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ArtTheftDetection;