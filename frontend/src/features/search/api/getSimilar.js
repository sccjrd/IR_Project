import { apiClient } from "../../../lib/apiClient";

/**
 * Fetch similar hacks from the backend.
 * Backend returns a plain array: [Hack, Hack, ...]
 */
export async function getSimilar({ hackId, limit = 6 }) {
  if (!hackId) {
    throw new Error("hackId is required to fetch similar results");
  }

  const data = await apiClient.get(
    "/api/search/similar/" + encodeURIComponent(hackId),
    {
      params: { limit },
    }
  );

  return data;
}
