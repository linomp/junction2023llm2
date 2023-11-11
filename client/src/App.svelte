<script lang="ts">
  let textInput: string = "";

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
        },
        body: JSON.stringify({
          value: textInput,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log(result);
      alert(
        `Submitted Text: ${textInput}\nResponse: ${JSON.stringify(
          result,
          null,
          2
        )}`
      );
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };
</script>

<main class="flex justify-center items-center h-screen">
  <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
    <h1 class="block text-gray-700 text-xl font-bold mb-2">Lino Maricón</h1>
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
  </div>
</main>
