import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en, { type Translation } from './en';
import ru from './ru';

export type Language = 'en' | 'ru';

export const LANGUAGE_STORAGE_KEY = 'manyS.language';

declare module 'i18next' {
  interface CustomTypeOptions {
    defaultNS: 'translation';
    resources: {
      translation: Translation;
    };
  }
}

const SUPPORTED_LANGUAGES: Language[] = ['en', 'ru'];

function getInitialLanguage(): Language {
  const saved = localStorage.getItem(LANGUAGE_STORAGE_KEY);
  if (saved === 'en' || saved === 'ru') {
    return saved;
  }
  const browser = navigator.language.toLowerCase();
  return browser.startsWith('ru') ? 'ru' : 'en';
}

void i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    ru: { translation: ru },
  },
  lng: getInitialLanguage(),
  fallbackLng: 'en',
  supportedLngs: SUPPORTED_LANGUAGES,
  interpolation: {
    escapeValue: false,
  },
});

// Persist choice and keep <html lang> in sync.
i18n.on('languageChanged', (lng) => {
  localStorage.setItem(LANGUAGE_STORAGE_KEY, lng);
  document.documentElement.lang = lng;
});

document.documentElement.lang = i18n.language;

export default i18n;
