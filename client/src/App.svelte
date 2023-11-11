<script lang="ts">
  import gsap from "gsap";
  interface BackendResponse {
    answer: string;
    confidence: number;
    sources: string[];
  }

  let textInput: string = "";
  let responseData: BackendResponse | null = null; // This will hold the response data

  const handleSubmit = async () => {
    responseData = null; // Clear previous response data
    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
        body: JSON.stringify({
          question: textInput,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      responseData = await response.json(); // Store the response data
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };
</script>

<main class="flex justify-center items-center h-screen">
  <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
    <h1 class="block text-gray-700 text-xl font-bold mb-2">
      Submit your query
    </h1>
    <form on:submit|preventDefault={handleSubmit} class="mb-4">
      <input
        type="text"
        bind:value={textInput}
        placeholder="Enter some text..."
        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      />
      <button
        type="submit"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4"
      >
        Submit
      </button>
    </form>
    {#if responseData}
      <div class="response">
        <p class="text-lg"><strong>Answer:</strong> {responseData.answer}</p>
        <p class="text-lg">
          <strong>Confidence:</strong>
          {responseData.confidence}
        </p>
        <p class="text-lg"><strong>Sources:</strong></p>
        <ul>
          {#each responseData.sources as source}
            <li>{source}</li>
          {/each}
        </ul>
      </div>
    {/if}
  </div>
</main>

<style>
  .response {
    background-color: #f3f4f6;
    border-radius: 8px;
    padding: 16px;
    margin-top: 16px;
  }
</style>
