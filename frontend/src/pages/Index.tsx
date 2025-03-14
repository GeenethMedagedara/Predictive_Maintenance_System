
import React from "react";
import { motion } from "framer-motion";
import FileUpload from "@/components/FileUpload";
import AnomalyVisualization from "@/components/AnomalyVisualization";
import useAnomalyDetection from "@/hooks/useAnomalyDetection";
import axios from 'axios';
import { usePrediction } from '../PredictionContext';

const Index = () => {
  const { 
    detectAnomalies, 
    isProcessing, 
    visualizationData, 
    selectedFile 
  } = useAnomalyDetection();

  const { setImageSrc } = usePrediction();

  const handleFileSelected = async (file: File) => {
    const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await axios.post("/upload", formData, {
            responseType: "blob",
        });

        const imageBlob = new Blob([response.data], { type: "image/png" });
        const imageUrl = URL.createObjectURL(imageBlob);
        setImageSrc(imageUrl);
    } catch (error) {
        console.error(error);
    }
    detectAnomalies(file);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-background to-secondary/30">      
      <main className="flex-1 container max-w-6xl mx-auto px-4 py-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mb-8 text-center max-w-3xl mx-auto"
        >
          <div className="inline-block px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-medium mb-2">
            Machine Learning
          </div>
          <h1 className="text-3xl font-bold mb-3 tracking-tight">
            Anomaly Detection Platform
          </h1>
          <p className="text-sm text-muted-foreground max-w-xl mx-auto">
            Upload your dataset and detect anomalies with our advanced machine learning algorithms. Visualize and identify patterns that stand out from normal behavior.
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-3">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
            >
              <h2 className="text-lg font-medium mb-3">Upload Data</h2>
              <p className="text-xs text-muted-foreground mb-4">
                Upload your CSV file containing the dataset you want to analyze.
              </p>
              
              <FileUpload 
                onFileSelected={handleFileSelected} 
                isLoading={isProcessing} 
                className="mb-4"
              />
              
              {selectedFile && (
                <div className="space-y-3">
                  <div className="bg-white/70 backdrop-blur-sm rounded-lg p-3 border">
                    <h3 className="text-xs font-medium mb-2">CSV Format Requirements</h3>
                    <ul className="text-xs text-muted-foreground space-y-1">
                      {/* <li className="flex items-start">
                        <span className="text-primary mr-1">•</span>
                        <span>File should contain <code className="text-xs bg-secondary/50 px-1 py-0.5 rounded">x</code> and <code className="text-xs bg-secondary/50 px-1 py-0.5 rounded">y</code> columns</span>
                      </li> */}
                      <li className="flex items-start">
                        <span className="text-primary mr-1">•</span>
                        <span>The column with the values should be labeled <code className="text-xs bg-secondary/50 px-1 py-0.5 rounded">value</code></span>
                      </li>
                      {/* <li className="flex items-start">
                        <span className="text-primary mr-1">•</span>
                        <span>Use <code className="text-xs bg-secondary/50 px-1 py-0.5 rounded">true/false</code> or <code className="text-xs bg-secondary/50 px-1 py-0.5 rounded">1/0</code> to indicate anomalies</span>
                      </li> */}
                    </ul>
                  </div>
                </div>
              )}
            </motion.div>
          </div>
          
          <motion.div 
            className="lg:col-span-11"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
          >
            <h2 className="text-lg font-medium mb-3">Anomaly Visualization</h2>
            <p className="text-xs text-muted-foreground mb-4">
              Visual representation of your data points with anomalies highlighted.
            </p>
            
            <AnomalyVisualization 
              data={visualizationData} 
              isLoading={isProcessing} 
            />
          </motion.div>
        </div>
      </main>
      
      <footer className="border-t border-border/50 py-4 text-center text-xs text-muted-foreground">
        <p>Anomaly Sightseeker &copy; {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
};

export default Index;
