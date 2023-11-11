<script lang="ts">
  import gsap from "gsap";
  import { onMount, afterUpdate } from "svelte";
  import Form from "./Form.svelte";
  import ResponseData from "./ResponseData.svelte";
  let isLoading = false; // New state for loading indicator

  interface BackendResponse {
    question: string;
    answer: string;
    confidence: number;
    sources: Array<{
      url: string | null;
      title: string;
      raw_content: string | null;
    }>;
  }
  let responseDatas: BackendResponse[] = []; // This will hold the array of response data
  let textInput: string = "";
  let responseData: BackendResponse | null = null; // This will hold the response data
  let showRawContentIndex = null; // This will hold the index of the response whose raw content should be shown

  const scrollToBottom = () => {
    const responsesContainer = document.querySelector(".responses-container");
    responsesContainer.scrollTop = responsesContainer.scrollHeight;
  };
  // Scroll to bottom after initial mount
  onMount(scrollToBottom);

  // Scroll to bottom on each update (when responseDatas changes)
  afterUpdate(scrollToBottom);

  const handleSubmit = async () => {
    isLoading = true; // Start loading

    responseData = null; // Clear previous response data
    try {
      console.log("com va", textInput);
      const response = await fetch("http://localhost:8001/query", {
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
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    } finally {
      isLoading = false; // Stop loading
    }
  };

  onMount(() => {
    const responsesContainer = document.querySelector(".responses-container");
    responsesContainer.scrollTop = responsesContainer.scrollHeight;
  });
</script>

<main class="flex flex-col justify-between h-screen">
  <div class="responses-container flex-1 overflow-y-auto">
    {#each responseDatas as responseData, responseIndex}
      <ResponseData {responseData} />
      {#if responseIndex === responseDatas.length - 1 && isLoading}
        <div class="loading-indicator"><div class="loading-spinner" /></div>
        <!-- Loading indicator for the latest message -->
      {/if}
    {/each}
    {#if responseDatas.length === 0 && isLoading}
      <div class="loading-indicator"><div class="loading-spinner" /></div>
      <!-- Loading indicator when there are no messages yet -->
    {/if}
  </div>
  <Form on:submit={handleSubmit} {isLoading} />
</main>

<style>
  .responses-container {
    padding-top: 1rem; /* Space at the top */
  }
  .loading-indicator {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
  }

  .loading-spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border-left-color: #09f;
    animation: spin 1s ease infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
