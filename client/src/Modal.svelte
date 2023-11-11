<script lang="ts">
  export let closeModal;
  import Close from "svelte-material-icons/Close.svelte";
  import Send from "svelte-material-icons/SendCircleOutline.svelte";

  function disableInput(event) {
    const urlInput = document.getElementById("url");
    const rawContentInput = document.getElementById("raw-content");

    if (event.target.id === "url" && event.target.value.trim() !== "") {
      rawContentInput.disabled = true;
    } else if (
      event.target.id === "raw-content" &&
      event.target.value.trim() !== ""
    ) {
      urlInput.disabled = true;
    } else {
      urlInput.disabled = false;
      rawContentInput.disabled = false;
    }
  }

  async function handleSubmit(event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(event.target); // Create FormData from the form
    const data = {
      title: formData.get("title"),
      url: formData.get("url"),
      raw_content: formData.get("raw-content"),
    };

    try {
      const response = await fetch("http://localhost:8001/sources", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        console.log("Data sent successfully");
        closeModal();
      } else {
        console.error("Failed to send data", response);
      }
    } catch (error) {
      console.error("Error sending data", error);
    }
  }
</script>

<div
  class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center"
>
  <div class="bg-white p-6 rounded shadow-lg relative">
    <!-- relative class added for absolute positioning of the X icon -->
    <button on:click={closeModal} class="absolute top-0 right-0 m-4">
      <Close class="cursor-pointer" />
      <!-- Use the Close icon -->
    </button>
    <form id="myForm" on:submit={handleSubmit}>
      <div class="mb-4">
        <label for="title" class="block text-gray-700 text-sm font-bold mb-2"
          >Title:</label
        >
        <input
          type="title"
          id="title"
          name="title"
          required
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <div class="mb-4">
        <label for="url" class="block text-gray-700 text-sm font-bold mb-2"
          >Url:</label
        >
        <input
          type="text"
          id="url"
          name="url"
          on:input={disableInput}
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <div class="mb-4">
        <label
          for="raw-content"
          class="block text-gray-700 text-sm font-bold mb-2">Raw content:</label
        >
        <textarea
          id="raw-content"
          name="raw-content"
          on:input={disableInput}
          rows="4"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          placeholder="Enter text here..."
        />
      </div>
      <div class="flex justify-center">
        <button type="submit" class="scale-150">
          <Send />
        </button>
      </div>
    </form>
  </div>
</div>
