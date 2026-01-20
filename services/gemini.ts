
import { GoogleGenAI, Type } from "@google/genai";
import { TutorObservation } from "../types.ts";

export const getTutorExplanation = async (mass: number, volume: number): Promise<TutorObservation> => {
  const density = mass / volume;
  
  // Acceso directo según las guías: el entorno proporciona process.env.API_KEY
  const apiKey = process.env.API_KEY;

  if (!apiKey) {
    return {
      explanation: `Calculando física básica: Masa de ${mass}g y volumen de ${volume}cm³ (Densidad: ${density.toFixed(2)} g/cm³).`,
      isFloating: density <= 1.0,
      scientificFact: "Configura la API_KEY para explicaciones avanzadas."
    };
  }

  // Inicialización según guías oficiales
  const ai = new GoogleGenAI({ apiKey });
  
  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: `Explica por qué un objeto de masa ${mass}g y volumen ${volume}cm³ (densidad ${density.toFixed(2)} g/cm³) ${density <= 1.0 ? 'flota' : 'se hunde'} en agua pura (densidad 1.0 g/cm³).`,
      config: {
        systemInstruction: "Eres un tutor de física. Responde siempre en formato JSON con los campos: explanation (string breve), isFloating (boolean), scientificFact (string con un dato curioso).",
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

    const result = JSON.parse(response.text || "{}");
    return {
      explanation: result.explanation || "Análisis completado.",
      isFloating: typeof result.isFloating === 'boolean' ? result.isFloating : density <= 1.0,
      scientificFact: result.scientificFact || "La densidad es una propiedad intensiva."
    };
  } catch (error) {
    console.error("Error en tutoría:", error);
    return {
      explanation: `Análisis manual: La densidad es ${density.toFixed(2)} g/cm³.`,
      isFloating: density <= 1.0,
      scientificFact: "Arquímedes descubrió el principio de flotabilidad en una tina."
    };
  }
};
