
import { GoogleGenAI, Type } from "@google/genai";
import { TutorObservation } from "../types.ts";

export const getTutorExplanation = async (mass: number, volume: number): Promise<TutorObservation> => {
  // Crear instancia dentro de la función según las directrices de la SDK para entornos dinámicos
  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
  const density = mass / volume;
  
  const prompt = `Actúa como un profesor de física experto. Analiza un objeto de ${mass}g y ${volume}cm³ (densidad: ${density.toFixed(2)} g/cm³).
  Explica su comportamiento de flotación y danos un dato científico curioso.
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
    return JSON.parse(text);
  } catch (error) {
    console.error("Error IA:", error);
    return {
      explanation: `La densidad es de ${density.toFixed(2)} g/cm³. Si esto es menor que la del líquido, flotará.`,
      isFloating: density <= 1.0,
      scientificFact: "El objeto más denso conocido es una estrella de neutrones."
    };
  }
};
