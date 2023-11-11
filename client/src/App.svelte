<script lang="ts">
  import gsap from "gsap";
  import { onMount, afterUpdate } from "svelte";

  interface BackendResponse {
    answer: string;
    confidence: number;
    sources: Array<{ url: string | null; title: string }>;
  }
  let responseDatas: BackendResponse[] = []; // This will hold the array of response data
  let textInput: string = "";
  let responseData: BackendResponse | null = null; // This will hold the response data

  const scrollToBottom = () => {
    const responsesContainer = document.querySelector(".responses-container");
    responsesContainer.scrollTop = responsesContainer.scrollHeight;
  };
  // Scroll to bottom after initial mount
  onMount(scrollToBottom);

  // Scroll to bottom on each update (when responseDatas changes)
  afterUpdate(scrollToBottom);

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

      const newResponseData = await response.json(); // Get the new response data
      responseDatas = [newResponseData, ...responseDatas]; // Use spread to trigger reactivity

      console.log("hola", responseDatas);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };
  onMount(() => {
    const responsesContainer = document.querySelector(".responses-container");
    responsesContainer.scrollTop = responsesContainer.scrollHeight;
  });
</script>

<main class="flex flex-col justify-between h-screen">
  <div class="responses-container flex-1 overflow-y-auto">
    {#each responseDatas as responseData}
      <div class="response bg-white shadow rounded px-4 py-2 my-2">
        <p class="text-lg"><strong>Answer:</strong> {responseData.answer}</p>
        <p class="text-lg">
          <strong>Confidence:</strong>
          {responseData.confidence}
        </p>
        <p class="text-lg"><strong>Sources:</strong></p>
        <ul>
          {#each responseData.sources as source}
            <li>{source.title}</li>
          {/each}
        </ul>
      </div>
    {/each}
  </div>
  <form
    on:submit|preventDefault={handleSubmit}
    class="bg-white shadow-md rounded px-8 pt-6 pb-8"
  >
    <h1 class="text-gray-700 text-xl font-bold mb-2">Submit your query</h1>
    <div class="mb-4">
      <input
        type="text"
        bind:value={textInput}
        placeholder="Enter your query..."
        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
      />
      <button
        type="submit"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4"
      >
        Submit
      </button>
    </div>
  </form>
</main>

<style>
  .responses-container {
    padding-top: 1rem; /* Space at the top */
  }
  .response {
    margin-bottom: 0.5rem; /* Space between messages */
  }
  form {
    padding-bottom: 1rem; /* Space at the bottom */
  }
</style>
