<script lang="ts">
  import { onMount, afterUpdate } from "svelte";
  import Form from "./Form.svelte";
  import ResponseData from "./ResponseData.svelte";
  let isLoading = false; // New state for loading indicator
  import Plus from "svelte-material-icons/PlusCircle.svelte";
  import Modal from "./Modal.svelte"; // Import your modal component

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
  let isModalOpen = false; // State to control modal visibility
  function addButtonClick() {
    isModalOpen = !isModalOpen;
  }
  const scrollToBottom = () => {
    const responsesContainer = document.querySelector(".responses-container");
    responsesContainer.scrollTop = responsesContainer.scrollHeight;
  };
  // Scroll to bottom after initial mount
  onMount(scrollToBottom);

  function closeModal() {
    isModalOpen = false; // This will reactively cause Svelte to remove the modal from the DOM
  }

  function handleFormSubmit(event) {
    textInput = event.detail.textInput; // Update the parent's textInput with the one from the form
    handleSubmit(); // Now call the submit handler that does the fetch
  }

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
      responseDatas = [...responseDatas, newResponseData]; // Use spread to trigger reactivity
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
  {#if isModalOpen}
    <Modal {closeModal} />
  {/if}
  <div class="responses-container flex-1 overflow-y-auto">
    {#each responseDatas as responseData, responseIndex}
      <ResponseData {responseData} />
      {#if responseIndex === responseDatas.length - 1 && isLoading}
        <div class="loading-indicator"><div class="loading-spinner" /></div>
      {/if}
    {/each}
    {#if responseDatas.length === 0 && isLoading}
      <div class="loading-indicator"><div class="loading-spinner" /></div>
    {/if}
  </div>
  <Form on:submit={handleFormSubmit} {isLoading} />
  <button on:click={addButtonClick} class="add-button">
    <Plus class="h-6 w-6" />
  </button>
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
  .add-button {
    position: absolute;
    top: 0;
    right: 0;
    margin: 1rem;
    cursor: pointer;
    /* Add more styling as needed */
  }
</style>
