<script lang="ts">
  export let responseData; // This declares responseData as a prop
  let showRawContentIndex = null;

  const toggleRawContent = (sourceIndex) => {
    const currentIndex = `${responseData.answer}-${sourceIndex}`;
    showRawContentIndex =
      showRawContentIndex === currentIndex ? null : currentIndex;
  };
</script>

<div
  id="response-{responseData.id}"
  class="response bg-white shadow rounded px-4 py-2 my-2"
>
  <p class="text-lg"><strong>Question:</strong> {responseData.question}</p>
  <!-- Display the question here -->
  <p class="text-lg"><strong>Answer:</strong> {responseData.answer}</p>
  <p class="text-lg">
    <strong>Confidence:</strong>
    {responseData.confidence}
  </p>
  <p class="text-lg"><strong>Sources:</strong></p>
  <ul>
    {#each responseData.sources as source, sourceIndex}
      <li class="source-title" on:click={() => toggleRawContent(sourceIndex)}>
        {source.title}
        {#if showRawContentIndex === `${responseData.answer}-${sourceIndex}`}
          <pre class="raw-content">{source.raw_content}</pre>
        {/if}
      </li>
    {/each}
  </ul>
</div>
