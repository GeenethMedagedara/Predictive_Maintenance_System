import React, { createContext, useState, useContext, ReactNode } from "react";

interface PredictionContextType {
  imageSrc: string | null;
  setImageSrc: (value: string | null) => void;
}

const PredictionContext = createContext<PredictionContextType | undefined>(undefined);

export const PredictionProvider = ({ children }: { children: ReactNode }) => {
  const [imageSrc, setImageSrc] = useState<string | null>(null);

  return (
    <PredictionContext.Provider value={{ imageSrc, setImageSrc }}>
      {children}
    </PredictionContext.Provider>
  );
};

export const usePrediction = () => {
  const context = useContext(PredictionContext);
  if (!context) {
    throw new Error("usePrediction must be used within a PredictionProvider");
  }
  return context;
};
