import { Button } from '@mui/material';
import TranslateIcon from '@mui/icons-material/Translate';
import { useTranslation } from 'react-i18next';
import type { Language } from '../i18n';

interface LanguageSwitcherProps {
  color?: 'inherit' | 'primary' | 'secondary';
}

export default function LanguageSwitcher({
  color = 'inherit',
}: LanguageSwitcherProps) {
  const { i18n } = useTranslation();
  const nextLanguage: Language = i18n.language === 'ru' ? 'en' : 'ru';

  return (
    <Button
      color={color}
      startIcon={<TranslateIcon />}
      onClick={() => void i18n.changeLanguage(nextLanguage)}
      aria-label={nextLanguage === 'ru' ? 'Русский' : 'English'}
    >
      {nextLanguage.toUpperCase()}
    </Button>
  );
}
