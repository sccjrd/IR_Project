import { apiClient } from "../../../lib/apiClient";

/**
 * Fetch hacks by category from the backend.
 * Backend returns: { total, page, page_size, total_pages, hits: [Hack, ...] }
 */
export async function getHacksByCategory({
  categoryName,
  page = 1,
  pageSize = 10,
}) {
  if (!categoryName) {
    throw new Error("categoryName is required to fetch hacks by category");
  }

  const data = await apiClient.get(
    `/api/search/categories/${encodeURIComponent(categoryName)}/hacks`,
    {
      params: {
        page,
        page_size: pageSize,
      },
    }
  );

  return data;
}
