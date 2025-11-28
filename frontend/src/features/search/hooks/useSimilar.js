import { useCallback, useState } from "react";
import { getSimilar } from "../api/getSimilar";

export function useSimilar(hackId, options = {}) {
  const { limit = 6 } = options;

  const [similar, setSimilar] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasFetched, setHasFetched] = useState(false);

  const fetchSimilar = useCallback(
    async (force = false) => {
      if (!hackId) return;
      if (hasFetched && !force) return;

      setLoading(true);
      setError(null);

      try {
        const raw = await getSimilar({ hackId, limit });

        const arr = Array.isArray(raw) ? raw : [];
        console.log("similar hacks for", hackId, arr);

        setSimilar(arr);
        setHasFetched(true);
      } catch (err) {
        console.error("Failed to load similar hacks:", err);
        setError(err?.message || "Failed to load similar hacks");
        setSimilar([]);
      } finally {
        setLoading(false);
      }
    },
    [hackId, limit, hasFetched]
  );

  return {
    similar,
    loading,
    error,
    hasFetched,
    fetchSimilar,
  };
}
