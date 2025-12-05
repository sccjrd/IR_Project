import { useCallback, useState, useEffect } from "react";
import { getTopCategories } from "../api/getTopCategories";

export function useTopCategories(options = {}) {
  const { limit = 6, autoFetch = true } = options;

  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasFetched, setHasFetched] = useState(false);

  const fetchCategories = useCallback(
    async (force = false) => {
      if (hasFetched && !force) return;

      setLoading(true);
      setError(null);

      try {
        const data = await getTopCategories({ limit });
        const arr = Array.isArray(data) ? data : [];

        setCategories(arr);
        setHasFetched(true);
      } catch (err) {
        setError(err?.message || "Failed to load top categories");
        setCategories([]);
      } finally {
        setLoading(false);
      }
    },
    [limit, hasFetched]
  );

  // Auto-fetch on mount if enabled
  useEffect(() => {
    if (autoFetch) {
      fetchCategories();
    }
  }, [fetchCategories, autoFetch]);

  const refresh = useCallback(() => {
    setHasFetched(false);
    fetchCategories(true);
  }, [fetchCategories]);

  return {
    categories,
    loading,
    error,
    hasFetched,
    fetchCategories,
    refresh,
  };
}
