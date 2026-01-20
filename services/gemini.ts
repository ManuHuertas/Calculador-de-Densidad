
import { GoogleGenAI, Type } from "@google/genai";
import { TutorObservation } from "../types.ts";

// Initialize the Google GenAI client exclusively using process.env.API_KEY.
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

export const getTutorExplanation = async (mass: number, volume: number): Promise<TutorObservation> => {
  const density = mass / volume;
  const prompt = `Como un profesor de física experto, analiza un objeto de ${mass}g y ${volume}cm³ (ρ=${density.toFixed(2)} g/cm³).
  Explica su comportamiento de flotación en agua (ρ=1) y danos un dato científico curioso.
  Responde estrictamente en formato JSON con los campos: explanation, isFloating, scientificFact.`;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        // Using responseSchema to ensure structured output.
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

    // Access the .text property directly (not as a method).
    const text = response.text;
    if (!text) throw new Error("Respuesta vacía");
    return JSON.parse(text);
  } catch (error) {
    console.error("Error al obtener la explicación del tutor:", error);
    return {
      explanation: `La densidad calculada es ${density.toFixed(2)} g/cm³. Como es ${density > 1 ? 'mayor' : 'menor'} que la del agua (1.0), el objeto se ${density > 1 ? 'hunde' : 'mantiene a flote'}.`,
      isFloating: density <= 1,
      scientificFact: "Dato curioso: El Mar Muerto es tan denso debido a su salinidad que los humanos flotan en él sin esfuerzo."
    };
  }
};
