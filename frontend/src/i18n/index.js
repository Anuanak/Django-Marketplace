import { createI18n } from 'vue-i18n'
import ru from '../locales/ru.json'
import en from '../locales/en.json'
import uk from '../locales/uk.json'

const messages = {
  ru,
  en,
  uk
}

const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('language') || 'ru',
  fallbackLocale: 'ru',
  messages
})

export default i18n
