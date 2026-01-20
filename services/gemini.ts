
import { GoogleGenAI, Type } from "@google/genai";
import { TutorObservation } from "../types.ts";

export const getTutorExplanation = async (mass: number, volume: number): Promise<TutorObservation> => {
  const density = mass / volume;
  
  let apiKey = "";
  try {
    // Acceso seguro a variables de entorno en el navegador
    apiKey = (typeof process !== 'undefined' && process.env) ? process.env.API_KEY || "" : "";
  } catch (e) {
    // Fallback silencioso si falla el acceso
  }

  if (!apiKey) {
    return {
      explanation: `Calculando física básica: Con una masa de ${mass}g y un volumen de ${volume}cm³, la densidad es ${density.toFixed(2)} g/cm³.`,
      isFloating: density <= 1.0,
      scientificFact: "Configura la API_KEY para obtener explicaciones avanzadas de la IA."
    };
  }

  const ai = new GoogleGenAI({ apiKey });
  const prompt = `Actúa como un profesor de física experto. Analiza un objeto de ${mass}g y ${volume}cm³ (densidad: ${density.toFixed(2)} g/cm³). 
  Explica su comportamiento de flotación en agua (d=1.0) y danos un dato científico curioso. 
  Responde obligatoriamente en JSON con los campos: explanation, isFloating, scientificFact.`;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            explanation: { type: Type.STRING },
            isFloating: { type: Type.BOOLEAN },
            scientificFact: { type: Type.STRING },
          },
          required: ["explanation", "isFloating", "scientificFact"],
        },
      },
    });

    const text = response.text;
    if (!text) throw new Error("Sin respuesta");
    return JSON.parse(text) as TutorObservation;
  } catch (error) {
    console.error("Error IA:", error);
    return {
      explanation: `La densidad calculada es de ${density.toFixed(2)} g/cm³.`,
      isFloating: density <= 1.0,
      scientificFact: "Dato técnico: Un objeto flota si desplaza un peso de líquido igual a su propio peso."
    };
  }
};
