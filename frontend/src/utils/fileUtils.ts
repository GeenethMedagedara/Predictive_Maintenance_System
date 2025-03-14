
/**
 * Utility functions for handling file operations
 */

/**
 * Reads a CSV file and returns its content as a string
 */
export const readCSVFile = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (event) => {
      if (event.target?.result) {
        resolve(event.target.result as string);
      } else {
        reject(new Error("Failed to read file"));
      }
    };
    
    reader.onerror = () => {
      reject(new Error("Error reading file"));
    };
    
    reader.readAsText(file);
  });
};

/**
 * Parses CSV string into an array of objects
 * This is a simple parser that assumes the first row is a header
 */
export const parseCSV = (csvString: string): Array<Record<string, string>> => {
  const lines = csvString.split('\n');
  const result = [];
  const headers = lines[0].split(',').map(header => header.trim());
  
  for (let i = 1; i < lines.length; i++) {
    if (!lines[i].trim()) continue;
    
    const obj: Record<string, string> = {};
    const currentLine = lines[i].split(',');
    
    for (let j = 0; j < headers.length; j++) {
      obj[headers[j]] = currentLine[j]?.trim() || '';
    }
    
    result.push(obj);
  }
  
  return result;
};

/**
 * Formats data for the visualization
 */
export const formatDataForVisualization = (
  data: Array<Record<string, string>>,
  xKey: string = 'x',
  yKey: string = 'y',
  anomalyKey: string = 'anomaly'
) => {
  return data.map(item => {
    const x = parseFloat(item[xKey] || '0');
    const y = parseFloat(item[yKey] || '0');
    const isAnomaly = item[anomalyKey]?.toLowerCase() === 'true' || item[anomalyKey] === '1';
    
    return {
      x,
      y,
      isAnomaly
    };
  });
};
