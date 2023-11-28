

export type QueryResponse = {
  answer: string;
};

const queryIndex = async (query: string): Promise<QueryResponse> => {
  const queryURL = new URL("http://localhost:8000/qa/{question}?");
  queryURL.searchParams.append("text", query);

  const response = await fetch(queryURL, { mode: "cors" });
  if (!response.ok) {
    return { answer: "Error in query"};
  }

  const queryResponse = (await response.json());

  return queryResponse;
};

export default queryIndex;