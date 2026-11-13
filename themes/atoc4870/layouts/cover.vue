<template>
  <div class="slidev-layout cover">
    <slot />
    <div v-if="$frontmatter.author" class="who">
      <div v-for="line in [].concat($frontmatter.author)" :key="line">{{ line }}</div>
    </div>
    <div v-if="$frontmatter.tagline" class="tagline">{{ $frontmatter.tagline }}</div>
  </div>
</template>
