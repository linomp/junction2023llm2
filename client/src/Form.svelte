<script lang="ts">
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  let textInput: string = "";

  function handleSubmit() {
    dispatch("submit", { query: textInput });
  }
</script>

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
