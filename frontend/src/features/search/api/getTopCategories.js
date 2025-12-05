import { apiClient } from "../../../lib/apiClient";

/**
 * Fetch top categories from the backend.
 * Backend returns: [{ category: string, count: number }, ...]
 */
export async function getTopCategories({ limit = 6 } = {}) {
  const data = await apiClient.get("/api/search/categories/top", {
    params: { limit },
  });

  return data;
}
