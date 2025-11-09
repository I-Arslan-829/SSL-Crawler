// src/app/components/api.ts

const start = process.env.NEXT_PUBLIC_API_URL

export async function fetchOverview() {
  try {
    const res = await fetch(`${start}/overview/data/`, {
      // Use next's cache control for dev, "no-store" disables SSR cache
      cache: "no-store",
    });
    if (!res.ok) throw new Error("API error");
    return await res.json();
  } catch (err) {
    throw err;
  }
}

// Add more fetchers as needed for your other dashboard pages!
