<script lang="ts">
  import gsap from "gsap";
  import { onMount, afterUpdate } from "svelte";
  import Form from "./Form.svelte";
  import ResponseData from "./ResponseData.svelte";

  interface BackendResponse {
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

      // Wait for the next tick to ensure the element is rendered
      setTimeout(() => {
        // Assume newResponseData has an id property or similar to identify it
        const element = document.getElementById(
          `response-${newResponseData.id}`
        );
        gsap.from(element, {
          duration: 0.5, // Animation duration in seconds
          opacity: 0, // Start with an opacity of 0
          y: 20, // Start 20 pixels below the final position
          ease: "power2.out", // An easing function for a smooth effect
        });
      }, 0);
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
    {#each responseDatas as responseData, responseIndex}
      <ResponseData {responseData} />
    {/each}
  </div>
  <Form on:submit={handleSubmit} />
</main>

<style>
  .responses-container {
    padding-top: 1rem; /* Space at the top */
  }
</style>
