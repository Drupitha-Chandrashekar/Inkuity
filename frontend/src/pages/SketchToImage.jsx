import React, { useState } from 'react';

function SketchToImage() {
  const [sketch, setSketch] = useState(null);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleSketchUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSketch(file);
      // Create preview URL
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!sketch) {
      setError('Please upload a sketch first');
      return;
    }

    setLoading(true);
    setError(null);
    setGeneratedImage(null);

    const formData = new FormData();
    formData.append('image', sketch);
    if (prompt) {
      formData.append('prompt', prompt);
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/generate-image/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Generation failed: ${response.statusText}`);
      }

      // Get the image blob from response
      const imageBlob = await response.blob();
      const imageUrl = URL.createObjectURL(imageBlob);
      setGeneratedImage(imageUrl);
    } catch (err) {
      console.error('Generation error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-blue-400">Sketch to Image Generator</h1>
        
        <div className="bg-gray-800 rounded-lg shadow-xl p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Upload Your Sketch</h2>
          
          <div className="mb-6">
            <label className="block text-gray-300 mb-2">Choose your sketch:</label>
            <input
              type="file"
              onChange={handleSketchUpload}
              accept="image/*"
              className="block w-full text-gray-300 bg-gray-700 rounded border border-gray-600 focus:border-blue-500 focus:outline-none p-2"
            />
          </div>

          {preview && (
            <div className="mb-6">
              <h3 className="text-gray-300 mb-2">Sketch Preview:</h3>
              <img 
                src={preview} 
                alt="Sketch preview" 
                className="max-w-full h-auto max-h-64 rounded border border-gray-600"
              />
            </div>
          )}

          <div className="mb-6">
            <label className="block text-gray-300 mb-2">Optional Prompt:</label>
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe what you want to generate (optional)"
              className="w-full p-2 bg-gray-700 border border-gray-600 rounded text-white"
            />
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading || !sketch}
            className={`px-6 py-2 rounded font-bold ${loading || !sketch ? 'bg-blue-800 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'} transition-colors`}
          >
            {loading ? 'Generating...' : 'Generate Image'}
          </button>
        </div>

        {error && (
          <div className="bg-red-900 text-red-100 p-4 rounded mb-6">
            Error: {error}
          </div>
        )}

        {generatedImage && (
          <div className="bg-gray-800 rounded-lg shadow-xl p-6">
            <h2 className="text-xl font-semibold mb-4">Generated Image</h2>
            <div className="flex justify-center">
              <img 
                src={generatedImage} 
                alt="Generated artwork" 
                className="max-w-full h-auto rounded border-2 border-blue-500"
              />
            </div>
            <div className="mt-4 flex justify-center">
              <a
                href={generatedImage}
                download="generated-artwork.png"
                className="px-4 py-2 bg-green-600 hover:bg-green-700 rounded text-white"
              >
                Download Image
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default SketchToImage;