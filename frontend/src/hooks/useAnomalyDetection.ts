
import { useState } from 'react';
import { readCSVFile, parseCSV, formatDataForVisualization } from '@/utils/fileUtils';
import { toast } from 'sonner';

interface UseAnomalyDetectionOptions {
  mockBackendResponse?: boolean;
  mockDelay?: number;
}

export const useAnomalyDetection = (options: UseAnomalyDetectionOptions = {}) => {
  const { mockBackendResponse = true, mockDelay = 2000 } = options;
  
  const [isProcessing, setIsProcessing] = useState(false);
  const [visualizationData, setVisualizationData] = useState<any[] | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  
  const detectAnomalies = async (file: File) => {
    setIsProcessing(true);
    setSelectedFile(file);
    setVisualizationData(null);
    
    try {
      if (mockBackendResponse) {
        // Mock backend response with a delay
        await new Promise(resolve => setTimeout(resolve, mockDelay));
        
        // For demo purposes, we'll generate a random visualization dataset
        const mockData = generateMockData();
        setVisualizationData(mockData);
        toast.success('Analysis complete', {
          description: `Detected ${mockData.filter(d => d.isAnomaly).length} anomalies in your data.`
        });
      } else {
        // This is where you would implement the real backend call
        const csvContent = await readCSVFile(file);
        const parsedData = parseCSV(csvContent);
        
        // Create FormData to send to the backend
        const formData = new FormData();
        formData.append('file', file);
        
        // Make API call to backend
        const response = await fetch('/api/detect-anomalies', {
          method: 'POST',
          body: formData,
        });
        
        if (!response.ok) {
          throw new Error('Failed to process file');
        }
        
        const responseData = await response.json();
        
        // Format the data for visualization
        const formattedData = formatDataForVisualization(
          responseData.data,
          responseData.xKey,
          responseData.yKey,
          responseData.anomalyKey
        );
        
        setVisualizationData(formattedData);
        toast.success('Analysis complete', {
          description: `Detected ${formattedData.filter(d => d.isAnomaly).length} anomalies in your data.`
        });
      }
    } catch (error) {
      console.error('Error processing file:', error);
      toast.error('Error processing file', {
        description: 'There was an error analyzing your data. Please try again.'
      });
    } finally {
      setIsProcessing(false);
    }
  };
  
  return {
    detectAnomalies,
    isProcessing,
    visualizationData,
    selectedFile,
  };
};

// Helper function to generate mock data for visualization
const generateMockData = () => {
  const data = [];
  
  // Generate normal data points
  for (let i = 0; i < 50; i++) {
    const x = Math.random() * 100;
    const y = Math.random() * 100;
    
    data.push({
      x,
      y,
      isAnomaly: false
    });
  }
  
  // Generate anomaly data points (fewer and more scattered)
  for (let i = 0; i < 5; i++) {
    const x = Math.random() * 100;
    const y = Math.random() * 100;
    
    data.push({
      x,
      y,
      isAnomaly: true
    });
  }
  
  return data;
};

export default useAnomalyDetection;
