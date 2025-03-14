
import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";
import Image from "../components/ui/image";
import { usePrediction } from "../PredictionContext";

interface AnomalyVisualizationProps {
  data: any[] | null;
  isLoading: boolean;
  className?: string;
}

const AnomalyVisualization: React.FC<AnomalyVisualizationProps> = ({ 
  data, 
  isLoading, 
  className 
}) => {
  // Calculate anomaly percentage if data exists
  const { imageSrc } = usePrediction();
  const anomalyPercentage = data 
    ? (data.filter(item => item.isAnomaly).length / data.length) * 100 
    : 0;
  
  // Function to get the appropriate visualization image based on anomaly percentage
  const getVisualizationImage = () => {
    if (anomalyPercentage > 15) {
      return "/visualization-high-anomaly.png";
    } else if (anomalyPercentage > 5) {
      return "/visualization-medium-anomaly.png";
    } else {
      return "/visualization-low-anomaly.png";
    }
  };
  
  const LoadingState = () => (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="w-full h-full min-h-[400px] flex flex-col items-center justify-center"
    >
      <div className="w-16 h-16 relative mb-8">
        <motion.div 
          className="absolute inset-0 border-4 border-primary/30 border-t-primary rounded-full"
          animate={{ rotate: 360 }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
        />
      </div>
      <motion.p 
        className="text-lg font-medium text-primary/80"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        Analyzing data
      </motion.p>
      <motion.p 
        className="text-sm text-muted-foreground mt-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        Detecting anomalies in your dataset
      </motion.p>
    </motion.div>
  );

  const EmptyState = () => (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="w-full h-full min-h-[400px] flex flex-col items-center justify-center p-8"
    >
      <motion.div 
        className="w-20 h-20 rounded-full bg-secondary/80 flex items-center justify-center mb-6"
        animate={{ 
          scale: [1, 1.05, 1],
          opacity: [0.7, 1, 0.7]
        }}
        transition={{ 
          duration: 4, 
          repeat: Infinity,
          repeatType: "reverse" 
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          className="w-10 h-10 text-primary/70"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
          />
        </svg>
      </motion.div>
      <h3 className="text-lg font-medium text-center mb-2">Visualization Area</h3>
      <p className="text-sm text-muted-foreground text-center max-w-md">
        Upload a CSV file to visualize anomalies in your data. The results will be displayed here.
      </p>
    </motion.div>
  );

  const VisualizationContent = () => {
    const anomalyCount = data?.filter(item => item.isAnomaly).length || 0;
    
    return (
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="w-full flex flex-col items-center justify-center py-4"
      >
        <div className="w-full max-w-[1200px] h-[500px] overflow-hidden rounded-xl shadow-md mb-4">
          <img 
            // src={getVisualizationImage()} 
            src={imageSrc} 
            alt="Anomaly visualization"
            className="w-full h-full object-cover"
            onError={(e) => {
              // Fallback to placeholder if image doesn't exist
              e.currentTarget.src = "/placeholder.svg";
            }}
          />
        </div>
        
        {/* <div className="bg-white/70 backdrop-blur-sm p-4 rounded-lg border shadow-sm">
          <h3 className="text-lg font-medium mb-2 text-center">Analysis Results</h3>
          <p className="text-sm text-center">
            <span className="font-semibold">Found {anomalyCount} anomalies</span> in your dataset 
            ({anomalyPercentage.toFixed(1)}% of total data points)
          </p>
        </div> */}
      </motion.div>
    );
  };

  return (
    <div className={cn(
      "w-full rounded-xl overflow-hidden bg-white/80 backdrop-blur-lg shadow-sm border p-4",
      className
    )}>
      <AnimatePresence mode="wait">
        {isLoading ? (
          <LoadingState key="loading" />
        ) : data ? (
          <VisualizationContent key="visualization" />
        ) : (
          <EmptyState key="empty" />
        )}
      </AnimatePresence>
    </div>
  );
};

export default AnomalyVisualization;
