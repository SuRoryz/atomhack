<script setup>
import { RouterView } from 'vue-router'
import { NConfigProvider, NLayout } from 'naive-ui'
import hljs from 'highlight.js/lib/core'
import jsonHighlight from 'highlight.js/lib/languages/json'

hljs.registerLanguage('json', jsonHighlight)
</script>

<template>
    <NConfigProvider :hljs="hljs">
        <NLayout>
            <RouterView />
        </NLayout>
    </NConfigProvider>
</template>
