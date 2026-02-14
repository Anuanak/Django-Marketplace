<template>
  <el-config-provider :locale="elementLocale">
    <router-view />
  </el-config-provider>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import ruLocale from 'element-plus/dist/locale/ru.mjs'
import enLocale from 'element-plus/dist/locale/en.mjs'
import ukLocale from 'element-plus/dist/locale/uk.mjs'

const { locale } = useI18n()

const elementLocale = computed(() => {
  const locales = {
    ru: ruLocale,
    en: enLocale,
    uk: ukLocale
  }
  return locales[locale.value] || ruLocale
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
}
</style>
